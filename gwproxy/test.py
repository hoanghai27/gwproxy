from gwproxy.proxy import TcpGwProxy
from gwproxy.tcp import TcpSession


class SessionHandler(TcpSession):
    def __init__(self, client_sock, server_ip, server_port):
        TcpSession.__init__(self, client_sock, server_ip, server_port)
        print("New session %s:%d" %(server_ip, server_port))

    def on_client_send(self, sock, data):
        print('>>> %s' % data.hex())

    def on_server_send(self, sock, data):
        print('<<< %s' % data.hex())

    def on_client_close(self, sock):
        super().on_client_close(sock)
        print("[x] Client closed %s" % sock)

    def on_server_close(self, sock):
        super().on_server_close(sock)
        print("[x] Server closed %s" % sock)


if __name__ == '__main__':
    proxy = TcpGwProxy('0.0.0.0', 5555, auto_fw=True)
    proxy.start(SessionHandler)
