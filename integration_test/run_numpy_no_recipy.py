"""
Script to load and save data using numpy.
"""

# Copyright (c) 2016 University of Edinburgh.

import sys
import numpy as np


def run_numpy(in_file, out_file):
    """
    Load data from in_file and save new data into out_file, using
    numpy.

    :param in_file: input file with comma-separated values
    :type in_file: str or unicode
    :param out_file: output file with comma-separated values
    :type out_file: str or unicode
    """
    data = np.loadtxt(in_file, delimiter=',')
    data = np.array([[1, 2, 3], [1, 4, 9]])
    np.savetxt(out_file, data, delimiter=',')

if __name__ == "__main__":
    run_numpy(sys.argv[1], sys.argv[2])
