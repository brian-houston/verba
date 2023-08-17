import argparse
import pathlib

parser = argparse.ArgumentParser(
        prog='verba',
        description='Latin learning tool'
    )

parser.add_argument('--filename', '-f', help='path to json file with settings', 
                    type=pathlib.Path)

parser.add_argument('--preset', '-p', help='preset library name, e.g. "LL"', 
                    type=pathlib.Path)

parser.add_argument('--hints', '-ht', help='print hints by default', 
                    action='store_true')

parser.add_argument('--ignore_macrons', '-i', help='ignore macrons when checking answers', 
                    action='store_true')
