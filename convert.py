#!/usr/bin/env python3

import sys
import os
import argparse
import csv

def process_args():
    '''
    Gather input & output files from command line and make sure
    they are valid.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    ### Make sure the input file exists.
    if not os.path.isfile(args.input):
        print("%s does not exist." % args.input)        
        sys.exit(1)
    elif not os.access(args.input, os.R_OK):
        print("%s is not readable." % args.input)
        sys.exit(1)

    ### Make sure that we can write into the target directory.
    dir = os.path.dirname(os.path.abspath(args.output))
    if not os.access(dir, os.W_OK):
        print("can't write output to %s." % args.output)
        sys.exit(1)
    
    return(args.input, args.output)

def name_from_customer_description(cd):
    return cd[:cd.find('(') - 1]

def order_number_from_customer_description(cd):
    return cd[cd.find('#') + 1:cd.find(')')]

def process_row(input_row, output_file):
    output_file.write(input_row['Customer Description'] + '\n')

if __name__ == '__main__':

    # Figure out what we're processing.
    process_args()
    input, output = process_args()
    # print("Reading from %s. Writing to %s." % (input, output))

    # Read input and output files and process each line.
    f_in = open(input, 'r')
    f_out = open(output, 'w')
    r = csv.DictReader(f_in)
    for row in r:
        process_row(row, f_out)


    # Cleanup
    f_in.close()
    f_out.close()

    sys.exit(0)
