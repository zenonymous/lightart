# lightart

Scripts for a light-art installation: an **LED pole** ("ledpaal") made of six
vertical LED strips. The main show makes the whole pole "breathe" in blue while
a band of accent colour spirals around it. The breathing speed (and, as
intended, the band brightness) reacts to how many visitors are nearby. The
visitor count comes from WiFi probe requests sent by passers-by's phones.

Built and run in **December 2020** on a Raspberry Pi. The installation is no
longer running, so this repository is kept **as an archive**. The comments,
variable names and commit messages are mostly in **Dutch**. See
[docs/GLOSSARY.md](docs/GLOSSARY.md).

## How it worked (one paragraph)

A Raspberry Pi ran two things. `monitor.sh` put a USB WiFi dongle in monitor
mode and logged phone probe requests with
[sniff-probes](https://github.com/brannondorsey/sniff-probes). Something that
is not in this repo turned that log into a single number in `/home/pi/drie`.
`show.sh` ran `artnet/zbreathe.py`, which read that number in a loop and sent
Art-Net (DMX over UDP) frames to an Art-Net LED controller at `2.0.0.2`. The
controller drove 6 strips × 48 "fixtures" × 2 RGB pixels, spread over 4 DMX
universes. A relay on GPIO 23 switched the LED power supply.

```
phones ──probe requests──▶ USB WiFi (monitor mode) ──▶ monitor.sh ──▶ /home/pi/output.txt
                                                                         │ (missing step)
                                                                         ▼
                                     show.sh ──▶ artnet/zbreathe.py ◀── /home/pi/drie (visitor count)
                                                        │
                                                 Art-Net / UDP 6454
                                                        ▼
                                  Art-Net controller 2.0.0.2 ──▶ 6 LED strips (a–f)
gpio/gpio_on.py / gpio_off.py ──▶ relay on BCM 23 ──▶ LED power supply
```

## Repository layout

| Path | What it is |
|---|---|
| `artnet/zbreathe.py` | **The production show.** The spiral "breathe" animation, driven by the visitor count. |
| `artnet/breathe.py` | Earlier version of the breathe show, without the visitor input. |
| `artnet/test.py` | The first hardware test: chases one fixture at a time up all strips. |
| `artnet/fade.py`, `artnet/funkyfade.py` | Early experiments (random fades; a different, older strip layout). |
| `artnet/ac.py`, `for.py`, `logic.py`, `syscall.py` | Small scratch scripts used to work out the loops and the file-reading logic. |
| `ola_scripts/` | Unmodified example scripts from the OLA project (GPL-2). An abandoned first approach. |
| `gpio/gpio_on.py`, `gpio_off.py` | Switch the LED power-supply relay on or off. |
| `show.sh` | Starts the show on the Pi. |
| `monitor.sh` | Starts the WiFi probe sniffer on the Pi. |
| `docs/` | Detailed documentation (see below). |

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): hardware, data flow, and what ran on the Pi.
- [docs/DMX_MAP.md](docs/DMX_MAP.md): the complete universe and channel map, pixel colour order, and the spiral maths.
- [docs/SCRIPTS.md](docs/SCRIPTS.md): a reference for every file.
- [docs/SHOW_LOGIC.md](docs/SHOW_LOGIC.md): what `zbreathe.py` actually does, step by step.
- [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md): bugs and pitfalls found during review.
- [docs/GLOSSARY.md](docs/GLOSSARY.md): Dutch words found in the code, and lighting terms.
- [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md): orientation for AI coding assistants.

## Running it (for reference)

Requirements: Python ≥ 3.7 (the Pi used `/usr/bin/python3.8`) and
**`pyartnet` 0.8.x**. The 1.x and 2.x releases have a completely different API.

```sh
pip install -r requirements.txt
python3 artnet/zbreathe.py      # needs /home/pi/drie and an Art-Net node at 2.0.0.2
```

The scripts send UDP to `2.0.0.2:6454`. Without the hardware they still run,
but nothing lights up. `zbreathe.py` also needs `/home/pi/drie` to exist and
to contain a number.
