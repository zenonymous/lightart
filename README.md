# lightart

Software for a light-art installation: an **LED pole** ("ledpaal") made of six
vertical LED strips. The main show makes the whole pole "breathe" in blue
while a red band spirals around it. The band gets brighter, and the breathing
slows down, as more visitors are nearby. The visitor count comes from WiFi
probe requests sent by passers-by's phones.

The installation first ran in **December 2020** on a Raspberry Pi. The original
scripts are kept as the historical record (their comments are in Dutch; see
[docs/GLOSSARY.md](docs/GLOSSARY.md)). In 2026 the `lightart` Python package
was added next to them. It is a clean, tested rewrite with the 2020 bugs
fixed, a browser simulator, the missing visitor counter, and systemd units.

```
phones ──probe requests──▶ USB WiFi (monitor mode) ──▶ sniff-probes ──▶ /home/pi/output.txt
                                                                            │
                                                     lightart count-visitors
                                                                            ▼
                                         lightart show ◀── /home/pi/drie (visitor count)
                                               │
                                        Art-Net / UDP 6454
                                               ▼
                         Art-Net controller 2.0.0.2 ──▶ 6 LED strips (a–f), 576 pixels
lightart power on|off ──▶ relay on BCM 23 ──▶ LED power supply
```

## Quick start (no hardware needed)

```sh
python3 -m lightart simulate            # writes simulation.html; open it in a browser
```

This records the fixed show and the 2020 original side by side, with a
visitor count that rises over one minute. Try `--visitors 0`,
`--visitors "0:0,20:8"`, `--show chase`, `--seconds 120`.

## Commands

The package needs Python ≥ 3.8 and only the standard library.

| Command | What it does |
|---|---|
| `python3 -m lightart show` | Runs the show on the pole (`--show breathe`, `legacy` or `chase`). Sends a blackout on exit. |
| `python3 -m lightart simulate` | Records shows on a virtual clock into a self-contained HTML player. |
| `python3 -m lightart count-visitors` | Follows the sniff-probes log and writes the visitor count to `/home/pi/drie`. |
| `python3 -m lightart power on\|off` | Switches the LED power-supply relay (needs RPi.GPIO). |

Add `--help` to any command for its options. Useful ones: `--host`,
`--base` / `--per-visitor` (band brightness), `--window` / `--min-rssi`
(visitor counting). To install on the Pi as services, see
[deploy/README.md](deploy/README.md).

## Repository layout

| Path | What it is |
|---|---|
| `lightart/` | **The current code.** `layout` (DMX map), `engine` (fades), `artnet` (UDP sender), `shows`, `visitors`, `simulator`, `power`, `cli`. |
| `tests/` | pytest suite. It includes a check that the generated DMX map matches the 2020 scripts exactly. |
| `deploy/` | systemd units, the `/etc/default/lightart` template, and the install guide. |
| `artnet/zbreathe.py` | *2020 original:* the production show (needs pyartnet 0.8, see `requirements.txt`). |
| `artnet/breathe.py`, `artnet/test.py` | *2020 originals:* an earlier breathe version and the first hardware test. |
| `gpio/`, `show.sh`, `monitor.sh` | *2020 originals:* the relay scripts and launchers (replaced by `deploy/`). |
| `experiments/` | *2020 scratch scripts* and OLA examples, unchanged. |
| `docs/` | Detailed documentation. |

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): hardware, data flow, software on the Pi, history.
- [docs/DMX_MAP.md](docs/DMX_MAP.md): the universe and channel map, pixel colour order, the spiral maths.
- [docs/SHOW_LOGIC.md](docs/SHOW_LOGIC.md): what the 2020 show did and what the fixed show does.
- [docs/SCRIPTS.md](docs/SCRIPTS.md): a reference for every file.
- [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md): the 2020 bugs and how the rewrite handles each one.
- [docs/GLOSSARY.md](docs/GLOSSARY.md): Dutch words in the code, and lighting terms.
- [deploy/README.md](deploy/README.md): running it on the Pi.
- [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md): orientation for AI coding assistants.

## Development

```sh
pip install pytest ruff
python3 -m pytest -q                 # tests
ruff check . && ruff format lightart tests
```

CI (`.github/workflows/ci.yml`) runs lint, the tests on Python 3.8 and
3.12, a byte-compile of the 2020 scripts, and a simulator smoke test.
