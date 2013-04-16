# Cave scene.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from os.path import dirname

# from diamond.music import Music

from data.scene import AbstractScene

# import music


class CaveScene(AbstractScene):

    def setup(self, display_layout):
        super(CaveScene, self).setup(display_layout, dirname(__file__))

        # music_ = Music()
        # music_.add(music)
        # music_.play()
        # music_.set_volume(50)
        # self.bind(music_)
