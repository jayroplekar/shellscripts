# Jay Roplekar   07/13/2004
# written based on various examples from the web
# Added more cleanup and the textbox highlighting etc 08/11/2004 Jay R
# Use string list and only search non-empty also saving and all records
# option and opening files general small clean up 08/19/2004 Jay R
# This "fork" is for  myCPI html claim outputs forking 05/01/06 Jay R
# Adding modified html output  05/15/06 Jay R

import Tkinter
import string, os, traceback
import tkFileDialog, tkFont,re
filter_list=[]

def process_claim(claim):
      global claim_num
      claim_num=''
#Following two tags are used to reduce the amounting of searching by finding the
# the exact narrative. Probably not very needed
      story1=re.compile('<p>', re.IGNORECASE)
#      story2= re.compile(\
#      'Warranty Information \(By Profit Center and Warranty Type\):',\
#      re.IGNORECASE)
      stop=re.compile('stop', re.IGNORECASE)
      claimtag=re.compile('<td><b>Claim Num:</b></td>', re.IGNORECASE)
      flag=0
      for i in range(len(claim)):
        if (story1.search(claim[i])  != None): flag=1
# if find stop do we need not go further, hard stop is for debugging anyways
# python search vs match, using search below
        if (claimtag.search(claim[i]) != None):
          tmp=claim[i+1].replace('\t<td>','')
          claim_num=tmp.replace('</td>\n','')
          #print "Claim no", claim_num
        if (stop.match(claim[i]) != None):
          print "Exiting as a stop found in the input"
          exit(0)
      if flag == 0: story1=story2 # Don't have the Parts tag make do with other
      for i in range(len(claim)-1):
        if (story1.search(claim[i])  != None):
           while ( claim[i]!= "\n"):
            i=i+1 #skip lines till we reach narrative
           narrative=[]
           while i <= len(claim)-1:
            if ( claim[i]!= "\n"):
              narrative.append(claim[i])
            i=i+1
           return(narrative)
           
def color_narrative(narrative, matchlist):
   for i in range(len(narrative)):
    for j in  range(len(narrative[i])):
      flag=0
      for k in  range(len(matchlist)):
        if (matchlist[k][0] == i) and  (matchlist[k][1]<=j)\
           and  (j<matchlist[k][2]) : flag=1
      if flag ==0 :
        output_text.insert(Tkinter.END,narrative[i][j],"normal")
      else:
        output_text.insert(Tkinter.END,narrative[i][j],"red")


def color_html(narrative,matchlist,fp2):
  for i in range(len(narrative)):
     output_line=[]
     for k in  range(len(matchlist)):
        if (matchlist[k][0] == i):
           start=matchlist[k][1]
           stop=matchlist[k][2]
           if (output_line == []):
            output_line=narrative[i][0:start]+'<font color="#FF0000">'\
            + narrative[i][start:stop]+'</font>'
           else:
            output_line=output_line+ '<font color="#FF0000">'\
            + narrative[i][start:stop]+'</font>'
     if (output_line == []):
      output_line=narrative[i]
     else:
      output_line=output_line+narrative[i][stop:]
     fp2.write(output_line)
     
def search_narrative(narrative, searchlist):
  matchlist=[]
  for i in range(len(narrative)):
       for j in range(len(searchlist)):
           search_result=searchlist[j].search(narrative[i])
           if (search_result != None):
# Following should be unnecessary as python should return None but kludge for now
            if (   (search_result.start() !=0) and (search_result.end() !=0)):
              matchlist.append((i,search_result.start(),search_result.end()))
  return(matchlist)
  
def build_filter_list(local_filter_list):
 global filter_file
#assume for now if it is not empty  we do not want to bug the user again with prompt
 if (len(filter_list) == 0):
   filter_file=tkFileDialog.askopenfile()
 else:
 #dummy call to force a read
   filter_file.seek(0)
   local_filter_list=[]
# do this everytime we come in so that if the filter file was updated we read it again
 print filter_file.tell()
 for line in filter_file:
# going through following to allow cut & paste from spreadsheet
  claims_in_a_line=line.split()
  for token in  claims_in_a_line:
    local_filter_list.append(token)
 print "number of claims in filterlist", len(filter_list)
 return(local_filter_list)
 #print filter_list
 
