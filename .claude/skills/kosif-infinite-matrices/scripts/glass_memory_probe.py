#!/usr/bin/env python3
"""Numerical A/B causal probe: light history steers particles, without any renderer."""
import argparse,math,json
def simulate(coupled,steps=56):
    mem=[0.0]*28
    p=[3.5,7.5,11.5,17.5,23.5]
    speed=[.11,-.06,.08,-.09,-.10]
    for t in range(steps):
        center=10+3.2*math.sin(t/4.0)
        mem=[min(9.,.966*v+(0.46*math.exp(-((j-center)/4.5)**2) if t<16 else 0.)) for j,v in enumerate(mem)]
        new=[]
        for i,y in enumerate(p):
            j=max(1,min(26,round(y)))
            slope=(mem[j+1]-mem[j-1])*.5
            new.append(max(1.,min(26.,y+speed[i]+(.060*slope if coupled else 0.))))
        p=new
    return p,sum(mem)
def probe():
    control,mc=simulate(False);trial,mt=simulate(True)
    d=sum(abs(a-b) for a,b in zip(control,trial))/len(control)
    return {"kind":"NUMERIC_COUNTERFACTUAL_NOT_VISUAL_RENDER","light_off_step":16,
            "same_initial_values":True,"mean_absolute_position_difference":round(d,7),
            "same_material_memory":abs(mc-mt)<1e-10,"causal_difference_detected":d>.001}
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--json",action="store_true");args=ap.parse_args()
    r=probe()
    print(json.dumps(r,indent=2) if args.json else str(r))
    raise SystemExit(0 if r["causal_difference_detected"] else 1)
