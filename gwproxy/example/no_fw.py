from gwproxy.proxy import TcpGwProxy
from gwproxy.tcp import TcpProxyCallback, TcpProxyThread


class NoFwCallback(TcpProxyCallback):
    def __init__(self, session: TcpProxyThread):
        self.session = session

    def on_server_connected(self):
        print("[+] Connected to {}:{} -> {}".format(self.session.server_host,
                                                    self.session.server_port,
                                                    self.session.server_sock))

    def on_client_send(self, data):
        print('>>> %s' % data.hex())
        self.session.send_to_server(data)

    def on_server_send(self, data):
        print('<<< %s' % data.hex())
        self.session.send_to_client(data)

    def on_client_close(self):
        print("[x] Client closed")

    def on_server_close(self):
        print("[x] Server closed")


if __name__ == '__main__':
    proxy = TcpGwProxy('0.0.0.0', 7777)
    proxy.start(NoFwCallback)
