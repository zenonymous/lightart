import pytest

from lightart.engine import Output, Pole, Runner, StopShow

A1 = ("a", 1)


class Frames(Output):
    def __init__(self):
        self.times = []

    def send(self, pole, now_ms):
        self.times.append(now_ms)


def test_linear_fade_and_completion():
    pole = Pole()
    pole.fade([A1], (0, 0, 200), 1000)
    pole.advance(500)
    assert pole.color(A1) == (0, 0, 100)
    assert pole.busy
    pole.advance(500)
    assert pole.color(A1) == (0, 0, 200)
    assert not pole.busy


def test_new_fade_replaces_running_one_from_current_value():
    pole = Pole()
    pole.fade([A1], (200, 0, 0), 1000)
    pole.advance(500)
    pole.fade([A1], (0, 0, 0), 100)  # like pyartnet: starts from (100, 0, 0)
    pole.advance(50)
    assert pole.color(A1) == (50, 0, 0)


def test_zero_duration_is_immediate():
    pole = Pole()
    pole.set([A1], (1, 2, 3))
    assert pole.color(A1) == (1, 2, 3)


def test_invalid_colour():
    with pytest.raises(ValueError):
        Pole().fade([A1], (0, 0, 256), 10)


def test_runner_wait_and_limit():
    out = Frames()
    runner = Runner(Pole(), [out], fps=25, realtime=False, limit_ms=200)
    runner.pole.fade([A1], (0, 0, 255), 120)
    runner.wait()
    assert out.times == [40, 80, 120]
    with pytest.raises(StopShow):
        runner.hold(1000)


def test_realtime_runner_sleeps():
    now = [0.0]
    slept = []

    def sleep(s):
        slept.append(s)
        now[0] += s

    runner = Runner(Pole(), [], fps=10, realtime=True, sleep=sleep, clock=lambda: now[0])
    runner.hold(300)
    assert slept == pytest.approx([0.1, 0.1, 0.1])


def test_realtime_runner_does_not_burst_after_falling_behind():
    now = [0.0]
    slept = []

    def sleep(s):
        slept.append(s)
        now[0] += s

    runner = Runner(Pole(), [], fps=10, realtime=True, sleep=sleep, clock=lambda: now[0])
    now[0] = 5.0  # e.g. the Pi stalled for 5 s
    runner.hold(300)
    assert slept == pytest.approx([0.1, 0.1])  # first frame resyncs, then normal pacing, no catch-up burst
