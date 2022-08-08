#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import socket
import time

import stun
from kruz import file_transfer_tcp as ft
from kruz.__version__ import __version__
from kruz.settings import DEFAULTS


def show_info(src_ip,src_port,enable_ipv6=True):
    if socket.has_dualstack_ipv6() and enable_ipv6:
        ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[1][4][0]
        print("Your Computer is supported IPv6.")
        print(f'IPv6 IP:Port: {ipv6}:{src_port}')
    nat_type, external_ip, external_port = stun.get_ip_info(
        src_ip, src_port,
        stun_host=DEFAULTS['stun_ip'],
        stun_port=DEFAULTS['stun_port'])
    lan_ips = socket.gethostbyname_ex(socket.gethostname())[2]
    print('NAT Type:', nat_type)
    print(f'External IP:Port: {external_ip}:{external_port}')
    for i in range(len(lan_ips)):
        print(f'LAN {i} IP:Port: {lan_ips[i]}:{src_port}')

def show_command_tips():
    pass

def arg_parse(parser,args):
    if args.show:
        show_info(args.src_ip,args.src_port)
        print('')
        print("Note: These IP and Port might be changed dynamically.")
        parser.exit()
    elif args.dst_ip and args.dst_port:
        print(f'Recving file from {args.dst_ip}:{args.dst_port}')
        tmp = time.time()
        ft.run_client(args.dst_ip,args.dst_port)
        print(f'File recved, cost {time.time()-tmp}s')
        parser.exit()
        

def run(args):
    show_info(args.src_ip,args.src_port)
    ft.run_server(args.filename,args.src_port)

def main():
    parser = argparse.ArgumentParser(description='A command line p2p file transfer')
    parser.add_argument('-v', '--version', help='version 版本信息',action='version',version='kruz v'+__version__)
    parser.add_argument('-d', '--debug', help='debug 显示调试信息', action="store_true",default=DEFAULTS['debug'])
    parser.add_argument('-s', '--show', help='show 显示本机信息', action='store_true')
    parser.add_argument('-p', '--src_port', help='port to listen on for sender 本机端口', type=int, default=DEFAULTS['src_port'])
    parser.add_argument('-i', '--src_ip', help='network interface for sender 本机IP', default=DEFAULTS['src_ip'])
    parser.add_argument('-P', '--dst_port', type=int,help='destination port which send file 目的端口')
    parser.add_argument('-I', '--dst_ip',help='destination ip which send file 目的IP')
    parser.add_argument('filename', type=str, nargs='?',
                    help='filename 文件名')
    args = parser.parse_args()
    arg_parse(parser,args)
    run(args)

if __name__ == '__main__':
    main()
