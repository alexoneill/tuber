#  robot_map.py
#  aoneill, wrhm, davidmcdonald13 - 02/04/17

import itertools

from constants import Actions, TileType

class RobotMap(object):
    def __init__(self):
        self._state = dict()

    def __getitem__(self, pos):
        return self._state[pos]

    def __delitem__(self, pos):
        del self._state[pos]

    def __contains__(self, pos):
        return (pos in self._state)

    def __len__(self):
        return len(self._state)

    def __iter__(self):
        # return self._state.iterkeys()
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
                if((best == None) or (best.dist > substate.dist)):
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
        return type('', object, {
            'x': x,
            'y': y,
            'resources': tile if(tile.GetType() == TileType.Resource) else None,
            'markers': markers,
            'dist': dist,
            'to_home': home_move
        })

    def _update_state(self, x, y, **kwargs):
        self[x, y].__dict__.update(kwargs)

    # Args:
    #   pos:   (int, int):  Tuple of global position of robot
    #   view:  (n x n x 3): List-like object describing the current world
    #                         view of the robot
    def update(self, pos, view):
        (rx, ry) = pos
        n = len(view)

        for (i, j) in itertools.product(xrange(n), xrange(n)):
            (gx, gy) = (rx + (i - (n // 2)), ry + (j - (n // 2)))
            (tile, num_robots, markers) = view[i][j]

            if((gx, gy) not in self):
                (move, dist) = self._best_move(self, gx, gy)
                self._state[(gx, gy)] = \
                    self._new_state(gx, gy, tile, markers, dist, move)
            else:
                self._update_state(gx, gy,
                    markers = markers
                )

