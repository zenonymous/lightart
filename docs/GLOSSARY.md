# Glossary

## Dutch → English (as used in code, comments and commits)

| Dutch | English | Where |
|---|---|---|
| ledpaal | LED pole (the installation) | commit messages |
| adem in / inademen | breathe in / inhale | `zbreathe.py`, `logic.py` |
| adem uit / uitademen | breathe out / exhale | `zbreathe.py`, `logic.py` |
| stap | step | step index (`step / 8`) |
| richting | direction | 1 = in, 0 = out |
| even / oneven | even / odd | step parity |
| rood / blauw / zacht blauw | red / blue / soft blue | colours |
| aantal | number, count | visitor count |
| bezoekers | visitors | comment in `zbreathe.py` |
| drie | three | `/home/pi/drie`, the visitor-count file |
| lampen | lamps | fixtures |
| zetten / zet … op | set / set … to | "zet rood" = set red |
| haal … weg | remove | "haal rood weg" = remove the red |
| volgende / vorige | next / previous | step |
| tijd om … | time to … | |
| even tukken | take a quick nap | `syscall.py` sleep |
| pleitte (pleite) | gone | slang |
| morgen testen | test tomorrow | commit message |
| meer debugging | more debugging | commit message |
| dit stukje is om … aan te geven | this bit declares … | comment |
| functie | function | `fade.py`, `test.py` |

## Lighting and networking terms

| Term | Meaning |
|---|---|
| DMX512 | A lighting control protocol: a universe of 512 channels, each 0–255. |
| Universe | One set of 512 DMX channels. Here: 0–3. |
| Art-Net | DMX universes sent over UDP (port 6454). Devices often use the 2.x.x.x network. |
| Fixture (here) | A group of 6 channels = 2 RGB pixels. This is the project's own term, not a real DMX fixture profile. |
| GRB | The byte order of WS281x pixels: green, red, blue. |
| Output correction (cubic) | pyartnet's brightness curve (≈ v³/255²), which makes fades look even to the eye. |
| Probe request | A WiFi frame that phones broadcast while looking for known networks. The installation counted these to estimate how many people were nearby. |
| Monitor mode | A WiFi card mode that captures all frames in the air. `sniff-probes` needs it. |
