import requests
from bs4 import BeautifulSoup

def get_request(url):
    r = requests.get(url)
    print(r)
    if r.status_code == 200:
        print('Get permission.')
        return r
    else:
        print('Not allowed.')
        return None

def get_number_of_comments(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    number_of_comments = int(soup.find('div', class_='fiw2dr-2').text.split('回應 ')[-1])
    print(f'have {number_of_comments} comments in page')
    return number_of_comments

def count_comments(url, number_of_comments):
    floor = 1
    comments = {}
    for f in range(int(number_of_comments)):
        comment_url = url + '/b/' + str(floor)
        r = requests.get(comment_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('div', class_='sc-7fxob4-4').text
        comment = soup.find('div', class_='phqjxq-0').text
        if name in comments:
            comments[name] += comment
        else:
            comments[name] = comment
        floor += 1
    return comments


def main():
    url = 'https://www.dcard.tw/f/funny/p/236067618'
    r = get_request(url)
    number_of_comments = get_number_of_comments(r)
    comments = count_comments(url, number_of_comments)
    for c in comments:
        print(f'{c}共有{len(c)}筆留言')


if __name__ == '__main__':
    main()








# spans = soup.find_all('div', class_='sc-1ghk0k7-0 bgugOF')
# comments = {}
# for span in spans:
#     count = 0
#     floor = span.find_parent('div')
#     for f in floor:
#         user = span.find('div', class_='sc-7fxob4-4 dbFiwE').text
#         comment = span.find('div', class_='phqjxq-0 fQNVmg').text
#         print(comment)
#         # if user in comments:
#         #     comments[user].append(comment)
#         # else:
#         #     comments[user] = comment
#     print(comments)


# print(comments)
