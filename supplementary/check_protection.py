"""Check the proposed budget map and its conditional fluid equilibrium.

Run from any directory with NumPy/SciPy installed. This is an algebra/finite-
difference audit, not an ns-3 experiment or a packet-level performance test.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

def budget(w,a,wmin,s):return a*wmin*s*(np.asarray(w)/wmin)**s

def step(s,R,T0,beta,gamma,eta):
 s=np.asarray(s);z=np.maximum(0,np.asarray(R)/T0-1)
 G=(gamma-T0)/T0;delta=(gamma-beta)/T0
 p=np.minimum(1,s*G/(z+delta*s))
 return s**(1-eta)*p**eta

def equilibrium(w,a,C,T0,beta,gamma,wmin):
 w=np.asarray(w);nom=T0+a*w.sum()/C
 if nom<=beta:s=1.
 else:
  s=brentq(lambda q:budget(w,a,wmin,q).sum()/C+(gamma-beta)*q-(gamma-T0),
           1e-15,1,xtol=1e-14)
 q=budget(w,a,wmin,s);R=T0+q.sum()/C;x=C*q/q.sum()
 return s,R,x,nom

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args();rng=np.random.default_rng(20261029)
 max_root=max_J=max_ev=0.;normal=overload=0
 T0,beta,gamma=16.8,80.,160.
 for _ in range(1000):
  n=int(rng.integers(2,15));wmin=10**rng.uniform(-2,0)
  U=10**rng.uniform(0,2);w=wmin*np.exp(rng.uniform(0,np.log(U),n))
  a,C=10**rng.uniform(2,5),10**rng.uniform(2,5)
  eta=min(.5,1/(1+math.log(U)))
  s,R,x,nom=equilibrium(w,a,C,T0,beta,gamma,wmin)
  assert np.allclose(budget(w,a,wmin,1),a*w)
  ss=np.linspace(.001,1,201)[:,None]
  assert np.all(np.diff(budget(w,a,wmin,ss),axis=0)>0)
  c=7.3
  assert np.allclose(budget(w*c,a/c,wmin*c,s),budget(w,a,wmin,s))
  trial=rng.uniform(.001,.999,n)
  assert np.all(step(trial,beta,T0,beta,gamma,eta)>trial)
  assert np.all(step(trial,gamma,T0,beta,gamma,eta)<trial)
  assert np.all(x/(C/n)>=(max(w)/min(w))**(-s)-1e-10)
  if s==1:
   normal+=1;assert R<=beta+1e-10
   assert np.allclose(step(np.ones(n),R,T0,beta,gamma,eta),1)
   continue
  overload+=1;assert beta<R<gamma
  max_root=max(max_root,abs(R-(gamma-(gamma-beta)*s)))
  assert np.allclose(step(np.full(n,s),R,T0,beta,gamma,eta),s)
  u=w/wmin;v=a*wmin/(C*T0);G=(gamma-T0)/T0;delta=(gamma-beta)/T0
  r=s*u**s*(1+s*np.log(u))
  J=(1-eta*delta*s/G)*np.eye(n)-eta*v/G*np.outer(np.ones(n),r)
  def mapping(y):
   si=np.exp(y);Ri=T0+float(budget(w,a,wmin,si).sum())/C
   return np.log(step(si,Ri,T0,beta,gamma,eta))
  yy=np.full(n,math.log(s));eps=1e-5;I=np.eye(n)
  num=np.column_stack([(mapping(yy+eps*I[j])-mapping(yy-eps*I[j]))/(2*eps) for j in range(n)])
  err=float(abs(J-num).max());max_J=max(max_J,err);assert err<1e-7
  ev=np.linalg.eigvals(J);max_ev=max(max_ev,float(max(abs(ev))))
  assert min(ev.real)>-1e-9 and max(abs(ev))<1
 examples=[];prevR=-1;prevs=2
 for n in [16,32,64,128,256,512,1024,4096]:
  w=np.tile([.5,.5,1.,2.],n//4);a=16000.;C=12000.
  s,R,x,nom=equilibrium(w,a,C,T0,beta,gamma,.5)
  assert R>prevR and s<=prevs
  prevR,prevs=R,s
  examples.append(dict(N=n,total_weight=float(w.sum()),scale=s,
       nominal_mean_RTT_us=nom,protected_mean_RTT_us=R,
       high_low_rate_ratio=float(max(x)/min(x)),min_rate_over_equal_share=float(min(x)/(C/n)),
       total_budget_payload_B=float(budget(w,a,.5,s).sum())))
 recovery=np.full(1,.05)
 for k in range(100):recovery=step(recovery,60,T0,beta,gamma,.4)
 assert recovery[0]>1-1e-10
 result=dict(all_pass=True,kind='analytic fluid-model audit',new_ns3_runs=0,random_seed=20261029,
   random_cases=1000,normal_cases=normal,protected_cases=overload,
   checked_properties=['nominal budget','budget monotonicity','weight unit invariance',
    'reduction at gamma','restoration below beta','relative service bound',
    'protected fixed point','finite-difference vector Jacobian','local Schur stability',
    'monotone delay for fixed-mix replication'],
   max_equilibrium_residual_us=max_root,max_Jacobian_error=max_J,
   max_quasistatic_eigenvalue=max_ev,
   example_parameters=dict(T0_us=T0,beta_us=beta,gamma_us=gamma,
      payload_capacity_B_per_us=12000,a_payload_B=16000,weight_pattern=[.5,.5,1,2]),
   examples=examples)
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['all_pass','random_cases','normal_cases','protected_cases',
       'max_equilibrium_residual_us','max_Jacobian_error','new_ns3_runs']},indent=2))

if __name__=='__main__':main()
