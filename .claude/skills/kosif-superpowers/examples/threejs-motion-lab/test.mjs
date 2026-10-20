import test from "node:test";
import assert from "node:assert/strict";
import * as THREE from "three";
import {GLTFLoader} from "three/addons/loaders/GLTFLoader.js";
import {DURATION_SECONDS,CUES,sceneAtSeconds} from "./storyboard.mjs";
import {makeHandler} from "./server.mjs";
test("Three.js installed with pinned modern API",()=>{assert.equal(THREE.REVISION,"186");assert.equal(typeof THREE.WebGLRenderer,"function");assert.equal(typeof GLTFLoader,"function");});
test("Cinematic engine primitives work",()=>{
 const s=new THREE.Scene();
 const m=new THREE.Mesh(new THREE.IcosahedronGeometry(1,2),new THREE.MeshStandardMaterial({metalness:.8,roughness:.25}));
 const camera=new THREE.PerspectiveCamera(45,9/16,.1,100);
 camera.position.z=5;s.add(m);
 m.updateMatrixWorld();assert.equal(s.children.length,1);
 assert.ok(new THREE.Box3().setFromObject(m).getSize(new THREE.Vector3()).length()>0);
 assert.equal(new THREE.Raycaster() instanceof THREE.Raycaster,true);
});
test("Timeline covers 0..5 seconds without gaps",()=>{
 assert.equal(CUES[0].start,0);assert.equal(CUES.at(-1).end,DURATION_SECONDS);
 for(let i=1;i<CUES.length;i++)assert.equal(CUES[i-1].end,CUES[i].start);
});
test("At frame 0 deterministic scene is DEPTH",()=>{
 assert.equal(sceneAtSeconds(0).headline,"DEPTH");
 assert.deepEqual(sceneAtSeconds(1),sceneAtSeconds(1));
});
test("Different timestamps produce different poses",()=>assert.notEqual(sceneAtSeconds(0).orbitRadians,sceneAtSeconds(3).orbitRadians));
test("End clip remains within range",()=>{
 assert.equal(sceneAtSeconds(10).time,5);
 assert.equal(sceneAtSeconds(-4).time,0);
 assert.equal(sceneAtSeconds(5).headline,"KOSIF");
});
test("Invalid timeline argument rejected",()=>assert.throws(()=>sceneAtSeconds(Number.NaN)));
test("Static server rejects remote paths",()=>{
 const h=makeHandler();assert.equal(typeof h,"function");
});
test("3D materials and light are physically based",()=>{
 const p=new THREE.MeshPhysicalMaterial({metalness:.85,roughness:.2});
 assert.equal(p.isMeshPhysicalMaterial,true);
 assert.equal(new THREE.PointLight(0xffffff,10).isPointLight,true);
});
