from symrep import *
import sys

n = sum(
    product(
        const(0.3),
        product(
            audio.sine(const(440)),
            audio.sine(const(0.5)),
        )
    ),
    product(
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
    ),
    product(
        const(0.3),
        audio.sine(const(220)),
    ),
    product(
        audio.sine(const(140)),
        audio.square(const(2), const(0.05)),
    ),
    product(
        const(0.5),
        audio.sine(const(100)),
        shift(
            audio.square(const(2), const(0.05)),
            const(0.25),
        )
    ),
    product(
        const(0.2),
        audio.sine(const(523)),
        audio.square(
            const(2),
            audio.sawtooth(const(1. / 60.)),
        ),
    )
)

with open("sound.dot", "w") as f:
    to_dot(n, f)
audio.stream_pcm(n, 44100, sys.stdout)
