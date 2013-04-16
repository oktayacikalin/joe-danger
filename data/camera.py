# Camera class which moves the scene around to keep the target in the center.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.node import Node
from diamond.sprite import Sprite


class Camera(object):

    def __init__(self, scene, target):
        assert isinstance(scene, Node)
        assert isinstance(target, Sprite) or isinstance(target, Node)
        self.scene = scene
        self.target = target

    def tick(self):
        screen_size = self.target.display.screen_size
        pos = self.target.pos
        offset = -pos[0], -pos[1]
        offset = screen_size[0] / 2 - pos[0], screen_size[1] / 2 - pos[1]
        # print pos, offset
        pos = self.scene.pos
        diff = (int((offset[0] - pos[0]) * 0.1), int((offset[1] - pos[1]) * 0.1))
        # print 'diff =', diff
        if diff[0] != 0 or diff[1] != 0:
            self.scene.set_pos_rel(*diff)
