# Jay Roplekar   09/29/2004
# written to strip multiple entries in system/component FMEAS so
# that they can be converted into a Validation FMEA  where controls are on
# header line
import string, os, re, traceback, glob

def process():
  global my_hash, string_array
  
  my_hash = {}
  string_array=[]

  outfile="Val_FMEA.dbg"
  fp2=open(outfile, 'w')
  fp2.write( "\n ####Current File:  "+fp.name+"\n")
  print "working on file", fp
  outfile2="Val_FMEA.csv"
  fp3=open(outfile2, 'a')
  tmp_line= fp.readline()
  #line=tmp_line
  line=tmp_line.strip()
# firstline for headers
  header=line.strip('"').split('","')
  print len(header)
  for i in range(len(header)):  my_hash[header[i]]=i
  #print my_hash
# block to find the first Warranty  tag and then the following
  while (  line != ""):
      tmp_line= fp.readline().strip()
      line=tmp_line.strip('"')
      line=line.rstrip('",')
      record=line.strip().split('","')
      string_array.append(record)
  else:
    fp.close()
    controls_list={}
    to_keep=[]
    dupl_list=[]
    for  i in range(len(string_array)):
     #print string_array[i]
     #fp2.write( "$$$"+repr(i)+","+repr(string_array[i][0:6])+"\n")
     to_keep.append(1)
     for j in range (i):
      try:
          if(  string_array[i][0:6]== string_array[j][0:6]):
            to_keep[i]=0
            dupl_list[j].append(i)
            #print 'Common cause ##', i, j ,string_array[i][0:6]\
            #,string_array[j][0:6]
            fp2.write( "\nCommon cause ##"+ repr(i)+ "  "+repr(j)+\
            "   "+ repr(string_array[i][0:6])\
            +"\n\t  "+repr(string_array[j][0:6]) )
            break
      except IndexError: print 'Error in dupl_list:', i, j, dupl_list
      
     if( to_keep[i]== 1): dupl_list.append([i])
     elif ( to_keep[i]== 0): dupl_list.append([])

     try:
        chk_control=string_array[i][my_hash['Control']]
        if (chk_control == ''):
          print 'Empty Control?'
          print header
          print string_array[i]
        if (controls_list.has_key(chk_control) != True):
             controls_list[chk_control]=1
     except IndexError:
      continue
      #print string_array[i],  my_hash['Control']
    # Done building Unique controls list
    #Output Headers to a CSV file in Failsafe format
    out_string=""
    for i in range(7):
      out_string=out_string+ '"'+header[i]+'",'
    out_string=out_string+ '"Severity",'
    #out_string=out_string+ '"Occurrence",'
    for k, v in controls_list.iteritems():
     out_string=out_string+ '"'+k+'",'
    out_string=out_string+ '\n'
    fp3.write(out_string)

    for i in range(len(dupl_list)):
      num_entries= len(dupl_list[i])
      if(num_entries > 0):
        controls={}
        for k, v in controls_list.iteritems():controls[k]=None
        curr_severity=0
        for j in range(num_entries):
          curr_rec=dupl_list[i][j]
          curr_control= string_array[curr_rec][my_hash['Control']]
          curr_detection=string_array[curr_rec][my_hash['Detection']]
          controls[curr_control]=curr_detection
          curr_occur=string_array[curr_rec][my_hash['Occurrence']]
          sev=string_array[curr_rec][my_hash['Severity']]
          if ( curr_severity < sev): curr_severity = sev
        #print i, string_array[i][0:6],curr_occur, curr_severity, controls
        #Block to output the current row of validation FMEA
        out_string=""
        for k in range(7):  out_string=out_string+ '"'+string_array[i][k]+'",'
        out_string=out_string+ '"'+curr_severity+'",'
        #out_string=out_string+ '"'+curr_occur+'",'
        for k, v in controls_list.iteritems():
            if ( controls[k]== None):
              out_string=out_string+ '"",'
            else:
              out_string=out_string+ '"'+controls[k]+'",'
        out_string=out_string+ '\n'
        fp3.write(out_string)
    #print controls_list, to_keep, dupl_list
    #print string_array
def main():
  global fp
  filelist=glob.glob('*.csv')
  print filelist
  for name in filelist:
    fp=open(name, 'r')
    process()
main()
