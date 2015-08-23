import symrep
import sys

n1 = symrep.product(
    symrep.const(0.3),
    symrep.product(
        symrep.audio.sine(symrep.const(440)),
        symrep.audio.sine(symrep.const(0.5)),
    )
)
n2 = symrep.product(
    symrep.const(0.3),
    symrep.product(
        symrep.audio.sine(symrep.const(360)),
        symrep.audio.sine(symrep.const(0.4)),
    )
)
n3 = symrep.product(
    symrep.const(0.3),
    symrep.audio.sine(symrep.const(500)),
)
n = symrep.sum(n1, n2, n3)

symrep.audio.to_wav(n, 44100, 10, sys.stdout)