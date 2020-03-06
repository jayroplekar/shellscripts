# Jay Roplekar   07/19/2004
# python script to check a common hits in a list of strings with another


import string, os, traceback, re

def process():
  num_records=0
  num_hit=0
  list1=[]
  list2=[]
  p=re.compile('#', re.IGNORECASE)

  fp1=open('C:\D\Programming\jay_ 5and10yearsummary1_warranty5.txt', 'r')
  fp2=open('C:\D\Programming\jay_ 5and10yearsummary1_warranty10.txt', 'r')

  fp=fp1
  line= fp.readline()
  #print line
  while (  line != ""):
        if p.match(line) != None:
          continue
        else:
          stripped_line=line.strip()
          tmp=stripped_line.split()
          list1.append(tmp[0])
        line=fp.readline()

  
  fp=fp2
  line= fp.readline()
  #print line
  while (  line != ""):
        if p.match(line) != None:
          continue
        else:
          stripped_line=line.strip()
          tmp=stripped_line.split()
          list2.append(tmp[0])
        line=fp.readline()

  for string in list1[0:20]:
    try:
      i= list2[0:20].index(string)
      num_hit=num_hit+1
      print num_hit, string
    except ValueError:
      continue

process()

