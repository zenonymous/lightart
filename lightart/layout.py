"""Physical layout of the pole and its DMX addresses.

It generates the same map as the 288 hand-written ``add_channel`` lines in
``artnet/zbreathe.py`` (checked by ``tests/test_layout.py``). See
``docs/DMX_MAP.md`` for the details.
"""

from __future__ import annotations

from typing import Dict, Iterator, List, Tuple

STRIPS = "abcdef"
FIXTURES_PER_STRIP = 48
PIXELS_PER_FIXTURE = 2
CHANNELS_PER_PIXEL = 3
CHANNELS_PER_FIXTURE = PIXELS_PER_FIXTURE * CHANNELS_PER_PIXEL
UNIVERSES = (0, 1, 2, 3)

# The strips are daisy-chained a -> b -> c (universes 0-1) and d -> e -> f
# (universes 2-3). The middle strip of each chain is reversed and crosses the
# universe boundary between fixture 11 and 12.
_SPLIT = 11

# Byte order of the pixels on the wire. Inferred from the original code, where
# [0, x, 0] was called "red" and [0, 0, x] "blue". See docs/DMX_MAP.md.
PIXEL_ORDER = "GRB"

# Spiral band: 6 blocks of 8 fixtures. Each next strip is one block higher.
BAND_SIZE = 8
STEPS = tuple(range(0, FIXTURES_PER_STRIP, BAND_SIZE))  # 0, 8, ..., 40

Fixture = Tuple[str, int]  # ("a", 1) .. ("f", 48)


def fixture_address(strip: str, n: int) -> Tuple[int, int]:
    """Return ``(universe, first DMX channel)`` for a fixture. Channels are 1-based."""
    if strip not in STRIPS:
        raise ValueError(f"unknown strip {strip!r}")
    if not 1 <= n <= FIXTURES_PER_STRIP:
        raise ValueError(f"fixture number {n} out of range 1..{FIXTURES_PER_STRIP}")
    index = STRIPS.index(strip)
    base = 0 if index < 3 else 2
    position = index % 3
    if position == 0:  # a, d: ascending in the first universe
        return base, CHANNELS_PER_FIXTURE * (n - 1) + 1
    if position == 1:  # b, e: descending, split across both universes
        if n > _SPLIT:
            return base, 577 - CHANNELS_PER_FIXTURE * n
        return base + 1, 67 - CHANNELS_PER_FIXTURE * n
    return base + 1, 61 + CHANNELS_PER_FIXTURE * n  # c, f: ascending


def all_fixtures() -> Iterator[Fixture]:
    for strip in STRIPS:
        for n in range(1, FIXTURES_PER_STRIP + 1):
            yield strip, n


def address_map() -> Dict[Fixture, Tuple[int, int]]:
    return {fx: fixture_address(*fx) for fx in all_fixtures()}


def band(step: int) -> List[Fixture]:
    """The fixtures of the spiral band at ``step`` (any int; it wraps).

    Strip k (a=0) gets fixtures ((step + j + 8k) mod 48) + 1 for j in 0..7,
    the same maths as ``artnet/ac.py`` and ``zbreathe.py``.
    """
    fixtures = []
    for k, strip in enumerate(STRIPS):
        for j in range(BAND_SIZE):
            fixtures.append((strip, (step + j + BAND_SIZE * k) % FIXTURES_PER_STRIP + 1))
    return fixtures
