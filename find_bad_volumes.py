import sys
import numpy as np
import subprocess
import glob
import os
import nibabel as nib


if len(sys.argv) < 4:
    print('usage python3 find_bad_volumes.py input_nifti bad_nifti good_nifti stddev')
    exit(0)

input_nifti = sys.argv[1]
bad_nifti = sys.argv[2]
good_nifti = sys.argv[3]
dev = int(sys.argv[4])

import tempfile
with tempfile.TemporaryDirectory() as tempdir:
    splits = os.path.join(tempdir, 'split')
        
    # temporarily change output type for speed
    fsl_type = os.getenv('FSLOUTPUTTYPE')
    os.putenv('FSLOUTPUTTYPE', 'NIFTI')

    command = 'fslsplit {} {}'.format(input_nifti, splits)
    subprocess.run(command, shell = True)
    vols = sorted(os.listdir(tempdir))

    for i,v in enumerate(vols):
        infile = os.path.join(tempdir, v)
        outfile = os.path.join(tempdir, v.split('.')[0])
        command = 'bet2 {} {} -f 0.3 -m -n'.format(infile, outfile)
        subprocess.run(command, shell = True)
    
    masks = sorted(glob.glob(os.path.join(tempdir, '*mask*')))
    masksize = list()
    for m in masks:
        img = nib.load(m)
        masksize.append(np.count_nonzero(img.get_data()))
    
    mean_mask = np.mean(masksize)
    std_mask = np.std(masksize)

    bad_vols = [i for i,x in enumerate(masksize) if x < (mean_mask - dev*std_mask)]

    # change back
    os.putenv('FSLOUTPUTTYPE', fsl_type)
 
print('{} bad volumes found'.format(len(bad_vols)))

if not bad_vols:
    exit()

from nilearn import image
img = image.load_img(input_nifti)
bad_img = image.index_img(img, bad_vols)
bad_img.to_filename(bad_nifti)
print('Bad volumes written to:', bad_nifti)

good_mask = np.ones(len(vols), dtype = bool)
good_mask[bad_vols] = False
good_img = image.index_img(img, good_mask)
good_img.to_filename(good_nifti)
print('Good volumes written to:', good_nifti)
    


