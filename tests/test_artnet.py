import socket

from lightart.artnet import ArtNetOutput, artdmx_packet, build_universes, cubic
from lightart.engine import Pole


def test_cubic_matches_pyartnet():
    assert cubic(255) == 255 and cubic(0) == 0 and cubic(1) == 0
    assert cubic(120) == round(120**3 / 255**2)


def test_packet_layout():
    pkt = artdmx_packet(3, bytes(512), sequence=7)
    assert pkt[:8] == b"Art-Net\x00"
    assert pkt[8:10] == b"\x00\x50"  # OpDmx, little endian
    assert pkt[10:12] == b"\x00\x0e"  # protocol 14
    assert pkt[12] == 7 and pkt[14] == 3 and pkt[15] == 0
    assert pkt[16:18] == (512).to_bytes(2, "big")
    assert len(pkt) == 18 + 512


def test_grb_order_and_addresses():
    pole = Pole()
    pole.set([("a", 1)], (255, 0, 0))  # red
    pole.set([("b", 1)], (0, 0, 255))  # blue; b1 lives in universe 1 at channel 61
    data = build_universes(pole)
    assert list(data[0][0:6]) == [0, 255, 0, 0, 255, 0]  # [g, r, b] x 2, as "rood" in zbreathe
    assert list(data[1][60:66]) == [0, 0, 255, 0, 0, 255]
    assert sum(data[2]) == sum(data[3]) == 0


def test_send_over_udp_and_blackout():
    rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx.bind(("127.0.0.1", 0))
    rx.settimeout(2)
    out = ArtNetOutput("127.0.0.1", rx.getsockname()[1])
    pole = Pole()
    pole.set(pole.fixtures, (255, 255, 255))
    out.send(pole)
    packets = [rx.recv(1024) for _ in range(4)]
    assert sorted(p[14] for p in packets) == [0, 1, 2, 3]
    assert packets[0][18] == 255
    out.close(pole)
    blackout = [rx.recv(1024) for _ in range(4)]
    assert all(sum(p[18:]) == 0 for p in blackout)
    rx.close()
