"""
Sample script that runs matplotlib.pyplot functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import sys
import matplotlib
# Set non-interactive matplotlib back-end.
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

from integration_test.script_test.base import Base


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
