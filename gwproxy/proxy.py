import socket

from gwproxy.tcp import TcpProxyThread
from gwproxy.util import get_dst_address


class TcpGwProxy:
    def __init__(self, host, port, auto_fw=False):
        self.host = host
        self.port = port
        self.auto_fw = auto_fw
        self.sessions = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, session_cls):
        self.sock.bind((self.host, self.port))
        self.sock.listen(200)
        print("TCP server proxy is listening on %s:%d" % (self.host, self.port))

        while True:
            client, address = self.sock.accept()
            self._on_accept(client, address, session_cls)

    def _on_accept(self, sock, address, callback_obj):
        sock.settimeout(60)
        ip, port = get_dst_address(sock)
        print('- New connection: %s:%s -> %s:%s' % (address[0], address[1], ip, port))
        proxy_thread = TcpProxyThread(sock, ip, port, callback_obj, self.auto_fw)
        proxy_thread.start()
        self.sessions.append(proxy_thread)

    def stop(self):
        print("TLS proxy is exiting ...")
        self.sock.close()