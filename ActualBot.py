import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
directions = [NORTH, EAST, SOUTH, WEST]
import random
import math
f = open("debug.txt", "w")


myID, game_map = hlt.get_init()
hlt.send_init("Tony's Bot")

#This functions finds the direction with the highest production
#It will average the production in a triangle in each given direction, and then return the direction with the heighest.
def fhpd(square):
##    #Go through each direction
##    h = 0
##    d = STILL
##
##    for direction, neighbor in enumerate(game_map.neighbors(square)):
##        t = 0
##        current = square
##        ls = []
##        for x in range(5):
##            t += game_map.get_target(current, direction).production
##            ls.append(game_map.get_target(current, direction))
##            ls.append(game_map.get_target(current, direction))
##            current = game_map.get_target(current, direction)
##            
##        while len(ls) > 0:
##            q = 0
##            for l in ls:
##                if q%2 == 0:
##                    t += game_map.get_target(l, (direction + 1)%3).production
##                    ls.pop(0)
##                    ls.append(game_map.get_target(l, (direction + 1)%3))
##                else:
##                    t += game_map.get_target(l, (direction + 3)%3).production
##                    ls.pop(0)
##                    ls.append(game_map.get_target(l, (direction + 3)%3))
##
##                q += 1
##            ls.pop(0)
##            ls.pop(0)
##
##        if t > h and neighbor.strength < square.strength:
##            h = t
##            d = direction
##    
##        return d
    h = 0
    d = STILL

    for direction, neighbor in enumerate(game_map.neighbors(square)):
        t = 0
        current = square
        for x in range(5):
            t += game_map.get_target(current, direction).production
            current = game_map.get_target(current, direction)
        if t > h and neighbor.strength < square.strength * 1.3 and (neighbor.owner != myID or game_map.get_target(neighbor, direction).owner != myID):
            h = t
            d = direction

    return d
            


        
        
#Get the weakest enemy (called when not surrounded by own territory preferably)
#Return still when not surrounded by  (takable) enemy
def fwe(square):
    mins = square.strength
    d = STILL
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.strength < mins and neighbor.owner != myID:
            mins = neighbor.strength
            d = direction
    
    return d

#Find nearest enemy. Returns 12 if no enemy within half map size.
def fne(square):
    d = 12
    maxD = game_map.width
    
    current = square
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        cd = direction
        current = neighbor
        dis = 0
        while dis < maxD and (current.owner == myID or current.owner == 0):
            dis += 1
            for direction2, neighbor2 in enumerate(game_map.neighbors(current)):
                if direction2 == cd:
                    current = neighbor2

        if dis < maxD:
            maxD = dis
            d = cd
    return d



    
#Find neaerest border

def fnb(square):
    d = NORTH
    maxD = game_map.width
    
    current = square
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        cd = direction
        current = neighbor
        dis = 0
        while dis < maxD and current.owner == myID:
            dis += 1
            for direction2, neighbor2 in enumerate(game_map.neighbors(current)):
                if direction2 == cd:
                    current = neighbor2

        if dis < maxD:
            maxD = dis
            d = cd
    return d
        
    
#Find highest production
def fhp(square):
    m = 0
    f = NORTH
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.production > m and neighbor.strength < square.strength:
            f = direction
        
    

    return direction




##def findenemy(square):
##    current = square 
##    #This should find and return the nearest direction towards an enemy.
##    ls1 = []
##    ls2 = []
##    ls3 = []
##
##    #go through each neighbor
##    for direction, neighbor in enumerate(game_map.neighbors(square)):
##        ls1.append(neighbor)
##        for x in range(2):
##        #for loops less than length of map
##            for current in ls1:
##                for direction1, neighbor1 in enumerate(game_map.neighbors(current)):
##                    ls2.append(neighbor1)
##            #add all neighbors from list to another list
##            ls1 = []
##            #clear first list
##            #check if anything in second list is not our own piece
##            for o in ls2:
##                if o.owner != myID and o.owner != 0:
##                    ls3.append([direction, x])
##                #if so, return direction
##            ls1 = ls2
##            ls2 = []
##            #list 1 = list 2, clear list 2
##    i = 0
##    for k in range(len(ls3)):
##        m = game_map.width
##        
##        if ls3[k][1] < m:
##            m = ls3[k][1]
##            i = k
##
##    if len(ls3) != 0:
##        f.write("test")
##        return ls3[i][0]
##    return NORTH



    
def assign_move(square):

    #If it is being attacked, i.e. has many enemies nearby, just attack
    if enemies > 30 and square.strength > square.production * 5:
        if fne(square) == 12:
            return Move(square, fnb(square))
        else:
            return Move(square, fne(square))
        
    total = 0
    #Full strength squares should head to nearest border
    if square.strength == 255:
        if fne(square) == 12:
            return Move(square, fnb(square))
        else:
            return Move(square, fne(square))



    #Go through all neighbours
    for direction, neighbor in enumerate(game_map.neighbors(square)):
       
        c = True
        total += neighbor.strength
        if neighbor.owner != myID:
            #The square is not surrounded by its own team
            c = False
            
##        if neighbor.owner != myID and neighbor.strength < square.strength:
##            #If it is next to a square of an enemy, and it is stronger, it will take it
##            
##            return Move(square, direction)
        
        #If it is next to a friendly neighbour and they are both relatively weak, try merge
        if neighbor.owner == myID and (square.strength < 80 and square.strength > 10) and (neighbor.strength < 80 and neighbor.strength > square.production):
            #remain still if the production is higher
            #make sure they do not waste too much:
            if neighbor.strength + square.strength >= 280:
                pass

            else:
                if square.production < neighbor.production:
                    return Move(square, direction)
                elif square.production == neighbor.production:
                    if random.randint(0, 1) == 1:
                        return Move(square, direction)
                    else:
                        return Move(square, STILL)
                else:
                    return Move(square, STILL)

  
                
    #Otherwise if the square is in its territory and quite strong, move towards nearest enemy preferably, or near border
    if c == True and square.strength > 40 and territory > 30:
        if fne(square) == 12:
            return Move(square, fnb(square))
        else:
            return Move(square, fne(square))


    #If it is surrounded by weak neighbors of its own type, then stay still
    if c == True and total < square.production * 12 and square.strength < 200:
        return Move(square, STILL)

    
    #If low on territory and high strength and at a border, move towards areas of high production
    if territory < 30 and square.strength > square.production * 4 and c == False:
        return Move(square, fhpd(square))
    
    #If low on territory and has medium strength, just go to nearest border (assuming it can take it)
    if territory < 30 and square.strength > square.production * 5:
        return Move(square, fwe(square))

    
    #If it is next to an enemy, take the weakest enemy
    if c == False:
        return Move(square, fwe(square))
    


        

    #If the square is weak, stay still
    return Move(square, STILL)

territory = 0
enemies = 0
while True:
    enemies = 0
    f.write("TEST")
    game_map.get_frame()
    territory = 0
    for square in game_map:
        if square.owner == myID:
            territory += 1
            for direction, neighbor in enumerate(game_map.neighbors(square)):
                if neighbor.owner != myID and neighbor.owner != 0:
                    enemies += 1
            
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)