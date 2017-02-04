#  robot_map.py
#  aoneill, wrhm, davidmcdonald13 - 02/04/17

import itertools

from constants import Actions, TileType

class RobotMap(object):
    def __init__(self):
        self._state = dict()

        # Add home state
        self._new_state(0, 0, None, [], 0, None)

    def __getitem__(self, pos):
        return self._state[pos]

    def __setitem__(self, pos, val):
        self._state[pos] = val

    def __delitem__(self, pos):
        del self._state[pos]

    def __contains__(self, pos):
        return (pos in self._state)

    def __len__(self):
        return len(self._state)

    def __iter__(self):
        return self._state.__iter__()

    # @private
    # Args:
    #       x: Global x position (relative to home base of (0, 0))
    #       y: Global y position (relative to home base of (0, 0))
    #
    # Return:
    #       A tuple of the move to make from this position to go home, and the
    #           total distance home
    def _best_move(self, x, y):
        best = None
        looks = (-1, 0, 1)
        for (dx, dy) in itertools.product(looks, looks):
            if(not(dx == dy == 0) and ((x + dx, y + dy) in self)):
                sub_state = self[x + dx, y + dy]
                if((best == None) or (best.dist > sub_state.dist)):
                    best = sub_state

        if(best is None):
            raise Exception('_best_move: (%d, %d) not possible!' % (x, y))

        dist = best.dist + 1
        if(best.x < x):
            if(best.y < y):
                return (Actions.MOVE_SW, dist)
            elif(best.y == y):
                return (Actions.MOVE_W, dist)
            else:
                return (Actions.MOVE_NW, dist)
        elif(best.x == x):
            if(best.y < y):
                return (Actions.MOVE_S, dist)
            else:
                return (Actions.MOVE_N, dist)
        else:
            if(best.y < y):
                return (Actions.MOVE_SE, dist)
            elif(best.y == y):
                return (Actions.MOVE_E, dist)
            else:
                return (Actions.MOVE_NE, dist)

    def _new_state(self, x, y, tile, markers, dist, home_move):
        self[x, y] = type('', (object, ), {
            'x': x,
            'y': y,
            'tile': tile,
            'markers': markers,
            'dist': dist,
            'to_home': home_move
        })

    def _update_state(self, x, y, markers):
        self[x, y].markers = markers

    # From http://stackoverflow.com/a/398302/1450189
    def _spiral(self, X, Y):
        x = y = 0
        dx = 0
        dy = -1
        for i in range(max(X, Y)**2):
            if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
                yield (x, y)
            if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                dx, dy = -dy, dx
            x, y = x+dx, y+dy

    # Args:
    #   pos:   (int, int):  Tuple of global position of robot
    #   view:  (n x n x 3): List-like object describing the current world
    #                         view of the robot
    def update(self, pos, view):
        (rx, ry) = pos
        n = len(view)

        for (i, j) in self._spiral(n, n):
            (gx, gy) = (rx + i, ry + j)
            (tile, num_robots, markers) = view[i][j]

            if((gx, gy) not in self):
                (move, dist) = self._best_move(gx, gy)
                self._new_state(gx, gy, tile, markers, dist, move)
            else:
                self._update_state(gx, gy,
                    markers = markers
                )

