#!/usr/bin/env python
from pylab import *
from scipy import stats
from fpformat import fix
import string
def histo_plotter (x, SPECS):
  # the histogram of the data
  n, bins, patches = hist(x, 50, normed=0)
  setp(patches, 'facecolor', 'g', 'alpha', 0.75)
  for i in range(len(SPECS)):
      out_of_spec=0
      for j in range(len(bins)):
       if(bins[j] <= SPECS[i]):
        setp(patches[j], 'facecolor', 'r', 'alpha', 0.75)
        out_of_spec=out_of_spec+n[j]
      out_summary="#of Samples Below "+str(SPECS[i])+" :"+str(out_of_spec)+\
     "\n From "+str(len(x))+" Samples "
  fp3.write(out_summary)   
  #print patches
  # add a 'best fit' line
  mu=stats.mean(x)
  sigma=stats.std(x)
  maxfreq=max(n)
  minval=min(x)
  out_summary2="Minimum Value: "+fix(minval,3)
  fp3.write(out_summary2)
#  print x, bins, n, mu, sigma
  y = normpdf( bins, mu, sigma)
  l = plot(bins, y, 'r--')
  #y = normpdf( bins)
  #l = plot(bins, n, 'r--')
  setp(l, 'linewidth', 1)
  xlabel('Clearance')
  ylabel('Count')
  title(r'$\rm{Histogram\ of\ Clearance}$')
  axis([bins[0], bins[49], 0.0, maxfreq])
  text(.01+bins[0], .9*maxfreq, out_summary,  color='r')
  text(.01+bins[0], .8*maxfreq, out_summary2,  color='b')
  grid(True)

  #savefig('histogram_demo',dpi=72)
  show()
def  get_variate(mu, tol, distrib):
  if distrib == -1: return(mu)
  if distrib ==  1: return(mu+ (-0.5+rand(1)[0])*2.0*tol)
  if distrib ==  2: return(mu+ (tol/3.0)*randn(1)[0])
  
def C15_stackup():
  global fp3
  distrib_list=["Fixed", "Unknown","Uniform", "Normal"]
  fp3=open('Stackup_summary.txt', 'a')	
  params=[  "Rod & Crank Thermal Growth",	"Piston Thermal Growth", \
  "Valve face to gage", "Block Center-top",	"Crank",	"Head machined seat depth", \
  "Rod-Pin Length", "Piston pin hole-top",	"Gasket Wire",	"Liner Step-Step", \
  "Gasket Flange(1)", "Gasket Flange (2)",	"Head bulge", \
  "Gasket Crush",	"Block & Liner Thermal Growth", "Nominal Brake Lift", \
  "Lash Variability", "Cylinder to Cylinder Lift", "Brake to Brake"]

  param_means= [-0.392,	-0.187,	-3.560,	425.450,	-85.725,	5.060,-270.760, \
  	-77.775,	1.625,	8.890,		0.250,	0.250,	-0.2, -0.604,  \
    	0.156, -1.91, 0.0, 0.0, 0.0]
  param_tols= [0.0, 0.0, 0.200, 0.150, 0.125, 0.100, 0.050,  \
     0.050, 0.025, 0.020, 0.013, 0.013, 0.0, 0.0, \
     0.0,  0.0, 0.202248, 0.125928, 0.0954]
# -1 -> no variation, 1-> uniform, 2-> Normal
  param_distrib=[ -1, -1, 1, 2, 1, 1, 1, \
   1, 1, 1, 1, 1, -1, -1, \
    -1, -1, 2, 2, 2]
  SPECS=[0.0]
  x=[]

  fp3.write("Parameter              Mean         Tolerance      Distribution \n")
  for j in range(len(params)):
	out_summary=params[j]+str(param_means[j])+ str(param_tols[j])\
	+str(distrib_list[param_distrib[j]+1])+"\n"
	#params[j]+str(param_means[j])+ str(param_tols[j])+
        fp3.write("\n"+out_summary)
  #exit(0)
  for i in  range(0,50):
   stackup=0.0
   for j in range(len(params)):
    val=get_variate(param_means[j],param_tols[j],param_distrib[j])
    stackup=stackup+val
   x.append(stackup)
  histo_plotter (x, SPECS)


  
#C15_stackup()
random_generator_test()