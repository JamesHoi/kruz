# -*- coding: UTF-8 -*-
# todo: ipv6 and ipv4 service open together
#       tcp hole punching like bt software
#       multi-threading sharing
#       tcp keep alive
#       tcp send computer info

import socket
import os
import struct
import time
from tqdm import tqdm

from kruz.settings import *

def read_file_size(file):
    size = file.seek(0, os.SEEK_END)
    file.seek(0)
    return size

def send_file(s,file):
    """
    构造发送的包头
    包头格式: |Type|File name Length|File Length
             Type: char[2]
             File name Length: char[2]
             File Length: uint
    ==============
    Type   | 含义
    ==============
    0x00 | 文件
    0x01 | 待定
    ==============
    发送完包头之后再发具体内容
    :param type: 包头的Type
    :param length: 要发送的数据长度
    :return: 包头
    """
    length = read_file_size(file)
    name = os.path.basename(file.name)
    if len(name) > 0xffff: 
        raise Exception("file name is too long")
    head = b""
    head = struct.pack('<2s2sI', 
            b'\x00\x00',
            len(name).to_bytes(2,byteorder="little"),
            length)
    s.send(head)
    s.send(name.encode("utf-8"))
    progress = tqdm(total=length,unit='B', unit_divisor=CHUNK_SIZE,unit_scale=True,desc=name)
    for _ in range(length//CHUNK_SIZE):
        progress.update(CHUNK_SIZE)
        s.send(file.read(CHUNK_SIZE))
    s.send(file.read(length%CHUNK_SIZE))

def run_server(filename,port,enable_ipv6=True):
    f = open(filename,"rb")
    addr = ("", port)
    if socket.has_dualstack_ipv6() and enable_ipv6:
        s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        s = socket.create_server(addr)
        print("IPv6 is not supported")
    
    s.listen(5)
    while True:
        c, addr = s.accept()
        print("Connected from", addr)
        send_file(c,f)
        break

def run_client(ip,port,filename=None):
    try:
        ipv6 = socket.has_dualstack_ipv6()
        if not ipv6 and ":" in ip: 
            raise Exception("IPv6 is not supported")
        if ipv6 and ":" in ip:
            s = socket.socket(family=socket.AF_INET6)
            s.connect((ip, port, 0, 0))
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
    except ConnectionRefusedError as e:
        print("Cannot connect to peer")
        return False
    
    print("Connected to peer {}:{}".format(ip,port))
    # analyze head
    head = s.recv(8)
    head_type, filename_length, length = struct.unpack('<2s2sI', head)
    if head_type == b'\x00\x00':
        tmp = int.from_bytes(filename_length, byteorder="little")
        filename = s.recv(tmp).decode() if filename == None else filename
        f = open(filename,"wb")
        progress = tqdm(total=length,unit='B', unit_divisor=CHUNK_SIZE,unit_scale=True,desc=filename)
        for _ in range(length//CHUNK_SIZE):
            progress.update(CHUNK_SIZE)
            f.write(s.recv(CHUNK_SIZE,socket.MSG_WAITALL))
        f.write(s.recv(length%CHUNK_SIZE,socket.MSG_WAITALL))
        f.close()
        s.close()
    return True