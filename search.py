import bz2 
import subprocess
from timeit import default_timer as timer
import mwparserfromhell 
import language_detect
import argparse
import xml.sax

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            if language_detect.filter_vi(self._values['title']):
                self._pages.append((self._values['title'], self._values['text']))

class Searcher(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._param ="Bánh rán"

    def setParam(self, input):
        self._param=input
    
    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            #if language_detect.filter_vi(self._values['title']):
            if self._param in self._values['title']:
                print(self._values['title'])
                self._pages.append((self._values['title'], self._values['text']))

handler = Searcher()
#parsing pages
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
argument_parser = argparse.ArgumentParser()
#getting search arguments
argument_parser.add_argument('input', metavar='Param', nargs='+',
                    help='provide input for a search')
arg = argument_parser.parse_args()
handler.setParam(arg.input[0])
data_path="viwiki-latest-pages-articles-multistream.xml.bz2"
#fout = open('testparse','w')
for i, line in enumerate(subprocess.Popen(['bzcat'], 
                         stdin = open(data_path), 
                         stdout = subprocess.PIPE).stdout):
    if (i + 1) % 10000 == 0:
        print(f'Processed {i + 1} lines so far.', end = '\r')
    try:
        parser.feed(line)
        if i>97784499: #This is the number of lines of the dump counted by bzcat. I never reached it but left it here just in case
            break
    except StopIteration:
        break
for page in handler._pages:
    print(page[0])
    # item =[]    
    # item.append(page[0])   
    # print(page[0])
    wiki = mwparserfromhell.parse(page[1])     
    wikitext = wiki.filter_text()
    # #print(f'There are {len(wikilinks)} wikilinks.')
    # #print(wikitext)
    text = wiki.strip_code().strip()[:500]
    text=text.split(".")
    processed=text[0]
    if text[1]:
        processed += text[1]
    if text[2]:
        processed+= text[2]
    print(processed)
    # item.append(processed)
    # fout.write("%s\n" % item)
    # #templates = wiki.filter_templates()
    # print(f'There are {len(templates)} templates.')
if not handler._pages:
    print("not found")
#for template in templates:
#    print(template.name)
#infobox = wiki.filter_templates(matches = 'Thông tin đơn vị hành chính Việt Nam')[0]
#information = {param.name.strip_code().strip(): param.value.strip_code().strip() for param in infobox.params}
#print(information)
