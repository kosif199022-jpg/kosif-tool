"""Independent geometry extension tests: mesh topology, pixels and object depth."""
import copy
from pathlib import Path
import sys
import unittest

SK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SK/"scripts"))
import native_3d as n


class NewPrimitiveTests(unittest.TestCase):
    def test_closed_cone_non_degenerate(self):
        verts,faces=n.cone()
        self.assertEqual(len(verts),18)
        self.assertEqual(len(faces),32)
        for a,b,c in faces:
            normal=n.cross(n.sub(verts[b],verts[a]),n.sub(verts[c],verts[a]))
            self.assertGreater(sum(x*x for x in normal),1e-8)

    def test_torus_manifold_closed_no_degenerate_triangles(self):
        verts,faces=n.torus()
        self.assertEqual((len(verts),len(faces)),(200,400))
        edges={}
        for a,b,c in faces:
            normal=n.cross(n.sub(verts[b],verts[a]),n.sub(verts[c],verts[a]))
            self.assertGreater(sum(x*x for x in normal),1e-10)
            for x,y in ((a,b),(b,c),(c,a)):
                pair=tuple(sorted((x,y)))
                edges[pair]=edges.get(pair,0)+1
        self.assertTrue(all(count==2 for count in edges.values()))
        self.assertGreater(len(edges),200)

    def test_independent_zbuffer_images_have_real_geometry(self):
        for shape in ("cone","torus"):
            with self.subTest(shape=shape):
                scene={"schema":n.SCHEMA,"width":160,"height":160,
                       "render_mode":"zbuffer","background":"#112233",
                       "camera":{"position":[4,-6,4],"target":[0,0,0],
                                 "ortho_scale":3},
                       "objects":[{"shape":shape,"color":"#D68C49",
                                   "scale":[2,2,2]}]}
                n.validate(scene)
                image=n.render(scene,1)
                self.assertGreater(len(image.getcolors(160*160)),3)

    def test_animated_torus_has_changed_pixels(self):
        from PIL import ImageChops
        scene={"schema":n.SCHEMA,"width":128,"height":128,
               "frames":20,"fps":10,"render_mode":"zbuffer",
               "objects":[{"shape":"torus","color":"#D68C49",
                           "keyframes":[{"frame":20,"location":[1,0,0]}]}]}
        a=n.render(scene,1)
        b=n.render(scene,20)
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())

    def test_invalid_shape_rejected(self):
        with self.assertRaises(ValueError):
            n.validate({"schema":n.SCHEMA,"objects":[{"shape":"__import__('os')"}]})


if __name__=="__main__":
    unittest.main()
