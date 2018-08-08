'''
Description: Grab sold house data from realestate.com.au
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import os
import re
import requests
import pandas as pd


url_pre = 'https://www.realestate.com.au/sold/in-'
url_end = '/list-1?includeSurrounding=false'


def readPostcode(file_name):
    os.chdir(os.path.dirname(__file__))
    postcode = pd.read_excel(file_name).sort_values(by=['Suburb','Postcode'])
    postcode = postcode.values
    postcode = set(postcode[:,0].tolist())
    return postcode

def createUrl(postcode):
    urls=[]
    for _ in postcode:
        url = '{}{}{}'.format(url_pre,_,url_end)
        urls.append(url)
    return urls
 
def sendrequest(url):
    supply = []
    for i in range(0,len(url)):
        try:
            r=requests.get(url[i])
        except Exception.Timeout as e:
            print(e)
        print(i, '---', r)
        # use regrlar expression to match the number before " total results"
        if len(re.findall('of \d+ total results',r.text)) != 0:        
            re1 = re.findall('of \d+ total results',r.text)[0]
            re2 = re.findall('\d+',re1)[0]
            # save number to supply 
            supply.append(int(re2))
        else:
            supply.append(0)
    return supply
 
def exportfile(supply):
    import pandas as pd
    import datetime
    rg = pd.read_excel(path)
    rg['supply'] = pd.Series(supply)
    print(rg.head())
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = 'SydneyPostCode_url_num'+day+'.xlsx'
    rg.to_excel(filename, index=False)      
 
if __name__ == '__main__':
    try:
        file_name = 'Victoria.xlsx'
        postcode = readPostcode(file_name)
        urls = createUrl(postcode)
        #r=requests.get(urls[0])
        r=requests.get('https://www.realestate.com.au//sold/property-apartment-vic-melbourne-128165818')
        print(r.text)
        if len(re.findall('of \d+ total results',r.text)) != 0:        
            re1 = re.findall('of \d+ total results',r.text)[0]
            re2 = re.findall('\d+',re1)[0]
            # save number to supply 
            print(int(re2))
        #print(supplyamount)
        #exportfile(supplyamount)
    except Exception as e:
        raise e