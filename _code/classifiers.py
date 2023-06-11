import numpy as np

def detect_blinks(eeg_data, std_dev=2):
    threshold = std_dev * np.std(eeg_data)

    # Find where the signal exceeds the threshold
    over_threshold = np.where(eeg_data > threshold)[0]

    if len(over_threshold) == 0:
        return 0

    # Find the gaps between the over-threshold regions
    diff = np.diff(over_threshold)
    gaps = np.where(diff > 1)[0]

    # Add the first and last region edges
    first_edge = -1
    last_edge = len(over_threshold)-1
    region_edges = np.concatenate([[first_edge], gaps, [last_edge]])

    
    blinks = np.zeros(len(eeg_data), dtype=int)
    for i in range(len(region_edges) - 1):
        start_point = over_threshold[region_edges[i] + 1]
        end_point = over_threshold[region_edges[i+1]]
        mid_point = (start_point + end_point) // 2
        blinks[mid_point] = 1
    
    return blinks

