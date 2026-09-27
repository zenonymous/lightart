# Show logic: `artnet/zbreathe.py`

This page describes what the code **actually does**, which differs from what
it was **meant to do** in a few places. Those places are marked ⚠ and listed
in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Main loop

```python
while True:
    a = int(digits of `cat /home/pi/drie`)        # visitor count
    if a > 0:
        for i in range(a, 0, -1): print(i)        # ⚠ i ends at 1, always
        for step in 0, 8, 16, 24, 32, 40:
            asyncio.run(breathe(i, step))         # intensity = 1
    else:
        for step in 0, 8, 16, 24, 32, 40:
            asyncio.run(breathe(0, step))         # intensity = 0
```

Each `breathe()` call starts the 4 nodes, runs its fades, waits for them to
finish, and stops the nodes again. Each call gets a fresh event loop.

## `breathe(intensity, step)`

- `timer` = 4500 ms, or 1500 ms if `intensity == 0`.
- `stap = step / 8`. When it is even (steps 0, 16, 32), `richting = 1`
  ("in"). When it is odd (steps 8, 24, 40), `richting = 0`.
- ⚠ The "in" block runs when `richting > 0` and the "out" block runs when
  `richting == 1`. Both conditions are true on even steps, and neither is
  true on odd steps. So **even steps do a full in + out breath, and odd steps
  do nothing**. That is 3 breaths per pass of the main loop.

### Inhale ("adem in")

1. All 288 fixtures fade to full blue `[0,0,255,0,0,255]` over `timer`.
2. The spiral band at `step` fades to `[0,intensity,0,0,intensity,0]` over
   1500 ms. This **replaces** the blue fade on those fixtures.
3. Wait until every fixture has finished.

### Exhale ("adem uit")

1. All fixtures fade to soft blue `[0,0,30,0,0,30]` over `timer`.
2. The band at `step` fades to soft blue over 1500 ms. ⚠ This is nested
   inside the fixture loop, so it runs 48 times. It does no harm, but it is
   wasted work.
3. The band at `step + 8` (the next block) fades to
   `[0,intensity,0,0,intensity,0]` over 1500 ms.
4. Wait until every fixture has finished.

## What a viewer saw

- **Nobody detected** (`drie` = 0): a quick breath (1.5 s in, 1.5 s out) from
  full blue to soft blue. The band is `[0,0,0,…]`, so it is a **dark spiral**
  cut out of the blue. It jumps positions 0 → 8, 16 → 24, 32 → 40.
- **Visitors detected**: a slow breath (4.5 s in, 4.5 s out). ⚠ The band
  intensity is always 1, which the cubic output correction turns into 0. So
  the band still looks **dark**, not red.

**Intended:** the author confirmed that the red band should get **brighter as
more visitors are detected**. The commented-out `# i = i*10` shows the plan:
scale the count up to a DMX brightness (it would need capping at 255).

## Timing summary

| State | One breath | One main-loop pass (3 breaths) |
|---|---|---|
| no visitors | ≈ 3 s | ≈ 9 s |
| visitors | ≈ 9 s | ≈ 27 s |

`/home/pi/drie` is read again only at the start of each main-loop pass.
