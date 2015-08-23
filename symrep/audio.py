import array
import datetime
import math
import struct
import symrep.base

def sine(freq, name=None):
    return symrep.base.Node(
        name, "sine",
        lambda t: math.sin(t * freq(t) * 2. * math.pi), {freq: "freq"})

def square(freq, duty, name=None):
    def gen(t):
        t = t * freq(t)
        t_frac = t - int(t)
        if t_frac < duty(t):
            return 1.
        return 0.
    return symrep.base.Node(name, "square", gen, {freq: "freq"})

def sawtooth(freq, name=None):
    def gen(t):
        t = t * freq(t)
        return t - int(t)
    return symrep.base.Node(name, "sawtooth", gen, {freq: "freq"})

def _to_short(val, max_amplitude=1.0):
    short_max = (2 ** 15) - 1
    val = int(val / max_amplitude * short_max)
    if val > short_max:
        return short_max
    elif val < -short_max:
        return -short_max
    return val

def _write_wav_header(stream, sample_rate, bits_per_sample, total_size):
    # begin file header
    stream.write("RIFF")
    stream.write(struct.pack("<I", total_size))
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


def to_wav(root, sample_rate, length, stream):
    bits_per_sample = 16
    data = array.array("h", map(
        lambda x: _to_short(x[1]),
        symrep.base.sample(root, 0., length, 1. / sample_rate)))

    # length of file is length of remaining bytes in the file header, length
    # of the format header, length of the data header and the data itself
    file_len = 4 + 24 + 8 + len(data)
    _write_wav_header(stream, sample_rate, 16, file_len)

    # begin data header
    stream.write("data")
    stream.write(struct.pack("<I", (bits_per_sample / 8) * len(data)))
    data.tofile(stream)

def stream_pcm(root, sample_rate, stream):
    _write_wav_header(stream, sample_rate, 16, 2 ** 32 - 1)
    stream.write("data")
    stream.write(struct.pack("<I", 2 ** 32 - 1))
    t = 0.
    while True:
        stream.write(struct.pack("<h", _to_short(root(t))))
        t += 1. / sample_rate
