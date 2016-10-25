"""
Sample script that runs matplotlib.pyplot functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import sys
import warnings
import matplotlib
# Suppress 'Matplotlib is building the font cache using fc-list. This
# may take a moment' warnings.
# From https://github.com/matplotlib/matplotlib/issues/5836#issuecomment-179592427
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
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
    matplotlib_sample = MatplotlibSample()
    matplotlib_sample.invoke(sys.argv)
