from mnelab.io.xdf import read_raw_xdf
import mne
from mne_bids import write_raw_bids, BIDSPath, make_dataset_description
from pathlib import Path
from pyxdf import load_xdf

# get dir of this script
dir_project = Path(__file__).parent

# set paths
dir_source = dir_project.joinpath(r'data\sourcedata')
dir_root_bids =  dir_project.joinpath(r'data\bids_mne')

# set bids info
task = 'SpotRotation'

# check for directories in source data
dirs_ids = [x for x in dir_source.iterdir() if x.is_dir()]

# check for .xdf files in each directory
for dir_id in dirs_ids:
    files_xdf = dir_id.glob('*.xdf')

    # process each xdf file with mne_bids
    for file_xdf in files_xdf:
        print(file_xdf)

        # get recoring info for BIDS
        sub_id = dir_id.name

        # find motion stream in .xdf file
        streams, _ = load_xdf(file_xdf)
        streams_ids = [stream["info"]["stream_id"] for stream in streams]
        stream_types = [stream['info']['type'] for stream in streams]

        # get id for motion stream
        motion_stream_id = streams_ids[stream_types.index(['Mocap'])]
        
        # load to mne
        raw = read_raw_xdf(file_xdf, stream_ids=[motion_stream_id], verbose=False)  # stream id has to be a list

        # delete events if they start before eeg recording
        events = mne.events_from_annotations(raw)
        bids_path = BIDSPath(subject=sub_id, task=task, datatype='beh', root=dir_root_bids)
        write_raw_bids(raw, bids_path, overwrite=True, allow_preload=True, format='EDF', verbose=True)

        print(f'Finished writing BIDS for participant {sub_id} and task {task}')



