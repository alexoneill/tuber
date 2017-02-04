#  PlayerRobot.py
#  aoneill, wrhm, davidmcdonald13 - 02/04/17

import random
import time

from robot import Robot
from constants import Actions, TileType

from robot_map import RobotMap

class player_robot(Robot):
    def __init__(self, args):
        super(self.__class__, self).__init__(args)

        self.roadmap = RobotMap()
        self.index = 0
        self.pos = (0, 0)

    def get_move(self, view):
      if(self.index < 125):
        self.roadmap.update(self.pos, view)
        (move, (dx, dy)) = [
            (Actions.MOVE_E, (1, 0)),
            (Actions.MOVE_N, (0, 1)),
            (Actions.MOVE_W, (-1, 0))
          ][self.index % 3]

        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        print (self.pos)
      else:
        self.roadmap.update(self.pos, view)
        space = self.roadmap[self.pos[0], self.pos[1]]
        assert (space.x == self.pos[0])
        assert (space.y == self.pos[1])


        move = space.to_home
        print(self.get_turn(), self.pos, move)
        if(move is None):
          move = Actions.MOVE_N

        (x, y) = self.pos
        if(move == Actions.MOVE_N):
          y += 1
        elif(move == Actions.MOVE_S):
          y -= 1
        elif(move == Actions.MOVE_E):
          x += 1
        elif(move == Actions.MOVE_W):
          x -= 1
        elif(move == Actions.MOVE_NE):
          x += 1
          y += 1
        elif(move == Actions.MOVE_NW):
          y += 1
          x -= 1
        elif(move == Actions.MOVE_SE):
          y -= 1
          x += 1
        elif(move == Actions.MOVE_SW):
          y -= 1
          x -= 1

        self.pos = (x, y)

      self.index += 1
      return (move, Actions.DROP_NONE)
