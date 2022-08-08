import socket
import threading

PORT = 19302
TEST_FILE_PATH = './tests/test_file'

def test_ipv6_server():
    addr = ("", PORT)
    if socket.has_dualstack_ipv6():
        s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        s = socket.create_server(addr)
        raise Exception("IPv6 is not supported")

    s.listen(1)  # 等待客户端连接
    c, addr = s.accept()  # 建立客户端连接
    with open(TEST_FILE_PATH,"rb") as f:
        c.sendfile(f)
    assert True
    

def test_ipv6_client():
    s = socket.socket(family=socket.AF_INET6)
    s.connect(('::1', PORT, 0, 0))
    data = s.recv(1024)
    data2 = s.recv(10)
    assert data2 == b'helloworld'

def test_ipv4_client():
    s = socket.socket()
    s.connect(("127.0.0.1", PORT))
    data = s.recv(1024)
    data2 = s.recv(10)
    assert data2 == b'helloworld'
