from gwproxy.proxy import TcpGwProxy
from gwproxy.tcp import TcpProxyCallback, TcpProxyThread


class NoFwCallback(TcpProxyCallback):
    def on_server_connected(self, session: TcpProxyThread):
        print("[+] Connected to {}:{} -> {}".format(session.server_host, session.server_port, session.server_sock))

    def on_client_send(self, session: TcpProxyThread, data):
        print('>>> %s' % data.hex())
        session.send_to_server(data)

    def on_server_send(self, session: TcpProxyThread, data):
        print('<<< %s' % data.hex())
        session.send_to_client(data)

    def on_client_close(self, session: TcpProxyThread):
        print("[x] Client closed")

    def on_server_close(self, session: TcpProxyThread):
        print("[x] Server closed")


if __name__ == '__main__':
    proxy = TcpGwProxy('0.0.0.0', 7777)
    proxy.start(NoFwCallback)
