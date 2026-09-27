# Experiments (Dec 2020)

Scratch scripts from building the installation. They are kept for the record
and are **not used by the show**. They were moved here from `artnet/` and
`ola_scripts/` in the 2026 tidy-up; their contents are unchanged.

| File | What it was for |
|---|---|
| `artnet/ac.py` | Prints the spiral band mapping (now `lightart.layout.band`). |
| `artnet/for.py` | Prints the fixture names a1…f48. |
| `artnet/logic.py` | A dry run of the even/odd breathe-step logic. |
| `artnet/syscall.py` | A prototype of reading `/home/pi/drie`. |
| `artnet/fade.py` | Random fades on random channels. |
| `artnet/funkyfade.py` | Segment fades on an **older strip layout** that doesn't match the final wiring. |
| `ola/fade.py`, `ola/randomloop.py` | OLA example scripts (GPL-2+, headers kept). This was the first approach, before pyartnet. |

They need pyartnet 0.8 (`requirements.txt`) or OLA, and hard-code the node at
`2.0.0.2`.
