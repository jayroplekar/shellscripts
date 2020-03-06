# Jay Roplekar   02/07/2005
# written based on various examples from the web
import string, os, re, traceback, glob
def main():
  global fp,fp2
  name='G-data_637.csv'
  fp=open(name, 'r')
  fp2=open('amp_curves.out', 'a')
  line= fp.readline()
  num_write=0
  while (  line != ""):
    line= fp.readline()
    line=line.strip()
    tokens=line.split(',')
    if (num_write == 3):
      #fp2.write( repr(tokens[0])+ ", "+ repr(tokens[1]) +",\n ")
      fp2.write( tokens[0]+ ", "+ tokens[3]+",\n ")
      num_write=0
    else:
      #fp2.write( repr(tokens[0])+ ", "+ repr(tokens[1]) +"," )
       fp2.write( tokens[0]+ ", "+ tokens[3]+", ")
       num_write=num_write+1
main()
