i
import numpy as np

def generate_data(length, num_spikes, spike_duration, baseline=0, noise=1, spike_magnitude=10):
    # Generate baseline EEG data with some noise
    data = np.random.normal(baseline, noise, length)

    # Add spikes at random points
    for _ in range(num_spikes):
        # Choose a random position for the spike
        spike_position = np.random.randint(0, length - spike_duration)
        
        # Increase the value over the duration of the spike
        data[spike_position:spike_position+spike_duration] += spike_magnitude

    return data

eeg_data = generate_data(250, 10, 5)
