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
from gwproxy.tcp import TcpProxyThread, TcpProxyCallback


class MyCallback(TcpProxyCallback):

    def on_server_connected(self, session: TcpProxyThread):
        print("[+] Connected to {}:{} -> {}".format(session.server_host, session.server_port, session.server_sock))

    def on_client_send(self, session: TcpProxyThread, data):
        print('>>> %s' % data.hex())
        # session.send_to_server(data)

    def on_server_send(self, session: TcpProxyThread, data):
        print('<<< %s' % data.hex())
        # session.send_to_client(data)

    def on_client_close(self, session: TcpProxyThread):
        print("[x] Client closed")

    def on_server_close(self, session: TcpProxyThread):
        print("[x] Server closed")
```

Start gateway proxy with that callback object:
```python
from gwproxy.proxy import TcpGwProxy


proxy = TcpGwProxy('0.0.0.0', 5555, auto_fw=True)
proxy.start(MyCallback)
```

In case of you want to modify tcp data, just set `auto_fw=False` and send it yourself on `on_client_send()` or `on_server_send()` by using `session.send_to_client(data)` or `session.send_to_server(data)`.

Good luck!
