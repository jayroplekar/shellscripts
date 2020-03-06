# Jay Roplekar   07/13/2004
# written based on various examples from the web
import Tkinter
import string, os, traceback
import tkFileDialog, tkFont,re


def say_hi():
        print "hi there, everyone!"

def process():
  num_records=0
  num_hit=0
  p=re.compile('Machine Information', re.IGNORECASE)
#  s1=re.compile(str1.get(), re.IGNORECASE)
#  s2=re.compile(str2.get(), re.IGNORECASE)
#  s3=re.compile(str3.get(), re.IGNORECASE)
  fp=open('C:\D\Programming\AFTERCOOLER WARRANTY CLAIMS.txt', 'r')
  s1=re.compile('brok', re.IGNORECASE)
  s2=re.compile('crack', re.IGNORECASE)
  s3=re.compile('leak', re.IGNORECASE)
  stop=re.compile('stop', re.IGNORECASE)
  line= fp.readline()
  print line
# block to find the first Warranty  tag and then the following
# Remember no goto in Python :-)  JR 07/15/2004
  while (  line != ""):
         #say_hi()

         #print "$$", line
         if p.match(line) != None:
            #print line
            flag=0
            num_records=num_records+1
            print "**", num_records , line
            line= fp.readline()
            while   (p.match(line) == None) and (  line != ""):
              #print line
              #process for the keywords
              if (stop.match(line) != None):
                print "&&&&&&&&&&", line
                exit(0)
              if (s1.search(line) != None) or (s2.search(line) != None)\
                 or (s3.search(line) != None):
                  #print line
                  if flag==0:
                    flag=1
                    num_hit=num_hit+1
                    print num_hit,  line
              line= fp.readline()

         # we are out of the while now
         else:
          line= fp.readline()
  else:
    fp.close()
    print "Total Records:", num_records, "Hits:", num_hit

process()

