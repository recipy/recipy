"""
Sample script that runs sklearn functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import numpy as np
from sklearn import datasets

from integration_test.packages.base import Base


class SklearnSample(Base):
    """
    Sample script that runs sklearn functions logged by recipy.

    This class assumes the existence of a data/sklearn directory,
    co-located with this file, with the following content:

    * data.svmlight: svmlight file.

    Running this script with argument 'create_sample_data' will create
    this file.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "sklearn")

    def load_svmlight_file(self):
        """
        Use sklearn.datasets.load_svmlight_file to load data.svmlight.
        """
        file_name = os.path.join(self.data_dir, "data.svmlight")
        datasets.load_svmlight_file(file_name)

    def dump_svmlight_file(self):
        """
        Use sklearn.datasets.dump_svmlight_file to save out.svmlight.
        """
        x = np.array([list(range(0, 5)), list(range(5, 10))])
        y = np.array([10, 20])
        file_name = os.path.join(self.data_dir, "out.svmlight")
        datasets.dump_svmlight_file(x, y, file_name,
                                    comment="Sample svmlight file")
        os.remove(file_name)

    def create_sample_data(self):
        """
        Create sample data files. The files created are:

        * data.svmlight: svmlight file
        """
        x = np.array([list(range(0, 5)), list(range(5, 10))])
        y = np.array([10, 20])
        file_name = os.path.join(self.data_dir, "data.svmlight")
        datasets.dump_svmlight_file(x, y, file_name,
                                    comment="Sample svmlight file")


if __name__ == "__main__":
    SklearnSample().invoke(sys.argv)
