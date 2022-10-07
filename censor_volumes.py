import argparse
import numpy as np
import subprocess
import os
import tempfile

parser = argparse.ArgumentParser(description='Censor epi volumes according to framewise displacement or other metric')

parser.add_argument('--input', help='nifti formatted file to censor', required=True)
parser.add_argument('--metrics', help='text file with values to be tested for censoring', required=True)
parser.add_argument('--threshold', type=float, help='threshold for censoring', required=True)
parser.add_argument('--output', help='name of output file', required=True)
parser.add_argument('--duration', type=float, help='minimum duration for retained blocks (optional)', default=0)
parser.add_argument('--points', help='name of file for stitch points (optional)', default=None)

args = parser.parse_args()

input_file = args.input

TR = float(subprocess.check_output(['fslval', input_file, 'pixdim4']))

fd_threshold = args.threshold
min_duration = args.duration
metric_data = np.loadtxt(args.metrics)
output_file = args.output
points_file = args.points

# duplicate first value, otherwise it will not be included in final output
metric_data = np.insert(metric_data, 0, metric_data[0])
peak_indices = np.where(metric_data > fd_threshold)[0]


with tempfile.TemporaryDirectory() as tempdir:
    # temporarily change output type for speed
    fsl_type = os.getenv('FSLOUTPUTTYPE')
    os.putenv('FSLOUTPUTTYPE', 'NIFTI')
    print('splitting ' + input_file)
    subprocess.call(['fslsplit', input_file, os.path.join(tempdir, 'split')])
    vols = sorted(os.listdir(tempdir))
    # duplicate 1st volume so it isn't excluded
    vols.insert(0, vols[0])
    blocks = np.split(vols, peak_indices)

    subblocks = [block[1:].tolist() for block in blocks if len(block[1:]) > min_duration/TR]

    print('{} long enough blocks'.format(len(subblocks)))
    
    file_list = [os.path.join(tempdir, name) for block in subblocks for name in block]
    
    # change back
    os.putenv('FSLOUTPUTTYPE', fsl_type)
    print('merging to ' + output_file)
    subprocess.call(['fslmerge', '-t', output_file] + file_list)

if points_file:
    stitch_points = ['0'] * sum([len(block) for block in subblocks])
    i = 0
    for block in subblocks:
        i += len(block)
        if (i < len(stitch_points)) :
            stitch_points[i] = '1'

    print('writing ' + points_file)
    with open(points_file, 'w') as f:
        for point in stitch_points:
            f.write(point)
            f.write('\n')
        
print('done')

    
    
