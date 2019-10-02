import select
import socket
from threading import Thread


class TcpProxyThread(Thread):
    def __init__(self, client_sock, server_host, server_port, session, auto_fw=False):
        Thread.__init__(self)
        self.session = session
        self.auto_fw = auto_fw

        self.sock_list = []
        self.server_host = server_host
        self.server_port = server_port
        self.client_sock = client_sock
        self.server_sock = None
        self.is_connected = False

    def connect_to_server(self):
        self.server_sock = socket.create_connection((self.server_host, self.server_port))
        self.is_connected = True

    def disconnect(self):
        self.client_sock.close()
        self.server_sock.close()
        self.is_connected = False

    def run(self):
        self.connect_to_server()
        self.session.on_server_connected(self.server_sock)
        self.sock_list = [self.client_sock, self.server_sock]
        while self.is_connected:
            self._do_send_recv()

    def _do_send_recv(self):
        iready, _, _ = select.select(self.sock_list, [], [])
        for sock in iready:
            data = sock.recv(2048)
            if not data:
                self._on_socket_close(sock)
                return

            if sock == self.client_sock:
                self.session.on_client_send(sock, data)
                if self.auto_fw:
                    self.server_sock.send(data)
            else:
                self.session.on_server_send(sock, data)
                if self.auto_fw:
                    self.client_sock.send(data)

    def _on_socket_close(self, sock):
        if sock == self.client_sock:
            self.session.on_client_close(sock)
        else:
            self.session.on_server_close(sock)
        self.disconnect()


class TcpSession:
    def __init__(self, client_sock, server_ip, server_port):
        self.client_sock = client_sock
        self.server_sock = None
        self.server_ip = server_ip
        self.server_port = server_port

    def on_server_connected(self, sock):
        self.server_sock = sock

    def on_client_send(self, sock, data):
        raise RuntimeError("Unimplemented TcpSession.on_client_send")

    def on_server_send(self, sock, data):
        raise RuntimeError("Unimplemented TcpSession.on_server_send")

    def on_client_close(self, sock):
        self.server_sock.close()

    def on_server_close(self, sock):
        self.client_sock.close()
