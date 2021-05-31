import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx')
if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'lxml')
    tables = soup.find_all('table', attrs={'cellpadding':'2'})
    colname = tables[0].find_next('tr', class_='tr01').text.strip().split('\n')
    data = []
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs:
            date, value, price = [td.text for td in tr.find_all('td')]
            if date == '日期':
                continue
            data.append([date, value, price])

df = pd.DataFrame(data, columns=colname)
# df.to_csv('big_eight.csv')
df.to_excel('big_eight.xlsx')
df.to_html('big_eight.html')
    