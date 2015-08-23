import numpy as np
from symrep import *

n = solids.union(
    solids.sphere(const(1)),
    solids.intersection(
        solids.sphere(const(3)),
        solids.translate(
            solids.sphere(const(2)),
            const(np.array((3., 0., 0.))),
        ),
    ),
)

with open("test.xyz", "w") as f:
    solids.write_pointcloud(
        n, (-1, -2, -2), (5, 2, 2), 100000, f)
