import numpy as n
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet
from pynput import keyboard

# Set the parameters
sample_rate = 250  # Hz
frequency1 = 10  # Hz
frequency2 = 25  # Hz

# Global variable to track the state of the space bar
space_pressed = False

# Function to handle key press events
def on_press(key):
    global space_pressed
    if key == keyboard.Key.space:
        space_pressed = True

# Function to handle key release events
def on_release(key):
    global space_pressed
    if key == keyboard.Key.space:
        space_pressed = False

# Function to send a sample through the LSL output
def send_sample(axis3):
    # Generate EEG-like data
    eeg_data1 = np.sin(2 * np.pi * frequency1 * time_passed) + np.random.normal(0, 0.1)
    eeg_data2 = np.sin(2 * np.pi * frequency2 * time_passed) + np.random.normal(0, 0.1)

    outlet.push_sample([eeg_data1 + axis3, eeg_data2])

if __name__ == "__main__":
    # Create listener and assign event handlers
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    # Create the stream info
    info = StreamInfo('Brandon Stream', 'EEG', 2, sample_rate, 'float32', 'myuid34234')
    # Create a stream outlet
    outlet = StreamOutlet(info)
    # Now, for an infinite amount of time, send samples
    time_passed = 0  # seconds
    while True:
        # Check if the space bar is pressed
        if space_pressed:
            axis3 = 5
        else:
            axis3 = 0

        send_sample(axis3)

        time.sleep(1 / sample_rate)
        time_passed += (1 / sample_rate)

