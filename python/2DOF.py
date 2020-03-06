#needed parameters
M1=50
M2=45
K1=500000
K2=200000
C1=200
C2=100
fp2=open('2DOF.out', 'a')
#fp2.write("# "+M1+M2+K1+K2+C1+C2)
fp2.write("# ")
fp2.write(" K1="+str(K1))
fp2.write(" M1="+str(M1))
fp2.write(" C1="+str(C1))
fp2.write(" K2="+str(K2))
fp2.write(" M2="+str(M2))
fp2.write(" C2="+str(C2))
fp2.write("\n")
for i in  range(1,500):
  omega=i*1.0
  num=(K2+omega*C2*1j)/(M1*omega*omega)
  denom=-1+(K2/(M2*omega*omega))+(C2/(M2*omega))*1j
  alpha=num/denom
  ratio1=(1+alpha)/(-1-alpha+(K1/(M1*omega*omega))+(C1/(M1*omega))*1j)
  ratio2=(1+ratio1)/(-1+(K2/(M2*omega*omega))+(C2/(M2*omega))*1j)
  #fp2.write( omega+ ", "+ repr(ratio1)+", "+ repr(abs(ratio1))+ ", "+ repr(ratio2)+", "+repr(abs(ratio2))+",\n ")
  fp2.write( str(omega)+ ", "+ str(abs(ratio1))+ ", "+str(abs(ratio2))+",\n ")
  #print omega,abs(ratio1),abs(ratio2)
