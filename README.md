# iMoVe BIDS Hands-on

This repository contains code for converting XDF files to BIDS format using Python and MATLAB.

## Data

Download the source data from: [DATA_LINK_PLACEHOLDER]

Place the XDF files in the `data/source/` directory.

## Python Workflow

### Prerequisites

Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

This will install the required packages:
- mne
- mne-bids
- pandas
- pyxdf
- ipykernel

### Running the Scripts

The Python scripts should be run in the following order:

### 1. EEG to BIDS
```bash
python python/Eeg2Bids.py
```
Converts EEG data from XDF files to BIDS format.

### 2. Motion to BIDS
```bash
python python/Motion2Bids.py
```
Converts motion capture data (IMU) from XDF files to BIDS format.

### 3. Participant Info to BIDS
```bash
python python/Participantinfo2Bids.py
```
Adds participant information to the BIDS dataset.

## MATLAB Workflow

### Prerequisites
- FieldTrip toolbox
- Helper functions: `stream_to_ft.m` and `xdf_inspect.m` (included in `matlab/` folder)

### Setup
1. Update the paths in `MoBIDS_handson_1_xdf2bids.m`:
   - `fieldTripPath`: Path to your FieldTrip installation
   - `matlabFolder`: Path to the `matlab/` folder in this repository
   - `xdfFileName`: Path to your XDF file
   - `bidsFolder`: Output directory for BIDS data

2. Ensure the helper functions are added to MATLAB path:
   - The script automatically adds `matlabFolder` to the path
   - Make sure `stream_to_ft.m` and `xdf_inspect.m` are in the `matlab/` folder

### Run
```matlab
run('matlab/MoBIDS_handson_1_xdf2bids.m')
```

This single script handles both EEG and motion data conversion to BIDS format using FieldTrip's `data2bids` function.

## Output

Both workflows create BIDS-formatted datasets in:
- Python: `data/bids_mne/`
- MATLAB: `data/bids_fieldtrip/`

## Relevant Links

### BIDS Specification
- [BIDS Specification](https://bids-specification.readthedocs.io/)
- [BIDS EEG](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html)
- [BIDS Motion](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/motion.html)

### MNE-Python
- [MNE-Python Documentation](https://mne.tools/stable/index.html)
- [MNE-BIDS Documentation](https://mne.tools/mne-bids/stable/index.html)
- [MNE-BIDS Tutorial: Converting data to BIDS](https://mne.tools/mne-bids/stable/auto_examples/convert_mne_sample.html)

### FieldTrip
- [FieldTrip Documentation](https://www.fieldtriptoolbox.org/)
- [FieldTrip data2bids Function](https://www.fieldtriptoolbox.org/reference/data2bids.m/)
- [FieldTrip BIDS Tutorial](https://www.fieldtriptoolbox.org/example/bids/)
