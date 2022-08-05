#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import socket
import stun
from octo.__version__ import __version__
from settings import DEFAULTS

def arg_parse(args):
    pass

def show_info(src_ip,src_port):
    nat_type, external_ip, external_port = stun.get_ip_info(
    src_ip, src_port,
    stun_host=DEFAULTS['stun_ip'],
    stun_port=DEFAULTS['stun_port'])
    lan_ips = socket.gethostbyname_ex(socket.gethostname())[2]
    print('NAT Type:', nat_type)
    print(f'External IP:Port: {external_ip}:{external_port}')
    for i in range(len(lan_ips)):
        print(f'LAN {i} IP:Port: {lan_ips[i]}:{src_port}')

def show_action(a):
    class customAction(argparse.Action):
        def __call__(self, parser, args, values=None, option_string=None):
            show_info(args.src_ip,args.src_port)
            print('')
            print("Note: These IP and Port might be changed dynamically.")
            parser.exit()
    return customAction

def main():
    parser = argparse.ArgumentParser(description='A command line p2p file transfer')
    parser.add_argument('-v', '--version', help='version 版本信息',action='version',version='octo v'+__version__)
    parser.add_argument('-d', '--debug', help='debug 显示调试信息', action="store_true",default=DEFAULTS['debug'])
    parser.add_argument('-s', '--show', help='show 显示本机信息', action=show_action("123"),nargs=0)
    parser.add_argument('-p', '--src_port', help='port to listen on for sender 本机端口', type=int, default=DEFAULTS['src_port'])
    parser.add_argument('-i', '--src_ip', help='network interface for sender 本机IP', default=DEFAULTS['src_ip'])
    parser.add_argument('-P', '--dst_port', type=int,help='destination port which send file 目的端口')
    parser.add_argument('-I', '--dst_ip',help='destination ip which send file 目的IP')
    parser.add_argument('filename', type=str, nargs='+',
                    help='filename 文件名')
    args = parser.parse_args()
    arg_parse(args)
    print(args.filename)

if __name__ == '__main__':
    main()
