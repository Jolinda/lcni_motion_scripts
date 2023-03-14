# lcni_motion_scripts
Scripts for dealing with subject motion in fmri

## censor_volumes.py  
This script takes a functional series in nifti format and a text file containing motion metrics and removes volumes exceeding a given value. There is also an option to specify a minimum duration for retained segments, and an option to output a file that indicates where the retained segment begin and end. This file will consist of a series of 1's and 0's: 1 will indicate the last volume in a segment, and all other volumes will be labeled 0. 

```
usage: python3 censor_volumes.py [-h] --input INPUT --metrics METRICS --threshold
                                      THRESHOLD --output OUTPUT [--duration DURATION]
                                      [--points POINTS]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         nifti formatted file to censor
  --metrics METRICS     text file with values to be tested for censoring
  --threshold THRESHOLD
                        threshold for censoring
  --output OUTPUT       name of output file
  --duration DURATION   minimum duration for retained blocks (optional)
  --points POINTS       name of file for stitch points (optional)
  ```
 


## find_bad_volumes.py  
This script attempts to find volumes where the subject has moved out of the field of view. It does this by performing brain extraction on each volume, calculating the number of voxels in the brain, and looking for volumes where the total number of brain voxels differs from the mean for the series by a given number of standard deviations.
```
usage: python3 find_bad_volumes.py input_nifti bad_nifti good_nifti stddev
input_nifti: file to inspect
bad_nifti: output file for extracted 'bad' volumes
good_nifti: output file for remaining 'good' volumes
stddev: integer threshold for how many standard deviations from the mean should be considered "bad"
```
