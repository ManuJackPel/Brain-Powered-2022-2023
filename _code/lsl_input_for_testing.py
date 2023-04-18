from pylsl import StreamInlet, resolve_stream

if __name__ == "__main__":
    streams = resolve_stream('name', 'dummy_sinewave')
    inlet = StreamInlet(streams[0])

    while True:
        sample, timestamp = inlet.pull_sample()
        print(sample[0])
            

