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

    def get_move(self, view):
        return (Actions.MOVE_N, Actions.DROP_NONE)
