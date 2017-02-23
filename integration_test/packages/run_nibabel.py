"""
Sample script that runs nibabel functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import nibabel as nib
import numpy as np

from integration_test.packages.base import Base


class NibabelSample(Base):
    """
    Sample script that runs nibabel functions logged by recipy.

    This class assumes the existence of a data/nibabel directory,
    co-located with this file, with the following content:

    * analyze_image.hdr + .img: plain ANALYZE image
    * mgh_image.mgh: MGH image
    * minc1_image.mnc: MINC1 image
    * minc2_image.mnc: MINC2 image
    * nifti1_image.nii: NIfTI1 image
    * nifti2_image.nii:  NIfTI2 image
    * parrec_image_par.PAR + .REC: Philips PAR/REC image
    * spm2_image.hdr + .img + .mat: SPM2 ANALYZE image
    * spm99_image.hdr + .img + .mat: SPM99 ANALYZE image

    Running this script with argument 'create_sample_data' will create
    all these files, except for parrec_image.PAR + .REC, minc1_image.mnc,
    minc2_image.mnc.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "nibabel")

    def get_data(self):
        """
        Get sample numpy data.

        :return: data
        :rtype: numpy.array
        """
        return np.arange(24, dtype=np.int16).reshape((2, 3, 4))

    def get_affine(self):
        """
        Get sample numpy affine data.

        :return: data
        :rtype: numpy.array
        """
        return np.diag([1, 2, 3, 1])

    def analyze_from_filename(self):
        """
        Use nibabel.analyze.AnalyzeImage.from_filename to
        load analyze_image.hdr + .img.
        """
        file_name = os.path.join(self.data_dir, "analyze_image")
        nib.analyze.AnalyzeImage.from_filename(file_name)

    def analyze_to_filename(self):
        """
        Use nibabel.analyze.AnalyzeImage.to_filename to
        save out_analyze_image.hdr + .img.
        """
        file_name = os.path.join(self.data_dir, "out_analyze_image")
        img = nib.AnalyzeImage(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".hdr")
        os.remove(file_name + ".img")

    def mgh_from_filename(self):
        """
        Use nibabel.freesurfer.mghformat.MGHImage.from_filename to
        load mgh_image.mgh.
        """
        file_name = os.path.join(self.data_dir, "mgh_image")
        nib.freesurfer.mghformat.MGHImage.from_filename(file_name)

    def mgh_to_filename(self):
        """
        Use nibabel.freesurfer.mghformat.MGHImage.to_filename to
        save out_mgh_image.mgh.
        """
        file_name = os.path.join(self.data_dir, "out_mgh_image")
        img = nib.freesurfer.mghformat.MGHImage(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".mgh")

    def minc1_from_filename(self):
        """
        Use nibabel.minc1.Minc1Image.from_filename to load minc1_image.mnc.
        """
        file_name = os.path.join(self.data_dir, "minc1_image")
        nib.minc1.Minc1Image.from_filename(file_name)

    def minc1_to_filename(self):
        """
        Use nibabel.minc1.Minc1Image.to_filename to save
        out_minc1_image.mnc.
        """
        file_name = os.path.join(self.data_dir, "out_minc1_image")
        img = nib.minc1.Minc1Image(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".minc")

    def minc2_from_filename(self):
        """
        Use nibabel.minc1.Minc2Image.from_filename to load minc2_image.mnc.
        """
        file_name = os.path.join(self.data_dir, "minc2_image")
        nib.minc2.Minc2Image.from_filename(file_name)

    def minc2_to_filename(self):
        """
        Use nibabel.minc2.Minc2Image.to_filename to save
        out_minc2_image.mnc.
        """
        file_name = os.path.join(self.data_dir, "out_minc2_image")
        img = nib.minc2.Minc2Image(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".minc")

    def nifti1_from_filename(self):
        """
        Use nibabel.Nifti1Image.from_filename to load nifti1_image.nii.
        """
        file_name = os.path.join(self.data_dir, "nifti1_image")
        nib.Nifti1Image.from_filename(file_name)

    def nifti1_to_filename(self):
        """
        Use nibabel.Nifti1Image.to_filename to save out_nifti1_image.nii.
        """
        file_name = os.path.join(self.data_dir, "out_nifti1_image")
        img = nib.Nifti1Image(self.get_data(), self.get_affine())
        img.to_filename(file_name)
        os.remove(file_name + ".nii")

    def nifti2_from_filename(self):
        """
        Use nibabel.Nifti2Image.from_filename to load nifti2_image.nii.
        """
        file_name = os.path.join(self.data_dir, "nifti2_image")
        nib.Nifti2Image.from_filename(file_name)

    def nifti2_to_filename(self):
        """
        Use nibabel.Nifti2Image.to_filename to save out_nifti2_image.nii.
        """
        file_name = os.path.join(self.data_dir, "out_nifti2_image")
        img = nib.Nifti2Image(self.get_data(), self.get_affine())
        img.to_filename(file_name)
        os.remove(file_name + ".nii")

    def parrec_from_filename(self):
        """
        Use nibabel.parrec.PARRECImage.from_filename to load
        parrec_image.PAR + .REC.
        """
        file_name = os.path.join(self.data_dir, "parrec_image.PAR")
        nib.parrec.PARRECImage.from_filename(file_name)

    def parrec_to_filename(self):
        """
        Use nibabel.parrec.PARRECImage.from_filename to load
        parrec_image.PAR + .REC then
        nibabel.parrec.PARRECImage.to_filename to save it as
        out_parrec_image.PAR + .REC.
        """
        file_name = os.path.join(self.data_dir, "parrec_image.PAR")
        par_file_name = os.path.join(self.data_dir, "out_parrec_image.PAR")
        rec_file_name = os.path.join(self.data_dir, "out_parrec_image.REC")
        img = nib.parrec.PARRECImage.from_filename(file_name)
        img.to_filename(par_file_name)
        os.remove(par_file_name)
        os.remove(rec_file_name)

    def spm2analyze_from_filename(self):
        """
        Use nibabel.spm2analyze.Spm2AnalyzeImage.from_filename to
        load spm2_image.hdr + .img + .mat.
        """
        file_name = os.path.join(self.data_dir, "spm2_image")
        nib.spm2analyze.Spm2AnalyzeImage.from_filename(file_name)

    def spm2analyze_to_filename(self):
        """
        Use nibabel.spm2analyze.Spm2AnalyzeImage.to_filename to
        save out_spm2_image.hdr + .img + .mat.
        """
        file_name = os.path.join(self.data_dir, "out_spm2_image")
        img = nib.spm2analyze.Spm2AnalyzeImage(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".hdr")
        os.remove(file_name + ".img")
        os.remove(file_name + ".mat")

    def spm99analyze_from_filename(self):
        """
        Use nibabel.spm99analyze.Spm99AnalyzeImage.from_filename to
        load spm99_image.hdr + .img + .mat.
        """
        file_name = os.path.join(self.data_dir, "spm99_image")
        nib.spm99analyze.Spm99AnalyzeImage.from_filename(file_name)

    def spm99analyze_to_filename(self):
        """
        Use nibabel.spm99analyze.Spm99AnalyzeImage.to_filename to
        save out_spm99_image.hdr + .img + .mat.
        """
        file_name = os.path.join(self.data_dir, "out_spm99_image")
        img = nib.spm99analyze.Spm99AnalyzeImage(self.get_data(), np.eye(4))
        img.to_filename(file_name)
        os.remove(file_name + ".hdr")
        os.remove(file_name + ".img")
        os.remove(file_name + ".mat")

    def create_sample_data(self):
        """
        Create sample data files. The files created are:

        * analyze_image.hdr + .img: plain ANALYZE image
        * mgh_image.mgh: MGH image
        * nifti1_image.nii: NIfTI1 image
        * nifti2_image.nii:  NIfTI2 image
        * spm2_image.hdr + .img + .mat: SPM2 ANALYZE image
        * spm99_image.hdr + .img + .mat: SPM99 ANALYZE image
        """
        file_name = os.path.join(self.data_dir, "analyze_image")
        analyze_img = nib.AnalyzeImage(self.get_data(), np.eye(4))
        analyze_img.to_filename(file_name)
        file_name = os.path.join(self.data_dir, "mgh_image")
        mgh_img = nib.freesurfer.mghformat.MGHImage(self.get_data(),
                                                    np.eye(4))
        mgh_img.to_filename(file_name)
        file_name = os.path.join(self.data_dir, "nifti1_image")
        nifti1_img = nib.Nifti1Image(self.get_data(), self.get_affine())
        nifti1_img.to_filename(file_name)
        file_name = os.path.join(self.data_dir, "nifti2_image")
        nifti2_img = nib.Nifti2Image(self.get_data(), self.get_affine())
        nifti2_img.to_filename(file_name)
        file_name = os.path.join(self.data_dir, "spm2_image")
        spm2_img = nib.spm2analyze.Spm2AnalyzeImage(self.get_data(),
                                                    np.eye(4))
        spm2_img.to_filename(file_name)
        file_name = os.path.join(self.data_dir, "spm99_image")
        spm99_img = nib.spm99analyze.Spm99AnalyzeImage(self.get_data(),
                                                       np.eye(4))
        spm99_img.to_filename(file_name)


if __name__ == "__main__":
    NibabelSample().invoke(sys.argv)