def  to_be_filterd_in(filter_list,claim_num):
  filter_status= filter.get()
  #print "Processing Claim:", claim_num, "Filter Status:", filter_status
  if  (filter_status == "None"): return(1)
  else:
    # exclude the files filter on
    if ( filter_status=="Exclude Specified"):
      try:
        in_list=filter_list.index(claim_num)
        #print "In Exclude: should exclude", claim_num
        return(0)
      except ValueError:
        return(1)
    # include the files filter on
    if ( filter_status== "Include Specified"):
      try:
        in_list=filter_list.index(claim_num)
        #print "Processing Claim:", claim_num, "should be in"
        return(1)
      except ValueError:
        return(0)
      
def process():
  global filter_list
  fp2=open('Parser_summary.html', 'w')
  num_records=0
  num_filtered_in=0
  num_hit=0
# filter certain claims capability
  if (filter.get() != "None"): filter_list=build_filter_list(filter_list)
  print "filter status is:",  filter.get()
  print filter_list
# The tag by which we separate warranty Claims
#  p=re.compile('Machine Information', re.IGNORECASE)
  p=re.compile('<table>', re.IGNORECASE)
# The tag by which we separate story within a warranty Claim
#  comment=re.compile('comment', re.IGNORECASE)
  comment=re.compile('<p>', re.IGNORECASE)
  searchlist=[]
  outputlist=[]
  fp2.write("##Searching file  "+fp.name+"\n <br>Using Following Strings:")
  for string in strlist:
    chkstring=string.get()
# The empty string check is sth I had add is python changed since 04 in what it returns?
    if ( ( chkstring != None) and ( chkstring != "")):
      print "##using string", chkstring, " for search"
      searchlist.append(re.compile(string.get(), re.IGNORECASE) )
      fp2.write("\n<br>"+chkstring)
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
            narrative=buffer+tmp_narrative
            num_records=num_records+1
# Do any work only if the claim is not on filter list
            #print "Claim Number:", claim_num, "Filter Output:", to_be_filterd_in(filter_list,claim_num)
            if ( to_be_filterd_in(filter_list,claim_num) == 1 ):
              num_filtered_in=num_filtered_in+1
              matchlist=search_narrative(narrative,searchlist)
              if ( matchlist != []):
                 output_line="\n <br>$$$$Current Record:  "+repr(num_records)+\
                 " Claim Number:"+claim_num+"\n"
                 
                 num_hit=num_hit+1
                 outputlist.append((num_records, claim_num,1))

                 fp2.write(output_line)
                 color_html(narrative,matchlist,fp2)

              else:
               outputlist.append((num_records, claim_num,0))
               
               if (raw_output.get()==1):
                output_line="\n $$$$Current Record:  "+repr(num_records)+\
                " Claim Number:"+claim_num+"\n"

                #output_text.insert(Tkinter.END, output_line, "a")
                fp2.write(output_line)
                #for output_line in narrative:
                #  output_text.insert(Tkinter.END, output_line,"normal")
                color_html(narrative,matchlist,fp2)
         else:
          line= fp.readline()
  else:
    #not close the line below so that we do not have open again and again
    #fp.close()
    fp.seek(0)
    output_line="\n <br>Total Records:  "+repr(num_records)+" Hits:  "+repr(num_hit)
    output_text.insert(Tkinter.END, output_line)
    fp2.write(output_line)
    try:
      output_line="\n<br>Note this filters claims listed in:  "+filter_file.name+\
      "# Claims Filtered in:"+repr(num_filtered_in)
      fp2.write(output_line)
    except NameError:
      output_line=""
    output_line="\n <br>Matched Entries <br> "
    fp2.write(output_line)

    for j in range(len(outputlist)):
       if (outputlist[j][2] == 1):
        fp2.write("\n<br>"+outputlist[j][1])
    #output_line="\n<br> Non-Matching Entries not printed <br>  "
    #fp2.write(output_line)
    #for j in range(len(outputlist)):
    #   if (outputlist[j][2] == 0):fp2.write(repr(outputlist[j]))
      
