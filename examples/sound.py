from symrep import *
import sys

n1 = product(
    const(0.3),
    product(
        audio.sine(const(440)),
        audio.sine(const(0.5)),
    )
)
n2 = product(
    const(0.2),
    audio.sine(
        product(
            const(400),
            piecewise(
                audio.sawtooth(const(1)),
                const(1),
                const(1),
            ),
        )
    )
)
n3 = product(
    const(0.3),
    audio.sine(const(220)),
)
n4 = product(
    audio.sine(const(140)),
    audio.square(const(2), const(0.05)),
)
n5 = product(
    audio.sine(const(170)),
    shift(
        audio.square(const(2), const(0.05)),
        const(0.25),
    )
)
n = sum(n1, n2, n3, n4, n5)

audio.stream_pcm(n, 44100, sys.stdout)
