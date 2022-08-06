#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import struct


# def init_sender(ip, port):
#     """
#     初始化建立TCP连接
#     :param ip: 目标主机ip
#     :param port: 目标主机端口
#     :return: socket对象
#     """
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect((ip, port))
#     except socket.error as msg:
#         print(msg)
#         sys.exit(1)
#     return s
def init_sender(port):
    """
    初始化建立UDP连接（服务端）
    :param port: 目标主机端口
    :return: socket连接对象
    """
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.bind(("", port))  # 绑定端口
        # c.listen(5)  # 等待客户端连接
        # s, addr = c.accept()  # 建立客户端连接
        # print('连接地址：', addr)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return c


def init_struct(head_type, file_len):
    """
    构造发送的包头
    包头格式: |Type|Padding|Length|
             Type: char
             Padding: char[3]
             Length: uint
    ==============
    Type   | 含义
    ==============
    0x00 | 文件
    0x01 | 待定
    ==============
    发送完包头之后再发具体内容
    :param head_type: 包头的Type
    :param file_len: 要发送的数据长度
    :return: 包头
    """
    sender_head = b""
    sender_head = struct.pack('<c3sI', head_type, b'0', file_len)
    print(len(sender_head))
    return sender_head


def file_open(file_path):
    """
    打开文件，返回文件流
    :param file_path: 要发送的文件的路径
    :return: 文件数据
    """
    try:
        file = open(file_path, "rb")
        file_data = file.read()
        file.close()
        return file_data
    except:
        print("Can't open " + file_path + "!")
        sys.exit(-1)


def send_file(port, file_path):
    """
    发送文件
    :param port: 目标主机端口
    :param file_path: 要发送的文件的路径
    :return: 发送结果
    """
    file_data = file_open(file_path)
    send_data = init_struct(b'\x00', len(file_data))
    print(len(send_data))
    # send_data += file_data
    s = init_sender(port)
    try:
        data, address = s.recvfrom(10)
        assert data == b'hello octo'
        print(address)
        s.sendto(send_data, address)
        data, address = s.recvfrom(7)
        assert data == b'head ok'
        s.sendto(file_data, address)
        return True
    except:
        return False
