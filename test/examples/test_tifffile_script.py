import recipy

import tifffile
import os

in_path = r'R:\Science\XFM\GaryRuben\git_repos\tmm_model\acsemble\data'
out_path = r'C:\temp'

im1 = tifffile.imread(os.path.join(in_path, 'golosio_100-C.tiff'))

tifffile.imsave(os.path.join(out_path, 'im1.tiff'), im1)
