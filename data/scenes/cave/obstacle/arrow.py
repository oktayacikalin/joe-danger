# Obstacle.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

import pygame

from diamond.ticker import Ticker
from diamond import event
from diamond.sound import Sound, ChannelArray
from diamond.effects import TransitionEffects

from data.obstacle import StickyObstacle


class Arrow(StickyObstacle):

    def __init__(self, *args, **kwargs):
        super(Arrow, self).__init__(*args, **kwargs)
        self.ticker = Ticker()
        self.ticker.start()
        self.transition_manager = TransitionEffects()
        self.transition_manager.start()
        self._detection_paused = False
        self.listeners.extend([
            event.add_listener(self.__on_collision_state_changed,
                               'collision.state.changed',
                               context__targets__contains=self),
        ])
        sound = Sound.get_instance()
        self.sound_array = ChannelArray(1)
        self.arrow_sound = sound.load('data/scenes/cave/sfx/arrow.ogg', volume=70)

    def __del__(self):
        self.transition_manager.join()
        self.ticker.join()
        super(Arrow, self).__del__()

    def setup(self):
        super(Arrow, self).setup()
        tilematrix = self._tilematrix
        tilematrix_rect = tilematrix.get_rect()
        # print self._tile_pos
        x, y = self._tile_pos[:2]
        direction = None
        start_pos = None
        end_pos = None

        # Check how we stuck in the wall and save the pos once.
        # z = 1 -> passability
        left = 'passability' in str(tilematrix.get_tile_id_at(x, y, 1))
        right = 'passability' in str(tilematrix.get_tile_id_at(x + 1, y, 1))
        if left and not right:
            # print 'should accel left'
            direction = -1
            start_pos = (x - 1, y)
        elif not left and right:
            # print 'should accel right'
            direction = 1
            start_pos = (x + 2, y)
        else:
            print 'completely within wall or no wall found. cannot do anything.'

        # Search for the first and last wall tile and save those positions.
        if direction == 1:
            x, y = start_pos
            while 1:
                if 'passability' in str(tilematrix.get_tile_id_at(x, y, 1)):
                    end_pos = (x + 2, y)
                    break
                x += 1
            # print start_pos, end_pos
            detection_width = end_pos[0] - start_pos[0]
        elif direction == -1:
            x, y = start_pos
            while 1:
                if 'passability/wall' in str(tilematrix.get_tile_id_at(x, y, 1)):
                    end_pos = (x - 2, y)
                    break
                x -= 1
            # print start_pos, end_pos
            detection_width = abs(end_pos[0] - start_pos[0])
        # print detection_width

        # Convert tile pos to real coords.
        start_pos = tilematrix.translate_to_pos(*start_pos)
        end_pos = tilematrix.translate_to_pos(*end_pos)
        # print start_pos, end_pos
        detection_rect = pygame.rect.Rect(start_pos, (end_pos[0] - start_pos[0], start_pos[1]))

        # Gather player and hot zones.
        player_rect = event.emit('player.get_status', 'rect')[0][1]
        detection_rect.h = player_rect.h
        # print detection_rect, player_rect        

        normalized_rect = detection_rect.copy()
        normalized_rect.normalize()

        self._detection_rect = detection_rect
        self._normalized_rect = normalized_rect
        self._detection_width = detection_width

    def on_node_added(self, *args, **kwargs):
        super(Arrow, self).on_node_added(*args, **kwargs)
        self.ticker.add(self.tick, 1000, dropable=True)

    def on_node_removed(self, *args, **kwargs):
        self.transition_manager.clear()
        self.ticker.clear()
        super(Arrow, self).on_node_removed(*args, **kwargs)

    def _unpause_detection(self):
        self._detection_paused = False

    def tick(self):
        if self._detection_paused:
            return

        tilematrix = self._tilematrix
        tilematrix_rect = tilematrix.get_rect()
        detection_rect = self._detection_rect
        normalized_rect = self._normalized_rect
        detection_width = self._detection_width

        # Gather player and hot zones.
        player_rect = event.emit('player.get_status', 'rect')[0][1]
        player_rect.x -= tilematrix_rect.x
        player_rect.y -= tilematrix_rect.y
        normalized_rect.h = player_rect.h

        # print 'tilematrix, normalized, collide =', tilematrix_rect, normalized_rect, tilematrix_rect.colliderect(normalized_rect)
        # print 'pos_real_in_tree =', self.pos_real_in_tree
        # print 'sector visible =', self._is_sector_visible  # works!

        # TODO Calculate view by taking tilematrix pos and screen size.
        screen_rect = self.display.get_rect()
        # print 'screen_rect =', screen_rect

        arrow_rect = self.get_rect()
        # print 'arrow_rect =', arrow_rect

        test_rect = normalized_rect.copy()
        test_rect.move_ip(tilematrix_rect.topleft)
        # print 'test_rect =', test_rect

        # Remove arrow and quit if sector, arrow and normalized_rect is not in view anymore.
        if not self._is_sector_visible and not arrow_rect.colliderect(screen_rect) \
            and not test_rect.colliderect(screen_rect):
            self._detection_paused = True
            self.ticker.clear()
            event.emit('tilematrix.obstacle.ready_for_cleanup', self)
            return

        # If player is in view, start to move.
        if normalized_rect.colliderect(player_rect):
            # print 'found!'
            self._detection_paused = True
            self.sound_array.play(self.arrow_sound)
            self.transition_manager.move_by(self, pos=(detection_rect.w, 0), msecs=detection_width * 20)
            x, y = tilematrix.translate_to_pos(*self._tile_pos[:2])
            self.transition_manager.add_change(self.set_pos, args=(x, y))
            self.transition_manager.add_change(self._unpause_detection, delay=500)

    def __on_collision_state_changed(self, context):
        if self._detection_paused:
            self.transition_manager.clear()
            x, y = self._tilematrix.translate_to_pos(*self._tile_pos[:2])
            self.transition_manager.add_change(self.set_pos, args=(x, y))
            self.transition_manager.add_change(self._unpause_detection, delay=1000)
