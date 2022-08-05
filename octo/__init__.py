
import argparse

def arg_parse(args):
    if(args.version):
        print('octo v0.1')

def main():
    parser = argparse.ArgumentParser(description='A command line p2p file transfer')
    parser.add_argument('-v', '--version', help='version 版本信息', action="store_true")
    args = parser.parse_args()
    arg_parse(args)