# Mortician

## Description

This is a simple framework to monitor various games, particularly morgue or score files for roguelike games. Mortician can monitor multiple games, via threading and inotify, and write to a single or individual files for updates on the games and player's deaths.

My use case is writing to a fifo which can be used for IRC or Twitter.

## Installation

    git clone https://github.com/phantom-voltage/mortician

## Useage

### Configuration
Configure the games via the config.yaml file. The included config.yaml should provide a decent example. Most information on games and morticians is just specifying directories.

### Parser
You will need to provide a parser function written in python. Yes, this is work beyond editing a configuration file, but I find this much more entertaining than writing monitoring scripts. The parser can be in a separate file. Add the function to the actions.py file, following the other examples.

I've included some for games like:

    + Cataclysm: Dark Days Ahead
    + Angband
    + Poschengband
    + More to come...

### Running
Right now there are fancy options like passing arguments. Simply...

    ./run.py

The output should show you all the configurations made, and then display the status of the workers.

To exit...

    ctrl+c


## To Do
    
    * Clean up code and comment properly
    * Create installation script
    * Look in various directories for configuration files for Mortician
    * Create more parsers for various roguelike games
    
    



