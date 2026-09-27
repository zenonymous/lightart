# DMX / Art-Net map

This is the layout used by `artnet/zbreathe.py`, `artnet/breathe.py` and
`artnet/test.py`. They all use the same fixture definitions. (`funkyfade.py`
uses an older, different layout. See the end of this page.)

## Conventions

- **Fixture** `fixture<strip><n>`: strip `a`–`f`, n = `1`–`48`. Each fixture
  is 6 consecutive DMX channels, i.e. 2 RGB pixels.
- DMX channels are **1-based** (pyartnet `add_channel(start=1, …)`). Only
  channels 1–510 are used, which is 170 pixels per universe.
- Fixture `n` has the same physical height on every strip. The code relies on
  this, so the reversed strips (b, e) are numbered backwards on the wire.
- The code creates 4 separate `ArtNetNode('2.0.0.2')` objects, one per
  universe. They all point at the same controller. A single node with 4
  universes would behave the same.

## Universe → fixture map

| Universe | DMX channels | Fixtures | Wire direction |
|---|---|---|---|
| 0 | 1–288 | a1 … a48 | ascending (`start = 6n − 5`) |
| 0 | 289–510 | b48 … b12 | descending (`start = 577 − 6n`) |
| 1 | 1–66 | b11 … b1 | descending (`start = 67 − 6n`) |
| 1 | 67–354 | c1 … c48 | ascending (`start = 61 + 6n`) |
| 2 | 1–288 | d1 … d48 | same as strip a |
| 2 | 289–510 | e48 … e12 | same as strip b |
| 3 | 1–66 | e11 … e1 | same as strip b |
| 3 | 67–354 | f1 … f48 | same as strip c |

So each controller output is one data line that snakes through three strips:
up a (or d), down b (or e), up c (or f). Channels 355–512 of universes 1 and
3 are not used.

## Pixel colour order

Each fixture takes 6 values: `[p1_0, p1_1, p1_2, p2_0, p2_1, p2_2]`.

- The code calls `[0, 0, 255, 0, 0, 255]` **blue** (`blauw`).
- The code calls `[0, x, 0, 0, x, 0]` **red** (`rood`).

That fits **GRB** byte order (index 0 = G, 1 = R, 2 = B), the usual order for
WS2811/WS2812 strips. So `[g, r, b, g, r, b]`. Note that `test.py` sends
`[c, 0, 0, …]`, which is green on GRB strips, not red.

## The spiral band

The shows split each strip into 6 blocks of 8 fixtures. For animation step
`s ∈ {0, 8, 16, 24, 32, 40}` and strip index `k` (a=0 … f=5), the band covers:

```
fixtures ((s + j + 8·k) mod 48) + 1   for j = 0 … 7
```

At `s = 0`: a1–8, b9–16, c17–24, d25–32, e33–40, f41–48. On every next strip
the band sits one block higher, so it winds once around the pole. Increasing
`s` moves the whole spiral up by one block, and it wraps around at the top.
`artnet/ac.py` is the scratch script that prints this mapping.

## Older layout in `funkyfade.py`

`funkyfade.py` uses segments named `stripN_{a,b,c,d}` of about 24 channels
each (around 95 channels per strip, two strips per universe, alternating
direction). It does not match the 48-fixture layout above. It seems to come
from an earlier or different wiring and should not be used as a reference.
