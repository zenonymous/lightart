"""Fade engine: per-fixture linear fades that run on a clock.

It works like pyartnet 0.8, which the original scripts used. A new fade on a
fixture replaces the one that is running and starts from the fixture's current
colour. ``Runner.wait()`` advances time until every fade has finished, the
equivalent of awaiting ``wait_till_fade_complete()`` on all channels.

Colours are logical RGB (0-255) before output correction. Outputs
(``lightart.artnet``, ``lightart.simulator``) turn them into wire bytes or
preview data.
"""

from __future__ import annotations

import time
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from lightart.layout import Fixture, all_fixtures

Color = Tuple[int, int, int]
BLACK: Color = (0, 0, 0)


class _Fade:
    __slots__ = ("duration", "elapsed", "start", "target")

    def __init__(self, start: Sequence[float], target: Color, duration: float):
        self.start = tuple(start)
        self.target = target
        self.duration = max(duration, 0.0)
        self.elapsed = 0.0

    def value(self) -> Tuple[float, float, float]:
        if self.duration <= 0 or self.elapsed >= self.duration:
            return tuple(float(c) for c in self.target)  # type: ignore[return-value]
        f = self.elapsed / self.duration
        return tuple(s + (t - s) * f for s, t in zip(self.start, self.target))  # type: ignore[return-value]


class Pole:
    """The current colour of every fixture, plus the fades that are running."""

    def __init__(self) -> None:
        self.fixtures: List[Fixture] = list(all_fixtures())
        self._values: Dict[Fixture, Tuple[float, float, float]] = {fx: (0.0, 0.0, 0.0) for fx in self.fixtures}
        self._fades: Dict[Fixture, _Fade] = {}

    def fade(self, fixtures: Iterable[Fixture], color: Color, duration_ms: float) -> None:
        color = _check_color(color)
        for fx in fixtures:
            self._fades[fx] = _Fade(self._values[fx], color, duration_ms)

    def set(self, fixtures: Iterable[Fixture], color: Color) -> None:
        self.fade(fixtures, color, 0)
        self.advance(0)

    def advance(self, dt_ms: float) -> None:
        done = []
        for fx, fade in self._fades.items():
            fade.elapsed += dt_ms
            self._values[fx] = fade.value()
            if fade.elapsed >= fade.duration:
                done.append(fx)
        for fx in done:
            del self._fades[fx]

    @property
    def busy(self) -> bool:
        return bool(self._fades)

    def color(self, fx: Fixture) -> Color:
        r, g, b = self._values[fx]
        return round(r), round(g), round(b)

    def colors(self) -> List[Color]:
        """The colours of all fixtures in ``self.fixtures`` order (a1..a48, b1, ...)."""
        return [self.color(fx) for fx in self.fixtures]


def _check_color(color: Sequence[int]) -> Color:
    if len(color) != 3 or not all(0 <= int(c) <= 255 for c in color):
        raise ValueError(f"colour must be 3 values 0..255, got {color!r}")
    return int(color[0]), int(color[1]), int(color[2])


class Output:
    """Receives one frame per tick."""

    def send(self, pole: Pole, now_ms: float) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def close(self, pole: Pole) -> None:
        pass


class StopShow(Exception):
    """Raised by ``Runner.wait()`` when the runner's time limit is reached."""


class Runner:
    """Advances a pole in fixed ticks and feeds every frame to the outputs.

    ``realtime=True`` sleeps between frames (live show). ``realtime=False``
    runs as fast as possible on a virtual clock (simulator, tests).
    """

    def __init__(
        self,
        pole: Pole,
        outputs: Sequence[Output],
        fps: float = 25.0,
        realtime: bool = True,
        limit_ms: Optional[float] = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if fps <= 0:
            raise ValueError("fps must be > 0")
        self.pole = pole
        self.outputs = list(outputs)
        self.frame_ms = 1000.0 / fps
        self.realtime = realtime
        self.limit_ms = limit_ms
        self.now_ms = 0.0
        self._sleep = sleep
        self._clock = clock
        self._next_wall = clock()

    def tick(self) -> None:
        if self.limit_ms is not None and self.now_ms >= self.limit_ms:
            raise StopShow
        self.pole.advance(self.frame_ms)
        self.now_ms += self.frame_ms
        for out in self.outputs:
            out.send(self.pole, self.now_ms)
        if self.realtime:
            self._next_wall += self.frame_ms / 1000.0
            delay = self._next_wall - self._clock()
            if delay > 0:
                self._sleep(delay)
            else:  # we fell behind: don't try to catch up with a burst
                self._next_wall = self._clock()

    def wait(self) -> None:
        """Run until every fade has finished."""
        while self.pole.busy:
            self.tick()

    def hold(self, ms: float) -> None:
        """Keep sending the current frame for ``ms`` milliseconds."""
        end = self.now_ms + ms
        while self.now_ms < end:
            self.tick()

    def close(self) -> None:
        for out in self.outputs:
            out.close(self.pole)
