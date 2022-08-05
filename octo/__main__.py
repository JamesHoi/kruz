#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
from octo.__version__ import __version__
from octo.settings import DEFAULTS

def arg_parse(args):
    if args.show:
        print('show')

def main():
    parser = argparse.ArgumentParser(description='A command line p2p file transfer')
    parser.add_argument('-v', '--version', help='version 版本信息',action='version',version='octo v'+__version__)
    parser.add_argument('-d', '--debug', help='debug 显示调试信息', action="store_true",default=DEFAULTS['debug'])
    parser.add_argument('-s', '--show', help='show 显示本机信息', action="store_true")
    parser.add_argument('-p', '--src-port', metavar='sp', help='port to listen on for sender 本机端口', type=int, default=DEFAULTS['src_port'])
    parser.add_argument('-i', '--src-ip', metavar='sip', help='network interface for sender 本机IP', default=DEFAULTS['src_ip'])
    parser.add_argument('-I', '--dst-ip',help='STUN host to use')
    parser.add_argument('-P', '--dst-port', type=int,default=DEFAULTS['dst_port'],help='STUN host port to use')
    parser.add_argument('filename', metavar='filename', type=str, nargs='+',
                    help='filename 文件名')
    args = parser.parse_args()
    arg_parse(args)
    print(args.filename)

if __name__ == '__main__':
    main()
