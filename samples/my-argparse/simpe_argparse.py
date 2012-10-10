import argparse
import sys


__author__ = 'neoinsanity'

if __name__ == '__main__':
    argv = sys.argv
    print argv
    argv.pop(0) # we must remove the first argment which is the script path
    # as it is not valid when the arguments are being passes explicitly into
    # the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--heartbeat', type=int, default=3)
    options = parser.parse_args(argv)
