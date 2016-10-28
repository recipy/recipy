"""
Sample script that runs lxml functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)
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

    def parse(self):
        """
        Use lxml.etree.parse to parse data.xml.
        """
        file_name = os.path.join(self.data_dir, "data.xml")
        with open(file_name, "r") as f:
            etree.parse(f)

    def iterparse(self):
        """
        Use lxml.etree.iterparse to parse data.xml.
        """
        file_name = os.path.join(self.data_dir, "data.xml")
        with open(file_name, "r") as f:
            etree.iterparse(file_name, events=("start", "end"))


if __name__ == "__main__":
    LxmlSample().invoke(sys.argv)
