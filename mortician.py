#!/usr/bin/env python

import inotify.adapters
import os
import threading

#from config import output_file

class Mortician:

    output_file = ""
    var_dir = os.getcwd()
    print_ctrl = True
 
    def action(self, event):
        print(event)  

    
#        def __init__(self, directory=os.getcwd(), action=action, recursive=False, watchfile=None, dbfile=None, fifo=None):
#        self.directory = directory
#        self.action = action
#        self.recursive = recursive
#        self.watchfile = watchfile
      
    
    def __init__(self, game, fifo=None):

        self.game = game
        self.action = game.action
        self.control_msg = "%s mortician found a corpse!\n" %(self.game.name)

        if fifo is None or fifo == "":
            self.fifo = Mortician.output_file
        else:
            self.fifo = fifo 
        
        if not game.recursive:
            self.notifier = inotify.adapters.Inotify()
        else:
            self.notifier = None

            
                
    def watch(self, kill_signal):
        print("%s mortician is watching for corpses." %(self.game.name))
        if not self.game.recursive:
            self.notifier.add_watch(self.game.score_directory)
        
        else:
            self.notifier = inotify.adapters.InotifyTree(self.game.score_directory)
    
        while not kill_signal.wait(1):
            for event in self.notifier.event_gen():
                if event is not None:
                    if 'IN_CLOSE_WRITE' in event[1] and not event[3].startswith("."):
                        if self.game.watchfile is not None:
                            if self.game.watchfile in event[3]:
                                print(self.control_msg)
                                self.action(self,event)

                        else:
                            print(self.control_msg)
                            self.action(self,event)
                else:
                    break

    """
     write to specified file with threading for named pipes
    """
    def write(self, msg):
        if self.fifo == "":
            print(msg)
        else:
            writer = threading.Thread(target=self.write_t, kwargs={'msg' : msg})
            writer.start()

    def write_t(self, msg):
        with open(self.fifo, "w") as fd:
            if Mortician.print_ctrl:
                fd.write(self.control_msg)
            fd.write(msg)
        print("%s mortician write finished." %(self.game.name))
            
            
        
