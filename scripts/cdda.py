#!/usr/bin/env python3

import sys
import re
import sqlite3
import codecs

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
            
def __updatedb(dbPath, p):
    
    conn = sqlite3.connect(dbPath)

    
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
                    ver text,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')
                    
    conn.execute('''INSERT INTO cdda_scores (name, prof, days, dist, kills, hshot, dmg, heal, cause, last, fmsg, ver, created_at)
                                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                 (str(p["name"]), str(p["prof"]), int(p["days"]), int(p["dist"]), int(p["kills"]), int(p["hshot"]), int(p["dmg"]), int(p["heal"]), p["cause"], str(p["last"]), str(p["fmsg"]), str(p["ver"]), str(p["date"])))

 
    conn.commit()
    conn.close()

    

def parse_player(date, linelist):

    ## Get version ##
    ver = __grab("Cataclysm - Dark Days Ahead version", linelist)
    ver = ver.split(" ")[6].strip()
    
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
        "fmsg" : final_message,
        "ver"  : ver,
        "date" : date
    }

    return player

#if __name__ == "__main__":
def autopsy_cdda(filePath, dbPath):

    with codecs.open(filePath, 'r', 'utf-8') as autopsy:
        linelist = autopsy.readlines()

    rawDate = filePath.split("-")[1:7]
    rawDate[5]=rawDate[5][:-4]
    
    date = rawDate[0]+ "-" + rawDate[1] + "-" + rawDate[2] \
         + " " + rawDate[3] + ":" + rawDate[4] + ":" + rawDate[5]
 

    p = parse_player(date, linelist)
   

    __updatedb(dbPath, p)


    return 
    

    
