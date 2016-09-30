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


