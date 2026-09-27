# Deploying on the Raspberry Pi

This replaces the old way of running things (`show.sh`, `monitor.sh`, the
`gpio/` scripts and an unrecorded cron setup) with systemd units that start at
boot and restart on failure.

| Unit | What it does |
|---|---|
| `lightart-show.service` | `python3 -m lightart show`: the fixed breathe show, sent to `2.0.0.2`. |
| `lightart-sniffer.service` | Runs `sniff-probes.sh` (tcpdump) → `/home/pi/output.txt`. |
| `lightart-visitors.service` | `python3 -m lightart count-visitors`: `output.txt` → `/home/pi/drie`. |
| `lightart-power-on.timer` / `-off.timer` | Switch the LED power relay on at 16:30 and off at 23:30. |

## Install

```sh
# 1. code (Python ≥ 3.8, no pip packages needed for the show)
cd /home/pi && git clone https://github.com/zenonymous/lightart.git
sudo apt install python3-rpi.gpio tcpdump gawk
git clone https://github.com/brannondorsey/sniff-probes.git /home/pi/sniff-probes

# 2. optional settings
sudo cp /home/pi/lightart/deploy/lightart.default /etc/default/lightart

# 3. units
sudo cp /home/pi/lightart/deploy/systemd/lightart-* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lightart-show lightart-sniffer lightart-visitors
sudo systemctl enable --now lightart-power-on.timer lightart-power-off.timer
```

Before you install, edit the timers' `OnCalendar=` lines to the opening
hours you want. `systemctl list-timers 'lightart*'` shows when each will next
fire.

## Operate

```sh
journalctl -fu lightart-show              # show log
journalctl -fu lightart-visitors          # "visitors: N" every 10 s
cat /home/pi/drie                          # current count
sudo systemctl start lightart-power-on     # power on now
sudo systemctl stop lightart-show          # stops and sends a blackout
python3 -m lightart show --show chase      # wiring test (stop the service first)
```

## Notes

- **Visitor count.** A phone counts for `--window` seconds (default 180)
  after its last probe request. Use `--min-rssi -70` (via
  `LIGHTART_COUNT_ARGS`) to ignore phones far away. Modern phones randomise
  their MAC address, so treat the count as "activity", not an exact number of
  people. sniff-probes only logs probes that carry an SSID.
- **Monitor mode.** sniff-probes calls `tcpdump -I`, which switches the
  interface into monitor mode itself. The USB dongle must support that. The
  interface name comes from `IFACE` in the unit (`wlx001f1f08a329`, the
  original dongle). Override it in `/etc/default/lightart`.
- **The log grows forever** (`tee -a`). The counter copes with truncation
  and rotation, so you can add a logrotate rule with `copytruncate`, or
  simply `truncate -s0 /home/pi/output.txt` now and then.
- **Legacy.** To run what ran in 2020 exactly, set
  `LIGHTART_SHOW_ARGS=--show legacy`, or run the original
  `artnet/zbreathe.py` with pyartnet 0.8 (`requirements.txt`).
