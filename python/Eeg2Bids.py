from mnelab.io.xdf import read_raw_xdf
import mne
from mne_bids import write_raw_bids, BIDSPath, make_dataset_description
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

    # find eeg stream in .xdf file
    streams, _ = load_xdf(file_xdf)
    streams_ids = [stream["info"]["stream_id"] for stream in streams]
    stream_types = [stream['info']['type'] for stream in streams]

    # get id for eeg stream
    eeg_stream_id = streams_ids[stream_types.index(['EEG'])]
    
    # load to mne
    raw = read_raw_xdf(file_xdf, stream_ids=[eeg_stream_id], verbose=False)  # stream id has to be a list
    
    # add BIDS relevant info (https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html#sidecar-json-_eegjson)
    raw.info['line_freq'] = 50  # specify power line frequency as required by BIDS (European line frequency here)
    
    # delete events if they start before eeg recording
    events, events_id  = mne.events_from_annotations(raw)
    # remove events that start before 0s
    events = events[events[:, 0] >= 0]

    # specify BIDS path and write
    bids_path = BIDSPath(subject=sub_id, task=TASK, datatype='eeg', root=dir_root_bids)
    write_raw_bids(raw, bids_path, events=events, event_id=events_id, overwrite=True, allow_preload=True, format='BrainVision', verbose=True)

    print(f'Finished writing BIDS for participant {sub_id} and task {TASK}')

# make dataset description
make_dataset_description(
    path=bids_path.root,
    name="Dual-task interference during gait in young and older adults",
    authors=["Lara Papin",  "Welzel, J.", "Debener, S."],
    acknowledgements="n/a",
    data_license="n/a",
    funding=[""],
    overwrite=True,
)
