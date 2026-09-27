"""Command line: ``python -m lightart <command>``."""

from __future__ import annotations

import argparse
import logging
import signal
import sys
from typing import List, Optional

from lightart import __version__
from lightart.shows import SHOWS, BreatheConfig

log = logging.getLogger("lightart")


def _config(args: argparse.Namespace) -> BreatheConfig:
    return BreatheConfig(
        slow_ms=args.slow_ms,
        fast_ms=args.fast_ms,
        band_ms=args.band_ms,
        base=args.base,
        per_visitor=args.per_visitor,
    )


def _add_show_options(p: argparse.ArgumentParser) -> None:
    g = p.add_argument_group("breathe show tuning")
    d = BreatheConfig()
    g.add_argument("--slow-ms", type=int, default=d.slow_ms, help="half-breath with visitors (default %(default)s)")
    g.add_argument("--fast-ms", type=int, default=d.fast_ms, help="half-breath without visitors (default %(default)s)")
    g.add_argument("--band-ms", type=int, default=d.band_ms, help="band fade time (default %(default)s)")
    g.add_argument(
        "--base", type=int, default=d.base, help="band brightness for 1 visitor, 0-255 (default %(default)s)"
    )
    g.add_argument(
        "--per-visitor",
        type=int,
        default=d.per_visitor,
        help="extra band brightness per additional visitor (default %(default)s)",
    )


def cmd_show(args: argparse.Namespace) -> int:
    from lightart.artnet import ArtNetOutput
    from lightart.engine import Pole, Runner
    from lightart.shows import run_forever
    from lightart.visitors import read_count

    def _terminate(signum, frame):  # systemd stop → clean blackout via finally
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, _terminate)
    output = ArtNetOutput(args.host, args.port, correction=args.correction)
    runner = Runner(Pole(), [output], fps=args.fps, realtime=True)
    log.info(
        "show %r → %s:%d at %s fps, visitors from %s", args.show, args.host, args.port, args.fps, args.visitors_file
    )
    try:
        run_forever(args.show, runner, lambda: read_count(args.visitors_file), _config(args))
    except KeyboardInterrupt:
        log.info("stopping, sending blackout")
    finally:
        runner.close()
    return 0


def cmd_simulate(args: argparse.Namespace) -> int:
    from lightart.simulator import parse_schedule, simulate

    shows = args.show or ["breathe", "legacy"]
    path = simulate(
        shows, args.seconds, parse_schedule(args.visitors), args.output, record_fps=args.fps, cfg=_config(args)
    )
    print(f"wrote {path} ({path.stat().st_size // 1024} KiB) - open it in a browser")
    return 0


def cmd_count(args: argparse.Namespace) -> int:
    from lightart.visitors import follow_and_count

    try:
        follow_and_count(
            args.log,
            args.out,
            window_s=args.window,
            min_rssi=args.min_rssi,
            interval_s=args.interval,
            from_start=args.from_start,
        )
    except KeyboardInterrupt:
        pass
    return 0


def cmd_power(args: argparse.Namespace) -> int:
    from lightart.power import set_power

    set_power(args.state == "on", pin=args.pin)
    log.info("LED power %s (BCM %d)", args.state, args.pin)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lightart", description="Drive the LED pole over Art-Net.")
    p.add_argument("--version", action="version", version=f"lightart {__version__}")
    p.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("show", help="run a show on the real pole (loops forever)")
    s.add_argument("--show", choices=sorted(SHOWS), default="breathe")
    s.add_argument("--host", default="2.0.0.2", help="Art-Net node IP (default %(default)s)")
    s.add_argument("--port", type=int, default=6454)
    s.add_argument("--fps", type=float, default=25.0)
    s.add_argument("--correction", choices=["cubic", "linear"], default="cubic")
    s.add_argument("--visitors-file", default="/home/pi/drie")
    _add_show_options(s)
    s.set_defaults(func=cmd_show)

    m = sub.add_parser("simulate", help="record shows into a self-contained HTML player")
    m.add_argument(
        "--show",
        action="append",
        choices=sorted(SHOWS),
        help="show to record, can be repeated (default: breathe and legacy side by side)",
    )
    m.add_argument("--seconds", type=float, default=60.0)
    m.add_argument(
        "--visitors",
        default="0:0,15:1,30:4,45:10",
        help='a constant ("3") or a schedule "seconds:count,..." (default %(default)s)',
    )
    m.add_argument("--fps", type=float, default=20.0, help="recording frame rate (default %(default)s)")
    m.add_argument("-o", "--output", default="simulation.html")
    _add_show_options(m)
    m.set_defaults(func=cmd_simulate)

    c = sub.add_parser("count-visitors", help="turn sniff-probes output into the visitor-count file")
    c.add_argument("--log", default="/home/pi/output.txt", help="sniff-probes output (default %(default)s)")
    c.add_argument("--out", default="/home/pi/drie", help="count file the show reads (default %(default)s)")
    c.add_argument("--window", type=float, default=180.0, help="seconds a phone stays counted (default %(default)s)")
    c.add_argument(
        "--min-rssi",
        type=int,
        default=None,
        help="ignore probes weaker than this dBm, e.g. -70, to count only nearby phones",
    )
    c.add_argument("--interval", type=float, default=10.0, help="seconds between updates (default %(default)s)")
    c.add_argument("--from-start", action="store_true", help="also read lines already in the log")
    c.set_defaults(func=cmd_count)

    w = sub.add_parser("power", help="switch the LED power-supply relay")
    w.add_argument("state", choices=["on", "off"])
    w.add_argument("--pin", type=int, default=23, help="BCM pin (default %(default)s)")
    w.set_defaults(func=cmd_power)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    return args.func(args)
