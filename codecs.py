import recipy

import lxml
import codecs

with codecs.open('UTF-8-demo.txt', 'r', encoding='utf-8') as f:
    print f.__class__
    lines = f.readlines()

# when this script is run, is does not show modules are being patched,
# although debug is on
# output:
#Jannekes-MacBook-Air-2:recipy janneke$ python test_codecs.py
#recipy run inserted, with ID bc07e88f-49f6-4e65-8883-798dbba58fdb
#codecs.StreamReaderWriter

# output for lxml/bs4 testing script (to show debug is on)
#Jannekes-MacBook-Air-2:recipy janneke$ python test_xml_in.py
#recipy run inserted, with ID 9277a026-7723-4783-9592-982246b4d2b2
#Patching lxml.etree
#Patching input function: parse
#Patching input function: iterparse
#Patching bs4
#Patching input function: BeautifulSoup
