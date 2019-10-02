import socket
import struct


def get_dst_address(sock):
    sv_addr = sock.getsockopt(0, 80, 16)
    _, port, ip, _ = struct.unpack('>HH4s8s', bytes(sv_addr))
    ip = socket.inet_ntoa(ip)
    return ip, port
