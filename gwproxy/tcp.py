from socket import socket, create_connection, timeout
import threading
from queue import Queue
from threading import Thread


class TcpTrafficHandler(Thread):
    def __init__(self, in_sock: socket, out_sock: socket, buff_size=1024):
        Thread.__init__(self)
        self._in_sock = in_sock
        self._out_sock = out_sock
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.buff_size = buff_size

        self._stop_event = threading.Event()

    def run(self) -> None:
        self._in_sock.settimeout(0.1)
        while not self.stopped():
            self.do_send()
            self.do_recv()

        self._in_sock.close()
        self._out_sock.close()

    def do_send(self):
        while not self.out_queue.empty():
            data = self.out_queue.get()
            try:
                self._out_sock.send(data)
            except (ConnectionError, OSError):
                return

    def do_recv(self):
        data = None
        try:
            data = self._in_sock.recv(self.buff_size)
        except timeout:
            return
        except (ConnectionError, OSError):
            self.stop()

        if data:
            self.in_queue.put(data)
        else:
            self.stop()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def send(self, data: bytes):
        self.out_queue.put(data)


class TcpProxyThread(Thread):
    def __init__(self, client_sock, server_host, server_port, callback_cls, auto_fw=False, buff_size=1024):
        Thread.__init__(self)
        self.callback_obj = callback_cls()
        self.auto_fw = auto_fw
        self.buff_size = buff_size

        self.sock_list = []
        self.server_host = server_host
        self.server_port = server_port
        self.client_sock = client_sock
        self.server_sock = None
        self.is_connected = False

        self.client: TcpTrafficHandler = None
        self.server: TcpTrafficHandler = None

    def _connect_to_server(self):
        self.server_sock = create_connection((self.server_host, self.server_port))

        self.client = TcpTrafficHandler(self.client_sock, self.server_sock, self.buff_size)
        self.client.start()
        self.server = TcpTrafficHandler(self.server_sock, self.client_sock, self.buff_size)
        self.server.start()

        self.is_connected = True

    def disconnect(self):
        self.is_connected = False
        self.client.stop()
        self.server.stop()

    def send_to_client(self, data: bytes):
        self.server.send(data)

    def send_to_server(self, data: bytes):
        self.client.send(data)

    def run(self):
        self._connect_to_server()
        self.callback_obj.on_server_connected(self)
        self.sock_list = [self.client_sock, self.server_sock]
        while self.client.is_alive() and self.server.is_alive():
            self._handle_in_queue(self.client_sock, self.client.in_queue)
            self._handle_in_queue(self.server_sock, self.server.in_queue)

        if self.client.is_alive():
            self._on_socket_close(self.client_sock)

        if self.server.is_alive():
            self._on_socket_close(self.server_sock)

    def _handle_in_queue(self, sock, queue, limit=10):
        i = 0
        while not queue.empty() and i < limit:
            data = queue.get()
            if sock == self.client_sock:
                self.callback_obj.on_client_send(self, data)
                if self.auto_fw:
                    self.server_sock.send(data)
            else:
                self.callback_obj.on_server_send(self, data)
                if self.auto_fw:
                    self.client_sock.send(data)
            i += 1

    def _on_socket_close(self, sock):
        if sock == self.client_sock:
            self.callback_obj.on_client_close(self)

        else:
            self.callback_obj.on_server_close(self)
        self.disconnect()


class TcpProxyCallback:
    def on_server_connected(self, session: TcpProxyThread):
        raise RuntimeError("Unimplemented TcpProxyThread.on_server_connected")

    def on_client_send(self, session: TcpProxyThread, data: bytes):
        raise RuntimeError("Unimplemented TcpProxyThread.on_client_send")

    def on_server_send(self, session: TcpProxyThread, data: bytes):
        raise RuntimeError("Unimplemented TcpProxyThread.on_server_send")

    def on_client_close(self, session: TcpProxyThread):
        raise RuntimeError("Unimplemented TcpProxyThread.on_client_close")

    def on_server_close(self, session: TcpProxyThread):
        raise RuntimeError("Unimplemented TcpProxyThread.on_server_close")
