#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.25.1
#  in conjunction with Tcl version 8.6
#    Oct 18, 2019 08:08:09 AM CDT  platform: Linux

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import Jay1_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    Jay1_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    Jay1_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {DejaVu Sans} -size 24 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("600x450+650+150")
        top.title("New Toplevel")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.083, rely=0.778, relheight=0.167
                , relwidth=0.833)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Labelframe''')

        self.Text1 = tk.Text(self.Labelframe1)
        self.Text1.place(relx=0.02, rely=0.267, relheight=0.613, relwidth=0.192
                , bordermode='ignore')
        self.Text1.configure(background="white")
        self.Text1.configure(font=font9)
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(wrap="word")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.167, rely=0.178, height=89, width=161)
        self.Button1.configure(command=Jay1_support.StartTest)
        self.Button1.configure(foreground="#16f926")
        self.Button1.configure(text='''Button''')

        self.Button1_1 = tk.Button(top)
        self.Button1_1.place(relx=0.533, rely=0.178, height=89, width=171)
        self.Button1_1.configure(activebackground="#f9f9f9")
        self.Button1_1.configure(command=Jay1_support.StartTest)
        self.Button1_1.configure(foreground="#16f926")
        self.Button1_1.configure(text='''Button''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="NewCommand")
        self.menubar.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Help!")

if __name__ == '__main__':
    vp_start_gui()





