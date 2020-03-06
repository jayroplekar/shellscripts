#from math import exp
import math, random
import string, os, traceback,sys
from scipy import stats

def process(nominal_load,load_stddev,alpha,beta,reduction,factor,guess):
  residual1=0.0
  residual0=1.0
  guess0=0.0
  guess1=guess
  new_load_mean=(1-.01*reduction)*nominal_load
  new_load_std_dev= (1-.01*reduction*factor)*load_stddev
  for i in range(0,100):
#    print "i=",i
    if ( (abs(residual0) < 1e-5) and (abs(residual1) < 1e-5) ):
      break
    residual0=residual1
    Z_val = stats.norm.ppf(1.0-.01*guess1)
    load_at_guess=new_load_mean+Z_val*new_load_std_dev
    strength_at_guess=alpha*(-math.log(1.0-.01*guess1))**(1.0/beta)
    residual1=load_at_guess-strength_at_guess
    tmp=guess1
    if ( residual1*residual0 <= 0):
      guess1=0.5*(tmp+guess0)
    else:
      guess1=tmp-(tmp-guess0)* (residual1/(residual1-residual0))
      if (guess1 <=0):guess1=.01
    guess0=tmp
#    print "Guess:", guess1, "residual:", residual1, "\n"
  if i > 90:
     out_summary="Unconverged!,"+str(i)+",Reduction=,"+str(reduction)+\
     ", Failure Rate=,"+str(guess1)+"\n "
  else:
     out_summary="Converged,"+str(i)+",Reduction=,"+str(reduction)+\
     ", Failure Rate=,"+str(guess1)+"\n "
  fp3.write(out_summary)
#  print "###out \n"
  return(guess1)
def load_variation():
   global fp3, a, b, alpha, beta
   fp3=open('Interference_Summary.csv', 'a')
# fatigue strengths
   B10= 150.0
   B50= 180.0
#reduce(LN(LN(1-0.1)/LN(1-0.5))) term for efficiency
   beta=-1.883854407/math.log(B10/B50)
# reduce B50/POWER(-LN(1-0.5), (1/C13))
   alpha=B50/( (0.693147181)**(1.0/beta))
   base_B10_FF=2.4
   base_failure_rate=1.2
# B13*POWER(-LN(1-(B5/100)),1/C13)
   strength_at_base_failure=alpha*(-math.log(1.0-.01*base_failure_rate))**(1.0/beta)
   Z_at_base_failure=stats.norm.ppf(1.0 - .01*base_failure_rate)
   nominal_load=B10/base_B10_FF
   load_stddev= (strength_at_base_failure-nominal_load)/Z_at_base_failure
   guess=base_failure_rate
   out_summary="#Infererence with B10="+str(B10)+" B50="+str(B50)+\
   " B10 FF at Nominal Load="+str(base_B10_FF)+" Base failure%="+str(guess)+"\n "
   fp3.write(out_summary)
   failure=process(nominal_load,load_stddev,alpha,beta,-21.4,1.0,guess)
   for i in range(0,0):
          reduction= i*5.0+.01
          failure=process(nominal_load,load_stddev,alpha,beta,reduction,1.0,guess)
          guess=failure
  #print entry1

def strength_variation():
   global fp3, a, b, alpha, beta
   fp3=open('Interference_Summary.csv', 'a')
# fatigue strengths
   B10= 150.0
   B50= 180.0
#reduce(LN(LN(1-0.1)/LN(1-0.5))) term for efficiency
   beta=-1.883854407/math.log(B10/B50)
# reduce B50/POWER(-LN(1-0.5), (1/C13))
   alpha=B50/( (0.693147181)**(1.0/beta))
   base_B10_FF=2.0
   base_failure_rate=3.3
# B13*POWER(-LN(1-(B5/100)),1/C13)
   strength_at_base_failure=alpha*(-math.log(1.0-.01*base_failure_rate))**(1.0/beta)
   Z_at_base_failure=stats.norm.ppf(1.0 - .01*base_failure_rate)
   nominal_load=B10/base_B10_FF
   load_stddev= (strength_at_base_failure-nominal_load)/Z_at_base_failure
   guess=base_failure_rate
   out_summary="#Infererence with B10="+str(B10)+" B50="+str(B50)+\
   " B10 FF at Nominal Load="+str(base_B10_FF)+" Base failure%="+str(guess)+"\n "
   fp3.write(out_summary)
# New fatigue strengths
   B10_new= 100.0
   B50_new= 130.0
#reduce(LN(LN(1-0.1)/LN(1-0.5))) term for efficiency
   beta_new=-1.883854407/math.log(B10_new/B50_new)
# reduce B50/POWER(-LN(1-0.5), (1/C13))
   alpha_new=B50_new/( (0.693147181)**(1.0/beta_new))
   failure=process(nominal_load,load_stddev,alpha_new,beta_new,0.01,0.0,guess)
   out_summary="#Infererence with B10="+str(B10_new)+" B50="+str(B50_new)+\
   " New B10 FF at Nominal Load="+str(base_B10_FF*B10_new/B10)+"Failure%="+str(failure)+"\n "
   fp3.write(out_summary)
strength_variation()
#load_variation()
