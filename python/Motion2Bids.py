from ast import Name
from mnelab.io.xdf import read_raw_xdf
import mne
from mne_bids import write_raw_bids, BIDSPath, make_dataset_description
import numpy as np
from pathlib import Path
from pyxdf import load_xdf

# get dir of this script
dir_project = Path(__file__).parent.parent

# set paths
dir_source = dir_project.joinpath(r'data\source')
dir_root_bids =  dir_project.joinpath(r'data\bids')

# set bids info
TASK = 'EvenTerrainWalking'

# check for directories in source data
files_xdf = dir_source.glob('*.xdf')

# process each xdf file with mne_bids
for file_xdf in files_xdf:
    print(f"Working on {file_xdf.name}")

    # get info for BIDS
    # id from file name, might be different for your data
    sub_id = file_xdf.stem.split('_')[0]

    # create BIDS folder
    bids_path = BIDSPath(subject=sub_id, task=TASK, session=None, datatype='eeg', root=dir_root_bids)
    subj_bidsmotion_path = Path(bids_path.root).joinpath(f"sub-{sub_id}",'motion')  # change datatype in path
    subj_bidsmotion_path.mkdir(exist_ok=True, parents=True)

    # find motion stream in .xdf file
    streams, _ = load_xdf(file_xdf)
    streams_ids = [stream["info"]["stream_id"] for stream in streams]
    stream_types = [stream['info']['type'] for stream in streams]
    stream_names = [stream['info']['name'] for stream in streams]

    # get motion streams 
    # Name of sensor on left foot: 'Movella DOT B5'
    # Name of sensor on right foot: 'Movella DOT B2'
    motion_lf = [s for s in streams if s['info']['name'][0] == 'Movella DOT B5'][0]
    motion_rf = [s for s in streams if s['info']['name'][0] == 'Movella DOT B2'][0]
    
    # get time difference between streams
    time_start_lf = motion_lf['time_stamps'][0]
    time_start_rf = motion_rf['time_stamps'][0]
    print(f"Time difference between left and right foot motion stream start: {time_start_rf - time_start_lf} seconds")

    left_foot = motion_lf['time_series'][:, :-1]  # Assuming left foot markers are in columns 60-63
    right_foot = motion_rf['time_series'][:, :-1]  # Assuming right foot markers are in columns 64-67
    motion_data = np.hstack([left_foot, right_foot]).squeeze()

    # create bids dataset
    TRACKSYS = 'IMU'
    srate_motion = float(motion_lf['info']['nominal_srate'][0])  # Sampling frequency for motion capture data
    print(f'Finished writing BIDS for participant {sub_id} and task {TASK}')


