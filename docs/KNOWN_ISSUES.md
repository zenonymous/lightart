# Known issues

These issues in the 2020 scripts were found in a code review in 2026. The
originals are kept unchanged as the historical record. The **Status** line
says how the `lightart` package (the rewrite) handles each one. Line numbers
refer to `artnet/zbreathe.py`.

## Behaviour bugs

1. **The visitor count never reaches the LEDs as brightness** (`:441-447`).
   `for i in range(a, 0, -1): print(i)` leaves `i == 1`, so `breathe(1, step)`
   is always called. With cubic output correction, 1 comes out as 0. The
   author confirmed the intent: the band should get brighter with more
   visitors. The commented-out `i = i*10` was the start of that.
   **Status:** fixed. `band_intensity()` gives 0 visitors → 0, then
   `base + per_visitor·(n−1)`, capped at 255. Both values can be tuned from
   the CLI.
2. **Odd steps do nothing, and even steps do both halves of the breath**
   (`:341-385`). The inhale runs when `richting > 0` and the exhale when
   `richting == 1`, both true on the same steps. The visible result is 3
   breaths per pass, and the band skips positions 8→16, 24→32 and 40→0.
   **Status:** fixed. There is one breath per step, and the band advances
   one block per breath.
3. **The "remove red" loop is nested inside the fixture loop** (`:393-405`).
   It runs 48 times instead of once. **Status:** fixed (it no longer exists in
   the rewrite).
4. **The band is dark, not red, when there are no visitors**
   (`[0, 0, 0, …]`). This was probably the intended idle look, so nobody
   should take it for a colour bug. **Status:** kept on purpose.

## Robustness

5. **The script crashes on a bad `/home/pi/drie`** (missing, empty, or no
   digits → `ValueError`), and nothing restarts it. **Status:** fixed.
   `read_count()` treats a bad file as 0 and logs a warning, the counter writes
   the file atomically, and systemd has `Restart=always`.
6. It reads the file through `subprocess.check_output("cat …", shell=True)`.
   **Status:** fixed. The rewrite uses `open()`.
7. `'\D'` is not a raw string (a `SyntaxWarning` on Python ≥ 3.12).
   **Status:** fixed in the rewrite.
8. **The nodes start and stop on every step.** No frames are sent between
   steps, and some controllers black out after a timeout. **Status:** fixed.
   The Runner sends a steady 25 fps, and sends a blackout on stop.
9. **The visitor-count producer was never committed** (`output.txt` → `drie`).
   **Status:** replaced by `lightart count-visitors`. Its sliding-window
   heuristic is a new design, not a recovery of the original.

## Code quality

10. There are 288 hand-written `fixtureXN = …add_channel(…)` lines, copied
    into 3 files and reached through `globals()[…]`. **Status:** fixed. The map
    is generated in `lightart/layout.py`, and a test checks it against the
    originals.
11. The spiral mapping appears 3 times, with shadowed `x`/`y` variables.
    **Status:** fixed. It is now one `band(step)` function.
12. `pyartnet` was not pinned, and ≥ 1.0 breaks the 2020 scripts.
    **Status:** pinned in `requirements.txt` for the originals. The rewrite
    does not use pyartnet.
13. `test.py` "stap 10" repeats the 4→5 step (a copy-paste error).
    **Status:** the original is unchanged. `--show chase` replaces it.
14. `experiments/artnet/funkyfade.py` uses a strip layout that no longer
    matches the hardware. **Status:** documented only.

## Open questions (can't be settled without the hardware)

- The pixel colour order is GRB, inferred from the naming in the code.
- Fixture 1 is shown at the **bottom** of each strip in the simulator. This is
  a guess.
- The strips are shown in order a–f around the pole, 60° apart. The spiral
  depends on this.
- Relay polarity: HIGH = power on (the owner confirmed that the relay switches
  the LED PSU). `power off` drives the pin LOW, where the original used a
  floating input.
