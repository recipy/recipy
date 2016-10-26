"""
Sample script that runs gdal functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import gdal
import os
import sys
import numpy as np

from integration_test.packages.base import Base


class GdalSample(Base):
    """
    Sample script that runs gdal functions logged by recipy.

    This class assumes the existence of a data/gdal directory,
    co-located with this file, with the following content:

    * image.tiff: TIFF file.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "gdal")
        print(("Data directory: ", self.data_dir))

    def open(self):
        """
        Use gdal.Open to load image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        print(("Loading image:", file_name))
        data_source = gdal.Open(file_name)
        print(("Data:", data_source))
        print(("X size:", data_source.RasterXSize))
        print(("Y size:", data_source.RasterYSize))

    def driver_create(self):
        """
        Use gdal.Driver.Create to create out_image.tiff.
        """
        file_name = os.path.join(self.data_dir, "out_image.tiff")
        image_format = "GTiff"
        driver = gdal.GetDriverByName(str(image_format))
        data_source = driver.Create(file_name, 50, 50, 1, gdal.GDT_Byte)
        raster = np.ones((50, 50), dtype=np.uint8)
        raster[10:40, 10:40] = 0
        raster = raster * 255
        print(("Saving:", file_name))
        data_source.GetRasterBand(1).WriteArray(raster)
        os.remove(file_name)

    def driver_createcopy(self):
        """
        Use gdal.Open to load image.tiff and gdal.Driver.CreateCopy to
        copy this to out_image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        out_file_name = os.path.join(self.data_dir, "out_image.tiff")
        data_source = gdal.Open(file_name)
        image_format = "GTiff"
        driver = gdal.GetDriverByName(str(image_format))
        print(("Saving:", out_file_name))
        driver.CreateCopy(out_file_name, data_source, 0)
        os.remove(out_file_name)


if __name__ == "__main__":
    GdalSample().invoke(sys.argv)
