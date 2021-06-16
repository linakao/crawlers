import requests
import time
from pymongo import MongoClient

client = MongoClient()

# time interval
def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec
 
second = sleep_time(0, 0, 5)

for i in range(1, 3):    
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E6%B0%B4%E6%B3%A2%E7%88%90&page={}&sort=sale/dc'.format(i)
    r = requests.get(url)
    print('crawling page {}'.format(i))
    if r.status_code == requests.codes.ok:
        data = (r.json())['prods']
        for d in data:
            client.pchome.products.insert_one(d)
            
    time.sleep(second)