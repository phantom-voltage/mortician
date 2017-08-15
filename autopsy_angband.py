#!/usr/bin/python
#
# by Erik Osheim
#
# External score parser/printer for Angband. It hardcores some
# values from p_races.txt and classes.txt for simplicitly.
# Should basically mimic the built-in format.
#
# One caveat: does not currently display the current (living)
# character, since this character's information is not in the
# score file.
#
# Seems to work as of 2014-07-04 (1aba7a8).

import os, sys
import cPickle as pickle
import sqlite3

#from config import angband_work_dir

#def updatedb(db_path, name, prof, days, dist, kills, headshots, dmg, healed):
def updatedb(self, p):

    conn = sqlite3.connect(self.game.db_path)

#    line1 = "%d - %s the %s %s, level %s, AU %d, Turns %d\n" % (p['pts'], p['name'], race, cls, clvl, p['gold'], p['turns'])
#    line2 = "Killed by %s %s\n" % (p['how'], dlvl)
    
    
    #check if db file has the requisite table#
    new = True
    
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for tname in tables:
        if tname[0] == "ang_scores":
            new = False

    if new:
        conn.execute('''CREATE TABLE ang_scores 
                    (id integer primary key,
                    name text,
                    pts integer,
                    raceid integer,
                    classid integer,
                    clvl integer,
                    max_clvl integer,
                    dlvl integer,
                    max_dlvl integer,
                    gold integer,
                    turns integer,
                    winner integer,
                    how text,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
                    
    conn.execute('''INSERT INTO ang_scores (name, pts, raceid, classid, clvl, max_clvl, dlvl, max_dlvl, gold, turns, winner, how)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                (str(p['name']), int(p['pts']), int(p['raceid']), int(p['classid']), int(p['clvl']), int(p['max_clvl']), int(p['dlvl']), int(p['max_dlvl']), int(p['gold']), int(p['turns']), int(0), str(p['how'])))

 
    conn.commit()
    conn.close()

 
races = {
    0: 'Human',
    1: 'Half-Elf',
    2: 'Elf',
    3: 'Hobbit',
    4: 'Gnome',
    5: 'Dwarf',
    6: 'Half-Orc',
    7: 'Half-Troll',
    8: 'Dunadan',
    9: 'High-Elf',
    10: 'Kobold',
}

classes = {
    0: 'Warrior',
    1: 'Mage',
    2: 'Priest',
    3: 'Rogue',
    4: 'Ranger',
    5: 'Paladin',
}

# remove trailing nulls/spaces
def trim(s):
    i = len(s) - 1
    while s[i] == '\0' or s[i] == ' ':
        i -= 1
    return i + 1

# parse a (decimal) integer
def parse_int(s):
    i = trim(s)
    return int(s[:i])

# parse a string
def parse_str(s):
    i = trim(s)
    return str(s[:i])

# parse a date. input format is @YYYYMMDD?
def parse_date(s):
    return s[1:5] + '-' + s[5:7] + '-' + s[7:9]

# display a player dictionary
def format(p):
    race = races.get(p['raceid'], 'Unknown')
    cls = classes.get(p['classid'], 'Unknown')

    if p['max_clvl'] == p['clvl']:
        clvl = p['clvl']
    else:
        clvl = '%s (Max %s)' % (p['clvl'], p['max_clvl'])

    if p['dlvl'] > 0:
        dlvl = 'on dungeon level %s' % p['dlvl']
    else:
        dlvl = 'in the town'

    if p['max_dlvl'] != p['dlvl']:
        dlvl = '%s (Max %s)' % (dlvl, p['max_dlvl'])

    line1 = "%d - %s the %s %s, level %s, AU %d, Turns %d\n" % (p['pts'], p['name'], race, cls, clvl, p['gold'], p['turns'])
    line2 = "Killed by %s %s\n" % (p['how'], dlvl)
    
    return line1+line2

# mighty main method
def score_parse(self,path):
#    if len(sys.argv) < 2:
#        print 'usage: %s SAVEFILE' % sys.argv[0]
#        print '    (e.g. lib/scores/scores.raw)'
#        sys.exit(1)

#    path = sys.argv[1]

    if not os.path.exists(path):
        print ('error: %r was not found' % path)
        sys.exit(2)

    with open(path, 'rb') as f:
        players = []
        while True:
            data = f.read(126)
            if data == "": break

            p = {
                'pts': parse_int(data[8:18]),
                'gold': parse_int(data[18:28]),
                'turns': parse_int(data[28:38]),
                'date': parse_date(data[38:48]),
                'name': parse_str(data[48:64]),
                'uid': parse_int(data[64:72]),
                'raceid': parse_int(data[72:75]),
                'classid': parse_int(data[75:78]),
                'clvl': parse_int(data[78:82]),
                'dlvl': parse_int(data[82:86]),
                'max_clvl': parse_int(data[86:90]),
                'max_dlvl': parse_int(data[90:94]),
                'how': parse_str(data[94:126]),
            }
            players.append(p)


    with open(self.var_dir+"/.angband_players", 'rb') as out:
        old_players = pickle.load(out)

    msg = ""
    for p in players:
        if p not in old_players:
            msg += format(p)
            
            if self.game.db_path is not None :
                updatedb(self,p)
        
    with open(self.var_dir+"/.angband_players", 'wb') as out:
        pickle.dump(players, out, -1)

    #print(msg)
    return msg

if __name__ == "__main__":
    score_parse() 
