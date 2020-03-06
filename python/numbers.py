#~ /***************************************************************************
 #~ *            numbers.py
 #~ *
 #~ *  Fri Oct 22 09:13:12 2004
 #~ *  Copyright  2004  Stas
 #~ *  stas@linux.isbeter.nl
 #~ ****************************************************************************/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#

RCFILE = 0

import os,sys,random
import pygame
from pygame.constants import *
from CPConstants import DATADIR
from utils import load_image,load_sound,font2surf,MyError
from SpriteUtils import CPinit,CPSprite

class Img:
    pass
class Snd:
    pass

class Balloon:
    def __init__(self,payload,start,end,up):
        self.payload = payload #must be a class object
        self.end = end
        self.start = start
        self.image = Img.balloon
        self.rect = self.image.get_rect()
        self.rect.move_ip(start)
        self.up = up
        
    def update(self):
        if self.rect.topleft[1] <= self.end[1]:
            #self.payload.show()
            self.rect = self.payload.rect
            self.rect.move_ip(self.end)
            self.image = self.payload.surface
            Snd.boom.play()
            return 1
        else:
            self.rect.move_ip(0,self.up)
            return 0
        
class Payload:
    def __init__(self,word,size,fcol,ttf):
        self.surface,spam = font2surf(word,size,fcol,ttf)
        self.rect = self.surface.get_rect()

class Token(CPSprite):
    def __init__(self,image,oper,start):
        CPSprite.__init__(self)
        self.start = start
        self.image = image
        self.oper = {"x":"*","/":"/","+":"+","-":"-"}[oper]
        self.rect = self.image.get_rect()
        self.rect.move_ip(start)
        self.playfield = pygame.Rect(0,0,800,500)
        
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.playfield.contains(pos+ (4,4)):
            self.rect.centerx,self.rect.centery = pos
        return 0



