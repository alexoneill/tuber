from robot import Robot
from constants import Actions, TileType
import random
import time
from robot_map import RobotMap
import math

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.toHome = []             
        self.numturns = 0            
        self.goinghome = False;      
        self.targetPath = None
        self.targetDest = (0,0)
        # self.ID = player_robot.data['maxID'] + 1
        self.location = (0,0)
        # player_robot.data['maxID'] = player_robot.data['maxID'] + 1
        # print(self.ID)
        self.instance = RobotMap()

    # returns a dictionary d s.t. d[(x,y)] = ()
    # def resourcesInView(self, view):

    # returns the total amount of resources within a scale x scale box centered
    # at self.location 
    # mode = 'COUNT' or 'VALUE'
    def localValue(self,scale,mode='VALUE'):
        (x,y) = self.location
        v = 0
        for dx in range(-scale/2,scale/2):
            for dy in range(-scale/2,scale/2):
                a = self.instance[(x+dx,y+dy)]
                # res = a.resources
                tile = a.tile
                tType = tile.getType()
                if tType != TileType.Resource:
                    v += 0
                    continue
                res = tile 
                if res == None:
                    v += 0
                    continue
                unitVal = res.Value()
                amt = res.AmountRemaining()
                if mode == 'VALUE':
                    v += unitVal * amt
                else:
                    v += amt
        return v


    # returns True iff the total amount of resources within a scale x scale
    # box centered at self.location is less than a given threshold
    # mode = 'COUNT' or 'VALUE'
    def isSparse(self,scale,thresh,mode):
        return self.localValue(scale,mode) < thresh

    #returns a list [(x,y)] of locations that are adjacent to at least one 
    # def getUnexploredBoundary(self):

    def dist(self,x1,y1,x2,y2):
        return ((x2-x1)**2.0 + (y2-y1)**2.0)**0.5

    # def isMountain(x,y):
    #     tile = self.instance[(x,y)]
    #     return tile.CanMove()


    # if the local view is resource-sparse and inventory is not full,
    # choose a closest unexplored location to navigate to.
    # NOPE: returns coordinates (relative to base) of new exploration point.
    # returns first move in shortest path to that location
    # Assumes current location is deemed "sparse" (see isSparse)
    # Assumes inventory not full
    def nextDirIfIdle(self,boxDim=101):
        foundLocs = [e for e in self.instance]
        # foundLocs = self.instance.keys()
        mind,minx,miny = -1.0,-1,-1
        # minhd = ~1.0 #heuristic distance
        (rx,ry) = self.location
        for x in range(-boxDim,boxDim):
            for y in range(-boxDim,boxDim):
                
                if (x,y) in foundLocs:
                    continue
                    # tile.CanMove()
                    # tile = self.instance[(x,y)]
                d = self.dist(x,y,rx,ry)
                # minhd = heurDist(rx,ry)
                if mind < 0.0 or d < mind:
                    mind = d
                    minx = x
                    miny = y
        # return (minx,miny)
        theta = math.atan2(ry-miny,rx-minx)
        angles = dict()
        for i in range(8):
            angles[i] = math.pi/2.0 + math.pi/4.0

        nextDir,mindt = -1,-1.0
        for i in range(8):
            dt = abs(theta-angles[i])
            if mindt < 0.0 or dt<mindt:
                nextDir,mindt = i,dt

        # return (Actions.MINE, Actions.DROP_NONE)
        # return (nextDir, Actions.DROP_NONE)
        return nextDir

    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below

    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################
    def get_move(self, view):
        # Todo: update self.instance on each call here

        # Returns home if you have one resource
        if(self.storage_remaining() == 0):
            self.goinghome = True

        # How to navigate back home
        if(self.goinghome):
            # You are at home
            if(self.toHome == []):
                self.goinghome = False
                return (Actions.DROPOFF, Actions.DROP_NONE)
            # Trace your steps back home
            prevAction = self.toHome.pop()
            revAction = self.OppositeDir(prevAction)
            assert(isinstance(revAction, int))
            return (revAction, Actions.DROP_NONE)

        viewLen = len(view)
        score = 0
        # Run BFS to find closest resource

        # Search for resources
        # Updates self.targetPath, sefl.targetDest
        self.ViewScan(view)
        
        # If you can't find any resources...go in a random direction!
        actionToTake = None
        if(self.targetPath == None):
            # actionToTake = self.FindRandomPath(view)
            actionToTake = self.nextDirIfIdle(boxDim=20)

        # Congrats! You have found a resource
        elif(self.targetPath == []):
            self.targetPath = None
            return (Actions.MINE, Actions.DROP_NONE)
        else:
            # Use the first coordinate on the path as the destination , and action to move
            actionToTake = self.UpdateTargetPath()
        self.toHome.append(actionToTake)
        #markerDrop = random.choice([Actions.DROP_RED,Actions.DROP_YELLOW,Actions.DROP_GREEN,Actions.DROP_BLUE,Actions.DROP_ORANGE])
        markerDrop = Actions.DROP_NONE
        assert(isinstance(actionToTake, int))
        return (actionToTake, markerDrop)

    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        possible_paths = list()
        possible_dests = list()
        # BFS TO find the next resource within your view
        while(len(queue)>0):
            path = queue[0]
            loc = path[0]
            queue = queue[1:]
            viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
            tile = view[viewIndex[0]][viewIndex[1]][0]
            if tile.CanMove():
                for i in range(8):
                    x = loc[0] + deltas[i][0]
                    y = loc[1] + deltas[i][1]
                    if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                        if((x,y) not in visited):
                            queue.append([(x,y)] + path[1:] + [deltas[i]])
                            visited.add((x,y))
                if (tile.GetType() == TileType.Resource and
                    tile.AmountRemaining() > 0):
                    possible_paths.append(path[1:])
                    possible_dests.append(path[0])

        max_value = -1
        self.targetPath = None
        self.targetDest = None
        for i in range(len(possible_paths)):
            dest = possible_dests[i]
            viewIndex = (dest[0] + viewLen//2,dest[1]+viewLen//2)
            tile = view[viewIndex[0]][viewIndex[1]][0]
            value = tile.Value()
            units = tile.AmountRemaining()
            moves = len(possible_paths[i])
            heuristic = value * units / (units + moves)
            if heuristic > max_value:
                max_value = heuristic
                self.targetPath = possible_paths[i]
                self.targetDest = dest

        return

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)

        while(True):
            actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                                          Actions.MOVE_S,Actions.MOVE_W,
                                          Actions.MOVE_NW,Actions.MOVE_NE,
                                          Actions.MOVE_SW,Actions.MOVE_SE])
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake

        return None

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake

