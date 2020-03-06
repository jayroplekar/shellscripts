# Jay Roplekar   09/21/2004
# written based on various examples from the web
import string, os, re, traceback, glob

def check_dict(dict, machine_name):
  if   dict.has_key(machine_name):
    dict[machine_name]=dict[machine_name]+1
  else:
    dict[machine_name]=1
def process_claim(claim):
      global searchlist
      searchlist=[]
      searchlist.append(re.compile('Sales Model:', re.IGNORECASE))
      searchlist.append(re.compile('Product Type:', re.IGNORECASE))
      searchlist.append(re.compile('Work Category:', re.IGNORECASE))
      searchlist.append(re.compile('Work Code:', re.IGNORECASE) )
      flag=0
      for i in range(len(claim)):
        for j in range(len(searchlist)):
          search_result=searchlist[j].search(claim[i])
          if (search_result != None):
            tmp=claim[i].split(':')
            #machine_name=repr(tmp[1] )
            machine_name=tmp[1].rstrip()
            check_dict(dict[j], machine_name)
def process():
  global dict
  dict = [{}, {}, {}, {}]
  tmp=fp.name
  outfile="Applications"
  fp2=open(outfile, 'a')
  fp2.write( "\n ####Current File:  "+fp.name)
  print "working on file", fp
  num_records=0
  num_hit=0

  p=re.compile('Machine Information', re.IGNORECASE)
  comment=re.compile('comment', re.IGNORECASE)

  line= fp.readline()
# block to find the first Warranty  tag and then the following
  while (  line != ""):
         if p.match(line) != None:
            claim=[]
            buffer=[]
            claim.append(line)
            line= fp.readline()
            claim.append(line)
            while   (p.match(line) == None) and (  line != ""):
              claim.append(line)
              if (comment.match(line) != None): buffer.append(line)
              line=fp.readline()
            tmp_narrative=process_claim(claim)
            if ( tmp_narrative != None):
              narrative=buffer+tmp_narrative
            else:
              narrative=buffer
            num_records=num_records+1
         else:
          line= fp.readline()
  else:
    fp.close()
    output_line="\n Total Records:  "+repr(num_records)+" Hits:  "+repr(num_hit)
    fp2.write(output_line)
    fp2.write("\n ####Following were Machines using this part: \n")
    for j in range(len(searchlist)):
      fp2.write("\n ####")
      for k, v in dict[j].iteritems():
        fp2.write( " "+ k+ "  "+repr(v)+"\n")
def main():
  global fp
  filelist=glob.glob('*.txt')
  print filelist
  for name in filelist:
    fp=open(name, 'r')
    process()
main()
