# Cave scene.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from os.path import dirname

# from diamond.music import Music

from data.scene import AbstractScene

# import music
from obstacle.wall_pit_left import WallPitLeft
from obstacle.wall_pit_right import WallPitRight
from obstacle.arrow import Arrow


class CaveScene(AbstractScene):

    def setup(self):
        super(CaveScene, self).setup(dirname(__file__))

        # music_ = Music()
        # music_.add(music)
        # music_.play()
        # music_.set_volume(50)
        # self.bind(music_)

        self._obstacle_classes.update(dict(
            wall_pit_left=WallPitLeft,
            wall_pit_right=WallPitRight,
            arrow=Arrow,
        ))