class Game(Img,Snd):    
    """  Numbers.py - part of childsplay.py, a suite of educational games for
  young children.
 """

    def __init__(self,screen,backgr,rcdic,basepath,libdir):
        Img.screen = screen
        Img.backgr = backgr
        CPinit(Img.screen,Img.backgr)# mandatory when using anything from the SpriteUtils
        ## Keep a original surface, because the background will be changed
        Img.backorg = backgr.convert()
        self.rcdic = rcdic
        self.clock = pygame.time.Clock()
        self.eventget = pygame.event.get
        self.basedir  = basepath
        self.libdir = libdir
        self.ttf = None # using pygame standard font
        self.gamelevels = range(1,4)
        self.gameitems = range(4)
        self.score = 0
        self.stop = 0
        file = os.path.join(self.libdir,'NumbersData','balloon.png')
        Img.balloon = load_image(file,1) 
        file = os.path.join(self.libdir,'NumbersData','shot.wav')
        Snd.boom = load_sound(file) 
        file = os.path.join(DATADIR,'wahoo.wav')
        Snd.wahoo = load_sound(file) 
        file = os.path.join(DATADIR,'bummer.wav')
        Snd.bummer = load_sound(file) 
        
        self._setup()
        
    def _setup(self):
        offset = 300
        self.tokensrects = []
        self.tokensdic = {}
        self.token_activate = 0
        for item in ['+','x','-','/']:
            size = 100
            fcol = (244,9,21)
            im,spam = font2surf(item,size,fcol,self.ttf)
            # to use later in check self.som???
            #setattr(Img,item,im)
            obj = Token(im,item,(offset,10))
            self.tokensdic[tuple(obj.rect)] = obj
            
            offset += 100
            self.tokensrects.append((Img.screen.blit(obj.image,obj.rect)))
        
        pygame.display.update(self.tokensrects)
        
    def _make_tuple_str(self,seq):
        return tuple(map(str,seq))
        
    def _make_list_str(self,seq):
        return list(map(str,seq))
    
    def _add(self,i):
        rand = random.choice
        a = rand(range(1,i+1))
        b = rand(range(1,i+1))
        c = a+b
        answer = self._make_list_str((a,'+',b,'=',c))
        return answer
    
    def _min(self,i):
        rand = random.choice
        b = rand(range(1,i+1))
        a = rand(range(b,i+1))
        c = a-b
        answer = self._make_list_str((a,'-',b,'=',c))
        return answer
    
    def _mul(self,i):
        rand = random.choice
        a = rand(range(1,i+1))
        b = rand(range(1,i+1))
        c = a*b
        answer = self._make_list_str((a,'x',b,'=',c))
        return answer
    
    def _div(self,i):
        s = self._mul(i)
        a = int(s[0])
        b = int(s[-1])
        c = b/a
        answer = self._make_list_str((b,'/',a,'=',c))
        return answer
              
    def start(self,l,spam):
        """  When the balloons pop get a operator with the left button. Put it at 
  the questionmark and hit the left button again.
  That's all for now."""
        
        self.dirty_rects = []
        self.objs_to_move = []
        
        Img.backgr.blit(Img.backorg,(0,0),(0,0,800,500)) # Restore org backgr
        self._setup()
        self.som = apply(random.choice((self._add,self._min,self._div,self._mul)), (l*3,))
        #self.som = self._div(l*3) # FOR TESTING
        #print self.som
        offset = 40
        for i in self.som:
            if i  in ('+','-','x','/'):
                self.operator = i
                i = '?'
            fcol = (226,178,31)
            payload = Payload(i,100,fcol,self.ttf)
            if i == '?':
                r = payload.rect
                self.hitzone = r.move(offset,200)
                s = pygame.Surface(r[-2:])
                s.blit(Img.backgr,(0,0))
                Img.hitzone_backgr = s 
                Img.question = payload.surface
                #print self.hitzone
            up = random.choice(range(-6,-1))
            bal = Balloon(payload,(offset,500),(offset,200),up)
            offset = offset + 100
            self.objs_to_move.append((bal))
        
        #print self.tokensrects,self.tokensdic.keys()
        #print self.objs_to_move
    
    def _select_activate(self):
        pos = pygame.Rect(pygame.mouse.get_pos() + (4,4))
        for rec in self.tokensrects:
            if rec.contains(pos):
                #print self.tokensdic
                Img.backgr.blit(Img.screen,(0,0,800,500))
                self.objs_to_move.append((self.tokensdic[tuple(rec)]))
                self.token_activate = 1
        return
    
    def __str__(self):
        """Must return the original, not translated, title of this game.
        It's needed by the high score class of childsplay."""        
        return "Numbers"
         

    def helptitle(self):
        return "Numbers"
    
    def help(self):
        txt=[_("The aim of the game:"),
        _("Try to find the arithmetic operator in simple mathematics exercises."),
        _("For example:  2 ? 2 = 4 -->  +"),
        " ",
        _("Difficulty : 6-7 years."),
        " ",
        _("Number of levels : 3"),
        " ",
        _("The exercises can be somewhat difficult, but the aim is to understand"),
        _("the relation between the numbers not the solution.")]
        
        return txt

    def loop(self,events):
        self.score = 0
        for event in events:
            if event.type is MOUSEBUTTONDOWN and self.objs_to_move == []:
                self._select_activate()
            elif event.type is MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                self._select_dropped()
        obj_remove = []
        # main blit stuff
        for obj in self.objs_to_move:
            self.dirty_rects.append((Img.screen.blit(Img.backgr,obj.rect,obj.rect)))
            flag = obj.update()
            self.dirty_rects.append((Img.screen.blit(obj.image,obj.rect)))
            if flag == 1: # balloon returns 1 if finished
                obj_remove.append((obj))
        pygame.display.update(self.dirty_rects)
        # remove objects until no balloons left
        if obj_remove:
            for item in obj_remove:
                self.objs_to_move.remove(item)
        if self.objs_to_move != []:
            self.stop = 0 # must be 0 if there are objects left, leave if all the objects are gone
        #self.stop = 0 # TEST WAARDE
        self.dirty_rects = []
        
        return self.stop,self.score
    
    def _select_dropped(self):
        if not self.token_activate: return
        pos = pygame.Rect(pygame.mouse.get_pos() + (4,4))
        #print pos
        #print self.hitzone
        if self.hitzone.contains(pos):
            obj = self.objs_to_move.pop()
            #print 'obj',obj.oper
            answer = "%s%s%s" % (self.som[0],obj.oper,self.som[2])
            
            answer = eval(answer)
            #print answer,' ',self.som[-1]
            if int(answer) == int(self.som[-1]):
                #if obj.oper == self.operator:
                r = Img.screen.blit(Img.backorg,self.hitzone,self.hitzone)    
                rr = Img.screen.blit(obj.image,obj.rect)
                pygame.display.update((r,rr))
                self.stop = -1
                Snd.wahoo.play()
                self.score = 20
                pygame.time.wait(2000)
                #good_answer
            else:
                #r = Img.screen.blit(Img.backorg,self.hitzone,self.hitzone)
                rr = Img.screen.blit(Img.question,self.hitzone)
                #rrr = Img.screen.blit(Img.backgr,obj.rect,obj.rect)
                pygame.display.update(rr)
                Snd.bummer.play()
                self.score = -5
                #wrong_answer
                obj.remove_sprite()
