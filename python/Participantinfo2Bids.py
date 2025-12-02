import json
import pandas as pd
from pathlib import Path

# get dir of this script
dir_project = Path(__file__).parent.parent

# set paths
dir_source = dir_project.joinpath(r'data\sourcedata')
dir_root_bids =  dir_project.joinpath(r'data\bids')

####
# Create new participant.tsv
####

# Sample participant data
data = {
    'participant_id': ['sub-VP014', 'sub-VP015'], # required column
    'age': [24, 70],
    'group': ['HYA', 'HOA']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a .tsv file
df.to_csv(dir_root_bids.joinpath('participants.tsv'), sep='\t', index=False)

####
# Read existing participants.tsv and modify
####

# Read the participants.tsv file
df = pd.read_csv(dir_root_bids.joinpath('participants.tsv'), sep='\t')

# Edit the participant data, where id is 'sub-1'
df.loc[df['participant_id'] == 'sub-VP014', 'age'] = 64

# assign the group 'control' to all participants
df['group'] = 'HOA'

# remove columns which MNE-BIDS automatically generated
# df = df.drop(columns=['height', 'weight'])

####
# Provide descriptions of the columns in the participants.tsv file
####
 
# Sample .json description for the participants.tsv columns
json_description = {
    "participant_id": {
        "Description": "Unique participant identifier"
    },
    "age": {
        "Description": "Age of the participant",
        "Units": "years"
    },
    "group": {
        "Description": "Group to which the participant belongs",
        "Levels": {
            "HYA": "Healthy Young Adults",
            "HOA": "Healthy Older Adults"
        }
    }
}

# Save the .json description to a file
with open(dir_root_bids.joinpath('participants.json'), 'w') as f:
    json.dump(json_description, f, indent=4)
    print(f'Created participants.tsv and participants.json in {dir_root_bids}')
