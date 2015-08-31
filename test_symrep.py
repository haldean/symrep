import symrep
import symrep.audio
import unittest

try:
    import numpy as np
except ImportError:
    import numpypy as np


class SymrepTest(unittest.TestCase):
    def test_const(self):
        n = symrep.const(4)
        self.assertEqual(n(0), 4)
        self.assertEqual(n(1), 4)
        self.assertEqual(n(2), 4)

    def test_sum(self):
        n1 = symrep.const(1)
        n2 = symrep.const(2)

        n = symrep.sum(n1, n2)
        self.assertEqual(n(0), 3)

        n = symrep.sum(n1, n1, n1)
        self.assertEqual(n(0), 3)

    def test_product(self):
        n = symrep.product(symrep.const(1), symrep.const(-3))
        self.assertEqual(n(0), -3)

        n1 = symrep.const(-4)
        n = symrep.product(symrep.const(-4), symrep.const(.5))
        self.assertEqual(n(0), -2)

    def test_sine(self):
        n = symrep.audio.sine(symrep.const(1))
        self.assertAlmostEqual(n(0), 0)
        self.assertAlmostEqual(n(0.25), 1)
        self.assertAlmostEqual(n(0.5), 0)
        self.assertAlmostEqual(n(0.75), -1)
        self.assertAlmostEqual(n(1), 0)

    def test_sine_modulation(self):
        n = symrep.audio.sine(
            symrep.audio.sawtooth(symrep.const(1)))
        self.assertAlmostEqual(n(0), 0)
        self.assertAlmostEqual(n(1), 0)

    def test_sawtooth(self):
        n = symrep.audio.sawtooth(symrep.const(1))
        self.assertEqual(n(0), 0)
        self.assertEqual(n(0.5), 0.5)
        self.assertAlmostEqual(n(1 - 1e-8), 1)
        self.assertEqual(n(1), 0)
        self.assertEqual(n(1.5), 0.5)

        n = symrep.audio.sawtooth(symrep.const(0.25))
        self.assertEqual(n(0), 0)
        self.assertEqual(n(2), 0.5)
        self.assertAlmostEqual(n(4 - 1e-8), 1)
        self.assertEqual(n(4), 0)
        self.assertEqual(n(6), 0.5)

    def test_collect_nodes(self):
        n1 = symrep.const(1)
        n2 = symrep.audio.sine(n1)
        n3 = symrep.sum(n1, n2)
        n4 = symrep.const(-2)
        n5 = symrep.product(n3, n4)
        nodes = symrep.collect_nodes(n5)
        self.assertEqual(len(nodes), 5)
        self.assertSetEqual(
            set(n.id for n in nodes),
            set((n1.id, n2.id, n3.id, n4.id, n5.id)))

    def test_dot(self):
        n = symrep.product(
            symrep.audio.sine(symrep.const(2)),
            symrep.product(
                symrep.audio.sine(symrep.const(3)),
                symrep.sum(
                    symrep.const(1),
                    symrep.const(1),
                )
            )
        )
        with open("test.dot", "w") as f:
            symrep.to_dot(n, f, name="test_dot")

    def test_sphere(self):
        n = symrep.solids.sphere(symrep.const(2))
        cloud = list(symrep.solids.sample_solid(
            n, -2. * np.ones(3), 2 * np.ones(3),
            symrep.solids.is_inside, 500))
        self.assertEqual(len(cloud), 500)
        for pt in cloud:
            self.assertLessEqual(np.linalg.norm(pt[:3]), 2.)

    def test_translate(self):
        n = symrep.solids.translate(
            symrep.solids.sphere(symrep.const(2)),
            symrep.const(np.array((4., 0., 0.))),
        )
        self.assertLessEqual(n((4., 0., 0.)), 0)
        self.assertLessEqual(n((4., 1.5, 0.)), 0)
        self.assertGreaterEqual(n((4., 2.5, 0.)), 0)
        self.assertGreaterEqual(n((0., 0., 0.)), 0)

if __name__ == "__main__":
    unittest.main()
