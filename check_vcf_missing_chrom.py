#!/usr/bin/env /cluster/lab/gcooper/software/envs/cytoplot/bin/python3.8
from __future__ import print_function
import cyvcf2
import argparse
import sys

parser = argparse.ArgumentParser(description="Return an error and corresponding sample IDs / chromosomes when one of the main chromosomes has no variant calls")
parser.add_argument('vcfs', type=str, nargs='+', help="Tabix'ed and indexed VCFs to check")
parser.add_argument('-c', '--nochrom', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()


chroms = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X'] # don't check Y

if not args.nochrom:
    chroms = ['chr' + x for x in chroms]

some_missing = False # flag for any missing in all files

for vcffile in args.vcfs:
    chrom_missing = False # flag for any chrom missing in this file
    vcf = cyvcf2.VCF(vcffile, strict_gt = True)
    for chrom in chroms:
        bad_chrom = False # flag for a specific chrom missing in this file
        members = vcf.samples.copy()
        for variant in vcf(chrom):
            if variant.call_rate == 1: #if we find a variant with call rate = 1 (called in all samples) we stop and go to next chrom
                members = [] # in this case, we've found an all-call variant so we blank the members list for this chrom.
                break
            else:
                for idx,gt in enumerate(variant.genotypes):
                    if gt[0] > 0 and gt[1] > 0:  # example genotype [[0, 1, False], [-1, -1, False], [-1, -1, False], [-1, -1, False]]; negative one for no-calls.
                        try:
                            members.remove(vcf.samples[idx]) # remove the member with good calls, based on their position in the original samples array
                        except ValueError:
                            continue

                if len(members) == 0: # every variant, we see if the list is empty. If it's one, then we've found the
                    break
        if len(members) > 0:
            chrom_missing = True
            some_missing = True
            for member in members:
                print('{} missing in sample {} in file {}'.format(chrom, member, vcffile))

    if not chrom_missing and args.verbose:
        print('Each samples has a call on all major chromosomes {} in {}'.format(",".join(chroms),vcffile))

if some_missing:
    sys.exit(1)
else:
    sys.exit(0)
