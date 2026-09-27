import pytest

from lightart.engine import Output, Pole, Runner
from lightart.layout import band
from lightart.shows import BLUE, SOFT_BLUE, BreatheConfig, band_intensity, breathe_cycle, chase_cycle, legacy_cycle


class Snapshots(Output):
    """Counts frames."""

    def __init__(self):
        self.frames = 0

    def send(self, pole, now_ms):
        self.frames += 1


def run(cycle, visitors, cfg=None):
    out = Snapshots()
    runner = Runner(Pole(), [out], fps=25, realtime=False)
    calls = []

    def count():
        calls.append(runner.now_ms)
        return visitors

    cycle(runner, count, cfg or BreatheConfig())
    return runner, calls


@pytest.mark.parametrize("visitors, expected", [(0, 0), (1, 120), (2, 135), (5, 180), (100, 255)])
def test_band_intensity_scales_with_visitors(visitors, expected):
    assert band_intensity(visitors, BreatheConfig()) == expected


def test_breathe_timing_and_final_state():
    runner, calls = run(breathe_cycle, visitors=3)
    assert len(calls) == 6  # every step is a breath (bug fixed)
    assert runner.now_ms == pytest.approx(6 * 2 * 4500, abs=12 * 40)  # each wait ends on a frame
    pole = runner.pole
    # last exhale: band moved to step 48 == step 0, red at the visitor intensity
    assert all(pole.color(fx) == (150, 0, 0) for fx in band(0))  # 120 + 2 * 15
    others = [fx for fx in pole.fixtures if fx not in set(band(0))]
    assert all(pole.color(fx) == SOFT_BLUE for fx in others)


def test_breathe_fast_without_visitors():
    runner, _ = run(breathe_cycle, visitors=0)
    assert runner.now_ms == pytest.approx(6 * 2 * 1500, abs=12 * 40)


def test_breathe_inhale_state():
    out = Snapshots()
    runner = Runner(Pole(), [out], fps=25, realtime=False, limit_ms=4520)  # 4500 ms inhale ends on the 113th frame
    from lightart.engine import StopShow

    with pytest.raises(StopShow):
        breathe_cycle(runner, lambda: 10, BreatheConfig())
    pole = runner.pole
    assert pole.color(("a", 1)) == (255, 0, 0)  # band(0), 10 visitors → full red
    assert pole.color(("a", 20)) == BLUE


def test_legacy_reproduces_2020_bugs():
    runner, calls = run(legacy_cycle, visitors=7)
    assert len(calls) == 1  # read once per pass
    assert runner.now_ms == pytest.approx(3 * 2 * 4500, abs=6 * 40)  # only 3 breaths
    assert all(
        runner.pole.color(fx) == (1, 0, 0) for fx in band(32 + 8)
    )  # last active step is 32; intensity stuck at 1


def test_chase_lights_every_fixture_once():
    runner, _ = run(chase_cycle, visitors=0)
    assert runner.now_ms > 6 * 48 * 60
    assert all(c == (0, 0, 0) for c in runner.pole.colors())
