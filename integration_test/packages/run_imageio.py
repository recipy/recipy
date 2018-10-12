"""
Sample script that runs imageio functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)
import recipy

import os
import sys
import imageio

from integration_test.packages.base import Base


class ImageioSample(Base):
    """
    Sample script that runs imageio functions logged by recipy.

    This class assumes the existence of a data/imageio directory,
    co-located with this file, with the following content:

    * image.tiff: tiff file
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "imageio")

    def imread(self):
        """
        Use imageio.imread to read image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        imageio.imread(file_name)

    def imwrite(self):
        """
        Use imageio.imwrite to write image.png.
        """
        file_name_in = os.path.join(self.data_dir, "image.tiff")
        file_name = os.path.join(self.data_dir, "image.png")
        im = imageio.imread(file_name_in)

        imageio.imwrite(file_name, im)
        os.remove(file_name)


if __name__ == "__main__":
    ImageioSample().invoke(sys.argv)
