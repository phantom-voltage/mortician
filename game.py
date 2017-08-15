#!/usr/bin/env python3

class Game(object):
    __slots__ = ['name', 'score_directory', 'action', 'recursive', 'watchfile', 'db_path']

    def __init__(self, name, score_directory, action, recursive=False, watchfile=None, db_path=None):
        self.name = name
        self.score_directory = score_directory
        self.action = action

        self.recursive = recursive
        
        self.watchfile = watchfile
    
        self.db_path = db_path
