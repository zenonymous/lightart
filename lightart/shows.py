"""The shows. Each takes a Runner and a visitor-count function and runs until stopped.

- ``breathe``: the production show from ``artnet/zbreathe.py`` with the bugs
  fixed. The spiral band gets brighter as more visitors are counted.
- ``legacy``: a faithful port of what ``zbreathe.py`` actually did,
  including its bugs. Use it to compare with ``breathe`` in the simulator.
- ``chase``: a wiring test. It lights each strip in turn from fixture 1 up to
  48 in a distinct colour.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Dict

from lightart.engine import BLACK, Color, Runner
from lightart.layout import FIXTURES_PER_STRIP, STEPS, STRIPS, all_fixtures, band

log = logging.getLogger(__name__)

BLUE: Color = (0, 0, 255)
SOFT_BLUE: Color = (0, 0, 30)

VisitorFn = Callable[[], int]


@dataclass
class BreatheConfig:
    slow_ms: int = 4500  # breath half-length when visitors are present (as original)
    fast_ms: int = 1500  # breath half-length when nobody is around (as original)
    band_ms: int = 1500  # fade time of the spiral band (as original)
    base: int = 120  # band brightness for 1 visitor
    per_visitor: int = 15  # extra brightness for each additional visitor
    max_intensity: int = 255


def band_intensity(visitors: int, cfg: BreatheConfig) -> int:
    """0 visitors → 0 (a dark band, as in the original); otherwise base + per-visitor, capped.

    The values are before cubic output correction, so 120 comes out as about
    26/255 on the wire (dim but visible) and 255 as full.
    """
    if visitors <= 0:
        return 0
    return min(cfg.max_intensity, cfg.base + cfg.per_visitor * (visitors - 1))


def red(intensity: int) -> Color:
    return (intensity, 0, 0)


def breathe_cycle(runner: Runner, visitors: VisitorFn, cfg: BreatheConfig) -> None:
    """One pass: 6 breaths, and the band moves one block per breath."""
    pole = runner.pole
    everything = list(all_fixtures())
    for step in STEPS:
        count = visitors()
        intensity = band_intensity(count, cfg)
        timer = cfg.slow_ms if count > 0 else cfg.fast_ms
        log.debug("step %d: visitors=%d intensity=%d timer=%d", step, count, intensity, timer)

        # inhale: everything to full blue, the band at `step` to red
        pole.fade(everything, BLUE, timer)
        pole.fade(band(step), red(intensity), cfg.band_ms)
        runner.wait()

        # exhale: everything to soft blue, the band moves on to the next block
        pole.fade(everything, SOFT_BLUE, timer)
        pole.fade(band(step), SOFT_BLUE, cfg.band_ms)
        pole.fade(band(step + 8), red(intensity), cfg.band_ms)
        runner.wait()


def legacy_cycle(runner: Runner, visitors: VisitorFn, cfg: BreatheConfig) -> None:
    """Exactly what artnet/zbreathe.py did, bugs included (see docs/SHOW_LOGIC.md)."""
    pole = runner.pole
    everything = list(all_fixtures())
    count = visitors()  # read once per pass
    intensity = 1 if count > 0 else 0  # bug: loop variable `i` always ends at 1
    for step in STEPS:
        timer = 1500 if intensity == 0 else 4500
        if (step // 8) % 2 == 1:
            continue  # bug: odd steps do nothing
        pole.fade(everything, BLUE, timer)
        pole.fade(band(step), (intensity, 0, 0), 1500)
        runner.wait()
        pole.fade(everything, SOFT_BLUE, timer)
        pole.fade(band(step), SOFT_BLUE, 1500)
        pole.fade(band(step + 8), (intensity, 0, 0), 1500)
        runner.wait()


CHASE_COLORS: Dict[str, Color] = {
    "a": (255, 0, 0),
    "b": (0, 255, 0),
    "c": (0, 0, 255),
    "d": (255, 255, 0),
    "e": (0, 255, 255),
    "f": (255, 0, 255),
}


def chase_cycle(runner: Runner, visitors: VisitorFn, cfg: BreatheConfig) -> None:
    """Wiring test: strip a red, b green, c blue, d yellow, e cyan, f magenta, from 1 up."""
    pole = runner.pole
    pole.set(list(all_fixtures()), BLACK)
    for strip in STRIPS:
        for n in range(1, FIXTURES_PER_STRIP + 1):
            pole.set([(strip, n)], CHASE_COLORS[strip])
            runner.hold(60)
        runner.hold(500)
        pole.set([(strip, n) for n in range(1, FIXTURES_PER_STRIP + 1)], BLACK)


SHOWS = {"breathe": breathe_cycle, "legacy": legacy_cycle, "chase": chase_cycle}


def run_forever(show: str, runner: Runner, visitors: VisitorFn, cfg: BreatheConfig) -> None:
    cycle = SHOWS[show]
    while True:
        cycle(runner, visitors, cfg)
