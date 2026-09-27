"""Visitor count: read it (for the show) and produce it (from sniff-probes).

sniff-probes (github.com/brannondorsey/sniff-probes) appends one line per WiFi
probe request that has a non-empty SSID::

    HH:MM:SS -NNdBm aa:bb:cc:dd:ee:ff "SSID"

The counter follows that file. It remembers when each MAC address was last
seen (by wall clock, because the log has no date) and writes the number of
distinct MACs seen within ``window`` seconds to the count file. The show
reads that file.

Caveat: modern phones randomise their MAC address in probe requests, so the
number is an estimate of activity, not an exact head count.
"""

from __future__ import annotations

import logging
import os
import re
import tempfile
import time
from typing import Callable, Dict, NamedTuple, Optional

log = logging.getLogger(__name__)

_LINE = re.compile(
    r"^(?P<time>\d{1,2}:\d{2}:\d{2})\s+(?:(?P<rssi>-?\d+)dBm\s+)?"
    r"(?P<mac>[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})\b"
)


class Probe(NamedTuple):
    time: str
    rssi: Optional[int]
    mac: str


def parse_line(line: str) -> Optional[Probe]:
    m = _LINE.match(line.strip())
    if not m:
        return None
    rssi = int(m.group("rssi")) if m.group("rssi") is not None else None
    return Probe(m.group("time"), rssi, m.group("mac").lower())


class VisitorCounter:
    """Distinct MACs seen within a sliding time window."""

    def __init__(self, window_s: float = 180.0, min_rssi: Optional[int] = None) -> None:
        self.window_s = window_s
        self.min_rssi = min_rssi
        self._last_seen: Dict[str, float] = {}

    def add(self, probe: Probe, now: float) -> bool:
        if self.min_rssi is not None and (probe.rssi is None or probe.rssi < self.min_rssi):
            return False
        self._last_seen[probe.mac] = now
        return True

    def count(self, now: float) -> int:
        cutoff = now - self.window_s
        for mac in [m for m, t in self._last_seen.items() if t < cutoff]:
            del self._last_seen[mac]
        return len(self._last_seen)


def write_count(path: str, count: int) -> None:
    """Write the count atomically, so the show never reads a half-written file."""
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".drie-", dir=directory)
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(f"{count}\n")
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def read_count(path: str) -> int:
    """Read the visitor count. A missing, empty or garbled file counts as 0.

    Like the original, every non-digit is ignored ("3\\n" and "aantal: 3" both
    give 3). The original crashed on an empty file; this returns 0 instead.
    """
    try:
        with open(path) as fh:
            digits = re.sub(r"\D", "", fh.read())
    except OSError as exc:
        log.warning("cannot read visitor count %s: %s (using 0)", path, exc)
        return 0
    if not digits:
        log.warning("visitor count file %s has no number (using 0)", path)
        return 0
    return int(digits)


def follow_and_count(
    log_path: str,
    out_path: str,
    window_s: float = 180.0,
    min_rssi: Optional[int] = None,
    interval_s: float = 10.0,
    from_start: bool = False,
    clock: Callable[[], float] = time.time,
    sleep: Callable[[float], None] = time.sleep,
    max_rounds: Optional[int] = None,
) -> None:
    """Follow ``log_path`` (like ``tail -F``) and rewrite ``out_path`` every ``interval_s``.

    It starts at the end of the file unless ``from_start`` is set: old lines
    carry no date, so their visitors can't be placed in the window. The file
    is reopened when it is truncated or replaced (log rotation).
    """
    counter = VisitorCounter(window_s, min_rssi)
    fh = None
    inode = None
    pending = ""
    rounds = 0
    while max_rounds is None or rounds < max_rounds:
        rounds += 1
        if fh is None:
            try:
                fh = open(log_path)
                inode = os.fstat(fh.fileno()).st_ino
                if not from_start:
                    fh.seek(0, os.SEEK_END)
                from_start = True  # after the first open, always read reopened files fully
            except OSError as exc:
                log.warning("waiting for %s: %s", log_path, exc)
        if fh is not None:
            chunk = fh.read()
            now = clock()
            if chunk:
                lines = (pending + chunk).split("\n")
                pending = lines.pop()  # keep an unfinished last line for later
                for line in lines:
                    probe = parse_line(line)
                    if probe:
                        counter.add(probe, now)
            try:
                st = os.stat(log_path)
                if st.st_ino != inode or st.st_size < fh.tell():
                    fh.close()
                    fh, pending = None, ""
            except OSError:
                fh.close()
                fh, pending = None, ""
        count = counter.count(clock())
        write_count(out_path, count)
        log.info("visitors: %d", count)
        sleep(interval_s)
