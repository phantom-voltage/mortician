#!/usr/bin/python

import yaml
from game import *
import sys
import actions
from termcolor import colored

from mortician import Mortician

def config_load():

    with open("config.yaml", "r") as config:
        
        cfg = yaml.load(config)
    #    print(cfg)

        
    #load defauls
    global_db = None
    global_var = None

    #for section in cfg:

    #if section.lower() == "settings":
        

    # Load global settings 
    print("Loading global settings...")
    
    for subsection in cfg["Settings"]: 
        if subsection == "global_db":
            if cfg["Settings"]["global_db"] is not None:
                global_db = cfg["Settings"]["global_db"]
                print("    Global database file:  " + colored(global_db, "green"))
            
        if subsection == "global_output":
            if cfg["Settings"]["global_output"] is not None:
                global_output = cfg["Settings"]["global_output"]
                Mortician.output_file = global_output
                print("    Global output file:  " + colored(Mortician.output_file, "green"))

        if subsection == "global_var":
            if cfg["Settings"]["global_var"] is not None:
                global_var = cfg["Settings"]["global_var"]
                Mortician.var_dir = global_var
                print("    Global var directory: " +colored(Mortician.var_dir, "green"))

        if subsection == "print_ctrl":
            if cfg["Settings"]["print_ctrl"] is not None:
                if cfg["Settings"]["print_ctrl"] == "False":
                    Mortician.print_ctrl = False
            print("    Print control messages: " +colored(Mortician.print_ctrl, "green"))
        

    # Load individual game comfigurations
    print("\nLoading game configurations...")


    games = []

    for section in cfg["Games"]:
        

        gcfg = cfg["Games"][section]

        game_func = getattr(actions, gcfg["action"])
        
        if global_db is not None:
            db = global_db

        else:
            db = gcfg["db_path"]
        
        the_game = Game(section, gcfg["score_dir"], game_func, gcfg["recursive"], gcfg["watch_file"], db)
        
               
        games.append(the_game)
        print("    Loaded " + colored( the_game.name, "blue"))

    morts = []
    i = 0

    print("\nCreating morticians...")
    for game in games:

        if cfg["Games"][game.name]["output_file"] is not None:
            morts.append(Mortician(game, cfg["Games"][game.name]["output_file"])) 
        else:
            morts.append(Mortician(game, None))
 
        print("    " + colored(morts[i].game.name, "blue") + ":")
        print("        Score Dir: " + colored(game.score_directory, "green"))
        print("        Action: " + colored(game.action, "green"))
        print("        Recursive: " + colored(game.recursive, "green"))
        print("        Watchfile: " + colored(game.watchfile, "green"))
        print("        DB Path: " + colored(game.db_path, "green") + "\n")
        
        print("        Output file: " + colored(morts[i].fifo, "green") + "\n")

        i += 1
        

    return morts
