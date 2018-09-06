'''
Description: Definitions of functions
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''
# import packages
import pandas as pd

# short names dictionary
address_dict = ({'road':'rd', 'street':'st', 'place':'pl', 'avenue':'ave',
                'parade':'pde', 'highway':'hwy', 'drive':'dr', 'grove':'gr',
                'crescent':'cres', 'court':'ct', 'close':'cl', 'circuit':'cct',
                'avenue':'ave', 
                })

# function to read postcode from excel file
def readPostcode(file_name):
    postcode = pd.read_excel(file_name).sort_values(by=['Postcode'])
    postcode = postcode.values
    postcode = postcode[:,0]
    return postcode

# function to create valid url according to postcode
def createUrl(postcode, page_no):
    url_pre = 'https://www.realestate.com.au/sold/in-'
    if postcode < 1000:
        url = '{}0{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    elif postcode < 10000:
        url = '{}{}/list-{}?includeSurrounding=false'.format(url_pre, postcode, page_no)
    else:
        print('Wrong postcode!!')
        exit()
    return url

# function to create valid url according to address
def createHouseUrl1(address, suburb, postcode, use_short):
    url_pre = 'https://www.realestate.com.au/property/'
    str_address = address.lower()
    if re.search(r'[0-9|a-z]+/[0-9]', str_address) is not None:
        str_address = 'unit-' + str_address
    if use_short:
        for key in address_dict.keys():
            street_name = re.search(key, str_address)
            if street_name is not None:
                str_address = re.sub(street_name.group(), address_dict[key], str_address)
    str_suburb = suburb.lower()
    if postcode < 1000:
        str_postcode = 'nt-0{:d}'.format(postcode)
    elif postcode < 2600:
        str_postcode = 'nsw-{:d}'.format(postcode)
    elif postcode < 2700:
        str_postcode = 'act-{:d}'.format(postcode)
    elif postcode < 2800:
        str_postcode = 'nsw-{:d}'.format(postcode)
    elif postcode < 3000:
        str_postcode = 'act-{:d}'.format(postcode)
    elif postcode < 4000:
        str_postcode = 'vic-{:d}'.format(postcode)
    elif postcode < 5000:
        str_postcode = 'qld-{:d}'.format(postcode)
    elif postcode < 6000:
        str_postcode = 'sa-{:d}'.format(postcode)
    elif postcode < 7000:
        str_postcode = 'wa-{:d}'.format(postcode)
    elif postcode < 8000:
        str_postcode = 'tas-{:d}'.format(postcode)
    str_address = '{}-{}-{}'.format(str_address, str_suburb, str_postcode)
    str_address = re.sub('[,|\s|/]', '-', str_address)
    for _ in range(4):
        str_address = re.sub('--', '-', str_address)
    url = url_pre + str_address
    return url

# function to create url according to REA_id
def createHouseUrl2(REA_id):
    url = 'https://www.realestate.com.au/property/lookup?id={:d}'.format(REA_id)
    return url