"""
Sample script that runs matplotlib.pyplot functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import warnings
import matplotlib
import matplotlib.pyplot as plt
from integration_test.packages.base import Base


class MatplotlibSample(Base):
    """
    Sample script that runs matplotlib functions logged by recipy.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data")
        print(("Data directory: ", self.data_dir))

    def savefig(self):
        """
        Use pyplot.plot to save "data.png".
        """
        file_name = os.path.join(self.data_dir, "out.png")
        plt.plot([1, 2, 3])
        print(("Saving plot:", file_name))
        plt.savefig(file_name)
        os.remove(file_name)

if __name__ == "__main__":
    MatplotlibSample().invoke(sys.argv)
