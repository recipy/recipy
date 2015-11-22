import recipy
import codecs
#import numpy
#from lxml import etree
from bs4 import BeautifulSoup


#with codecs.open('/Users/janneke/Downloads/note.xml', 'r', encoding='utf-8') as f:
#    root = etree.parse(f)

#root = etree.parse('/Users/janneke/Downloads/note.xml')

#context = etree.iterparse('/Users/janneke/Downloads/note.xml')

with codecs.open('/Users/janneke/Downloads/note.xml', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')


#with codecs.open('/Users/janneke/Downloads/UTF-8-demo.txt', 'r', encoding='utf-8') as f:
#    print f.__class__
#    lines = f.readlines()
