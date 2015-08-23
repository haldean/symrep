import numpy as np
from symrep import *
from symrep.solids import *

n = union(
    difference(
        intersection(
            translate(
                sphere(const(1.0)),
                vec(-1, 0., 0.),
            ),
            translate(
                box(size(2., 2., 1.75)),
                vec(-1., 0., 0.25),
            ),
        ),
        translate(
            cylinder(
                const(0.35),
                const(2.0),
            ),
            vec(-1., 0., 0.),
        ),
    ),
    intersection(
        sphere(const(3.)),
        translate(
            sphere(const(2.)),
            vec(3., 0., 0.),
        ),
    ),
    translate(
        difference(
            sphere(const(2.)),
            sphere(const(1.5)),
            translate(
                sphere(const(2.)),
                vec(1., 0., 0.),
            ),
        ),
        vec(0., 3., 0.),
    ),
)

with open("sphere.dot", "w") as f:
    to_dot(n, f)

points = sample_solid(
    n, (-2, -2, -2), (5, 5, 2), is_on_surface(0.05), max_sec=30)
with open("sphere.xyz", "w") as f:
    solids.write_point_cloud(points, f)
