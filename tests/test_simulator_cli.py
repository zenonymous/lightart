import base64
import json
import re

import pytest

from lightart.cli import build_parser, main
from lightart.simulator import parse_schedule, record, render_html, schedule_value


def test_schedule():
    s = parse_schedule("20:3,45:0")
    assert s == [(0.0, 0), (20.0, 3), (45.0, 0)]
    assert [schedule_value(s, t) for t in (0, 19.9, 20, 60)] == [0, 0, 3, 0]
    assert parse_schedule("4") == [(0.0, 4)]


def test_record_and_render():
    rec = record("breathe", seconds=2, schedule=[(0, 2)], fps=20, record_fps=20)
    assert len(rec.frames) == 40
    assert all(len(f) == 288 * 3 for f in rec.frames)
    html = render_html([("breathe", rec)], 20, "t")
    data = json.loads(re.search(r"const DATA = (\{.*?\});\n", html).group(1))
    assert len(base64.b64decode(data["recordings"][0]["frames"])) == 40 * 288 * 3
    assert "__DATA__" not in html


def test_cli_simulate(tmp_path, capsys):
    out = tmp_path / "sim.html"
    assert main(["simulate", "--seconds", "1", "--visitors", "2", "-o", str(out)]) == 0
    assert out.stat().st_size > 1000
    assert "wrote" in capsys.readouterr().out


def test_cli_rejects_unknown_show():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["show", "--show", "nope"])
