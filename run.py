#!/usr/bin/env python

import inotify.adapters
import os
import time

from mortician import Mortician
from game import Game

from actions import *
from config_load import config_load

import threading

from termcolor import colored


    
def main():

    
    morts = config_load()
    #morts = []
    
    workers = []

    kill_signal = threading.Event()
    j = 0
    for i in morts:
        workers.append(threading.Thread(target=i.watch, args=[kill_signal]))
        workers[j].start()
        j += 1
        

    
    time.sleep(1)
    print("\nAll watches have started.")
    
    try:
        while True:
            time.sleep(11)
    except KeyboardInterrupt:
        print("\n" + colored('Keyboard Interrupt received, exiting threads...', 'red'))
        kill_signal.set()
        

        for j in range(len(workers)):
            
            print("joining workers now...")
            #morts[j].stop()
            workers[j].join(2)

        
        
        

#    angband = Game("Angband", angband_score_dir, angband_action, False, "scores.lok", db_path)
#    cataclysm = Game("Cataclysm", cataclysm_score_dir, cataclysm_action, True, None, db_path)

#    cdda = Mortician(cataclysm)
#    ang = Mortician(angband)

#    morts = [ ang, cdda ]
#    workers = []
    
#    for i in morts:
#        workers.append(threading.Thread(target=i.watch))
        
    #ang.watch()
    
#    for i in workers:
#        i.start()
        
   
if __name__ == "__main__":
    main()
