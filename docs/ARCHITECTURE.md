# Architecture

## Physical setup (as reconstructed from the code)

| Component | Details |
|---|---|
| LED pole ("ledpaal") | 6 vertical LED strips, named **a–f** in code. |
| Per strip | 48 "fixtures". Each fixture is 6 DMX channels = **2 RGB pixels**, so 96 pixels per strip and 576 pixels in total. |
| Colour order | Very likely **GRB** (WS281x-style), inferred: see [DMX_MAP.md](DMX_MAP.md#pixel-colour-order). |
| LED controller | Art-Net node at IP **`2.0.0.2`** (the standard Art-Net 2.x.x.x range), UDP port 6454. It uses 4 universes (0–3). |
| Wiring | Serpentine: a → b → c are daisy-chained over universes 0–1, and d → e → f over universes 2–3. Strip b and strip e run in reverse and cross a universe boundary. See [DMX_MAP.md](DMX_MAP.md). |
| Brain | A Raspberry Pi (user `pi`, repo checked out at `/home/pi/lightart`). |
| Visitor sensor | A USB WiFi dongle, interface `wlx001f1f08a329`, in monitor mode. |
| Power | A relay on Pi GPIO **BCM 23** switched the LED power supply. |

Because the strips stand around the pole, the diagonal band that `zbreathe.py`
draws (8 fixtures further up on each next strip) shows up as a **spiral**.

## Software on the Pi

```
/home/pi/
├── lightart/                 this repo
├── sniff-probes/             third-party: github.com/brannondorsey/sniff-probes
├── output.txt                written by sniff-probes (via monitor.sh)
└── drie                      a single number: the visitor count (read by zbreathe.py)
```

1. **`monitor.sh`** runs `sniff-probes.sh` on the monitor-mode interface with
   channel hopping off (`CHANNEL_HOP=0`). It appends the probe requests it sees
   to `/home/pi/output.txt`.
2. **Missing step.** Some script or cron job turned `output.txt` into a number
   in `/home/pi/drie`. The most likely method is counting the unique MAC
   addresses seen in a recent time window. The file name means "three" in
   Dutch, which may hint at a 3-minute window, but that is a guess. **This
   code was never committed, and its author no longer remembers how it
   worked.** Anything that writes digits to `/home/pi/drie` works:
   `zbreathe.py` strips every non-digit character before it calls `int()`.
3. **`show.sh`** runs `/usr/bin/python3.8 /home/pi/lightart/artnet/zbreathe.py`.
   How it was started (cron `@reboot`, `rc.local`, by hand) is not recorded.
4. **`gpio/gpio_on.py` / `gpio_off.py`** switch the LED power supply relay.
   They were probably run by cron for the opening hours, but this is not
   recorded.

## Libraries

- **pyartnet 0.8.x** (asyncio). The scripts rely on this API:
  - `ArtNetNode(host)` → `.add_universe(n)` → `.add_channel(start=, width=)`
  - `channel.add_fade(values, duration_ms)`: a **new fade replaces a running
    fade** on that channel. The start value is whatever the channel shows at
    that moment.
  - `await channel.wait_till_fade_complete()`
  - `universe.output_correction = output_correction.cubic`: brightness is
    mapped roughly as `v³/255²`, so low values such as 1 come out as 0.
  - `await node.start()` / `await node.stop()` start and stop the 25 fps
    send loop.
  - pyartnet ≥ 1.0 renamed and restructured all of this. Do not upgrade
    without porting the code.
- **RPi.GPIO**: only used in `gpio/`.
- **OLA** (`ola.ClientWrapper`): only used in `experiments/ola/`. It needs the
  `olad` daemon and was abandoned in favour of pyartnet.

## The 2026 rewrite

The `lightart` package replaces the pieces above without changing the
hardware. It keeps the same paths, IP and pin by default:

- `lightart show` replaces `show.sh` + `zbreathe.py`. It uses its own
  stdlib Art-Net sender (no pyartnet), sends 25 fps continuously (no gaps
  between steps), survives a missing or empty `drie`, and blacks out on stop.
- `lightart count-visitors` fills the gap between `output.txt` and `drie`.
- `lightart power` replaces `gpio/`.
- systemd units in `deploy/` start everything at boot and restart it on failure.

## Timeline (from the git history)

The scratch files named here now live in `experiments/`.

| Date | What happened |
|---|---|
| 2020-12-09 | Initial upload (the OLA examples, `fade.py`, `funkyfade.py`, `test.py`). Many web-UI edits to `test.py`, a fixture-by-fixture chase. |
| 2020-12-12 | GPIO relay scripts. `for.py` and `ac.py` used to work out the fixture naming and the spiral mapping. `breathe.py`. |
| 2020-12-15/16 | `zbreathe.py` created and "tested!" on the pole ("morgen testen op de ledpaal" = "test on the LED pole tomorrow"). `logic.py` used to debug the even/odd step logic. |
| 2020-12-19/20 | `monitor.sh` (probe sniffing) and `syscall.py` (reading `/home/pi/drie`). The visitor count was wired into `zbreathe.py`. |
| 2020-12-21 | `show.sh`, final tweaks. This is the last 2020 commit. |
| 2026-09 | Documentation, the `lightart` package rewrite, simulator, visitor counter, systemd units, tests and CI. The scratch scripts moved to `experiments/`. |
