# Known issues

These were found during a code review in 2026. None of them has been fixed,
because the repo is kept as an archive of what actually ran. Line numbers
refer to `artnet/zbreathe.py`.

## Behaviour bugs

1. **The visitor count never reaches the LEDs as brightness** (`:441-447`).
   `for i in range(a, 0, -1): print(i)` leaves `i == 1`, so
   `breathe(1, step)` is always called. With cubic output correction, 1
   comes out as 0. The author confirmed the intent: the band should get
   brighter with more visitors. The commented-out `i = i*10` was the start of
   that (it would need `min(…, 255)`).
2. **Odd steps do nothing, and even steps do both halves of the breath**
   (`:341-385`). The inhale runs when `richting > 0` and the exhale when
   `richting == 1`, both true on the same steps. It was probably meant to be
   `if … else`, or `richting == 0` for the exhale. The visible result is 3
   breaths per pass, and the band skips positions 8→16, 24→32 and 40→0.
3. **The "remove red" loop is nested inside the fixture loop** (`:393-405`,
   indentation). It runs 48 times instead of once. The result looks the same,
   but it wastes CPU on the Pi.
4. **The band is dark, not red, when there are no visitors.** Setting the band
   to `[0, intensity, 0, …]` with `intensity == 0` switches it off. This may
   well have been the intended "idle" look. It is recorded here so nobody
   takes it for a colour bug.

## Robustness

5. **The script crashes on a bad `/home/pi/drie`.** If the file is missing,
   empty or has no digits, `int('')` raises `ValueError` and the show stops.
   `show.sh` has no restart loop and no systemd `Restart=`.
6. It reads the file through `subprocess.check_output("cat …", shell=True)`
   instead of `open()`.
7. `'\D'` is not a raw string, which gives a `SyntaxWarning` on Python ≥ 3.12.
8. **The nodes start and stop on every step.** Each `asyncio.run()` creates a
   new loop and restarts the 4 senders. Between steps no frames are sent. Most
   controllers hold the last frame, but some black out after a timeout.

## Code quality (why editing is error-prone)

9. There are 288 hand-written `fixtureXN = universeK.add_channel(…)` lines,
   copied into 3 files. The code reaches them through
   `globals()["fixture{}{}".format(...)]`. One typo in an address silently
   swaps pixels. The map could be generated with the formulas in
   [DMX_MAP.md](DMX_MAP.md).
10. The spiral mapping block appears 3 times in `zbreathe.py` and uses `x`
    and `y` for different things in nested scopes (the lambda shadows the
    outer `x`, and `y` is reused as a loop variable).
11. `pyartnet` is not pinned in the original code. `pyartnet` ≥ 1.0 breaks
    every script (`requirements.txt` now pins `<0.9`).
12. `test.py` "stap 10" repeats the fixture 4→5 step (a copy-paste error).
13. `funkyfade.py` uses a strip layout that no longer matches the hardware.
