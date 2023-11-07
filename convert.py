#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import decimal

ITEM_WEIGHT = 2.45
ITEM_PRICE = 45
ITEM_TITLE = 'Martani 2023'

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

def name(input_row, card_name, shipping_name):
    result = input_row[shipping_name]
    if result == '':
        result = input_row[card_name]
    return result

def street_1(input_row, card_street_1, shipping_street_1):
    result = input_row[shipping_street_1]
    if result == '':
        result = input_row[card_street_1]
    return result

def street_2(input_row, card_street_2, shipping_street_2):
    result = input_row[shipping_street_2]
    if result == '':
        result = input_row[card_street_2]
    return result

def city(input_row, card_city, shipping_city):
    result = input_row[shipping_city]
    if result == '':
        result = input_row[card_city]
    return result

def state(input_row, card_state, shipping_state):
    result = input_row[shipping_state]
    if result == '':
        result = input_row[card_state]
    return result

def zip(input_row, card_zip, shipping_zip):
    result = input_row[shipping_zip]
    if result == '':
        result = input_row[card_zip]
    return result

def country(input_row, card_country, shipping_country):
    result = input_row[shipping_country]
    if result == '':
        result = input_row[card_country]
    return result

def quantity(input_row, description):
    """Extract the quantity from the description."""
    result = 0

    d = input_row[description]
    start = d.index('x') + 1
    end = d.index('=')
    num = d[start:end]
    result = int(num.strip())
    
    return result

def weight(input_row, description):
    result = 0

    num_items = quantity(input_row, description)
    result = round((ITEM_WEIGHT * num_items), 2)
    
    return result

def total(input_row, description):
    """Extract the total paid from the description. The result is a string."""
    result = 0

    d = input_row[description]
    start = d.index('TOTAL:')
    end = d.rindex('USD')
    num = d[start + len('TOTAL: $'):end]
    result = num.strip()

    return result

### TODO ... implement this function properly.
import random
def is_express_shipping(input_row, description):
    random.seed()
    return random.choice((True, False))

def title(input_row, description):
    result = ITEM_TITLE

    if is_express_shipping(input_row, description):
        result += ' **'
    
    return result

def const(input_row, c):
    return c

def executor(func, data):
    return func(**data)

def get_output_data(input_row):
    result = {}

    for field in FIELD_MAP:
        input_val = FIELD_MAP[field]
        output_val = None
        if input_val is None:
            pass
        elif isinstance(input_val, str):
            output_val = input_row[input_val]
        else: # a function
            func = input_val[0]
            args = input_val[1]
            args['input_row'] = input_row
            output_val = executor(func, args)
        
        result[field] = output_val

    return result

FIELD_MAP = {
    # 'output': 'input',
    'Order Number': 'WF Order Id (metadata)',
    'Order Date': 'Created (UTC)',
    'Recipient Name': (name, {'card_name':'Card Name',
                              'shipping_name':'Shipping Name'}),
    'Company': None,
    'Email': 'Customer Email',
    'Phone': None,
    'Street Line 1': (street_1, {'card_street_1':'Card Address Line1',
                                 'shipping_street_1':
                                 'Shipping Address Line1'}),
    'Street Number': None,
    'Street Line 2': (street_2, {'card_street_2':'Card Address Line2',
                                 'shipping_street_2':
                                 'Shipping Address Line2'}),
    'City': (city, {'card_city':'Card Address City',
                    'shipping_city':'Shipping Address City'}),
    'State/Province': (state, {'card_state':'Card Address State',
                               'shipping_state':'Shipping Address State'}),
    'Zip/Postal Code': (zip, {'card_zip':'Card Address Zip',
                              'shipping_zip': 'Shipping Address Postal Code'}),
    'Country': (country, {'card_country':'Card Address Country',
                          'shipping_country':'Shipping Address Country'}),
    # 'Item Title': (const, {'c':ITEM_TITLE}),
    'Item Title': (title, {'description':'Description'}),
    'SKU': None,
    'Quantity': (quantity, {'description':'Description'}),
    'Item Weight': (const, {'c':ITEM_WEIGHT}),
    'Item Weight Unit': (const, {'c':'lb'}),
    'Item Price': (const, {'c':ITEM_PRICE}),
    'Item Currency': (const, {'c':'USD'}),
    'Order Weight': (weight, {'description':'Description'}),
    'Order Weight Unit': (const, {'c':'lb'}),
    'Order Amount': (total, {'description':'Description'}),
    'Order Currency': (const, {'c':'USD'})
}

if __name__ == '__main__':

    # Figure out what we're processing.
    process_args()
    input, output = process_args()
    # print("Reading from %s. Writing to %s." % (input, output))

    # Read input and output files and process each line.
    f_in = open(input, 'r')
    f_out = open(output, 'w')
    r = csv.DictReader(f_in, dialect='excel')
    w = csv.DictWriter(f_out, dialect='excel', fieldnames=FIELD_MAP.keys())

    w.writeheader()
    for row in r:
        w.writerow(get_output_data(row))

    # Cleanup
    f_in.close()
    f_out.close()

    sys.exit(0)
