#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 
import sys
import os 
con = None

try:
    con = sqlite3.connect('test.db')
    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')  
    data = cur.fetchone()
    
    print "SQLite version: %s" % data                
    
except sqlite3.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()