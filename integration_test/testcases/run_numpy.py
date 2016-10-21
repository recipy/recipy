"""
recipy numpy test cases.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import sys
import numpy as np

from integration_test.testcases.base import Base


class NumpyTests(Base):
    """
    recipy numpy test cases.

    This class assumes the existence of a data/numpy directory,
    co-located with this file, with the following content:

    * data.csv: comma-separated values
    * data_incomplete.csv: comma-separated values with missing
      entries (e.g. "1,2,3,4,5", "2,4,6,,"
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "numpy")
        print(("Data directory: ", self.data_dir))

    def loadtxt(self):
        """
        Use numpy.loadtxt to load data.csv.
        """
        file_name = os.path.join(self.data_dir, "data.csv")
        print(("Loading data:", file_name))
        data = np.loadtxt(file_name, delimiter=",")
        print(("Data:", data.shape))
        print(data)

    def fromfile(self):
        """
        Use numpy.fromfile to load data.csv.
        """
        file_name = os.path.join(self.data_dir, "data.csv")
        print(("Loading data:", file_name))
        data = np.fromfile(file_name, sep=",")
        print(("Data:", data.shape))
        print(data)

    def genfromtxt(self):
        """
        Use numpy.genfromtxt to load data_incomplete.csv.
        """
        file_name = os.path.join(self.data_dir, "data_incomplete.csv")
        print(("Loading data:", file_name))
        data = np.genfromtxt(file_name, delimiter=",",
                             missing_values="", filling_values=-1)
        print(("Data:", data.shape))
        print(data)

    def save(self):
        """
        Use numpy.savetxt to save a file tmpdata.npy.
        """
        file_name = os.path.join(self.data_dir, "tmpdata.npy")
        data = np.arange(10)
        print(("Data:", data.shape))
        print(data)
        print(("Saving data:", file_name))
        np.save(file_name, data)

    def savez(self):
        """
        Use numpy.savez to save a file tmpdata.npz.
        """
        file_name = os.path.join(self.data_dir, "tmpdata.npz")
        data1 = np.arange(5)
        data2 = np.arange(20, 30)
        print(("Data:", data1.shape))
        print(data1)
        print(("Data:", data2.shape))
        print(data2)
        print(("Saving data:", file_name))
        np.savez(file_name, data1=data1, data2=data2)

    def savez_compressed(self):
        """
        Use numpy.savez_compressed to save a file tmpdata.npz.
        """
        file_name = os.path.join(self.data_dir, "tmpdata.npz")
        data1 = np.arange(5)
        data2 = np.arange(20, 30)
        print(("Data:", data1.shape))
        print(data1)
        print(("Data:", data2.shape))
        print(data2)
        print(("Saving data:", file_name))
        np.savez_compressed(file_name, data1=data1, data2=data2)

    def savetxt(self):
        """
        Use numpy.savetxt to save a file tmpdata.txt.
        """
        file_name = os.path.join(self.data_dir, "tmpdata.txt")
        data = np.arange(10)
        print(("Data:", data.shape))
        print(data)
        print(("Saving data:", file_name))
        np.savetxt(file_name, data)

if __name__ == "__main__":
    numpy_tests = NumpyTests()
    numpy_tests.invoke(sys.argv)
