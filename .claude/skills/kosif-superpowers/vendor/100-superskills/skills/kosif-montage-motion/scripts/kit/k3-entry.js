/* esbuild entry for three-kit.bundle.js: the kit (and three.js) as one classic script on window.K3.
   Rebuild:  python kmotion.py kit-bundle   (needs `npm install three@0.186.1 esbuild` somewhere on NODE_PATH or in scripts/) */
import * as K3 from "./three-kit.js";
window.K3 = K3;
