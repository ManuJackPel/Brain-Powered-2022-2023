import numpy as np
import matplotlib.pyplot as plt
import mne

data = np.genfromtxt('sample_eeg_data_motor_imagery.txt', delimiter=',').T # import and transpose data
data_mv = data/100000 # Converting to microVolt

ch_names = ['Fp1','Fp2','F3','F4','C3','C4','P3','P4','O1','O2','A1','A2','F7','F8','T3','T4','T5','T6','Fz','Cz','Pz','marker?']
sfreq = 200                             # specify sampling frequency of data
channel_type = 'eeg'                    # Specify channel type

info = mne.create_info(                 # Create MNE info file with measurement meta data
    ch_names, 
    sfreq, 
    channel_type, 
    verbose=None)    

raw = mne.io.RawArray(data_mv,info)     # convert data to raw format

print(raw.info)

# raw.plot_psd(fmax=50)                 # Legacy but seems better?
psd = raw.compute_psd(fmax=50)#.plot()  # compute frequency PSD (and optionally plot)
psd_data = psd.to_data_frame()          # convert psd to dataframe
# raw.plot(block=True)                  # plot data

# Create events
events = mne.make_fixed_length_events(raw, id=1, start=5, stop=10, duration=1, first_samp=True, overlap=0)
print(events)
mne.viz.plot_events(events, sfreq=raw.info['sfreq'])

# Creating epochs
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5)
epochs.plot_image()