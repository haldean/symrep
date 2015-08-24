from __future__ import division

import numpy as np
import random
import symrep.base
import time


def vec(*v):
    if len(v) == 3:
        fill = np.zeros(4)
        fill[:3] = v
        v = fill
    return symrep.base.const(v)

def point(*p):
    if len(p) == 3:
        fill = np.ones(4)
        fill[:3] = p
        p = fill
    return symrep.base.const(p)

def size(*s):
    return symrep.base.const(np.array(s))

def transform(n, T, name=None, nodetype="transform"):
    return symrep.base.Node(
        name, nodetype, lambda t: n(T(t).dot(t)), {n: "value", T: "transform"})

def translate(n, trans, name=None):
    return symrep.base.shift(n, invert(trans), name=name)

def union(*nodes):
    return symrep.base.Node(
        None, "union", lambda t: min(map(lambda n: n(t), nodes)),
        {n: "value" for n in nodes})

def intersection(*nodes):
    return symrep.base.Node(
        None, "intersection", lambda t: max(map(lambda n: n(t), nodes)),
        {n: "value" for n in nodes})

def invert(n, name=None):
    return symrep.base.Node(name, "invert", lambda t: -n(t), {n: "value"})

def difference(base, *subs):
    return intersection(base, invert(union(*subs)))

def sphere(radius, name=None):
    return symrep.base.Node(
        name, "sphere",
        lambda t: np.linalg.norm(t[:3]) - radius(t), {radius: "radius"})

def cylinder(radius, height, name=None):
    def eval_t(t):
        circle_dist = np.linalg.norm(t[:2])
        axial_dist = abs(t[2])
        return max(circle_dist - radius(t), axial_dist - height(t) / 2.)
    return symrep.base.Node(
        name, "cylinder", eval_t, {radius: "radius", height: "height"})

def box(size, name=None):
    return symrep.base.Node(
        name, "box", lambda t: max(abs(t[:3]) - size(t) / 2.),
        {size: "size"})

def sample_solid(root, lo, hi, eval_pt, max_points=None, max_sec=None):
    if max_points is None and max_sec is None:
        raise ValueError(
            "either a deadline or a number of points must be given")
    found = 0
    tried = 0
    t = np.ones(4)
    start = time.time()
    while max_points is None or found < max_points:
        t[0] = random.uniform(lo[0], hi[0])
        t[1] = random.uniform(lo[1], hi[1])
        t[2] = random.uniform(lo[2], hi[2])
        if eval_pt(root, t):
            yield np.array(t)
            found += 1
        tried += 1
        if tried % 1000 == 0:
            elapsed = time.time() - start
            if elapsed > max_sec:
                break
    print("tried {} points to find {}".format(tried, found))
    print("estimated scene density: {}".format(found / tried))

def is_inside(root, t):
    return root(t) <= 0

def is_on_surface(accuracy):
    def eval_t(root, t):
        val = root(t)
        return val <= 0 and abs(val) <= accuracy
    return eval_t

class VoxelMap(object):
    def __init__(self, voxels, lo, hi, resolution):
        self.voxels = voxels
        self.lo = lo
        self.hi = hi
        self.resolution = resolution

def voxelize(points, lo=None, hi=None, resolution=None, voxel_map=None):
    if voxel_map is None:
        size = (hi - lo)[:3]
        px_size = np.ceil(size / resolution).astype(np.int)
        print("allocating voxel array of size {}".format(
            "x".join(map(str, px_size))))
        print("    scene size is {:.3f}x{:.3f}x{:.3f}".format(*size))
        print("    using {:.3f} megabytes".format(np.product(px_size) * 1e-6))
        voxel_map = VoxelMap(
            np.zeros(px_size, dtype=np.uint8), lo, hi, resolution)
    else:
        voxel_map.voxels.fill(0)
    for p in points:
        idx = ((p[:3] - lo) / resolution).astype(np.int)
        voxel_map.voxels[tuple(idx)] = 1
    return voxel_map

def write_point_cloud(points, f):
    for point in points:
        f.write("{} {} {}\n".format(*(point[:3])))

