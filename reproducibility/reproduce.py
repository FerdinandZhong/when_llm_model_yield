"""Reproduce main rates and common-cohort paired contrasts from coded outcomes.

Run: python reproduce.py
Requires NumPy only. No network, API calls, or original research repository.
Inputs preserve assigned clusters and invalid outcomes. Codes are -1 invalid,
0 retained initial option, 1 adopted target, 2 other revision. They do not
authenticate original parsing, initial eligibility, or survey provenance.
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np

HERE = Path(__file__).resolve().parent
SEED = 20260926
BOOTSTRAP = 2000

def specs():
    return {
        'generic_minus_bare_no_authority': {'merit':1,'bare':-1},
        'generic_minus_bare_with_authority': {'merit_authority':1,'authority':-1},
        'formal_minus_bare_no_authority': {'formal':1,'bare':-1},
        'formal_minus_bare_with_authority': {'formal_authority':1,'authority':-1},
        'authority_with_bare': {'authority':1,'bare':-1},
        'authority_with_generic': {'merit_authority':1,'merit':-1},
        'authority_with_formal': {'formal_authority':1,'formal':-1},
        'generic_authority_interaction': {'merit_authority':1,'authority':-1,'merit':-1,'bare':1},
        'formal_authority_interaction': {'formal_authority':1,'authority':-1,'formal':-1,'bare':1},
        'bare_minus_neutral': {'bare':1,'neutral':-1},
        'verified_minus_generic_no_authority': {'verified':1,'merit':-1},
        'verified_minus_generic_with_authority': {'verified_authority':1,'merit_authority':-1},
        'authority_with_verified': {'verified_authority':1,'verified':-1},
        'verified_generic_authority_interaction': {'verified_authority':1,'merit_authority':-1,'verified':-1,'merit':1},
    }

def main():
    meta=json.loads((HERE/'analysis_inputs.json').read_text())
    path=HERE/'analysis_inputs.npz'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['npz_sha256']
    data=np.load(path,allow_pickle=False)
    rates=list(csv.DictReader((HERE/'standardized_rates.csv').open()))
    contrasts=list(csv.DictReader((HERE/'within_model_contrasts.csv').open()))
    results=[]
    for g in meta['groups']:
        idx=g['array_index'];codes=data[f'outcomes_{idx}'];clusters=data[f'clusters_{idx}']
        conditions=g['conditions'];indices={c:i for i,c in enumerate(conditions)}
        mask=(codes>=0).all(axis=1);n=int(mask.sum());k=int(clusters.max())+1
        assert k==g['assigned_clusters'] and len(codes)==g['assigned_histories']
        counts=np.bincount(clusters,weights=mask.astype(float),minlength=k)
        rng=np.random.default_rng(SEED)
        draws=np.concatenate([rng.integers(0,k,size=(min(64,BOOTSTRAP-start),k)) for start in range(0,BOOTSTRAP,64)])
        denominator=counts[draws].sum(axis=1)
        def interval(values):
            sums=np.bincount(clusters,weights=np.where(mask,values,0),minlength=k)
            num=sums[draws].sum(axis=1)
            return np.quantile(num[denominator>0]/denominator[denominator>0],[.025,.975])*100
        def matches(r):return all(r[c]==g[c] for c in ('model','domain','setting'))
        for r in filter(matches,rates):
            values=(codes[:,indices[r['condition']]]==1).astype(float)
            assert n==int(r['n']) and int(values[mask].sum())==int(r['target'])
            lo,hi=interval(values);point=float(values[mask].mean()*100)
            assert np.allclose([point,lo,hi],[float(r[c]) for c in ('target_percent','ci_low','ci_high')],atol=1e-8,rtol=0),r
            results.append(dict(model=g['model'],domain=g['domain'],setting=g['setting'],statistic=r['condition'],endpoint='target',n=n,estimate=point,ci_low=float(lo),ci_high=float(hi)))
        for r in filter(matches,contrasts):
            if r['cohort']!='common_all_conditions_valid':continue
            weights=specs()[r['contrast']]
            values=sum(w*((codes[:,indices[c]]==1) if r['endpoint']=='target' else (codes[:,indices[c]]>0)).astype(float) for c,w in weights.items())
            lo,hi=interval(values);point=float(values[mask].mean()*100)
            assert n==int(r['n'])
            assert np.allclose([point,lo,hi],[float(r[c]) for c in ('difference_pp','ci_low','ci_high')],atol=1e-8,rtol=0),r
            results.append(dict(model=g['model'],domain=g['domain'],setting=g['setting'],statistic=r['contrast'],endpoint=r['endpoint'],n=n,estimate=point,ci_low=float(lo),ci_high=float(hi)))
        print(g['model'],g['domain'],g['setting'],'verified',flush=True)
    with (HERE/'reproduced_results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    report={'numpy_version':np.__version__,'seed':SEED,'resamples':BOOTSTRAP,'main_rate_cells':len(rates),'common_cohort_contrasts':len(results)-len(rates),'all_estimates_and_intervals_match':True,'tolerance':1e-8,'inference_calls':0}
    (HERE/'reproduction_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
