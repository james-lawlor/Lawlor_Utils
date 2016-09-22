#Purpose: select random lines from a file
#Input: a text file with any headers/metatdata beginning with #

import sys
import getopt
from time import clock
from random import SystemRandom

def main(argv):

    input_filename = ""
    output_filename = ""
    fraction_to_print = 0
    added_metadata = False

    try:
        opts, args = getopt.getopt(argv, "hi:o:f:")
    except getopt.GetoptError:
        print "print_random_lines.py -i <input filename> -o <output filename> -f <fraction to print>"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "print_random_lines.py -i <input filename> -o <output filename> -f <fraction to print>"
            sys.exit(2)
        elif opt == "-i":
            input_filename = arg
        elif opt == "-o":
            output_filename = arg
        elif opt == "-f":
            fraction_to_print = float(arg)
    if input_filename == "" or output_filename == "" or fraction_to_print <= 0 or fraction_to_print >= 1:
        print "Incorrect or missing options."
        print "print_random_lines.py -i <input filename> -o <output filename> -f <fraction to print>"
        sys.exit(2)


    with open(input_filename, "r") as input_file_handle:
        with open(output_filename, "w") as output_file_handle:
            for line in input_file_handle:
                if line.startswith("#"):
                    output_file_handle.write(line)
                else:
                    if added_metadata is False:
                        output_file_handle.write("#Using print_random_lines.py, approximately %.2f percent of lines have been selected from " % (fraction_to_print*100) + input_filename + "\n")
                        added_metadata = True
                    random_number = SystemRandom(clock()).random()
                    if random_number <= fraction_to_print:
                        output_file_handle.write(line)




if __name__=="__main__":
   main(sys.argv[1:])