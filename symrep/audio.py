import array
import math
import struct
import symrep

def sine(freq):
    return symrep.Node(
        "sin", lambda t: math.sin(t * freq(t) / (2 * math.pi)), [freq])

def to_wav(root, sample_rate, length, stream):
    num_samples = int(math.ceil(length * sample_rate))
    print 'generating', num_samples, 'samples'
    bits_per_sample = 32

    def sample_t():
        i = t = 0
        while i < num_samples:
            yield t
            i += 1
            t += 1 / sample_rate

    data = array.array("f", (root(t) for t in sample_t()))
    print 'data is', len(data), 'samples'
    import pprint; pprint.pprint(data[:20])

    # begin file header
    stream.write("RIFF")
    stream.write(struct.pack("<I",
        # length of file is length of remaining bytes in the file header, length
        # of the format header, length of the data header and the data itself
        4 + 24 + 8 + len(data)))
    stream.write("WAVE")

    # begin fmt block header
    stream.write("fmt ")
    stream.write(struct.pack("<IHHIIHH",
        16,           # length of format block
        1,            # use PCM encoding
        1,            # number of channels
        sample_rate,
        int((sample_rate * bits_per_sample) / 8.),
        bits_per_sample / 8,
        bits_per_sample,
    ))

    # begin data header
    stream.write("data")
    stream.write(struct.pack("<I", len(data)))
    data.tofile(stream)

if __name__ == "__main__":
    with open("test.wav", "w") as f:
        to_wav(sine(symrep.const(440)), 41000, 10, f)