def file_menu():
    file_btn = Tkinter.Menubutton(menu_frame, text='File', underline=0)
    file_btn.pack(side=Tkinter.LEFT, padx="2m")
    file_btn.menu = Tkinter.Menu(file_btn)
    file_btn.menu.add_command(label="Open", underline=0, command=GetSource)
    file_btn.menu.add_command(label='Exit', underline=0, command=file_btn.quit)
    file_btn['menu'] = file_btn.menu
    return file_btn

def action_menu():
    action_btn = Tkinter.Button(menu_frame, text='Process',command=process )
    action_btn.pack(side=Tkinter.RIGHT, padx="2m")
    print_all=Tkinter.Checkbutton(menu_frame, text='Print All Records?',\
                variable=raw_output)
    save_all=Tkinter.Checkbutton(menu_frame, text='Save Summary?',\
                variable=save_output)
    filter_some=Tkinter.OptionMenu(menu_frame,filter,\
                  "None", "Exclude Specified", "Include Specified")
    print_all.pack(side=Tkinter.RIGHT, padx="2m")
    save_all.pack(side=Tkinter.RIGHT, padx="2m")
    filter_some.pack(side=Tkinter.RIGHT, padx="2m")
    #print raw_output.get()
    #action_btn['menu'] = action_btn.menu
    return action_btn

def help_menu():
    help_btn = Tkinter.Menubutton(menu_frame, text='Help!', underline=0,)
    help_btn.pack(side=Tkinter.LEFT, padx="2m")
    help_btn.menu = Tkinter.Menu(help_btn)
    help_btn['menu'] = help_btn.menu
    return help_btn

def init_vars():
    global  str1, str2, str3, strlist
    global  raw_output, save_output, filter
    strlist=[]
    for i in range(3): strlist.append(Tkinter.StringVar())
    str1 = Tkinter.StringVar()
    str2= Tkinter.StringVar()
    str3= Tkinter.StringVar()
    raw_output=Tkinter.IntVar()
    save_output=Tkinter.IntVar()
    filter=Tkinter.StringVar()

# set these as myCPI "feature"
    save_output.set(1)
    filter.set("None")
    
def GetSource():
    global fp
    fp=tkFileDialog.askopenfile()

def GetSearchStr():
    for i in range(3):
      Tkinter.Entry(history_frame, width=30,
                  textvariable=strlist[i]).pack(side=Tkinter.LEFT, padx=5, pady=5)
def main():
  global root, history_frame, info_line, menu_frame, info_frame
  global output_text
  root = Tkinter.Tk()
  root.title('JR: Warranty Info Parser')
  init_vars()
  
  #-- Create the menu frame, and menus to the menu frame
  menu_frame = Tkinter.Frame(root)
  menu_frame.pack(fill=Tkinter.X, side=Tkinter.TOP)
  menu_frame.tk_menuBar(file_menu(), action_menu(), help_menu())

  #-- Create the history frame (to be filled in during runtime)
  helv16 = tkFont.Font( family="Helvetica", size=16, weight="bold" )
  history_frame2 = Tkinter.Frame(root)
  history_frame2.pack(fill=Tkinter.X, side=Tkinter.TOP, pady=2)
  Tkinter.Label(history_frame2, width=15,
                  text="Phrase1", font=helv16).pack(side=Tkinter.LEFT)
  Tkinter.Label(history_frame2, width=15,
                  text="Phrase2", font=helv16).pack(side=Tkinter.LEFT)
  Tkinter.Label(history_frame2, width=15,
                  text="Phrase3", font=helv16).pack(side=Tkinter.LEFT)
                  
  #-- Create the history frame (Right now use text entries here)
  history_frame=  Tkinter.Frame(root)
  history_frame.pack(fill=Tkinter.X, side=Tkinter.TOP, pady=2)
  
  #--Output summary is being written here
  info_frame = Tkinter.Frame(root)
  info_frame.pack(fill=Tkinter.X, side=Tkinter.BOTTOM, pady=3)
  output_text=Tkinter.Text(info_frame)
  output_text.pack(fill=Tkinter.BOTH,expand=Tkinter.YES)
  output_text.tag_config("a", foreground="blue", underline=1)
  output_text.tag_config("red", foreground="red", underline=1)

  GetSearchStr()
  root.mainloop()

main()

