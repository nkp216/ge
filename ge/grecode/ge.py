#!/usr/bin/python
# -*- coding: utf-8 -*-

#    This is gui to the command-line application grecode Bernhard Kubicek
#    https://github.com/bkubicek/grecode

#    Copyright (C) 2020  Navrotskyi Kostiantyn

import pygtk
pygtk.require("2.0")
import gtk

import glib
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
import hal
import pango
import linuxcnc
import traceback
import sys,os , select
import subprocess

import  time
import  atexit, tempfile, shutil
import gobject
import preferences

BASE = os.path.dirname(os.path.realpath(__file__))
WIDGETSDIR = os.path.join(BASE, 'modules')
datadir = os.path.join(BASE, "share", "linuxcnc")
xmlname =os.path.join(BASE, "img", "grecode.glade") #483x411 

GLADE_DIR = os.path.join(BASE, 'img')
grecode_path = os.path.join(BASE, 'grecode')


class GE(object):

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(xmlname) 

        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")

        self.window.set_position(5)
        self.window.show()

        self.chb2 = self.builder.get_object("checkbutton2")
        self.chb3 = self.builder.get_object("checkbutton3")
        self.chb3.set_sensitive(0)#TODO
        
        self.rb4 = self.builder.get_object("radiobutton4")
        self.rb4.connect("toggled",self.toggle_lang,4 ) 
        self.rb5 = self.builder.get_object("radiobutton5")
        self.rb5.connect("toggled",self.toggle_lang,5 )          

                 
        self.prefs = preferences.preferences()
        self.lang = None
        self.set_patameter()                               
       
        self.init_button()        
             
        image_set = ('image1',)
                     
        self.image_list = dict(((i, self.builder.get_object(i))) for i in image_set)

        self.nb   = self.builder.get_object("notebook1")
        self.en2   = self.builder.get_object("entry2")
        self.en3   = self.builder.get_object("entry3")
        self.en4   = self.builder.get_object("entry4")
        self.en5   = self.builder.get_object("entry5")
        self.en2.set_text("1")    
        self.en3.set_text("1")    
        self.en5.set_text("100.0")    
        self.en4.set_text("100.0")
                
        self.en6   = self.builder.get_object("entry6")              
        self.en7   = self.builder.get_object("entry7") 
        
        self.en8   = self.builder.get_object("entry8")              
        self.en9   = self.builder.get_object("entry9")        
        self.en8.set_text("0")         
        self.en9.set_text("0") 
                
        self.en7.set_text("1") 
           
        self.help_stop = False 
        self.help_image_iter = 1 
                     
        gobject.timeout_add(4000, self.help)          


         
    def init_button(self):
             
        self.button1  = self.builder.get_object("hal_button1")
        self.button1.connect("pressed", self.pressed, 1)
        self.button1.connect("enter", self.enter, 'locale/%s/c1.png' % self.lang)
        
        self.button2  = self.builder.get_object("hal_button2")
        self.button2.connect("pressed", self.pressed,2)
        self.button2.connect("enter", self.enter, 'locale/%s/c2.png' % self.lang)        

        self.button3  = self.builder.get_object("hal_button3")
        self.button3.connect("pressed", self.pressed,3)
        self.button3.connect("enter", self.enter, 'locale/%s/c3.png' % self.lang)      
 
        self.button4  = self.builder.get_object("hal_button4")
        self.button4.connect("pressed", self.pressed,4)
        self.button4.connect("enter", self.enter, 'locale/%s/c4.png' % self.lang)                      

        self.button5  = self.builder.get_object("hal_button5")
        self.button5.connect("pressed", self.pressed,5)
        self.button5.connect("enter", self.enter, 'locale/%s/c5.png' % self.lang)

        self.button6  = self.builder.get_object("hal_button6")
        self.button6.connect("pressed", self.pressed,6)
        self.button6.connect("enter", self.enter, 'locale/%s/c6.png' % self.lang) 
        
        self.button7  = self.builder.get_object("hal_button7")
        self.button7.connect("pressed", self.pressed, 7)
        self.button7.connect("enter", self.enter, 'locale/%s/c7.png' % self.lang) 
        
        self.button8  = self.builder.get_object("hal_button8")
        self.button8.connect("pressed", self.pressed,8)
        self.button8.connect("enter", self.enter, 'locale/%s/c8.png' % self.lang)        

        self.button9  = self.builder.get_object("hal_button9")
        self.button9.connect("pressed", self.pressed,9)
        self.button9.connect("enter", self.enter, 'locale/%s/c9.png' % self.lang)        
 
        self.button10  = self.builder.get_object("hal_button10")
        self.button10.connect("pressed", self.pressed,10)
        self.button10.connect("enter", self.enter, 'locale/%s/c10.png' % self.lang)                      

        self.button11  = self.builder.get_object("hal_button11")
        self.button11.connect("pressed", self.pressed,11)
        self.button11.connect("enter", self.enter, 'locale/%s/c11.png' % self.lang) 

        self.button12  = self.builder.get_object("hal_button12")
        self.button12.connect("pressed", self.pressed,12)
        self.button12.connect("enter", self.enter, 'locale/%s/c12.png' % self.lang)         
        
                     
    def back(self, widget, data=None):
        self.nb.set_current_page(0)

    def leave(self, widget, data=None):
        self.set_image('image1', 'czero.png') 
        
    def set_image(self, image_name, file_name):   
        self.image_list[image_name].set_from_file(os.path.join(GLADE_DIR, file_name))        
        
    def help(self,  data=None):
        if self.help_image_iter > 12:
            self.help_stop = False
            self.set_image('image1', 'czero.png')
        if self.help_stop:
            self.anime()          
        return True

    def anime(self): 
        png = "locale/%s/c%dL.png" % (self.lang, self.help_image_iter)
        self.set_image('image1', png)          
    
        self.timer_id = gobject.timeout_add(100, self.big) 
                           
    def big(self,  data=None):
        png = "locale/%s/c%d.png" % (self.lang, self.help_image_iter)
        self.set_image('image1', png) 
        self.help_image_iter += 1    
        return False   
           
   
    def pressed(self, widget, page): 
        self.help_stop = False  
        self.nb.set_current_page(page) 
     
    def enter(self, widget, i):
        self.help_stop = False
        if not self.chb2.get_active(): return

        png = "%s" % i
        self.set_image('image1', png)           
        
    def help_on(self, widget, data=None):
        self.set_image('image1', 'locale/%s/c.png'% self.lang)
        self.help_stop = True
        self.help_image_iter = 1 

