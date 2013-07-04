# Obstacle.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.ticker import Ticker
from diamond import event
from diamond.sound import Sound, ChannelArray
from diamond.effects import TransitionEffects

from data.obstacle import SectorObstacle


class WallPitRight(SectorObstacle):

    def __init__(self, *args, **kwargs):
        super(WallPitRight, self).__init__(*args, **kwargs)
        self.ticker = Ticker()
        self.ticker.start()
        self.transition_manager = TransitionEffects()
        self.transition_manager.start()
        self.hide()
        self.is_collapsed = True
        self.listeners.extend([
            event.add_listener(self.__on_collision_state,
                               'collision.state',
                               context__targets__contains=self),
        ])
        sound = Sound.get_instance()
        self.sound_array = ChannelArray(1)
        self.spring_sound = sound.load('data/scenes/cave/sfx/spring2.ogg', volume=90)
        self.return_sound = sound.load('data/scenes/cave/sfx/nails.ogg', volume=90)

    def __del__(self):
        self.transition_manager.join()
        self.ticker.join()
        super(WallPitRight, self).__del__()

    def on_node_removed(self, *args, **kwargs):
        self.transition_manager.clear()
        self.ticker.clear()
        super(WallPitRight, self).on_node_removed(*args, **kwargs)

    def __hide(self):
        self.hide()
        self.set_pos_rel(-32, 0)
        self.is_collapsed = True

    def __show(self):
        self.show()
        self.transition_manager.wait(3000)
        self.transition_manager.add_change(self.sound_array.play, args=[self.return_sound])
        self.transition_manager.move_by(self, pos=(32, 0), msecs=1000)
        self.transition_manager.add_change(self.__hide)

    def __on_collision_state(self, context):
        # print '***', context
        rect = self.get_bounding_rect()
        # print rect, self.get_rect()
        rect.x += 12
        rect.y += 4
        rect.w -= 12
        rect.h -= 8
        player_rect = context['source'].get_bounding_rect()
        # print rect, player_rect
        if self.is_collapsed and rect.colliderect(*player_rect):
            self.is_collapsed = False
            self.sound_array.play(self.spring_sound)
            self.ticker.clear()
            self.ticker.add(self.__show, 20, onetime=True)
