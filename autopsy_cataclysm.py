#!/usr/bin/env python

import sys
import re
import sqlite3

season_length = 14

def __grab(term, lines):
    for line in lines:
        if term in line:
            return line

def __get_line(term, lines):
    num = 0
    for line in lines:
        num = num+1 
        if term in line:
            return num
            
def __updatedb(self, p):
    
    conn = sqlite3.connect(self.game.db_path)

    
    #check if db file has the requisite table#
    new = True
    
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for tname in tables:
        if tname[0] == 'cdda_scores':
            new = False

    if new:
        conn.execute('''CREATE TABLE cdda_scores
                    (id integer primary key,
                    name text,
                    prof text,
                    days integer,
                    dist integer,
                    kills integer,
                    hshot integer,
                    dmg integer,
                    heal integer,
                    cause text,
                    last text,
                    fmsg text,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
                    
    conn.execute('''INSERT INTO cdda_scores (name, prof, days, dist, kills, hshot, dmg, heal, cause, last, fmsg)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                 (str(p["name"]), str(p["prof"]), int(p["days"]), int(p["dist"]), int(p["kills"]), int(p["hshot"]), int(p["dmg"]), int(p["heal"]), str(p["cause"]), str(p["last"]), str(p["fmsg"])))

 
    conn.commit()
    conn.close()

    

def parse_player(linelist):
    
     ## Get name ##
    name = __grab("In memory of:", linelist)
    name = name.split(':')[1].strip()

    ## Get last words, if any ##
    last_words = __grab("Last words:", linelist)

    if last_words == None:
        cause = linelist[-1]
    else:
        last_words = last_words.split("|")[3].split(":")[1].strip()
        cause = linelist[len(linelist)-2]

    ## Get cause of death and check if suicide ##
    cause = __grab("was killed in", linelist)
    cause = cause.split(' ',1)[1].strip()

    suicide_check = __grab("committed suicide", linelist)
    
    if suicide_check != None:
       cause = re.sub('was killed', 'committed suicide', cause)


    ## Get profession ##
    prof = __grab("when the apocalypse began", linelist)
    prof = prof.split("when the apocalypse began")[0]
    

    ## Ignore "he/she was a " words
    temp = prof.split(" ")
    prof = ""

    for i in range(3,len(temp)):
        prof = prof + " " + temp[i]
    prof=prof.strip() 

    ## Find number of kills ##
    kills = __grab("Total kills", linelist)

    if kills != None:
       kills = kills.split(':')[1].strip()
       kills = int(kills)
    else:
        kills = 0


    ## Find days survived ##
    day_lines = linelist[-1]
    
    season = day_lines.split(",")[1].strip()
    season = season[:-2]
    num_list = re.findall("\d+", day_lines)

    days = (int(num_list[0])-1)*56 + int(num_list[1])
    
    if season == "Summer":
        days += 14
    elif season == "Autumn":
        days += 28
    elif season == "Winter":
        days += 42

    
        
    ## Get Distance Traveled ##
    dist = __grab("Distance walked", linelist).split(":")[1].strip()
    dist = dist.split(" ")[0]

    ## Get Damage taken ##
    dmg = __grab("Damage taken", linelist).split(":")[1].strip()
    dmg = dmg.split(" ")[0]
    
    ## Get Damage healed ##
    heal = __grab("Damage healed", linelist).split(":")[1].strip()
    heal = heal.split(" ")[0]

    ## Get Headshots ##
    hshot = __grab("Headshots", linelist).split(":")[1].strip()
    hshot = hshot.split(" ")[0]

    ## Get final message ##
    num= __get_line("Kills", linelist)
    final_message = linelist[num-3].strip()
       
    ## Get final message given to player, there are probably more things I need to filter out. ##
    if final_message.count('Unknown') == 0 and final_message.count('Safe mode') == 0:
        final_message = final_message.split(' ',1)[1]
        final_message = final_message[:-1]
        final_message = re.sub('AM|PM', '', final_message).strip()
    
         #__updatedb(self, name, prof, days, dist, kills, hshot, dmg, heal)
    player = {
        "name" : name,
        "prof" : prof,
        "days" : days,
        "dist" : dist,
        "kills": kills,
        "hshot": hshot,
        "dmg": dmg,
        "heal": heal,
        "cause" : cause,
        "last" : last_words,
        "fmsg" : final_message
    }

    return player

#if __name__ == "__main__":
def autopsy_cdda(self, file_path):

    try:
        autopsy = open(file_path, 'r')
    except IOError:
        print("Could not open %s"%(file_path))

    ## File stuff ##
    with autopsy:
        linelist = autopsy.readlines()

    p = parse_player(linelist)
   
    
    ## Create first line of output
    msg = "%s, the %s, %s"%(p["name"], p["prof"], p["cause"])

    if p["last"] != None:
        msg += " \"" + p["last"] + "\"\n"
    else:
        msg += "\n"


    if p["fmsg"] != None:
        msg += "[" + p["fmsg"] +"]" + "\n"

    msg += "Days: %d Kills: %d Dist: %s Dmg: %s heal: %s hshot: %s\n" %(p["days"], p["kills"], p["dist"], p["dmg"], p["heal"], p["hshot"])

    if self.game.db_path is not None:
         __updatedb(self, p)


    return msg
    

    
