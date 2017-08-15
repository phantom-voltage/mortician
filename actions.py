#!/usr/bin/env python

from autopsy_angband import score_parse as autopsy_ang
from autopsy_cataclysm import autopsy_cdda
from autopsy_poschengband import score_parse as autopsy_pcb

def action_cataclysm(self, event):
    msg = autopsy_cdda(self, "%s/%s"%(event[2], event[3]))

    if msg is not None:
        self.write(msg)
        

def action_angband(self, event):
    msg = autopsy_ang(self, "%s/scores.raw" % (event[2]))
    
    if msg is not None:
        self.write(msg)

def action_poschengband(self, event):
    msg = autopsy_pcb(self, "%s/scores.raw" % (event[2]))
    
    if msg is not None:
        self.write(msg)
