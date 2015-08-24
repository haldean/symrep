import numpy as np
from symrep import *
from symrep.render import *
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
bbox_lo = np.array((-2., -2., -2.))
bbox_hi = np.array((5., 5., 2.))

with open("sphere.dot", "w") as f:
    to_dot(n, f)

points = list(sample_solid(
    n, bbox_lo, bbox_hi, is_inside, max_sec=30))
with open("sphere.xyz", "w") as f:
    solids.write_point_cloud(points, f)

voxel_map = voxelize(points, bbox_lo, bbox_hi, 0.1)
show_voxels(voxel_map)
