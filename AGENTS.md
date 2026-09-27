# AGENTS.md: orientation for AI coding assistants

## What this is

Python scripts for a Dec-2020 light-art installation: an LED pole of 6
strips driven over **Art-Net** from a Raspberry Pi. The production show is
**`artnet/zbreathe.py`**, a blue "breathing" animation with a spiral band
whose behaviour depends on a visitor count. The count comes from WiFi probe
sniffing and is read from `/home/pi/drie`.

**Status: archive.** The installation no longer runs and there is no
hardware to test against. Treat the existing scripts as the historical record
of what ran.

## Read first

1. `README.md`: overview and data-flow diagram.
2. `docs/SHOW_LOGIC.md`: what `zbreathe.py` really does (it differs from the intent).
3. `docs/DMX_MAP.md`: universes, channel formulas, GRB order, spiral maths.
4. `docs/KNOWN_ISSUES.md`: bugs you will otherwise rediscover.
5. `docs/SCRIPTS.md` and `docs/GLOSSARY.md` (the comments are in Dutch).

## Key facts

- **pyartnet 0.8.x only** (`requirements.txt`). Its API:
  `ArtNetNode(ip).add_universe(n).add_channel(start=, width=)`,
  `add_fade(list, ms)` (a new fade **replaces** the running one), and
  `await wait_till_fade_complete()`. Do not "upgrade" to 1.x/2.x without
  porting every script.
- Controller at `2.0.0.2`, universes 0–3, and DMX channels are 1-based.
- 288 fixtures `fixture{a..f}{1..48}`, each 6 channels = 2 GRB pixels. They
  are module-level globals looked up by name with `globals()[...]`. The
  identical 288-line block appears in `zbreathe.py`, `breathe.py` and
  `test.py`.
- Strips b and e are wired in reverse and cross a universe boundary at
  fixture 11/12.
- Hard-coded Pi paths: `/home/pi/drie`, `/home/pi/output.txt`,
  `/home/pi/sniff-probes/`, `/usr/bin/python3.8`, interface `wlx001f1f08a329`,
  GPIO BCM 23 (relay for the LED power supply).
- The step that turned `output.txt` into `/home/pi/drie` is **not in the repo
  and unknown**. Do not invent it and document it as if it existed.
- The author's intent for the band: **brighter red with more visitors**.
  Because of a bug it is always sent at intensity 1 (≈ off).

## Working rules

- There is no hardware, no tests and no CI. You cannot verify light output.
  Syntax-check with `python3 -m py_compile artnet/*.py`. Do not run the
  `artnet/` scripts expecting a result. `zbreathe.py` loops forever and needs
  `/home/pi/drie`.
- Keep the original scripts intact as the historical record. Put new or
  refactored code in new files or modules, unless the owner explicitly asks
  for in-place fixes.
- `ola_scripts/` are GPL-2 third-party examples. Leave their headers alone.
- Keep the docs in `docs/` in sync with any behaviour change, especially
  `KNOWN_ISSUES.md` and `SHOW_LOGIC.md`.
- The owner writes Dutch comments. English is fine for new docs and code.
