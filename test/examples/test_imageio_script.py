import recipy

import imageio
import os

in_path = r'R:\Science\XFM\GaryRuben\git_repos\tmm_model\acsemble\data'
out_path = r'C:\temp'

im1 = imageio.imread(os.path.join(in_path, 'golosio_100-C.tiff'))
im2 = imageio.imread(os.path.join(in_path, 'Ni_test_phantom2.png'))

imageio.imwrite(os.path.join(out_path, 'im1.png'), im1)
imageio.imwrite(os.path.join(out_path, 'im2.png'), im2)
