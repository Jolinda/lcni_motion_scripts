# lcni_motion_scripts
Scripts for dealing with subject motion in fmri

censor_volumes.py
This script takes a functional series in nifti format and a text file containing motion metrics and removes volumes exceeding a given value. There is also an option to specify a minimum duration for retained segments, and an option to output a file that indicates where the retained blocks begin and end.

find_bad_volumes.py
This script attempts to find volumes with extreme levels of motion such that the subject moves out of the field of view. It does this by performing brain extraction on each volume, calculating the number of voxels, and looking for those where the total number of brain voxels differs from the mean for the series by X standard deviations.
