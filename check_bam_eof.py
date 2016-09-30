#!/usr/bin/env python
# Purpose: Check that an input BAM file has the correct EOF tag.
# Input:
# Output: A list of BAMs without the EOF tag

# Note:
# Per http://seqanswers.com/forums/showthread.php?t=15363
# The final 28 bytes of a BAM should read:
# 0x1f 0x8b 0x08 0x04 0x00 0x00 0x00 0x00
# 0x00 0xff 0x06 0x00 0x42 0x43 0x02 0x00
# 0x1b 0x00 0x03 0x00 0x00 0x00 0x00 0x00
# 0x00 0x00 0x00 0x00

import argparse
import sys
import subprocess

true_eof = ['1f', '8b', '08', '04', '00', '00', '00', '00', '00', 'ff', '06', '00', '42', '43', '02', '00', '1b', '00', '03', '00', '00', '00', '00', '00', '00', '00', '00', '00']
parser = argparse.ArgumentParser()
parser.add_argument("bams", nargs='*', help="One or more filenames/filepaths of BAMs to check for EOF")
parser.add_argument("-f", "--bam_list_filename", help="A list of filenames/filepaths of BAMs to check for EOF")
# create an optional positional argument for a list of bams; args.bams will be a list
args = parser.parse_args()

# check for validity of inputs

if (args.bam_list_filename is None) and (args.bams == []):
    print "\nError: You must specify either a list of BAM filenames/paths or one or more BAM paths\n"
    parser.print_help()
    sys.exit(2)

if (args.bams != []):
    bams = args.bams
    if (args.bam_list_filename is not None):
        print "\nWarning: You entered file of BAM paths *and* individual BAM paths. Ignoring the file of BAM paths.\n"
else:
    with open(args.bam_list_filename,"r") as f:
        bams = f.read().splitlines()


for bam_file in bams:
    cmd = "tail -n 1 " + bam_file + " | hexdump -C | tail -n 5"
    command = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    (bam_tail, err) = command.communicate()
    bam_tail_words = bam_tail.rsplit(' ')
    #transform bam_tail from string into list of strings

    tail_bits = []

    #canonical hexdump returns 2-column hex bytes, offset position, and ACSII strings. Only the hex bytes will have len of 2
    for item in bam_tail_words:
        if len(item) != 2:
            continue
        else:
            tail_bits.append(item)

    candidate_eof = tail_bits[-28:]
    #candidate_eof is now the last 28 bytes of the file, in order

    if candidate_eof == true_eof:
        continue
    else:
        print "Could not find EOF for: " + bam_file


