import re
from collections import defaultdict

import pytest
from conftest import ROOT

from lightart.layout import (
    CHANNELS_PER_FIXTURE,
    STEPS,
    STRIPS,
    address_map,
    all_fixtures,
    band,
    fixture_address,
)

_DEF = re.compile(r"fixture([a-f])(\d+) = universe(\d)\.add_channel\(start=(\d+),\s*width=6\)")


@pytest.mark.parametrize("script", ["artnet/zbreathe.py", "artnet/breathe.py", "artnet/test.py"])
def test_generated_map_matches_original_scripts(script):
    source = (ROOT / script).read_text()
    original = {(s, int(n)): (int(u), int(start)) for s, n, u, start in _DEF.findall(source)}
    assert len(original) == 288
    assert original == address_map()


def test_no_overlaps_and_within_dmx_range():
    used = defaultdict(set)
    for fx in all_fixtures():
        universe, start = fixture_address(*fx)
        channels = set(range(start, start + CHANNELS_PER_FIXTURE))
        assert min(channels) >= 1 and max(channels) <= 510
        assert not used[universe] & channels, fx
        used[universe] |= channels


def test_band_matches_original_mapping():
    # the expression from artnet/ac.py / zbreathe.py
    for step in (*STEPS, 48):
        expected = []
        for index, letter in enumerate("abcdef"):
            mapping = [((x + index * 8) % 48) + 1 for x in range(step, step + 8)]
            expected += [(letter, n) for n in mapping]
        assert band(step) == expected


def test_band_is_a_spiral():
    fixtures = band(0)
    firsts = [n for s, n in fixtures[::8]]
    assert firsts == [1, 9, 17, 25, 33, 41]
    assert {s for s, _ in fixtures} == set(STRIPS)


def test_bad_fixture():
    with pytest.raises(ValueError):
        fixture_address("g", 1)
    with pytest.raises(ValueError):
        fixture_address("a", 49)
