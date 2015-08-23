import matplotlib.pyplot as plt
import numpy
import sys

dat = numpy.genfromtxt(
    sys.stdin,
    delimiter=",",
    names=True)
cols = dat.dtype.names
for col in cols:
    if col in ["t"] + sys.argv:
        continue
    plt.plot(dat["t"], dat[col], label=col)
plt.legend()
plt.show()
