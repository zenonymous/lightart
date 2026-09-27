"""Minimal Art-Net (ArtDMX) sender. It replaces pyartnet and uses only the stdlib."""

from __future__ import annotations

import logging
import socket
from typing import Callable, Dict, Optional

from lightart.engine import Output, Pole
from lightart.layout import PIXEL_ORDER, PIXELS_PER_FIXTURE, UNIVERSES, fixture_address

log = logging.getLogger(__name__)

ARTNET_PORT = 6454
DMX_SIZE = 512
_HEADER = b"Art-Net\x00" + bytes([0x00, 0x50]) + bytes([0x00, 14])  # OpDmx, protocol 14


def cubic(value: float) -> int:
    """pyartnet's ``output_correction.cubic``: v**3 / 255**2."""
    return round(value**3 / (255 * 255))


def linear(value: float) -> int:
    return round(value)


CORRECTIONS: Dict[str, Callable[[float], int]] = {"cubic": cubic, "linear": linear}


def build_universes(pole: Pole, correction: Callable[[float], int] = cubic) -> Dict[int, bytearray]:
    """Map the pole's colours to 512-byte DMX buffers, one per universe."""
    lut = [correction(v) for v in range(256)]
    order = ["RGB".index(c) for c in PIXEL_ORDER]
    data = {u: bytearray(DMX_SIZE) for u in UNIVERSES}
    for fx in pole.fixtures:
        universe, start = fixture_address(*fx)
        rgb = pole.color(fx)
        pixel = bytes(lut[rgb[i]] for i in order)
        offset = start - 1
        buf = data[universe]
        for p in range(PIXELS_PER_FIXTURE):
            buf[offset + 3 * p : offset + 3 * p + 3] = pixel
    return data


def artdmx_packet(universe: int, data: bytes, sequence: int = 0) -> bytes:
    if len(data) % 2 or not 2 <= len(data) <= DMX_SIZE:
        raise ValueError("ArtDMX data length must be even and 2..512")
    return (
        _HEADER
        + bytes([sequence & 0xFF, 0x00, universe & 0xFF, (universe >> 8) & 0x7F])
        + len(data).to_bytes(2, "big")
        + bytes(data)
    )


class ArtNetOutput(Output):
    def __init__(
        self,
        host: str,
        port: int = ARTNET_PORT,
        correction: str = "cubic",
        sock: Optional[socket.socket] = None,
    ) -> None:
        self.address = (host, port)
        self.correction = CORRECTIONS[correction]
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if host.endswith(".255"):
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sequence = 0

    def send(self, pole: Pole, now_ms: float = 0.0) -> None:
        self._sequence = self._sequence % 255 + 1  # 1..255; 0 means "disabled"
        for universe, data in build_universes(pole, self.correction).items():
            try:
                self.sock.sendto(artdmx_packet(universe, data, self._sequence), self.address)
            except OSError as exc:  # e.g. network down: keep the show alive
                log.warning("Art-Net send to %s failed: %s", self.address, exc)

    def close(self, pole: Pole) -> None:
        """Send a blackout so the strips don't freeze on the last frame."""
        self._sequence = self._sequence % 255 + 1
        for universe in UNIVERSES:
            try:
                self.sock.sendto(artdmx_packet(universe, bytes(DMX_SIZE), self._sequence), self.address)
            except OSError as exc:
                log.warning("Art-Net blackout to %s failed: %s", self.address, exc)
        self.sock.close()
