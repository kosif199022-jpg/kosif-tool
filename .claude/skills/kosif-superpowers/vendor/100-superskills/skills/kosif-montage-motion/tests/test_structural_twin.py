"""Physics-correctness checks for a tiny determinate axial truss, plus trust gates."""
import copy
import math
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import structural_twin as st
import twin_dashboard
import kmotion
import proplan

class StructuralTwinTests(unittest.TestCase):
    def setUp(self): self.m=st.sample()

    def test_commands(self):
        self.assertIn('structural',kmotion.C)
        self.assertIn('twinview',kmotion.C)

    def test_reactions_are_balanced(self):
        r=st.analyse(self.m)
        self.assertAlmostEqual(r['reactions_n']['A.y']+r['reactions_n']['C.y'],12000,places=6)
        self.assertAlmostEqual(r['reactions_n']['A.y'],6000,places=6)
        self.assertAlmostEqual(r['reactions_n']['C.y'],6000,places=6)
        self.assertAlmostEqual(r['reactions_n']['A.x'],0,places=6)

    def test_member_forces_match_hand_calculation(self):
        r=st.analyse(self.m)
        v={m['id']:m['axial_n'] for m in r['members']}
        self.assertAlmostEqual(v['AB'],-12000/math.sqrt(2),places=5)
        self.assertAlmostEqual(v['BC'],-12000/math.sqrt(2),places=5)
        self.assertAlmostEqual(v['AC'],6000,places=5)

    def test_scaling_changes_stress_not_failure_load_factor_definition(self):
        a=st.analyse(self.m,1)
        b=st.analyse(self.m,2)
        self.assertAlmostEqual(a['first_failure_multiplier'],2*b['first_failure_multiplier'],places=6)
        self.assertAlmostEqual(a['members'][0]['axial_n']*2,b['members'][0]['axial_n'],places=5)

    def test_swap_cannot_hide_next_bottleneck(self):
        res=st.compare_swap(self.m,'AB',{'area_m2':0.0002})
        self.assertAlmostEqual(res['first_failure_multiplier_delta'],0,places=7)
        self.assertEqual(res['after']['ranked_failure_modes'][0]['id'],'BC')
        self.assertEqual(st.analyse(self.m)['ranked_failure_modes'][0]['id'],'AB')

    def test_break_path_reports_instability(self):
        r=st.failure_path(self.m,3.2)
        self.assertEqual(r['steps'][0]['status'],'idealized_member_removed')
        self.assertEqual(r['steps'][-1]['status'],'unstable_after_removal')

    def test_singular_supports_fail_closed(self):
        m=copy.deepcopy(self.m);m['supports']={}
        with self.assertRaisesRegex(st.StructuralError,'Unstable'):
            st.analyse(m)

    def test_invalid_geometry_and_nan(self):
        m=copy.deepcopy(self.m);m['nodes']['B']=[0,0]
        with self.assertRaisesRegex(st.StructuralError,'Zero-length'):
            st.analyse(m)
        m=copy.deepcopy(self.m);m['loads'][0]['fy_n']=float('nan')
        with self.assertRaisesRegex(st.StructuralError,'finite'):
            st.analyse(m)

    def test_swap_parameter_restricted(self):
        with self.assertRaises(st.StructuralError):
            st.compare_swap(self.m,'AB',{'new_script':'malware'})
        with self.assertRaises(st.StructuralError):
            st.compare_swap(self.m,'AB',{'area_m2':-1})

    def test_malformed_report_blocked(self):
        with self.assertRaises(ValueError):twin_dashboard.build({'schema':'unknown'})

    def test_dashboard_self_contained_no_remote_dependencies(self):
        r=st.report(self.m,'AB',{'area_m2':0.0002})
        html=twin_dashboard.build(r)
        self.assertIn('SHAPE · JOINT · LOAD · BREAK · SWAP · RANK',html)
        self.assertIn('__EMBEDDED_BASE64__',twin_dashboard.HTML)
        self.assertNotIn('__EMBEDDED_BASE64__',html)
        self.assertNotIn('src="http',html)

    def test_router_phys_sim_vs_animation(self):
        p=proplan.plan('اختبر الوصلات والأحمال ونقاط الانهيار وقارن تبديل جزء في مجسم 3d')
        self.assertEqual(p['intent'],'structural_twin')
        self.assertIn('structural',p['available_commands'])
        self.assertIn('twinview',p['available_commands'])
        self.assertEqual([x['beat'] for x in p['timeline']['shots']], ['shape','joint','load','break','swap','rank'])
        self.assertEqual(p['full_pro_status'],'NOT_FULL_PRO')
        self.assertEqual(proplan.plan('اصنع أنيميشن تنين 3D')['intent'],'3d_motion')
        self.assertEqual(proplan.plan('برومبت صورة محاكاة فيزياء')['intent'],'prompt')

if __name__=='__main__':unittest.main()
