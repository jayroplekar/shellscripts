#from math import exp
import math, random
import string, os, traceback,sys
def main():
  global a, b, alpha, beta
  fp2=open('Explicit_Integration_Summary.dat', 'w')
  fp3=open('Explicit_Integration_Summary.csv', 'w')
## 735: 72100 lb => 32.7 Ton + Payload 36 Ton
## 740: 83700 lb => 37.97 Ton + Payload 46 with 10% marginc included
  M1=68700.0
  M2=83970.0
#  V1=16.09 #36 mph
#  V1=14.305 #32 MPH
#  V2=14.305 #32 MPH
  V1=7.0
  V2=7.0
  #P= 300.0*745.7 # 300 HP @ 1500 erpm in watts
  P= 450.0*745.7 # 450 HP @ 2100 erpm in watts
  time=0.0
  dt=0.002
  grade=0.05
  out_summary="#Parameters: M1="+str(M1)+" M2="+str(M2)+\
  " V1="+str(V1)+" V2="+str(V2)+\
  " Braking Power (HP)="+ str((P/745.7))+" Grade (%)="+ str(grade*100.0)+"\n "
  fp3.write(out_summary)

  for j in range(0,40000):
        time=time+dt
        dV1=-((P-9.8*M1*grade*V1)*dt )/(M1*V1)
        V1=V1+dV1
        dV2=-((P-9.8*M2*grade*V2)*dt )/(M2*V2)
        V2=V2+dV2
        out_summary=str(time)+"  "+str(V1*2.237)+"  "+str(V2*2.237)+\
        "  "+str(dV1*2.237)+"  "+str(dV2*2.237)+",\n "
        fp2.write(out_summary)
        if (j%1000 == 0.0):
          out_summary=str(time)+","+str(V1/2.237)+","+str(V2/2.237)+",\n "
          fp3.write(out_summary)
        if ( V1*(V1-dV1) <0): fp3.write("Sign change in V1")
        if ( V2*(V2-dV2) <0): fp3.write("Sign change in V2")
  #print entry1

main()
