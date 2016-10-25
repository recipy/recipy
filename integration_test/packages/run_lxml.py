"""
Sample script that runs lxml functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import sys
from lxml import etree

from integration_test.packages.base import Base


class LxmlSample(Base):
    """
    Sample script that runs lxml functions logged by recipy.

    This class assumes the existence of a data/lxml directory,
    co-located with this file, with the following content:

    * data.xml: XML file
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "lxml")
        print(("Data directory: ", self.data_dir))

    def parse(self):
        """
        Use lxml.etree.parse to parse data.xml.
        """
        file_name = os.path.join(self.data_dir, "data.xml")
        print(("Parsing:", file_name))
        with open(file_name, "r") as f:
            tree = etree.parse(f)
            print("Tree:")
            print((etree.tostring(tree)))
            print("Tag:")
            print((tree.getroot().tag))

    def iterparse(self):
        """
        Use lxml.etree.iterparse to parse data.xml.
        """
        file_name = os.path.join(self.data_dir, "data.xml")
        print(("Iteratively parsing:", file_name))
        with open(file_name, "r") as f:
            for event, element in etree.iterparse(file_name,
                                                  events=("start", "end")):
                print(("%5s, %4s, %s" % (event, element.tag, element.text)))

if __name__ == "__main__":
    lxml_sample = LxmlSample()
    lxml_sample.invoke(sys.argv)
