import requests
import sys
import json
import codecs
import os
from bs4 import BeautifulSoup

def main():

    r = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')
    r.encoding = 'utf-8-sig'
    o = json.loads(r.text)
    parse(o)

def parse(o):
    for k, v in o[0].items():
        parseDate(v)

def parseDate(date):
    for v in date:
        parseNews(v)

def parseNews(news):
    news_id = news['news_id']
    news_time = news['news_prearranged_time'].replace(':', '-')
    title = news['title']
    title_ruby = news['title_with_ruby']
    news_uri = 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(news_id) + '.html'

    news_folder = 'data/' + news_time + '_' + news_id + '_' + title
    news_folder = news_folder.replace(' ', '_')
    news_file = str(news_id) + '.html'

    if os.path.isdir(news_folder) == False:
        os.makedirs(news_folder)

        r = requests.get(news_uri)
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, 'html.parser')
        date = soup.find('p', attrs={'id':'newsDate'}).contents[0]
        title = soup.find('div', attrs={'id':'newstitle'})#.find('h2')
        article = soup.find('div', attrs={'id':'newsarticle'})

        for a in article.findAll('a'):
            a.unwrap()

        with open(news_folder + '/' + news_file, "w") as f:
            print("<!DOCTYPE html>", file=f)
            print("<html lang='ja'>", file=f)
            print("<head><meta charset='utf-8'></head>", file=f)
            print("<style>p { font-size: 120%; line-height: 3.2; padding-bottom: 20px; }</style>", file=f)
            print("<body>", file=f)
            print(title, file=f)
            print(article, file=f)
            print("</body>", file=f)
            print("</html>", file=f)

        if news['has_news_easy_voice'] == True:
            voice_file = news['news_easy_voice_uri']
            voice_uri = 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(voice_file)
            r = requests.get(voice_uri)
            with open(news_folder + '/' + voice_file, "wb") as f:
                f.write(r.content)

main()
