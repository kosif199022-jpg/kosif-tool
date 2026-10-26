"""3D (space truss) checks: a symmetric tripod against the hand calculation, equilibrium, mechanisms, axis rules."""
import copy
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import structural_twin as st


def tripod(P=900.0, r=1.0, h=2.0):
    nodes = {'D': [0.0, h, 0.0]}
    for i, nid in enumerate('ABC'):
        a = 2 * math.pi * i / 3
        nodes[nid] = [r * math.cos(a), 0.0, r * math.sin(a)]
    el = lambda i: {'id': i + 'D', 'a': i, 'b': 'D', 'area_m2': 1e-4, 'young_pa': 2e11, 'strength_pa': 2.5e8}
    return {'nodes': nodes, 'supports': {n: ['x', 'y', 'z'] for n in 'ABC'},
            'elements': [el(n) for n in 'ABC'], 'loads': [{'node': 'D', 'fy_n': -P}]}


class SpaceTrussTests(unittest.TestCase):
    def test_tripod_matches_hand_calculation(self):
        P, r, h = 900.0, 1.0, 2.0
        res = st.analyse(tripod(P, r, h))
        L = math.hypot(r, h)
        self.assertEqual(res['dimension'], 3)
        for m in res['members']:
            self.assertAlmostEqual(m['axial_n'], -P * L / (3 * h), places=5)
            self.assertEqual(m['mode'], 'compression')
        self.assertAlmostEqual(sum(v for k, v in res['reactions_n'].items() if k.endswith('.y')), P, places=5)
        for axis in 'xz':
            self.assertAlmostEqual(sum(v for k, v in res['reactions_n'].items() if k.endswith('.' + axis)), 0, places=5)
        self.assertIn('z_m', res['displacements_m']['D'])

    def test_swap_and_break_work_in_3d(self):
        m = tripod()
        sw = st.compare_swap(m, 'AD', {'area_m2': 2e-4})
        self.assertGreater(sw['after']['ranked_failure_modes'][-1]['failure_load_multiplier'],
                           sw['before']['ranked_failure_modes'][-1]['failure_load_multiplier'])
        path = st.failure_path(m, 1e6)
        self.assertEqual(path['steps'][-1]['status'], 'unstable_after_removal')

    def test_planar_space_truss_is_a_mechanism(self):
        m = tripod()
        for n in 'ABCD':
            m['nodes'][n][1] = 0.0 if n != 'D' else 0.0
        m['nodes']['D'] = [0.1, 0.0, 0.1]
        with self.assertRaisesRegex(st.StructuralError, 'Unstable'):
            st.analyse(m)

    def test_mixed_dimensions_and_bad_axes_rejected(self):
        m = tripod(); m['nodes']['A'] = [1.0, 0.0]
        with self.assertRaises(st.StructuralError):
            st.analyse(m)
        m = tripod(); m['supports']['A'] = ['w']
        with self.assertRaises(st.StructuralError):
            st.analyse(m)
        m2 = st.sample(); m2['loads'][0]['fz_n'] = 10
        with self.assertRaisesRegex(st.StructuralError, 'fz_n'):
            st.analyse(m2)

    def test_pure_python_and_numpy_agree(self):
        res = st.analyse(tripod())
        K = [[4.0, 1.0], [1.0, 3.0]]
        self.assertEqual([round(v, 10) for v in st.solve_linear(K, [1, 2])], [round(v, 10) for v in st._solve(K, [1, 2])])
        self.assertTrue(res['first_failure_multiplier'] > 0)


if __name__ == '__main__':
    unittest.main()
