import operator


def const(val):
    return Node("const {}".format(val), lambda _: val, [])

def sum(*nodes):
    return Node(
        "sum",
        lambda t: reduce(operator.add, (n(t) for n in nodes), 0),
        nodes)

def product(*nodes):
    return Node(
        "product",
        lambda t: reduce(operator.mul, (n(t) for n in nodes), 1),
        nodes)

def piecewise(pre, post, split):
    return Node(
        "piecewise",
        lambda t: pre(t) if t < split(t) else post(t - split(t)),
        [pre, post, split])

def shift(n, shift):
    return Node("shift", lambda t: n(t + shift(t)), [n, shift])

class Node(object):
    _next_id = 0

    def __init__(self, name, func, deps):
        self.id = Node._next_id
        Node._next_id += 1

        self.name = name
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
        reduce(set.union, map(collect_nodes, root.deps), set()))

def collect_edges(root):
    edges = [(root.id, dep.id) for dep in root.deps]
    for dep in root.deps:
        edges.extend(collect_edges(dep))
    return edges

def to_dot(root, stream, name="symrep"):
    stream.write("digraph {name} {{\n".format(name=name))
    for node in collect_nodes(root):
        stream.write("{id} [label=\"{name}\\n{id}\"];\n".format(
            id=node.id, name=node.name))
    for n1, n2 in collect_edges(root):
        stream.write("{n2} -> {n1};\n".format(n1=n1, n2=n2))
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
