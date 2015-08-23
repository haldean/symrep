import numpy as np
from symrep import *
from symrep.solids import *

n = union(
    sphere(const(1)),
    intersection(
        sphere(const(3)),
        translate(
            sphere(const(2)),
            vec(3., 0., 0.),
        ),
    ),
    translate(
        difference(
            sphere(const(2)),
            sphere(const(1.5)),
            translate(
                sphere(const(2)),
                vec(1., 0., 0.),
            ),
        ),
        vec(0., 3., 0.),
    ),
)

with open("sphere.dot", "w") as f:
    to_dot(n, f)

points = sample_solid(
    n, (-2, -2, -2), (5, 5, 2), 20000, is_inside)
with open("test.xyz", "w") as f:
    solids.write_point_cloud(points, f)
