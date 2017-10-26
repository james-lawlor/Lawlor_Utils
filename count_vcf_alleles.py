import sys
import logging
from future_builtins import zip
from collections import deque
from itertools import count
logging.basicConfig(level=logging.WARNING)
def ilen(it):
	# From StackOverflow: https://stackoverflow.com/questions/5384570/whats-the-shortest-way-to-count-the-number-of-items-in-a-generator-iterator
    # Make a stateful counting iterator
    cnt = count()
    # zip it with the input iterator, then drain until input exhausted at C level
    deque(zip(it, cnt), 0) # cnt must be second zip arg to avoid advancing too far
    # Since count 0 based, the next value is the count
    return next(cnt)


def allele_generator(filename):
	with open(filename, 'r') as file:
		for rawline in file:
			if rawline.startswith("#"):
				continue
			logging.debug(rawline)
			try:
				line = rawline.strip().split('\t')
				chrom = line[0]
				pos = line[1]
				vcf_id = line[2]
				ref = line[3]
				alts = line[4]
				for alt in alts.split(','):
					data = (chrom,pos,ref,alt)
					logging.debug(data)
					yield data
			except IndexError:
				print "This is probably not a VCF with the right number of columns (chrom pos id ref alt)"
				print "Line:\n%s" % rawline
				sys.exit()

input_filename = sys.argv[1]
print "Number of alleles: {:,}".format(ilen(allele_generator(input_filename)))



