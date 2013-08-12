# Camera class which moves the scene around to keep the target in the center.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.node import Node
from diamond.sprite import Sprite
from diamond.decorators import time


class Camera(object):

    def __init__(self, node, target):
        assert isinstance(node, Node)
        assert isinstance(target, Sprite) or isinstance(target, Node)
        self.node = node
        self.target = target

    # @time
    def tick(self, dt):
        s_w, s_h = self.node.window._screen_size
        t_x, t_y = self.target._x, self.target._y
        t_x += self.target._texture.width / 2
        t_y += self.target._texture.height / 2
        o_x, o_y = s_w / 2, s_h / 2
        # print t_x, t_y, o_x, o_y
        n_x, n_y = self.node._x, self.node._y
        d_x, d_y = (o_x - n_x - t_x), (o_y - n_y - t_y)
        # print abs(d_x), abs(d_y)
        a_x, a_y = abs(d_x), abs(d_y)
        f_x = (0.01 * (a_x / 10.0)) if a_x < 100 else 0.1
        f_y = (0.01 * (a_y / 10.0)) if a_y < 100 else 0.1
        d_x *= f_x * (1.0 + dt)
        d_y *= f_y * (1.0 + dt)
        if abs(d_x) < 0.3: d_x = 0
        if abs(d_y) < 0.3: d_y = 0
        # d_x, d_y = int(d_x), int(d_y)
        # print 'diff =', (d_x, d_y)
        if d_x != 0 or d_y != 0:
            self.node.set_position_relative(d_x, d_y)
