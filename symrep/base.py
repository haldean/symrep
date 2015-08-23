from __future__ import division

import functools
import numpy as np
import operator
import random


def const(val):
    return Node(str(val), "const", lambda _: val, {})

def sum(*nodes):
    return Node(
        None, "sum",
        lambda t: functools.reduce(operator.add, (n(t) for n in nodes), 0),
        {n: "value" for n in nodes})

def product(*nodes):
    return Node(
        None, "product",
        lambda t: functools.reduce(operator.mul, (n(t) for n in nodes), 1),
        {n: "value" for n in nodes})

def piecewise(pre, post, split, name=None):
    return Node(
        name, "piecewise",
        lambda t: pre(t) if t < split(t) else post(t - split(t)),
        {pre: "pre", post: "post", split: "split"})

def shift(n, shift, name=None):
    return Node(
        name, "shift", lambda t: n(t + shift(t)), {n: "value", shift: "shift"})

class Node(object):
    _next_id = 0

    def __init__(self, name, nodetype, func, deps):
        self.id = Node._next_id
        Node._next_id += 1

        self.name = name
        self.nodetype = nodetype
        self.func = func
        self.deps = deps

    def __call__(self, t):
        return self.func(t)

def sample(root, min_t, max_t, delta_t):
    t = min_t
    while t < max_t:
        yield t, root(t)
        t += delta_t

def collect_nodes(root):
    return set([root]).union(
        functools.reduce(
            set.union, map(collect_nodes, root.deps.keys()), set()))

def collect_edges(root):
    edges = [(root.id, dep.id, dep_type)
             for dep, dep_type in root.deps.items()]
    for dep in root.deps.keys():
        edges.extend(collect_edges(dep))
    return edges

def to_dot(root, stream, name="symrep"):
    stream.write("digraph {name} {{\n".format(name=name))
    stream.write("graph [rankdir=LR];\n")
    stream.write("node [fontsize=8,fontname=monospace,shape=box];\n")
    stream.write("edge [fontsize=8,fontname=monospace];\n")
    for node in collect_nodes(root):
        if node.name is not None:
            label = "{node.name}\\n{node.nodetype}".format(node=node)
        else:
            label = "id={node.id}\\n{node.nodetype}".format(node=node)
        stream.write("{id} [label=\"{label}\"];\n".format(
            id=node.id, label=label))
    for n1, n2, label in collect_edges(root):
        stream.write("{n2} -> {n1} [label=\"{label}\"];\n".format(
            n1=n1, n2=n2, label=label))
    stream.write("}\n")

def dump_samples(root, min_t, max_t, delta_t, f):
    nodes = list(collect_nodes(root))
    nodes.sort(key=lambda n: n.id)
    f.write("t," + ",".join(str(n.id) for n in nodes) + "\n")
    t = min_t
    while t < max_t:
        f.write("{},".format(t))
        f.write(",".join(repr(n(t)) for n in nodes))
        f.write("\n")
        t += delta_t
