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

    def open(self):
        """
        Use gdal.Open to load image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        gdal.Open(file_name)

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
        data_source.GetRasterBand(1).WriteArray(raster)
        # Avoid PermissionError on Windows when trying to delete
        # file_name. From:
        # http://stackoverflow.com/questions/22068148/extremely-frustrating-behavior-with-windowserror-error-32-to-remove-temporary
        data_source.FlushCache()
        driver = None
        data_source = None
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
        driver.CreateCopy(out_file_name, data_source, 0)
        os.remove(out_file_name)


if __name__ == "__main__":
    GdalSample().invoke(sys.argv)
