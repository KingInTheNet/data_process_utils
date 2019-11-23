from bs4 import BeautifulSoup
from urllib.request import urlopen,urlparse,urlretrieve
import os

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
    #print(b)
    return b
def download(url):
    name, ext = os.path.splitext(getFilename(url))
    if ext != ".xml":
        if !os.path.exists(getFilename(url)):
            urlretrieve(url, getFilename(url)) 
            print(getFilename(url))

def scrap(url):
    links = getLinks(url)
    for link in links:
        download(url+link)
#        try:
#            download(url+link)
#        except Exception as e:
#            print('exception here: '+link) 
scrap('https://dumps.wikimedia.org/viwiki/latest/')

