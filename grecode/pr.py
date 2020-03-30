#!/usr/bin/env python
# --*-- coding:utf-8 --*--
# example radiobuttons.py
 
import pygtk
pygtk.require('2.0')
import gtk
 
class RadioButtons:
    def callback(self, widget, data=None):
        print "%s было нажато %s" % (data, ("OFF", "ON")[widget.get_active()])
 
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False
 
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
   
        self.window.connect("delete_event", self.close_application)
 
        self.window.set_title("Переключатели")
        self.window.set_border_width(0)
 
        box1 = gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
 
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
 
        button = gtk.RadioButton(None, "переключатель 1")
        button.connect("toggled", self.callback, "переключатель 1")
        box2.pack_start(button, True, True, 0)
        button.show()
 
        button = gtk.RadioButton(button, "переключатель 2")
        button.connect("toggled", self.callback, "переключатель 2")
        button.set_active(True)
        box2.pack_start(button, True, True, 0)
        button.show()
 
        button = gtk.RadioButton(button, "переключатель 3")
        button.connect("toggled", self.callback, "переключатель 3")
        box2.pack_start(button, True, True, 0)
        button.show()
 
        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 0)
        separator.show()
 
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, False, True, 0)
        box2.show()
 
        button = gtk.Button("Закрыть")
        button.connect_object("clicked", self.close_application, self.window,
                              None)
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        self.window.show()
 
def main():
    gtk.main()
    return 0       
 
if __name__ == "__main__":
    RadioButtons()
    main()
