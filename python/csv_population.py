# Jay Roplekar   09/29/2006
# Written to  convert rwa population csv file for plotting
# Note rwa exports csv with double quotes so a file touched by
# excel won't be handled correctly
import string, os, re, traceback, glob, sys, time

def process():

  outfile="population.dbg"
  fp2=open(outfile, 'a')
  fp2.write( "\n ####Current File:  "+fp.name+"\n")
  print "working on file", fp
  outfile2="population.txt"
  fp3=open(outfile2, 'a')
# discard top 3 lines
  tmp_line= fp.readline()
  tmp_line= fp.readline()
  tmp_line= fp.readline()
  tmp_line= fp.readline().strip()
  fp2.write("arrangements filtered out:\n")
  while (  tmp_line != ""):

      line=tmp_line.strip('"')
      line=line.rstrip('",')
      record=line.strip().split('","')
#above splitting make this rwa specific solution no desire/need to make
# it
      include=-1
      if (arrlist == []):
        include =0
      else:
        try:
          include=1+arrlist.index(record[15])
          #print "##checking for arrangement:",record[15],"result=",include
        except ValueError:
          include=-1
          fp2.write( "  "+record[15]+"\n")
      if (include !=-1):
        try:
          str1=time.strptime(record[4],"%d%b%Y")
          date=time.strftime("%m/%d/%Y",str1)
          hrs=record[11]
        except IndexError:
          print "IndexError for line:", line, record
        out_string=date+"\t"+hrs+"\n"
        fp3.write(out_string)
        
      tmp_line= fp.readline().strip()
def main():
  global fp, arrlist
  filelist=glob.glob('*pop*.csv')
  print filelist
  try:
    arrlist_file=sys.argv[1]
    print  "Using file to filter arrs:", arrlist_file
  except IndexError:
    arrlist_file=""
  arrlist=[]
  if (arrlist_file != ""):
    fp4=open(arrlist_file, 'r')
    tmp_line= fp4.readline().strip()
    while (  tmp_line != ""):
      arrlist.append(tmp_line)
      tmp_line= fp4.readline().strip()
  for name in filelist:
    fp=open(name, 'r')
    process()
main()
