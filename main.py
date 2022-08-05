#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse

def arg_parse(args):
    if(args.version):
        print('octo v0.1')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A command line p2p file transfer')
    parser.add_argument('-v', '--version', help='version 版本信息', action="store_true")
    args = parser.parse_args()
    arg_parse(args)
