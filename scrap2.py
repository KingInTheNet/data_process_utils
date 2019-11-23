from bs4 import BeautifulSoup
from urllib.request import urlopen,urlparse,urlretrieve
import os
import time
def getLinks(url):
    html_page = urlopen(url)
    soup = BeautifulSoup(html_page,'lxml')
    links = []

    for link in soup.findAll('a'):
        links.append(link.get('href'))

    return links
def getFilename(url):
    a = urlparse(url)
    b = os.path.basename(a.path)
    print(b)
    return b
def download(url):
    name, ext = os.path.splitext(getFilename(url))[1][1:]
    if ext != "xml":
        urlretrieve(url, getFilename(url)) 

def scrap(url):
    links = getLinks(url)
    for link in links:
	start=time.time()
        download(url+link)
        print("  "+time.time()-start) 
try:
    scrap('https://dumps.wikimedia.org/viwiki/latest/')
except Exception as e:
    pass
