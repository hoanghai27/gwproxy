# GwProxy
Gateway proxy for Python 3

## Build

```shell script
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
```

## Install
Using setuptools
```shell script
python3 setup.py install
```

Using pip
```shell script
pip install https://gitlab.com/hoanghai27/gwproxy.git
```

## Usage
Define your own session handler class:
```python
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
```

Start gateway proxy with that handler:
```python
from gwproxy.proxy import TcpGwProxy


proxy = TcpGwProxy('0.0.0.0', 5555, auto_fw=True)
proxy.start(SessionHandler)
```

In case of you want to modify tcp data, just set `auto_fw=False` and send it yourself on `on_client_send()` or `on_server_send()`.

Good luck!
