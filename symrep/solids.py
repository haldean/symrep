import numpy as np
import random
import symrep.base


def transform(n, T, name=None, nodetype="transform"):
    return symrep.base.Node(
        name, nodetype, lambda t: n(T(t).dot(t)), {n: "value", T: "transform"})

def translate(n, trans, name=None):
    def getT(t):
        T = np.eye(4)
        T[:3, 3] = -trans(t)
        return T
    return transform(n, getT, name=name, nodetype="translate")

def sphere(radius, name=None):
    return symrep.base.Node(
        name, "sphere",
        lambda t: np.linalg.norm(t[:3]) - radius(t), {radius: "radius"})

def union(*nodes):
    return symrep.base.Node(
        None, "union", lambda t: min(map(lambda n: n(t), nodes)),
        {n: "value" for n in nodes})

def intersection(*nodes):
    return symrep.base.Node(
        None, "intersection", lambda t: max(map(lambda n: n(t), nodes)),
        {n: "value" for n in nodes})

def to_pointcloud(root, hi, lo, num_points):
    found = 0
    tried = 0
    t = np.ones(4)
    while found < num_points:
        t[0] = random.uniform(lo[0], hi[0])
        t[1] = random.uniform(lo[1], hi[1])
        t[2] = random.uniform(lo[2], hi[2])
        if root(t) < 0:
            yield t
            found += 1
        tried += 1
    print("tried {} points to find {}".format(tried, num_points))

def write_pointcloud(root, hi, lo, num_points, f):
    num_written = 0
    for point in to_pointcloud(root, hi, lo, num_points):
        f.write("{} {} {}\n".format(*(point[:3])))
