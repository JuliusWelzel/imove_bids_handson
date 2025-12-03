% configure paths 
fieldTripPath   = 'C:\Users\juliu\Documents\MATLAB\fieldtrip-20251201'; 
matlabFolder    = 'C:\Users\juliu\Nextcloud\Talks\imove_bids_handson\matlab';
xdfFileName     = 'C:\Users\juliu\Nextcloud\Talks\imove_bids_handson\data\source\VP037.xdf';
bidsFolder      = 'C:\Users\juliu\Nextcloud\Talks\imove_bids_handson\data\bids_fieldtrip';

% add fieldtrip 
addpath(matlabFolder);
addpath(fieldTripPath)
ft_defaults
[filepath,~,~] = fileparts(which('ft_defaults'));
addpath(fullfile(filepath, 'external', 'xdf'))

% 1. load and inspect xdf
%--------------------------------------------------------------------------
streams                         = load_xdf(xdfFileName);
[streamNames, channelMetaData]  = xdf_inspect(streams); 

% keep track of data modalities (find entries from output)
% indices are better found this way because stream order may differ between
% recordings 

EEGStreamName           = 'Android_EEG - PRO_009'; 
EEGStreamInd            = find(strcmp(streamNames, EEGStreamName)); 

EventStreamName         = 'UDP_Markers - PRO_009'; 
EventStreamInd          = find(strcmp(streamNames, EventStreamName)); 

MotionStreamName        = 'Movella DOT B3';
MotionStreamInd         = find(strcmp(streamNames, MotionStreamName)); 

% 2. convert streams to fieldtrip data structs  
%--------------------------------------------------------------------------
EEGftData           = stream_to_ft(streams{EEGStreamInd});
cfg = [];
cfg.channel = 'all';
EEGftData = ft_selectdata(cfg, EEGftData);
% Remove channels containing Acc, Gyro, or Quad
channelsToKeep = ~contains(EEGftData.label, {'Acc', 'Gyro', 'Quat'});
cfg = [];
cfg.channel = EEGftData.label(channelsToKeep);
EEGftData = ft_selectdata(cfg, EEGftData);

MotionftData        = stream_to_ft(streams{MotionStreamInd}); 
MotionftData.trial{1} = MotionftData.trial{1}(1:end-1,:);

% 3. Save time synch information
%--------------------------------------------------------------------------

% compute difference between onset times
onsetDiff = MotionftData.hdr.FirstTimeStamp - EEGftData.hdr.FirstTimeStamp; 

% time synchronization using scans.tsv acq field
% later to be entered as cfg.scans.acq_time = string, should be formatted according to RFC3339 as '2019-05-22T15:13:38'
eegOnset        = [1990,01,01,00,00,0.000];             % [YYYY,MM,DD,HH,MM,SS]
motionOnset     = [1990,01,01,00,00,onsetDiff];

eegAcqNum       = datenum(eegOnset);
eegAcqTime      = datestr(eegAcqNum,'yyyy-mm-ddTHH:MM:SS.FFF');
motionAcqNum    = datenum(motionOnset);
motionAcqTime   = datestr(motionAcqNum,'yyyy-mm-ddTHH:MM:SS.FFF');

% 4. enter generic metadata
%--------------------------------------------------------------------------
cfg                                         = [];
cfg.bidsroot                                = bidsFolder;
cfg.sub                                     = 'VP037';
cfg.task                                    = 'EvenTerrainWalking';
cfg.scans.acq_time                          = datetime('now');

% required for dataset_description.json
cfg.dataset_description.Name                = 'Dual-task interference during gait in young and older adults';
cfg.dataset_description.BIDSVersion         = '1.9';

% optional for dataset_description.json
cfg.dataset_description.Authors             = {"Lara Papin",  "Welzel, J.", "Debener, S."};


% 5. enter eeg metadata and feed to data2bids function
%--------------------------------------------------------------------------
cfg.datatype = 'eeg';
cfg.eeg.Manufacturer                = 'mbt';
cfg.eeg.PowerLineFrequency          = 50; 
cfg.eeg.EEGReference                = 'REF'; 
cfg.eeg.SoftwareFilters             = 'n/a'; 

% time synch information in scans.tsv file
cfg.scans.acq_time  = eegAcqTime; 

data2bids(cfg, EEGftData);

% 6. enter motion metadata and feed to dat2bids functino
%--------------------------------------------------------------------------
cfg                             = rmfield(cfg, 'eeg'); 
cfg.datatype                    = 'motion'; 
cfg.tracksys                    = 'IMU';
cfg.motion.TrackingSystemName   = 'Movella';


% specify channel details, this overrides the details in the original data structure
cfg.channels = [];
cfg.channels.name = {
  'LeftFoot_Accel_x'
  'LeftFoot_Accel_y'
  'LeftFoot_Accel_z'
  'LeftFoot_Gyro_x'
  'LeftFoot_Gyro_y'
  'LeftFoot_Gyro_z'
  };
cfg.channels.component= {
  'x'
  'y'
  'z'
  'x'
  'y'
  'z'
  };
cfg.channels.type = {
  'ACCEL'
  'ACCEL'
  'ACCEL'
  'GYRO'
  'GYRO'
  'GYRO'
  };
cfg.channels.units = {
  'm/s^2'
  'm/s^2'
  'm/s^2'
  'deg/s'
  'deg/s'
  'deg/s'
  };


cfg.channels.tracked_point = {
  'LeftFoot'
  'LeftFoot'
  'LeftFoot'
  'LeftFoot'
  'LeftFoot'
  'LeftFoot'
  };

% rename the channels in the data to match with channels.tsv
MotionftData.label = cfg.channels.name;

% time synch information in scans.tsv file
cfg.scans.acq_time  = motionAcqTime; 

data2bids(cfg, MotionftData);
