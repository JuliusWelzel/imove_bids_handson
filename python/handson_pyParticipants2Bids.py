import json
import pandas as pd
from pathlib import Path

# get dir of this script
dir_project = Path(__file__).parent

# set paths
dir_source = dir_project.joinpath(r'data\sourcedata')
dir_root_bids =  dir_project.joinpath(r'data\bids')

####
# Create new participant.tsv
####

# Sample participant data
data = {
    'participant_id': ['sub-1', 'sub-2'], # required column
    'age': [25, 30],
    'group': ['control', 'patient']
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
df.loc[df['participant_id'] == 'sub-1', 'age'] = 26

# assign the group 'control' to all participants
df['group'] = 'control'

# remove height and weight column
df = df.drop(columns=['height', 'weight'])

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
            "control": "Control participant without medication",
            "patient": "Patient participant receiving medication"
        }
    }
}

# Save the .json description to a file
with open(dir_root_bids.joinpath('participants.json'), 'w') as f:
    json.dump(json_description, f, indent=4)
    print(f'Created participants.tsv and participants.json in {dir_root_bids}')
