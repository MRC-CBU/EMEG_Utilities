#!/imaging/local/software/miniconda/envs/mne0.18/bin/python
"""
==================================================================================
Apply pre-computed ICA to EEG/MEG data in fiff-format to remove eye-movement
artefacts.
Requires ICA decomposition from Fiff_Compute_ICA.py.
For more help, type Fiff_Apply_ICA.py -h.
Based on MNE-Python.
For a tutorial on ICA in MNE-Python, look here:
https://martinos.org/mne/stable/auto_tutorials/preprocessing/plot_artifacts_correction_ica.html
==================================================================================
"""
# Olaf Hauk, Python 3, July 2019, Feb 2020

from sys import argv, exit
import argparse

import mne

print(__doc__)

print('MNE %s.\n' % mne.__version__)

if len(argv) == 1:
    # display help message when no args are passed.
    exit(1)

###
# PARSE INPUT ARGUMENTS
###

parser = argparse.ArgumentParser(description='Apply ICA.')

parser.add_argument('--FileRawIn', help='Input filename for raw data.')
parser.add_argument('--FileICA', help='Output file for ICA decomposition (default FileRawIn-ica.fif).', default='')
parser.add_argument('--FileRawOut', help='Output filename for raw data (default FileRawIn_ica_raw.fif).', default='')
parser.add_argument('--ICAcomps', help='ICA components to remove (default: as specified in precomputed ICA).', nargs='+', type=int, default=[])

args = parser.parse_args()

print(mne)

###
# create filenames
###

# get filename stem for case with and without suffix .fif
filestem = args.FileRawIn.split('.fif')[0]

# raw-filenames to be subjected to ICA for this subject
if args.FileRawIn[-4:] != '.fif':

    raw_fname_in = filestem + '.fif'

else:

    raw_fname_in = args.FileRawIn

# save raw with ICA applied and artefacts removed
if args.FileRawOut == '':

    raw_fname_out = filestem + '_ica_raw.fif'

else:

    raw_fname_out = args.FileRawOut

# file with ICA decomposition
if args.FileICA == '':

    ica_fname_in = filestem + '-ica.fif'

else:

    ica_fname_in = args.FileICA

###
# APPLY ICA
###

print('Reading raw file %s' % raw_fname_in)
raw = mne.io.read_raw_fif(raw_fname_in, preload=True)

print('Reading ICA file %s' % ica_fname_in)
ica = mne.preprocessing.read_ica(ica_fname_in)

# if ICA components to be removed specified on command line
if args.ICAcomps != []:

    ica.exclude = args.ICAcomps

print('Applying ICA to raw file, removing components:')
print(' '.join(str(x) for x in ica.exclude))

ica.apply(raw)

print('Saving raw file with ICA applied to %s' % raw_fname_out)
raw.save(raw_fname_out, overwrite=True)
