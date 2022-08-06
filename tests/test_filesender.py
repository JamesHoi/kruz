# -*- coding: UTF-8 -*-

import octo.filesender as sender
import socket


def test_send():
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.bind(("", 9999))  # 绑定端口
    assert sender.send_file(c, "./send_test_file") == True
