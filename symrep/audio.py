import array
import math
import struct
import symrep.base

def sine(freq):
    return symrep.base.Node(
        "sin", lambda t: math.sin(t * freq(t) * 2. * math.pi), [freq])

def square(freq):
    pass

def _to_short(val, max_amplitude=1.0):
    short_max = (2 ** 15) - 1
    val = int(val / max_amplitude * short_max)
    if val > short_max:
        return short_max
    elif val < -short_max:
        return -short_max
    return val

def to_wav(root, sample_rate, length, stream):
    bits_per_sample = 16
    data = array.array("h", map(
        lambda x: _to_short(x[1]),
        symrep.base.sample(root, 0., length, 1. / sample_rate)))

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
    stream.write(struct.pack("<I", 4 * len(data)))
    data.tofile(stream)

if __name__ == "__main__":
    n = symrep.base.product(
        sine(symrep.base.const(440)),
        sine(symrep.base.const(0.2)),
    )
    with open("test.wav", "w") as f:
        to_wav(n, 44100, 5, f)
