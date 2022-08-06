#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import struct


# def init_recver(port):
#     """
#     初始化建立TCP连接
#     :param ip: 目标主机ip
#     :param port: 目标主机端口
#     :return: socket连接对象
#     """
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.bind(("0.0.0.0", port))  # 绑定端口
#         s.listen(5)  # 等待客户端连接
#         c, addr = s.accept()  # 建立客户端连接
#         print('连接地址：', addr)
#     except socket.error as msg:
#         print(msg)
#         sys.exit(1)
#     return c
def init_recver(ip, port):
    """
    初始化建立UDP连接（客户端）
    :param ip: 目标主机ip
    :param port: 目标主机端口
    :return: socket对象
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((ip, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return s


def init_struct(head_type, file_len):
    """
    构造发送的包头
    包头格式: |Type|Padding|Length|
             Type: char       1bytes
             Padding: char[3] 3bytes
             Length: uint     4bytes
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


def analyze_struct(head):
    """
    解析报文头
    :param head: 报文头
    :return: 报文类型[char] , 数据长度[uint]
    """
    head_type, padding, length = struct.unpack('<c3sI', head)
    return head_type, length


def file_save(file_data, file_path):
    """
    接收文件并保存
    :param file_data: 文件数据
    :param file_path: 保存文件的路径
    :return: 保存结果
    """
    try:
        file = open(file_path, "wb")
        file.write(file_data)
        file.close()
        return True
    except:
        print("Can't save " + file_path + "!")
        return False


def recv_file(ip, port, file_path='./temp_file'):
    """
    接收文件
    :param ip: 主机ip
    :param port: 主机端口
    :param file_path: 保存的文件的路径(默认是 ./temp_file )
    :return: 接收文件的结果
    """
    c = init_recver(ip, port)
    address = (ip, port)
    c.sendto(b'hello octo', address)
    head, temp = c.recvfrom(8)  # 接收报文头
    print(head)
    head_type, length = analyze_struct(head)
    if head_type == b'\x00':  # 接收文件
        c.sendto(b'head ok', address)
        file_data, temp = c.recvfrom(length)
        print(file_data)
        file_save(file_data, file_path)
        print("Recv " + str(length) + " bytes!")
        return True
    else:
        sys.exit(-1)


