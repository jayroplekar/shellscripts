# Jay Roplekar   07/13/2004
# written based on various examples from the web
# Added more cleanup and the textbox highlighting etc 08/11/2004 Jay R
# Use string list and only search non-empty also saving and all records
# option an dopening files general small clean up 08/19/2004 Jay R

import Tkinter
import string, os, traceback
import tkFileDialog, tkFont,re

def process_claim(claim):
      story1=re.compile('Warranty Information \(Parts used\):', re.IGNORECASE)
      story2= re.compile(\
      'Warranty Information \(By Profit Center and Warranty Type\):',\
      re.IGNORECASE)
      stop=re.compile('stop', re.IGNORECASE)
      flag=0
      for i in range(len(claim)):
        if (story1.search(claim[i])  != None): flag=1
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
        elif (stop.match(claim[i]) != None):
          print "Exiting as a stop found in the input"
          exit(0)
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
        
def search_narrative(narrative, searchlist):
  matchlist=[]
  for i in range(len(narrative)):
       for j in range(len(searchlist)):
           search_result=searchlist[j].search(narrative[i])
           if (search_result != None):
            matchlist.append((i,search_result.start(),search_result.end()))
  return(matchlist)
  
def process():
  fp2=open('Parser_summary.txt', 'w')
  global output_text
  info_frame = Tkinter.Frame(root)
  info_frame.pack(fill=Tkinter.X, side=Tkinter.BOTTOM, pady=3)
  output_text=Tkinter.Text(info_frame)
  output_text.pack(fill=Tkinter.BOTH,expand=Tkinter.YES)
  output_text.tag_config("a", foreground="blue", underline=1)
  output_text.tag_config("red", foreground="red", underline=1)
  num_records=0
  num_hit=0
  p=re.compile('Machine Information', re.IGNORECASE)
  comment=re.compile('comment', re.IGNORECASE)
  searchlist=[]

  for string in strlist:
    if ( string.get() != None):
      print string.get()
      searchlist.append(re.compile(string.get(), re.IGNORECASE) )

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
            matchlist=search_narrative(narrative,searchlist)

            if ( matchlist != []):
               output_line="\n $$$$Current Record:  "+repr(num_records)+"\n\n"
               output_text.insert(Tkinter.END, output_line, "a")
               color_narrative(narrative,matchlist)
               num_hit=num_hit+1
               if (save_output.get() == 1):
                fp2.write(output_line)
                for output_line in narrative:
                   fp2.write(output_line)
            elif (raw_output.get() ==1):
             output_line="\n $$$$Current Record:  "+repr(num_records)+"\n\n"
             output_text.insert(Tkinter.END, output_line, "a")
             for output_line in narrative:
              output_text.insert(Tkinter.END, output_line,"normal")
         else:
          line= fp.readline()
  else:
    fp.close()
    output_line="\n Total Records:  "+repr(num_records)+" Hits:  "+repr(num_hit)
    output_text.insert(Tkinter.END, output_line)
    if (save_output.get() == 1):fp2.write(output_line)
    
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
    print_all.pack(side=Tkinter.RIGHT, padx="2m")
    save_all.pack(side=Tkinter.RIGHT, padx="2m")
    print raw_output.get()
    #action_btn['menu'] = action_btn.menu
    return action_btn

def help_menu():
    help_btn = Tkinter.Menubutton(menu_frame, text='Help', underline=0,)
    help_btn.pack(side=Tkinter.LEFT, padx="2m")
    help_btn.menu = Tkinter.Menu(help_btn)
    help_btn.menu.add_command(label="How To", underline=0)
    help_btn.menu.add_command(label="About", underline=0)
    help_btn['menu'] = help_btn.menu
    return help_btn

def init_vars():
    global  str1, str2, str3, strlist
    global  raw_output, save_output
    strlist=[]
    for i in range(3): strlist.append(Tkinter.StringVar())
    str1 = Tkinter.StringVar()
    str2= Tkinter.StringVar()
    str3= Tkinter.StringVar()
    raw_output=Tkinter.IntVar()
    save_output=Tkinter.IntVar()

def GetSource():
    global fp
    fp=tkFileDialog.askopenfile()

def GetSearchStr():
    for i in range(3):
      Tkinter.Entry(history_frame, width=30,
                  textvariable=strlist[i]).pack(side=Tkinter.LEFT, padx=5, pady=5)
def main():
  global root, history_frame, info_line, menu_frame, info_frame
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
  history_frame=  Tkinter.Frame(root)
  history_frame.pack(fill=Tkinter.X, side=Tkinter.TOP, pady=2)
  GetSearchStr()
  root.mainloop()
  
  
main()

