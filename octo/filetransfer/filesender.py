#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import struct


def init_sender(ip, port):
    """
    初始化建立TCP连接
    :param ip: 目标主机ip
    :param port: 目标主机端口
    :return: socket对象
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return s


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


def send_file(ip, port, file_path):
    """
    发送文件
    :param ip: 目标主机ip
    :param port: 目标主机端口
    :param file_path: 要发送的文件的路径
    :return: 发送结果
    """
    file_data = file_open(file_path)
    send_data = init_struct(b'\x00', len(file_data))
    send_data += file_data
    s = init_sender(ip, port)
    try:
        s.send(send_data)
        return True
    except:
        return False
