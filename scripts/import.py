#!/usr/bin/env python

import os
import sys


from cdda import autopsy_cdda
from pcb  import score_parse as autopsy_pcb
from ang  import score_parse as autopsy_ang

def main():
    
    
    if len(sys.argv) < 4 or sys.argv[1] == "-h":
        print("import usage:")
        print("import [game] [path_to_morgue] [path_to_db]")
        
        print("\nGames supported are:")
        print("\tAngband\n\tCataclysm:DDA\n\tPoschengband")

        print("\n")
        return



    game = sys.argv[1]
    morguePath = sys.argv[2]
    dbPath = sys.argv[3]


    fileQueue = os.listdir(morguePath)
    print("%d files found!" %(len(fileQueue)))
    
    


#    print(os.listdir(os.getcwd()))

    print(game)
    print(morguePath)
    print(dbPath)
    #print(fileQueue)

#    print(morguePath+"/"+fileQueue[0])

#    rawDate = fileQueue[0].split("-")[1:7]
#    rawDate[5]=rawDate[5][:-4]
#    print(rawDate)

#    date = rawDate[0]+ "-" + rawDate[1] + "-" + rawDate[2] \
#         + " " + rawDate[3] + ":" + rawDate[4] + ":" + rawDate[5]
#    print(date)


    print("\nWe are processing %s files:\n" %(game))

    if game == "cdda":

        for f in fileQueue:
            fullPath = morguePath+"/"+f

            if os.path.isdir(fullPath) or os.path.getsize(fullPath) == 0:
                continue

            print(fullPath)
            autopsy_cdda(fullPath, dbPath)
        
        print("Import complete!\n")

    elif game == "pcb":
        
        autopsy_pcb(morguePath+"/scores.raw", dbPath)

    elif game == "ang":
        
        autopsy_ang(morguePath+"/scores.raw", dbPath)
    
        
    
    
    
        

    


    
    


if __name__ == "__main__":
    main()
