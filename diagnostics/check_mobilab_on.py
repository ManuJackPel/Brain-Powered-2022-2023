from pylsl import StreamInlet, resolve_stream

streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

while True:
    data, timestamp = inlet.pull_sample()
    print(timestamp)
