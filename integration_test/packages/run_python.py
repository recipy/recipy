"""
Sample script that runs Python functions logged by recipy.
"""

# Copyright (c) 2016, 2018 University of Edinburgh and Netherlands eScience
# Center

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import warnings
import pytest

from integration_test.packages.base import Base


class PythonSample(Base):
    """
    Sample script that runs Python functions logged by recipy.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "python")

    def open_write_args(self):
        """
        Use recipy.open to save a file out.txt.
        """
        file_name = os.path.join(self.current_dir, "out.txt")
        with recipy.open(file_name, 'w') as f:
            f.write("This is a test")
        os.remove(file_name)

    def warn(self):
        """
        Raise a warning.
        """
        warnings.warn('This is a warning.')

    def error(self):
        """
        Raise an error.
        """
        with pytest.raises(ValueError):
            raise ValueError('This is an error.')

    def open_write_kwargs(self):
        """
        Use recipy.open to save a file out.txt.
        """
        file_name = os.path.join(self.current_dir, "out.txt")
        with recipy.open(file_name, mode='w') as f:
            f.write("This is a test")
        os.remove(file_name)

    def open_read_args(self):
        """
        Use recipy.open to save a file out.txt.
        """
        file_name = os.path.join(self.data_dir, "in.txt")
        with recipy.open(file_name, 'r') as f:
            pass

    def open_read_kwargs(self):
        """
        Use recipy.open to save a file out.txt.
        """
        file_name = os.path.join(self.data_dir, "in.txt")
        with recipy.open(file_name, mode='r') as f:
            pass

    def open_default(self):
        """
        Use recipy.open to save a file out.txt.
        """
        file_name = os.path.join(self.data_dir, "in.txt")
        with recipy.open(file_name) as f:
            pass

if __name__ == "__main__":
    PythonSample().invoke(sys.argv)
