#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import socket
import time
import threading
from dataclasses import dataclass, replace
import stun
import sys

from kruz import access_code as ac
from kruz import file_transfer_tcp as ft
from kruz.__version__ import __version__
from kruz.settings import DEFAULTS, CHUNK_SIZE

@dataclass
class ComputerInfo:
    user_name: str
    lan_ips: list
    src_port: int
    ipv6_ip: str
    nat_type: str
    external_ip: str
    external_port: int

def init_info(src_ip,src_port):
    nat_type, external_ip, external_port = stun.get_ip_info(
        src_ip, src_port,
        stun_host=DEFAULTS['stun_ip'],
        stun_port=DEFAULTS['stun_port'])
    lan_ips = socket.gethostbyname_ex(socket.gethostname())[2]
    lan_ips.reverse()
    info = ComputerInfo(
        user_name=socket.gethostname(),
        lan_ips=lan_ips,
        src_port=DEFAULTS['src_port'],
        ipv6_ip=socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[1][4][0] if socket.has_dualstack_ipv6() else None,
        nat_type=nat_type,
        external_ip=external_ip,
        external_port=external_port,
    )
    return info

def show_info(info,lan_ip_num=1):
    if socket.has_dualstack_ipv6():
        print("Your Computer is supported IPv6.")
        print(f'IPv6 address: {info.ipv6_ip}:{info.src_port}')
    if lan_ip_num == 'max': lan_ip_num = len(info.lan_ips)
    
    print('NAT Type:', info.nat_type)
    print(f'External address{"  " if lan_ip_num > 1 else ""}: {info.external_ip}:{info.external_port}')
    lan_ip_num = min(lan_ip_num, len(info.lan_ips))
    for i in range(lan_ip_num):
        tmp = f' {i}' if lan_ip_num > 1 else ''
        print(f'Internal address{tmp}: {info.lan_ips[i]}:{info.src_port}')

def show_tips(info,enable_ipv6=True):
    print('Tips, use the commands below can recv file:')
    if info.ipv6_ip != None and enable_ipv6: print(f'kruz recv {info.ipv6_ip} {info.src_port}')
    print(f'kruz recv {info.external_ip} {info.external_port}')
    print(f'kruz recv {info.lan_ips[0]} {info.src_port}')

def share(args):
    files = args.filename
    if len(files) == 0: raise Exception('No file has been chosen')
    ipv6 = not args.disable_ipv6
    thread = threading.Thread(target=ft.run_server,args=(files[0],args.src_port),kwargs={'enable_ipv6':ipv6},)    
    thread.start()
    info = init_info(args.src_ip,args.src_port)
    if args.check:
        num = 'max' if args.all else 1
        show_info(info,lan_ip_num=num)
    show_tips(info,enable_ipv6=ipv6)
    if args.short: 
        key = ac.upload(info)
        print(f'kruz recv -k {key}')
    print('')
    print('Share server started, waiting for client...')
    thread.join()

def recv(args):
    tmp = time.time()
    if args.key:
        info = ac.download(args.key)
        ip = info['ipv6_ip'] if 'ipv6_ip' in info else info['external_ip']
        port = info['src_port'] if 'ipv6_ip' in info else info['external_port']
    else:
        ip = args.ip
        port = args.port
    success = ft.run_client(ip,port,filename=args.filename)
    if success: print(f'File recved, cost {time.time()-tmp}s')

def check(args):
    num = 'max' if args.all else 1
    info = init_info(DEFAULTS['src_ip'],DEFAULTS['src_port'])
    show_info(info,lan_ip_num=num)
    print('')
    print("Note: These IP and Port might be changed dynamically.")
    if not args.all: print("You can add option -a to check all IPs.")

def main():
    example_text = """Command examples:
Share file: kruz share file1.txt file2.txt
Recv file:  kruz recv 127.0.0.1 19302
Show info:  kruz check"""
    parser = argparse.ArgumentParser(description='A command line p2p file transfer',epilog=example_text,prog='kruz',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', help='version 版本信息',action='version',version='kruz v'+__version__)
    parser.add_argument('-d', '--debug', help='debug 显示调试信息', action="store_true",default=DEFAULTS['debug'])
    #parser.add_argument('--chunk-size', help='chunk-size 传输块大小', type=int, default=4096)

    subparsers = parser.add_subparsers(help='sub-command help',dest='cmd')
    parser_check = subparsers.add_parser('check', help='check 显示本机信息')
    parser_check.add_argument('-a','--all',help='all 显示所有信息',action='store_true',default=DEFAULTS['check-all'])

    parser_recv = subparsers.add_parser('recv', help='recv a file from a peer 接收文件')
    parser_recv.add_argument('ip', type=str,nargs='?',help='destination ip which share file 目的IP')
    parser_recv.add_argument('port', type=int,nargs='?',help='destination port which share file 目的端口')
    parser_recv.add_argument('-f', '--filename', type=str,help='rename recved file/folder 重命名文件(夹)',default=None)
    parser_recv.add_argument('-k',"--key", help='key 提取码',action='store',nargs='?',default=None)

    parser_send = subparsers.add_parser('share', help='share a file to a peer 分享文件')
    parser_send.add_argument('-p', '--src-port', help='port to listen on for share pc 本机端口', type=int, default=DEFAULTS['src_port'])
    parser_send.add_argument('-i', '--src-ip', help='network interface for share pc 本机IP', default=DEFAULTS['src_ip'])
    parser_send.add_argument('--disable-ipv6',help='disable ipv6',action='store_true',default=DEFAULTS['disable-ipv6'])
    parser_send.add_argument('-c','--check',action='store_true',help='check 显示本机信息',default=False)
    parser_send.add_argument('--short',help='short link 生成提取码',action='store_true',default=DEFAULTS['short-link'])
    parser_send.add_argument('filename', type=str, nargs='*',help='filename 文件名')

    try:
        args = parser.parse_args()
    except:
        if args.key == None:
            return
    if args.cmd == 'share':
        share(args)
    elif args.cmd == 'recv':
        recv(args)
    elif args.cmd == 'check':
        check(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
