"""
Sample script that runs PIL/pillow functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
from PIL import Image

from integration_test.packages.base import Base


class PilSample(Base):
    """
    Sample script that runs PIL/pillow functions logged by recipy.

    This class assumes the existence of a data/pil directory,
    co-located with this file, with the following content:

    * data.png: PNG image.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "pil")
        print(("Data directory: ", self.data_dir))

    def image_open(self):
        """
        Use PIL.Image.open to load data.png.
        """
        file_name = os.path.join(self.data_dir, "data.png")
        print(("Loading image:", file_name))
        with Image.open(file_name) as f:
            print(("Size:", f.size))

    def image_save(self):
        """
        Use PIL.Image.open to load data.png then PIL.Image.save
        to save data.png as out.png.
        """
        file_name = os.path.join(self.data_dir, "data.png")
        out_file_name = os.path.join(self.data_dir, "out.png")
        print(("Loading image:", file_name))
        with Image.open(file_name) as f:
            print(("Size:", f.size))
            out_image = f.rotate(90)
            print(("Saving rotated image:", out_file_name))
            out_image.save(out_file_name)
        os.remove(out_file_name)


if __name__ == "__main__":
    PilSample().invoke(sys.argv)
