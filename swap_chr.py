#!/usr/bin/env/python

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file to add or remove chr tag from beginning of line")
parser.add_argument("-o", "--output", help="Output filename")
parser.add_argument("--add", help="Add chr to chromosome field at beginning of line", action="store_true")
parser.add_argument("--remove", help="Remove chr from chromosome field at beginning of line", action="store_true")
args = parser.parse_args()

if args.input is None:
    print("Error: no input specified.")
    parser.print_help()
    sys.exit(1)

if (args.add is False and args.remove is False) or (args.add is True and args.remove is True):
    print("Error: must specify either add or remove")
    parser.print_help()
    sys.exit(1)

if args.output is None:
    if args.remove is True:
        outputfilename = args.input + ".nochr"
    elif args.add is True:
        outputfilename = args.input + ".wchr"
else:
    outputfilename = args.output


with open(args.input,"r") as inputfile:
    with open(outputfilename,"w") as outputfile:
        if args.add is True:
            # ADD CHR
            for line in inputfile:
                if line.startswith("#"):
                    outputfile.write(line)

                else:
                    outputfile.write(str("chr" + line))

        elif args.remove is True:
            #do remove stuff
            for line in inputfile:
                if line.startswith("#"):
                    outputfile.write(line)

                else:
                    outputfile.write(line[3:])
        else:
            print("We should never get here.")
            sys.exit(1)

