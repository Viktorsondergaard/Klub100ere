#!/usr/bin/env python3
import argparse
import csv
import subprocess
import os

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('-beercounter', action='store_true', default=False,
                    help='Set shoutout for beer counting')
parser.add_argument('-shoutouts', type=str, default=os.path.join(os.path.curdir, 'prepared_shoutouts'),
                    help='Input shoutouts folder')
parser.add_argument('-tracks', type=str, default=os.path.join(os.path.curdir, 'prepared_tracks'),
                    help='Input tracks folder')
parser.add_argument('-output', type=str, default=os.path.join(os.path.curdir, 'klub100.mp3'),
                    help='Output file')

args = parser.parse_args()

if not os.path.exists(args.shoutouts) or not os.path.exists(args.tracks):
    exit(1)

inputs = []

with open('klub.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    for i, row in enumerate(reader, 1):
        if os.path.exists(args.shoutouts + f"/{i}.wav"):
            inputs.append('-i')
            inputs.append(os.path.join(args.shoutouts, str(i) + '.wav'))
        else:
            if args.beercounter:
                if i == 17 or i == 34 or i == 51 or i == 67 or i == 83:
                    inputs.append('-i')
                    inputs.append(os.path.join(args.shoutouts, "0_stiv" + '.wav'))
                else:
                    inputs.append('-i')
                    inputs.append(os.path.join(args.shoutouts, str(0) + '.wav'))
            else:
                inputs.append('-i')
                inputs.append(os.path.join(args.shoutouts, str(0) + '.wav'))
        
        inputs.append('-i')
        inputs.append(os.path.join(args.tracks, str(i) + '.wav'))

filter_ = ''.join(('[' + str(a) + ':0]' for a in range(0, 2 * i))) + 'concat=n=' + str(2 * i) + ':v=0:a=1[out]'

print(inputs)
process = subprocess.Popen(['ffmpeg', *inputs, '-filter_complex', filter_, '-map', '[out]', args.output],
                           stdout=subprocess.PIPE)
process.communicate()
