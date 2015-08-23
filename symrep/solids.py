import numpy as np
import random
import symrep.base


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

def sample_solid(root, lo, hi, num_points, eval_pt):
    found = 0
    tried = 0
    t = np.ones(4)
    while found < num_points:
        t[0] = random.uniform(lo[0], hi[0])
        t[1] = random.uniform(lo[1], hi[1])
        t[2] = random.uniform(lo[2], hi[2])
        if eval_pt(root, t):
            yield t
            found += 1
        tried += 1
    print("tried {} points to find {}".format(tried, num_points))

def is_inside(root, t):
    return root(t) <= 0

def is_on_surface(root, t, accuracy):
    val = root(t)
    return val <= 0 and abs(val) <= accuracy

def write_point_cloud(points, f):
    for point in points:
        f.write("{} {} {}\n".format(*(point[:3])))
