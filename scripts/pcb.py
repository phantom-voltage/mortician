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

#from config import poschengband_work_dir

#def updatedb(db_path, name, prof, days, dist, kills, headshots, dmg, healed):
def update_db(dbPath, p):

    conn = sqlite3.connect(dbPath)

#    line1 = "%d - %s the %s %s, level %s, AU %d, Turns %d\n" % (p['pts'], p['name'], race, cls, clvl, p['gold'], p['turns'])
#    line2 = "Killed by %s %s\n" % (p['how'], dlvl)
    
    
    #check if db file has the requisite table#
    new = True
    
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for tname in tables:
        if tname[0] == "pcb_scores":
            new = False

    if new:
        conn.execute('''CREATE TABLE pcb_scores 
                    (id integer primary key,
                    name text,
                    pts integer,
                    sex text,
                    raceid integer,
                    classid integer,
                    pers integer,
                    clvl integer,
                    max_clvl integer,
                    dlvl integer,
                    max_dlvl integer,
                    gold integer,
                    turns integer,
                    winner integer,
                    how text,
                    ver text,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
                    
    conn.execute('''INSERT INTO pcb_scores (name, pts, sex, raceid, classid, pers, clvl, max_clvl, dlvl, max_dlvl, gold, turns, winner, how, ver, created_at)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                (str(p['name']), int(p['pts']), str(p['sex']), int(p['raceid']), int(p['classid']), int(p['pers']), int(p['clvl']), int(p['max_clvl']), int(p['dlvl']), int(p['max_dlvl']), int(p['gold']), int(p['turns']), int(0), str(p['how']), str(p['ver']), str(p['date'])))

 
    conn.commit()
    conn.close()

races = {
    0: 'Human',
    1: 'Tonberry',
    2: 'Demigod',
    3: 'Hobbit',
    4: 'Gnome',
    5: 'Dwarf',
    6: 'Snotling',
    7: 'Half-Troll',
    8: 'Amberite',
    9: 'High-Elf',
    10: 'Barbarian',
    11: 'Half-Ogre',
    12: 'Half-Giant',
    13: 'Half-Titan',
    14: 'Cyclops',
    15: 'Yeek',
    16: 'Klackon',
    17: 'Kobold',
    18: 'Nibelung',
    19: 'Dark-Elf',
    20: 'Draconian',
    21: 'Mindflayer',
    22: 'Imp',
    23: 'Golem',
    24: 'Skeleton',
    25: 'Zombie',
    26: 'Vampire',
    27: 'Spectre',
    28: 'Sprite',
    29: 'Beastman',
    30: 'Ent',
    31: 'Archon',
    32: 'Balrog',
    33: 'Dunadan',
    34: 'Shadow Fairy',
    35: 'Kutar',
    36: 'Android',
    37: 'Doppelganger',
    38: 'Jelly',
    39: 'Spider',
    40: 'Dragon',
    41: 'Lich',
    42: 'Xorn',
    43: 'Angel',
    44: 'Hound',
    45: 'Giant',
    46: 'Beholder',
    47: 'Demon',
    48: 'Hydra',
    49: 'Leprechaun',
    50: 'Troll',
    51: 'Centaur',
    52: 'Elemental',
    53: 'Sword',
    54: 'Golem',
    55: 'Quylthulg',
    56: 'Possessor',
    57: 'Vampire',
    58: 'Ring',
    59: 'Mimic',
    60: 'Wood_elf',
    61: 'Centipede',
    62: 'Vortex'
}

 
classes = {
    0: 'Warrior',
    1: 'Mage',
    2: 'Priest',
    3: 'Rogue',
    4: 'Ranger',
    5: 'Paladin',
    6: 'Warrior Mage',
    7: 'Chaos Warrior',
    8: 'Monk',
    9: 'Mindcrafter',
    10: 'High-Mage',
    11: 'Tourist',
    12: 'Imitator',
    13: 'Beastmaster',
    14: 'Sorcerer',
    15: 'Archer',
    16: 'Magic-Eater',
    17: 'Bard',
    18: 'Red-Mage',
    19: 'Samurai',
    20: 'Forcetrainer',
    21: 'Blue-Mage',
    22: 'Cavalry',
    23: 'Berserker',
    24: 'Weaponsmith',
    25: 'Mirror-Master',
    26: 'Ninja',
    27: 'Sniper',
    28: 'Time Lord',
    29: 'Blood Knight',
    30: 'Warlock',
    31: 'Archaeologist',
    32: 'Duelist',
    33: 'Wild-Talent',
    34: 'Rune Knight',
    35: 'Weaponmaster',
    36: 'Blood Mage',
    37: 'Necromancer',
    38: 'Psion',
    39: 'Rage Mage',
    40: 'Scout',
    41: 'Mauler',
    42: 'Monster',
    43: 'Mystic',
    44: 'Devicemaster',
    45: 'Yellow_mage',
    46: 'Gray-Mage',
    47: 'Skillmaster'
}

personalities = {
    0: 'Ordinary',
    1: 'Mighty',
    2: 'Shrewd',
    3: 'Pious',
    4: 'Nimble',
    5: 'Fearless',
    6: 'Combat',
    7: 'Lazy',
    8: 'Sexy',
    9: 'Lucky',
    10: 'Patient',
    11: 'Munchkin',
    12: 'Craven',
    13: 'Hasty'
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
def score_parse(path, dbPath):
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
            data = f.read(139)
            if data == "": break

            p = {
                'ver': parse_str(data[0:6]),
                'pts': parse_int(data[8:18]),
                'gold': parse_int(data[18:28]),
                'turns': parse_int(data[28:38]),
                'date': parse_date(data[38:48]),
                'name': parse_str(data[48:64]),
                'uid': parse_int(data[64:72]),
                'sex': parse_str(data[72:74]),
                'raceid': parse_int(data[74:77]),
                'classid': parse_int(data[77:80]),
                'pers': parse_int(data[80:83]),
                'clvl': parse_int(data[83:87]),
                'dlvl': parse_int(data[87:91]),
                'max_clvl': parse_int(data[91:95]),
                'max_dlvl': parse_int(data[95:99]),
                'how': parse_str(data[99:139]),
            }
            players.append(p)


    for p in players:
       update_db(dbPath, p)

    with open(".pcb_players", "wb") as out:
        pickle.dump(players, out, -1)
        
    return 

if __name__ == "__main__":
    score_parse() 
