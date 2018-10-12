"""
Sample script that runs tifffile functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)
import recipy

import os
import sys
import numpy
import tifffile

from integration_test.packages.base import Base


class TifffileSample(Base):
    """
    Sample script that runs tifffile functions logged by recipy.

    This class assumes the existence of a data/tifffile directory,
    co-located with this file, with the following content:

    * image.tiff: tiff file
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "tifffile")

    def imread(self):
        """
        Use tifffile.imread to read image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        tifffile.imread(file_name)

    def imsave(self):
        """
        Use tifffile.imsave to write image2.tiff.
        """
        #file_name_in = os.path.join(self.data_dir, "image.tiff")
        file_name = os.path.join(self.data_dir, "image2.tiff")

        data = numpy.array([1, 2, 3])
        #im = tifffile.imread(file_name_in)

        tifffile.imsave(file_name, data)
        os.remove(file_name)


if __name__ == "__main__":
    TifffileSample().invoke(sys.argv)
