# AGENTS.md: orientation for AI coding assistants

## What this is

Software for a light-art installation from Dec 2020: an LED pole of 6 strips
driven over **Art-Net** from a Raspberry Pi. The show is a blue "breathing"
animation with a red spiral band that reacts to a visitor count. The count is
estimated from WiFi probe requests.

The repo has two layers:

| Layer | Where | Rules |
|---|---|---|
| **Current code** | `lightart/` (package), `tests/`, `deploy/` | Stdlib only, Python ≥ 3.8. Tested and linted. Make changes here. |
| **2020 originals** | `artnet/`, `gpio/`, `show.sh`, `monitor.sh`, `experiments/` | The historical record. Do not edit unless the owner explicitly asks. CI only byte-compiles them. |

The installation is not currently running and **there is no hardware** to
test against. The owner calls the project an archive, but welcomes
improvements in `lightart/`.

## Read first

1. `README.md`: overview, commands, layout.
2. `docs/SHOW_LOGIC.md`: the 2020 show compared with the fixed show.
3. `docs/DMX_MAP.md`: universes, channel formulas, GRB order, spiral maths.
4. `docs/KNOWN_ISSUES.md`: the 2020 bugs and their status.
5. `docs/ARCHITECTURE.md`, `deploy/README.md`, `docs/GLOSSARY.md` (Dutch).

## Package map (`lightart/`)

| Module | Responsibility |
|---|---|
| `layout.py` | Strips a–f × 48 fixtures (6 channels = 2 pixels each), `fixture_address()`, `band(step)`, `PIXEL_ORDER = "GRB"`. |
| `engine.py` | `Pole` (per-fixture linear fades; a new fade replaces the running one, as in pyartnet 0.8), `Runner` (fixed fps, real-time or virtual clock, `wait()`, `hold()`, `limit_ms` → `StopShow`), `Output` interface. |
| `artnet.py` | ArtDMX packets over UDP, the cubic output correction, the RGB→GRB wire mapping, a blackout on close. |
| `shows.py` | `breathe` (fixed), `legacy` (a faithful port with the 2020 bugs), `chase` (wiring test), `BreatheConfig`. |
| `visitors.py` | sniff-probes line parser, sliding-window counter, a `tail -F`-style follower, atomic `write_count`, tolerant `read_count`. |
| `simulator.py` + `sim_template.html` | Records frames on a virtual clock into a self-contained HTML player. |
| `power.py` | Relay on BCM 23 (HIGH = on). |
| `cli.py` | `python -m lightart show / simulate / count-visitors / power`. |

## Key facts

- Controller at `2.0.0.2`, universes 0–3, DMX channels 1-based. Strips b and e
  are wired in reverse and cross a universe boundary at fixture 11/12.
  `tests/test_layout.py` checks the generated map against the 288 hand-written
  lines in the 2020 scripts. Keep that test passing.
- Colours in `lightart` are logical RGB. `artnet.py` applies the cubic
  correction (`v³/255²`, so values below ~40 are effectively off) and the GRB
  order. The simulator shows values before correction.
- The show's visitor intent was confirmed by the owner: **a brighter red band
  with more visitors**. Without visitors the band is dark and the breath is
  fast (1.5 s), as in 2020.
- The 2020 step that produced `/home/pi/drie` is lost. `count-visitors` is a
  2026 replacement, not a reconstruction.
- The GRB order and the "fixture 1 at the bottom" orientation are inferred
  from the code, not confirmed on hardware.
- The 2020 scripts need **pyartnet 0.8.x** (`requirements.txt`). The
  `lightart` package does not use pyartnet.

## Working rules

- Before finishing, run: `python3 -m pytest -q`, `ruff check .`,
  `ruff format --check lightart tests`, and
  `python3 -m compileall -q artnet experiments gpio`.
- Stay compatible with Python 3.8: keep `from __future__ import annotations`
  and `typing.List/Optional` in runtime positions. Do not use `match` or
  3.9+ only APIs.
- No runtime dependencies in `lightart` (RPi.GPIO is imported lazily in
  `power.py`).
- You can't see real LEDs. Use `python3 -m lightart simulate` and the tests
  to check behaviour. Headless Chromium can screenshot the HTML.
- `experiments/ola/` holds GPL-2 third-party examples. Leave their headers
  alone.
- When behaviour changes, update `docs/SHOW_LOGIC.md` and
  `docs/KNOWN_ISSUES.md`.
