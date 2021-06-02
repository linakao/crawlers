import requests
import json
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


def crawl(date):
    r = requests.get(
        'https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}'.format(date.year, date.month,
                                                                                         date.day))
    if r.status_code == requests.codes.ok:
        DOWNLOADS_DIR = 'futures_downloads'
        day = f'{date.year}-{date.month}-{date.day}'
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        filepath = os.path.join(DOWNLOADS_DIR, day + '.txt')
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return

        data = {}
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', class_='table_f')

        try:
            trs = table.find_all('tr')[3:]
            print('Crawling data for', day)
        except AttributeError:
            print('No data for', day)
            return
        for tr in trs:
            ths = tr.find_all('th')
            if len(ths) == 3:
                product = ths[1].text.strip()
                who = ths[2].text.strip()
            elif len(ths) == 2:
                break
            else:
                who = ths[0].text.strip()
            tds = tr.find_all('td')
            cells = [int((td.text.strip()).replace(',', '')) for td in tds]

            headers = ['交易多方口數', '交易多方契約金額', '交易空方口數', '交易空方契約金額', '交易淨額口數', '交易淨額契約金額', '未平倉多方口數', '未平倉多方契約金額',
                       '未平倉空方口數',
                       '未平倉空方契約金額', '未平倉淨額口數', '未平倉淨額契約金額']

            contents = {headers[i]: cells[i] for i in range(len(headers))}

            if product not in data:
                data[product] = {who: contents}
            else:
                data[product][who] = contents

        with open(filepath, 'w') as f:
            json_str = json.dumps(data, indent=3)
            f.write(json_str)

    else:
        print('connetion error', date)


date = datetime.today()
all_date = []
while True:
    date = date - timedelta(days=1)
    all_date.append(date)
    if date < datetime.today() - timedelta(days=730):
        break

start = time.time()
with ThreadPoolExecutor(max_workers=8) as executor:
    for date in all_date:
        executor.submit(crawl(date), date)
end = time.time()
print('it was took', end - start, 'seconds')



