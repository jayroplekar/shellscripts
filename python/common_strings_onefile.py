# Jay Roplekar   07/19/2004
# python script to check a common hits in a list of strings with another


import string, os, traceback, re

def process():
  num_records=0
  num_hit=0
  list1=[]
  list2=[]
  p=re.compile('#', re.IGNORECASE)

  fp1=open('C:\D\Programming\jay_ 5and10yearsummary1_warranty5+10.txt', 'r')

  fp=fp1
  line= fp.readline()
  #print line
  while (  line != ""):
        if p.match(line) != None:
          continue
        else:
          stripped_line=line.strip()
          tmp=stripped_line.split()
          try:
           list1.append(tmp[0])
           list2.append(tmp[5])
          except IndexError:
            print "%%%", line
        line=fp.readline()

  


  for string in list1:
    try:
      i= list2.index(string)
      num_hit=num_hit+1
      print num_hit, string
    except ValueError:
      continue




process()

