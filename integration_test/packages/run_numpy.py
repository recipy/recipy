"""
Sample script that runs numpy functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import numpy as np

from integration_test.packages.base import Base


class NumpySample(Base):
    """
    Sample script that runs numpy functions logged by recipy.

    This class assumes the existence of a data/numpy directory,
    co-located with this file, with the following content:

    * data.csv: comma-separated values
    * data_incomplete.csv: comma-separated values with missing
      entries (e.g. "1,2,3,4,5", "2,4,6,,"

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "numpy")

    def loadtxt(self):
        """
        Use numpy.loadtxt to load data.csv.
        """
        file_name = os.path.join(self.data_dir, "data.csv")
        np.loadtxt(file_name, delimiter=",")

    def fromfile(self):
        """
        Use numpy.fromfile to load data.csv.
        """
        file_name = os.path.join(self.data_dir, "data.csv")
        np.fromfile(file_name, sep=",")

    def genfromtxt(self):
        """
        Use numpy.genfromtxt to load data_incomplete.csv.
        """
        file_name = os.path.join(self.data_dir, "data_incomplete.csv")
        np.genfromtxt(file_name, delimiter=",",
                      missing_values="", filling_values=-1)

    def load(self):
        """
        Use numpy.load to load out.npy.
        """
        file_name = os.path.join(self.data_dir, "out.npy")
        np.load(file_name)

    def save(self):
        """
        Use numpy.savetxt to save a file out.npy.
        """
        file_name = os.path.join(self.data_dir, "out.npy")
        data = np.arange(10)
        np.save(file_name, data)
        os.remove(file_name)

    def savez(self):
        """
        Use numpy.savez to save a file out.npz.
        """
        file_name = os.path.join(self.data_dir, "out.npz")
        data1 = np.arange(5)
        data2 = np.arange(20, 30)
        np.savez(file_name, data1=data1, data2=data2)
        os.remove(file_name)

    def savez_compressed(self):
        """
        Use numpy.savez_compressed to save a file out.npz.
        """
        file_name = os.path.join(self.data_dir, "out.npz")
        data1 = np.arange(5)
        data2 = np.arange(20, 30)
        np.savez_compressed(file_name, data1=data1, data2=data2)
        os.remove(file_name)

    def savetxt(self):
        """
        Use numpy.savetxt to save a file out.txt.
        """
        file_name = os.path.join(self.data_dir, "out.txt")
        data = np.arange(10)
        np.savetxt(file_name, data)
        os.remove(file_name)

if __name__ == "__main__":
    NumpySample().invoke(sys.argv)
