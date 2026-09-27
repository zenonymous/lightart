# Script reference

For the current `lightart/` package see the module map in
[AGENTS.md](../AGENTS.md#package-map-lightart) and `python3 -m lightart --help`.
This page covers the **2020 original scripts**.

Status key: **prod** = ran in the installation · **dev** = development or test
tool · **scratch** = throwaway experiment · **vendored** = third-party example.

## Shell

| File | Status | Description |
|---|---|---|
| `show.sh` | prod (2020) | `/usr/bin/python3.8 /home/pi/lightart/artnet/zbreathe.py`. It has no shebang and no restart logic. |
| `monitor.sh` | prod (2020) | Runs `/home/pi/sniff-probes/sniff-probes.sh` on `wlx001f1f08a329` and writes to `/home/pi/output.txt` with channel hopping off. The interface must already be in monitor mode. |

## `artnet/` and `experiments/artnet/` (pyartnet 0.8)

The scratch files were moved to `experiments/artnet/` in 2026; their contents are unchanged.

| File | Status | Description |
|---|---|---|
| `zbreathe.py` | **prod (2020)** | The spiral breathing show that reacts to the visitor count. It loops forever. Details: [SHOW_LOGIC.md](SHOW_LOGIC.md). |
| `breathe.py` | dev | The previous version of `breathe()`. For each of the 6 band positions it lights the band green-channel 255, waits, then turns it off, one strip after another. Runs once (6 steps) and exits. There is no visitor input. |
| `test.py` | dev | The first hardware test, with the same fixture map. `fixture1(color)` blinks fixture 1 of every strip. The main block runs it for `color` 0..254. `functie()` is a hand-written chase through fixtures 1–9. Its "stap 10" repeats 4→5 by copy-paste mistake. |
| `experiments/artnet/fade.py` | scratch | A single node. It fades 4 random 6-channel groups in universes 0/1 to random values, then to black. |
| `experiments/artnet/funkyfade.py` | scratch | Older strip layout (see [DMX_MAP.md](DMX_MAP.md#older-layout-in-funkyfadepy)). `strips_a..d(color, timer)` set the first channel of each segment. At the moment it only calls `strips_d(255, 1000)`. |
| `experiments/artnet/ac.py` | scratch | Prints the spiral band mapping for each strip letter. |
| `experiments/artnet/for.py` | scratch | Prints the fixture names `a1`…`f48`. It is the prototype of the `globals()["fixture{:c}{}"]` lookup. |
| `experiments/artnet/logic.py` | scratch | A dry run of the even/odd (`adem in`/`adem uit`) step logic. |
| `experiments/artnet/syscall.py` | scratch | A prototype of reading `/home/pi/drie` in a loop. |

## `gpio/` (RPi.GPIO, BCM numbering)

| File | Status | Description |
|---|---|---|
| `gpio_on.py` | prod (2020) | Sets BCM 23 as an output, drives it HIGH (relay → LED PSU on), and exits without cleanup, so the pin stays HIGH. |
| `gpio_off.py` | prod (2020) | Sets up BCM 23, then calls `GPIO.cleanup()`. That turns the pin back into an input, which releases the relay (LED PSU off). |

## `experiments/ola/` (Open Lighting Architecture; formerly `ola_scripts/`)

| File | Status | Description |
|---|---|---|
| `fade.py` | vendored | OLA's `ola_simple_fade.py` example (© 2014 Sean Sill, GPL-2+). |
| `randomloop.py` | vendored/modified | OLA's `ola_send_dmx.py` example (© 2005 Simon Newton, GPL-2+). It was changed to send a random 512-channel frame to universe 0 once a second, 255 times. The `a, b, c, d` arguments are not used. |

These need `olad` running and the `ola` Python bindings. They are not used by
the show.

## Replaced by

| 2020 | 2026 replacement |
|---|---|
| `show.sh` + `artnet/zbreathe.py` | `lightart-show.service` → `python3 -m lightart show` (`--show legacy` reproduces 2020 exactly) |
| `monitor.sh` | `lightart-sniffer.service` |
| the lost `output.txt` → `drie` step | `lightart-visitors.service` → `python3 -m lightart count-visitors` |
| `gpio/gpio_on.py`, `gpio_off.py` | `python3 -m lightart power on/off` + `lightart-power-*.timer` |
| `artnet/test.py` | `python3 -m lightart show --show chase` |
