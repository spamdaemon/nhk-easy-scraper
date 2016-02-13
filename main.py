import requests
import sys
from bs4 import BeautifulSoup

r = requests.get('http://www3.nhk.or.jp/news/html/20160210/k10010404101000.html')

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

outtext = soup.prettify()
print(repr(soup.prettify()))
