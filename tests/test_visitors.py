import os

import pytest

from lightart.visitors import (
    Probe,
    VisitorCounter,
    follow_and_count,
    parse_line,
    read_count,
    write_count,
)


def test_parse_sniff_probes_line():
    assert parse_line('21:14:03 -67dBm A4:5E:60:AA:BB:CC "Ziggo1234"') == Probe("21:14:03", -67, "a4:5e:60:aa:bb:cc")
    assert parse_line('9:01:02 aa:bb:cc:dd:ee:ff "x"') == Probe("9:01:02", None, "aa:bb:cc:dd:ee:ff")
    assert parse_line("garbage") is None
    assert parse_line("") is None


def test_counter_window_and_rssi():
    c = VisitorCounter(window_s=60, min_rssi=-70)
    assert c.add(Probe("", -50, "a"), now=0)
    assert not c.add(Probe("", -80, "b"), now=0)  # too far away
    assert not c.add(Probe("", None, "c"), now=0)  # unknown strength
    c.add(Probe("", -60, "d"), now=50)
    c.add(Probe("", -60, "a"), now=55)  # seen again: stays counted
    assert c.count(now=100) == 2
    assert c.count(now=116) == 0


@pytest.mark.parametrize("content, expected", [("3\n", 3), ("aantal: 12", 12), ("", 0), ("none", 0)])
def test_read_count(tmp_path, content, expected):
    p = tmp_path / "drie"
    p.write_text(content)
    assert read_count(str(p)) == expected


def test_read_count_missing_file(tmp_path):
    assert read_count(str(tmp_path / "nope")) == 0


def test_write_count_atomic(tmp_path):
    p = tmp_path / "drie"
    write_count(str(p), 5)
    write_count(str(p), 6)
    assert p.read_text() == "6\n"
    assert os.listdir(tmp_path) == ["drie"]


def test_follow_new_lines_truncation_and_window(tmp_path):
    log = tmp_path / "output.txt"
    out = tmp_path / "drie"
    log.write_text('10:00:00 -50dBm aa:aa:aa:aa:aa:01 "old"\n')  # before start: ignored
    now = [1000.0]
    script = {
        1: lambda: log.open("a").write(
            '10:00:01 -50dBm aa:aa:aa:aa:aa:02 "x"\n10:00:01 -50dBm aa:aa:aa:aa:aa:03 "y"\n'
        ),
        2: lambda: log.write_text('10:00:02 -50dBm aa:aa:aa:aa:aa:04 "z"\n'),  # truncated / rotated
        3: lambda: None,
    }
    results = []

    def sleep(_):
        results.append(int(out.read_text()))
        n = len(results)
        now[0] += 100
        if n in script:
            script[n]()

    follow_and_count(str(log), str(out), window_s=150, interval_s=0, clock=lambda: now[0], sleep=sleep, max_rounds=5)
    # t=1000: 0 (the old line is skipped); t=1100: 02+03; t=1200: truncation seen, still 2;
    # t=1300: reopened and 04 counted, while 02/03 (last seen at 1100) left the 150 s window; t=1400: 04
    assert results == [0, 2, 2, 1, 1]
