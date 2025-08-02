from argparse import ArgumentParser
from time import sleep
from subprocess import run
from os import listdir

parser = ArgumentParser(prog='Python daemon', description='Restart python script if failed after 30 seconds, retry 3 times.')
parser.add_argument('file', type=str, help='The python script file name.')
args = parser.parse_args()

file = args.file
if file not in listdir('.'):
    raise FileNotFoundError

count = 0
while count < 3:
    count += 1
    exit_code = run(['python', file])
    if exit_code.returncode == 0:
        break
    else:
        print('Retry after 30 seconds.')
        sleep(30)
