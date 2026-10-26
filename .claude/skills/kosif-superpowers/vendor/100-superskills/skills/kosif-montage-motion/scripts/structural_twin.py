"""KOSIF Structural Twin v0.2 — illustrative, deterministic 2D (plane) and 3D (space) pin-jointed truss analysis.

NOT a certified finite-element solver. Rigid connections, bending, shear, torsion, buckling,
contact, dynamics, plasticity, and material nonlinearities are out of scope.
NumPy is used when present (pure-Python fallback otherwise). No network and no side effects beyond requested output files.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

SCHEMA = 'kosif.structural-twin.v0.1'
# 2D models keep the original limits; 3D space trusses (v0.2 of the solver) may be larger and use NumPy when present
MAX_NODES, MAX_ELEMENTS = 400, 1600
AXES = ('x', 'y', 'z')
FORCE_KEYS = ('fx_n', 'fy_n', 'fz_n')


class StructuralError(ValueError):
    pass


def number(v, name, positive=False):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise StructuralError(f'{name} must be a finite number')
    if positive and v <= 0:
        raise StructuralError(f'{name} must be positive')
    if abs(v) > 1e16:
        raise StructuralError(f'{name} exceeds safety bound')
    return float(v)


def dimension(model):
    """2 for [x, y] nodes (plane truss), 3 for [x, y, z] nodes (space truss); every node must agree."""
    sizes = {len(xy) for xy in model['nodes'].values() if isinstance(xy, (list, tuple))}
    if len(sizes) != 1 or next(iter(sizes)) not in (2, 3):
        raise StructuralError('Every node must have the same [x_m,y_m] or [x_m,y_m,z_m] coordinates')
    return next(iter(sizes))


def validate(model):
    if not isinstance(model, dict):
        raise StructuralError('Model must be a JSON object')
    nodes = model.get('nodes')
    elements = model.get('elements')
    supports = model.get('supports', {})
    loads = model.get('loads', [])
    if not isinstance(nodes, dict) or not (2 <= len(nodes) <= MAX_NODES):
        raise StructuralError(f'nodes must contain 2..{MAX_NODES} entries')
    if not isinstance(elements, list) or not (1 <= len(elements) <= MAX_ELEMENTS):
        raise StructuralError(f'elements must contain 1..{MAX_ELEMENTS} entries')
    if not isinstance(supports, dict) or not isinstance(loads, list):
        raise StructuralError('supports must be an object and loads an array')
    for k, xy in nodes.items():
        if not isinstance(k, str) or not k or not isinstance(xy, (list, tuple)) or len(xy) not in (2, 3):
            raise StructuralError('Each node must have an id and [x_m,y_m] or [x_m,y_m,z_m]')
        for c, axis in zip(xy, AXES):
            number(c, f'node {axis}')
    dim = dimension(model)
    for k, axes in supports.items():
        if k not in nodes or not isinstance(axes, list) or not axes or len(set(axes)) != len(axes) or any(a not in AXES[:dim] for a in axes):
            raise StructuralError(f'Support axes must be {"/".join(AXES[:dim])} at a known node')
    names=set()
    for e in elements:
        if not isinstance(e, dict) or not isinstance(e.get('id'),str) or not e['id'] or e['id'] in names:
            raise StructuralError('Element ids must be unique strings')
        names.add(e['id'])
        a,b=e.get('a'),e.get('b')
        if a not in nodes or b not in nodes or a == b:
            raise StructuralError('Element endpoints must be two different known nodes')
        if math.dist(nodes[a],nodes[b]) < 1e-8:
            raise StructuralError('Zero-length member')
        for key in ('area_m2','young_pa','strength_pa'):
            number(e.get(key), f'{e["id"]}.{key}', positive=True)
    if len(loads)>MAX_NODES*3:
        raise StructuralError('Too many loads')
    for l in loads:
        if not isinstance(l,dict) or l.get('node') not in nodes:
            raise StructuralError('Each load needs known node')
        for key in FORCE_KEYS:
            number(l.get(key,0),key)
        if dim == 2 and l.get('fz_n', 0):
            raise StructuralError('fz_n needs a 3D model ([x,y,z] nodes)')
    return model


def solve_linear(matrix, rhs):
    """Partial pivot Gaussian elimination; detect kinematic singularities."""
    n=len(rhs)
    a=[list(map(float,matrix[i]))+[float(rhs[i])] for i in range(n)]
    ref=max((abs(v) for row in matrix for v in row),default=1.0)
    if ref == 0: raise StructuralError('Unstable structure: no stiffness')
    for k in range(n):
        i=max(range(k,n), key=lambda r:abs(a[r][k]))
        if abs(a[i][k]) <= ref*1e-12:
            raise StructuralError('Unstable or ill-conditioned truss: insufficient supports/members')
        if i!=k: a[k],a[i]=a[i],a[k]
        for j in range(k+1,n):
            mult=a[j][k]/a[k][k]
            if mult == 0.0: continue
            for m in range(k+1,n+1): a[j][m]-=mult*a[k][m]
            a[j][k]=0
    x=[0.0]*n
    for i in range(n-1,-1,-1):
        x[i]=(a[i][n]-sum(a[i][j]*x[j] for j in range(i+1,n)))/a[i][i]
    return x


def _solve(matrix, rhs):
    """NumPy LU when available (a 3D bunny truss has ~100 DOF: milliseconds instead of seconds); the pure-Python
    eliminator otherwise. Both fail closed on a mechanism (singular stiffness)."""
    try:
        import numpy as np
    except ImportError:
        return solve_linear(matrix, rhs)
    K = np.asarray(matrix, dtype=float)
    if not K.size or not np.abs(K).max():
        raise StructuralError('Unstable structure: no stiffness')
    w = np.linalg.eigvalsh(K)                                # K is symmetric positive semi-definite
    if w[0] <= w[-1] * 1e-12:
        raise StructuralError('Unstable or ill-conditioned truss: insufficient supports/members')
    return np.linalg.solve(K, np.asarray(rhs, dtype=float)).tolist()


def analyse(model, scale=1.0, remove=()):
    validate(model);scale=number(scale,'load_scale', positive=True)
    dim=dimension(model); axes=AXES[:dim]
    ids=list(model['nodes']); index={nid:i for i,nid in enumerate(ids)}; n=len(ids)*dim
    k=[[0.0]*n for _ in range(n)]; f=[0.0]*n; terms={}
    for e in model['elements']:
        if e['id'] in remove:continue
        a,b=e['a'],e['b']; pa=model['nodes'][a]; pb=model['nodes'][b]
        L=math.dist(pa,pb); cos=[(pb[j]-pa[j])/L for j in range(dim)]
        dofs=[index[a]*dim+j for j in range(dim)]+[index[b]*dim+j for j in range(dim)]
        v=[-c for c in cos]+cos
        stiffness=e['area_m2']*e['young_pa']/L
        for u in range(2*dim):
            for w in range(2*dim): k[dofs[u]][dofs[w]]+=stiffness*v[u]*v[w]
        terms[e['id']]=(e,L,cos,dofs,stiffness)
    for l in model.get('loads',[]):
        offset=dim*index[l['node']]
        for j,key in enumerate(FORCE_KEYS[:dim]):
            f[offset+j]+=l.get(key,0)*scale
    fixed=set()
    for nid, sup in model.get('supports',{}).items():
        for j,axis in enumerate(axes):
            if axis in sup:fixed.add(dim*index[nid]+j)
    free=[i for i in range(n) if i not in fixed]
    if not free:raise StructuralError('No free degrees of freedom')
    reduced=[[k[i][j] for j in free] for i in free]
    disp=_solve(reduced,[f[i] for i in free]); u=[0.0]*n
    for i,val in zip(free,disp):u[i]=val
    members=[]
    for id,(e,L,cos,dofs,stiffness) in terms.items():
        elong=sum(cos[j]*(u[dofs[dim+j]]-u[dofs[j]]) for j in range(dim))
        axial=stiffness*elong; stress=axial/e['area_m2']; util=abs(stress)/e['strength_pa']
        load_factor=round(1/util,8) if util>1e-15 else None
        members.append({'id':id, 'a':e['a'], 'b':e['b'],'length_m':round(L,8),
                        'axial_n':round(axial,7),'stress_pa':round(stress,6),
                        'utilization':round(util,9),'failure_load_multiplier':load_factor,
                        'mode':'tension' if axial>1e-9 else ('compression' if axial < -1e-9 else 'zero'),
                        'capacity_stress_pa':e['strength_pa'], 'area_m2':e['area_m2']})
    ranking=sorted(members,key=lambda m:(float('inf') if m['failure_load_multiplier'] is None else m['failure_load_multiplier'],m['id']))
    displacements={nid:{f'{axis}_m':round(u[dim*i+j],12) for j,axis in enumerate(axes)} for nid,i in index.items()}
    reactions={}
    for nid,i in index.items():
        for j,axis in enumerate(axes):
            idx=dim*i+j
            if idx in fixed:
                v=sum(k[idx][c]*u[c] for c in range(n))-f[idx]
                reactions[f'{nid}.{axis}']=round(v,7)
    return {'schema':SCHEMA,'dimension':dim,
            'assumptions':f'{dim}D linear elastic, small-displacement, pin joints, axial stress only',
            'load_scale':scale,'displacements_m':displacements,'reactions_n':reactions,
            'members':members,'ranked_failure_modes':ranking,
            'first_failure_multiplier':ranking[0]['failure_load_multiplier'] if ranking else None,
            'failed_at_current_load':[m['id'] for m in members if m['utilization']>=1]}


def failure_path(model, load_scale=1.0, max_steps=10):
    """Hypothetical brittle member-removal sequence, not fracture propagation analysis."""
    remaining=set(e['id'] for e in model['elements']); removed=[];steps=[]
    for i in range(min(max_steps,len(remaining)+1)):
        try:
            r=analyse(model,scale=load_scale,remove=set(e['id'] for e in model['elements'])-remaining)
        except StructuralError as exc:
            steps.append({'step':i, 'status':'unstable_after_removal', 'detail':str(exc)})
            break
        failing=[m for m in r['members'] if m['utilization'] >= 1]
        if not failing:
            steps.append({'step':i,'status':'stable_under_idealized_model','remaining':len(remaining)})
            break
        worst=sorted(failing,key=lambda m:(-m['utilization'],m['id']))[0]
        remaining.remove(worst['id']);removed.append(worst['id'])
        steps.append({'step':i, 'status':'idealized_member_removed', 'element':worst['id'],
                      'utilization_before_removal':worst['utilization']})
    return {'load_scale':load_scale,'steps':steps,'removed_members':removed,
            'warning':'Removal at strength threshold is hypothetical; no buckling, fracture, fatigue or dynamic redistribution.'}


def compare_swap(model, element_id, changes):
    original=analyse(model)
    modified=copy.deepcopy(model)
    el=next((e for e in modified['elements'] if e['id']==element_id),None)
    if el is None: raise StructuralError('Unknown element to swap')
    if not isinstance(changes,dict) or not changes or any(k not in ('area_m2','young_pa','strength_pa') for k in changes):
        raise StructuralError('Swap may modify area_m2, young_pa or strength_pa only')
    for key,value in changes.items():el[key]=number(value,key,positive=True)
    after=analyse(modified)
    return {'element_id':element_id, 'changes':changes,'before':original,'after':after,
            'first_failure_multiplier_delta':None if original['first_failure_multiplier'] is None or after['first_failure_multiplier'] is None
            else round(after['first_failure_multiplier']-original['first_failure_multiplier'],8),
            'warning':'Comparisons are within the stated simplified model, not safety approval.'}


def sample():
    # Determinate three-bar truss, 2 support nodes (fixed A, vertical roller C), top B loaded.
    return {'name':'Illustrative triangular truss (not calibrated to a real object)',
            'units':{'length':'m','force':'N','stress':'Pa'},
            'nodes':{'A':[0,0],'B':[1,1],'C':[2,0]},
            'supports':{'A':['x','y'],'C':['y']},
            'elements':[
                {'id':'AB','a':'A','b':'B','area_m2':0.0001,'young_pa':2e11,'strength_pa':2.5e8},
                {'id':'BC','a':'B','b':'C','area_m2':0.0001,'young_pa':2e11,'strength_pa':2.5e8},
                {'id':'AC','a':'A','b':'C','area_m2':0.0001,'young_pa':2e11,'strength_pa':2.5e8}],
            'loads':[{'node':'B','fy_n':-12000}]}


def report(model, swap_element=None, changes=None, fracture_scale=2):
    original=analyse(model)
    result={'schema':SCHEMA,'model':model,'baseline':original,
            'hypothetical_failure_path':failure_path(model,fracture_scale),
            'source_note':'Model parameters are user-supplied or illustrative, NEVER extracted from pixels as verified geometry or material properties.',
            'scope_warning':'Illustrative engineering education ONLY; not validated for construction, medical, manufacturing or other safety decisions.'}
    if swap_element:result['swap']=compare_swap(model,swap_element,changes)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',type=Path, help='A truss model JSON. Omit only when --sample is provided.')
    ap.add_argument('--sample',action='store_true',help='Use synthetic sample; no real-object claim')
    ap.add_argument('--out',type=Path,help='Output report JSON')
    ap.add_argument('--swap',help='Member ID to replace, e.g. AB')
    ap.add_argument('--area',type=float,help='New area in square metres, requires --swap')
    ap.add_argument('--young',type=float,help='New Young modulus (Pa), requires --swap')
    ap.add_argument('--strength',type=float,help='New material strength (Pa), requires --swap')
    ap.add_argument('--fracture-scale',type=float,default=2,help='Hypothetical brittle failure load multiplier')
    args=ap.parse_args()
    if args.sample==bool(args.model):ap.error('Choose exactly one of --model or --sample')
    if args.swap is None and any(x is not None for x in (args.area,args.young,args.strength)):
        ap.error('--area/--young/--strength require --swap')
    try:
        m=sample() if args.sample else json.loads(args.model.read_text(encoding='utf8'))
        changes={name:value for name,value in (('area_m2',args.area),('young_pa',args.young),('strength_pa',args.strength)) if value is not None}
        if args.swap and not changes:ap.error('--swap requires a replacement parameter')
        out=report(m,args.swap,changes,number(args.fracture_scale,'fracture-scale',positive=True))
    except (StructuralError,ValueError) as exc:
        ap.error(str(exc))
    payload=json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(payload,encoding='utf8')
    print(payload)

if __name__=='__main__':main()
