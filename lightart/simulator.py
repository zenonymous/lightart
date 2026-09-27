"""Record a show on a virtual clock and write a self-contained HTML player.

The preview shows the *logical* colours (before cubic output correction).
Your screen already applies a perceptual (sRGB) curve, so this looks closer to
what the eye saw on the pole than the corrected wire values would.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from lightart.engine import Output, Pole, Runner, StopShow
from lightart.layout import FIXTURES_PER_STRIP, PIXELS_PER_FIXTURE, STRIPS
from lightart.shows import SHOWS, BreatheConfig

TEMPLATE = Path(__file__).with_name("sim_template.html")

Schedule = List[Tuple[float, int]]  # (seconds, visitors), sorted


def parse_schedule(text: str) -> Schedule:
    """Parse "0:0,20:3,45:0" (at t=0s nobody, at 20s three visitors, ...), or a plain "3"."""
    text = text.strip()
    if ":" not in text:
        return [(0.0, int(text))]
    points = []
    for part in text.split(","):
        t, v = part.split(":")
        points.append((float(t), int(v)))
    points.sort()
    if points[0][0] > 0:
        points.insert(0, (0.0, 0))
    return points


def schedule_value(schedule: Schedule, seconds: float) -> int:
    value = schedule[0][1]
    for t, v in schedule:
        if t <= seconds:
            value = v
    return value


class Recorder(Output):
    """Keeps every n-th frame as 288×3 bytes (fixture order a1..a48, b1, ...)."""

    def __init__(self, every: int = 1) -> None:
        self.every = max(1, every)
        self.frames: List[bytes] = []
        self.visitors: List[int] = []
        self.current_visitors = 0
        self._n = 0

    def send(self, pole: Pole, now_ms: float) -> None:
        self._n += 1
        if (self._n - 1) % self.every:
            return
        self.frames.append(bytes(c for rgb in pole.colors() for c in rgb))
        self.visitors.append(self.current_visitors)


def record(
    show: str,
    seconds: float,
    schedule: Schedule,
    fps: float = 25.0,
    record_fps: float = 25.0,
    cfg: Optional[BreatheConfig] = None,
) -> Recorder:
    cfg = cfg or BreatheConfig()
    recorder = Recorder(every=max(1, round(fps / record_fps)))
    runner = Runner(Pole(), [recorder], fps=fps, realtime=False, limit_ms=seconds * 1000)

    def visitors() -> int:
        recorder.current_visitors = schedule_value(schedule, runner.now_ms / 1000)
        return recorder.current_visitors

    cycle: Callable = SHOWS[show]
    try:
        while True:
            cycle(runner, visitors, cfg)
    except StopShow:
        pass
    return recorder


def render_html(recordings: Sequence[Tuple[str, Recorder]], fps: float, title: str) -> str:
    payload = {
        "fps": fps,
        "strips": STRIPS,
        "fixturesPerStrip": FIXTURES_PER_STRIP,
        "pixelsPerFixture": PIXELS_PER_FIXTURE,
        "recordings": [
            {
                "name": name,
                "frames": base64.b64encode(b"".join(rec.frames)).decode("ascii"),
                "visitors": rec.visitors,
            }
            for name, rec in recordings
        ],
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    return html.replace("__TITLE__", title).replace("__DATA__", json.dumps(payload, separators=(",", ":")))


def simulate(
    shows: Sequence[str],
    seconds: float,
    schedule: Schedule,
    out: str,
    record_fps: float = 20.0,
    cfg: Optional[BreatheConfig] = None,
) -> Path:
    recordings = [
        (name, record(name, seconds, schedule, fps=record_fps, record_fps=record_fps, cfg=cfg)) for name in shows
    ]
    path = Path(out)
    path.write_text(render_html(recordings, record_fps, "LED pole simulator"), encoding="utf-8")
    return path
