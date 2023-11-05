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

def name(card_name, shipping_name):
    return 'name'

def street_1(card_street_1, shipping_street_1):
    return 'street_1'

def street_2(card_street_2, shipping_street_2):
    return 'street_2'

def city(card_city, shipping_city):
    return 'city'

def state(card_state, shipping_state):
    return 'state'

def zip(card_zip, shipping_zip):
    return 'zip'

def country(card_country, shipping_country):
    return 'country'

def quantity(description):
    return 'quantity'

def weight(description):
    return 'weight'

def total(total_items):
    return 'total'

def const(c):
    return c


field_map = {
    # 'output': 'input',
    'Order Number': 'WF Order Id (metadata)',
    'Order Date': 'Created (UTC)',
    'Recipient Name': name('Card Name', 'Shipping Name'),
    'Company': None,
    'Email': 'Customer Email',
    'Phone': None,
    'Street Line 1': street_1('Card Address Line1', 'Shipping Address Line1'),
    'Street Number': None,
    'Street Line 2': street_2('Card Address Line2', 'Shipping Address Line2'),
    'City': city('Card Address City', 'Shipping Address City'),
    'State/Province': state('Card Address State', 'Shipping Address State'),
    'Zip/Postal Code': zip('Card Address Postal Code',
                           'Shipping Address Postal Code'),
    'Country': country('Card Address Country', 'Shipping Address Country'),
    'Item Title': None,
    'SKU': None,
    'Quantity': quantity('Description'),
    'Item Weight': const(2.2), # CONFIRM
    'Item Weight Unit': const('lb'),
    'Item Price': const(45),
    'Item Currency': const('USD'),
    'Order Weight': weight(quantity('Description')),
    'Order Weight Unit': const('lb'),
    'Order Amount': total(quantity('Desciption')),
    'Order Currency': const('USD')
}
    

def process_row(input_row, output_file):
    for field in field_map:
        val = field_map[field]
        print(val, end=", ")
    print('')
    # output_file.write(input_row['Customer Description'] + '\n')

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
