"""
Sample script that runs numpy functions logged by Beautiful Soup.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import sys
from bs4 import BeautifulSoup

from integration_test.packages.base import Base


class Bs4Sample(Base):
    """
    Sample script that runs Beautiful Soup functions logged by
    recipy.

    This class assumes the existence of a data/bs4 directory,
    co-located with this file, with the following content:

    * data.html: HTML file
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "bs4")
        print(("Data directory: ", self.data_dir))

    def beautifulsoup(self):
        """
        Use bs4.BeautifulSoup to load data.html.
        """
        file_name = os.path.join(self.data_dir, "data.html")
        print(("Loading data:", file_name))
        with open(file_name, "r") as f:
            soup = BeautifulSoup(f, "lxml")
            print("Pretty-printed data:")
            print((soup.prettify()))


if __name__ == "__main__":
    bs4_sample = Bs4Sample()
    bs4_sample.invoke(sys.argv)
