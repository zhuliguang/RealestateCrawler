import pandas as pd
import os
import requests
import re

os.chdir(os.path.dirname(__file__))
path = 'SydneyPostCode_url.xlsx'
df = pd.read_excel(path)
df.head()

def readlist(path):
    import pandas as pd
    rg = pd.read_excel(path)
    url=[]
    for i in range(0,len(rg)):
        url.append(rg.loc[i]['url'])
    return url
 
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
        path = 'SydneyPostCode_url.xlsx'
        urls = readlist(path)
        #print(urls[0],'------',urls[-1])
        #supplyamount =sendrequest(urls)
        r=requests.get(urls[0])
        print(r)
        if len(re.findall('of \d+ total results',r.text)) != 0:        
            re1 = re.findall('of \d+ total results',r.text)[0]
            re2 = re.findall('\d+',re1)[0]
            # save number to supply 
            print(int(re2))
        #print(supplyamount)
        #exportfile(supplyamount)
    except Exception as e:
        raise e