#########################################################################test        
    def test(self, widget, data=None):
        """ grecode -align alignx alingy     in.ngc -o out.ngc """ 
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -align  middle min '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error align'         
#############################################################################        
        
       
    def makeabsolut(self, widget, data=None):
        """ grecode -makeabsolut   in.ngc -o out.ngc """ 
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -makeabsolut   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error makeabsolut'         
                

    def killn(self, widget, data=None):
        """ grecode  -killn  in.ngc -o out.ngc """
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -killn   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error killn' 

 
    def yflip(self, widget, data=None):
        """ grecode  -yflip  in.ngc -o out.ngc """
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -yflip   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error yflip'  
             
    def xflip(self, widget, data=None):
        """ grecode  -xflip  in.ngc -o out.ngc """
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -xflip   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error xflip'  
                
    def cw(self, widget, data=None):
        """ grecode  -cw  in.ngc -o out.ngc """
        try:      
            st.poll()
            path = st.file 
            tempfile = os.path.join(tempdir, os.path.basename(path))                      
            comand = "'%s'  -cw   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error cw' 
            
                    
    def ccw(self, widget, data=None):
        """ grecode  -ccw  in.ngc -o out.ngc """
        try:
            st.poll()
            path = st.file  
            tempfile = os.path.join(tempdir, os.path.basename(path))             
            comand = "'%s'  -ccw   '%s' -o '%s'  "% (grecode_path, path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit() 
        except:
            print 'error ccw' 
            
            
    def rot(self, widget, data=None):
        """ grecode -rot 315   in.ngc -o out.ngc """
        try:
            a = float(self.en6.get_text())
            if a == None: return            
            st.poll()
            path = st.file              
            tempfile = os.path.join(tempdir, os.path.basename(path))          
            comand = "'%s' -rot '%s'  '%s' -o '%s'  "% (grecode_path,a , path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit()         
        except:
            print 'error rot' 

    def scale (self, widget, data=None):
        """ grecode -scale 3  3.ngc -o 3.ngc """
        try:
            k = float(self.en7.get_text())
            if k == None: return            
            st.poll()
            path = st.file              
            tempfile = os.path.join(tempdir, os.path.basename(path))          
            comand = "'%s' -scale '%s'  '%s' -o '%s'  "% (grecode_path,k , path, tempfile)
            self.filter_program(comand , path, tempfile)
            os.system("axis-remote '%s'" % (tempfile))
            self.quit()         
        except:
            print 'error scale' 
            
            
    def shift(self, widget, data=None):
        """ grecode -shift  200 180   in.ngc -o out.ngc  """      
        try:
            st.poll()
            path = st.file  
            tempfile = os.path.join(tempdir, os.path.basename(path))                   
            x = float(self.en8.get_text())
            y = float(self.en9.get_text())
            print 'x=',x
            print 'y=',y     
            comand = "'%s'  -shift '%s' '%s'   '%s' -o '%s'  "% (grecode_path,x ,y , path, tempfile)
            self.filter_program(comand , path, tempfile)       
            os.system("axis-remote '%s'" % (tempfile))
            self.quit()         
        except:
            print 'error shift'
            
            
    def copies(self, widget, data=None):
        """ grecode -copies 2 3 200 180   in.ngc -o out.ngc """       
        try:
            st.poll()
            path = st.file  
            tempfile = os.path.join(tempdir, os.path.basename(path))                   
            n = int(self.en2.get_text())
            m = int(self.en3.get_text())  
            s = float(self.en5.get_text())
            q = float(self.en4.get_text())    
            comand = "'%s'  -copies '%s' '%s' '%s' '%s'  '%s' -o '%s'  "% (grecode_path,n ,m ,s ,q, path, tempfile)
            self.filter_program(comand , path, tempfile)       
            os.system("axis-remote '%s'" % (tempfile))
            self.quit()         
        except:
            print 'error copies'    

    def filter_program(self, comand,  infilename, outfilename):
        outfile = open(outfilename, "w")
        print 'infilename=',infilename
        infilename_q = infilename.replace("'", "'\\''")
        print 'infilename1_q=',infilename_q

        p = subprocess.Popen(["sh", "-c", comand],
                              stdin=None,
                              stdout=None,
                              stderr=None )
        p.wait()
        outfile.close()  

        try:
            while p.poll() is None:
                r,w,x = select.select([p.stderr], [], [], 0.100)
                if r:
                    stderr_line = p.stderr.readline()
            return p.returncode,# "".join(stderr_text)
        finally:
            pass


    def set_patameter(self):    
        try:
            vel = self.prefs.getpref( "language", 1, int ) 
            if vel==1: self.lang = 'ru' ; self.rb4.set_active(1)  
            if vel==2: self.lang = 'en' ; self.rb5.set_active(1) 
            vel = self.prefs.getpref( "prompt", 2, int )             
            if vel==1: self.chb2.set_active(1)
            else:      self.chb2.set_active(0)    
        except:
            print 'error set_patameter'
                         
    def seve_patameter(self):
        try:
            if self.rb4.get_active(): vel = 1 ; self.lang = 'ru'
            if self.rb5.get_active(): vel = 2 ; self.lang = 'en'
            self.prefs.putpref("language", vel, int)
            vel = int(self.chb2.get_active())
            self.prefs.putpref("prompt", vel, int)            
        except:
            print 'error save_patameter'             
                
    def toggle_lang(self, widget, data=None):     
        if 4==data:  self.lang = 'ru'       
        if 5==data:  self.lang = 'en'          
        self.init_button()            
           
    def on_window1_destroy(self, widget, data=None):
        self.seve_patameter()
        gtk.main_quit()  
                
    def quit(self):
        self.seve_patameter()
        gtk.main_quit() 


def remove_tempdir(t):
    shutil.rmtree(t)
tempdir = tempfile.mkdtemp()

   
st = linuxcnc.stat()
c = linuxcnc.command()
           
if __name__ == "__main__":
  app = GE()
  gtk.main()
