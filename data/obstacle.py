# Global obstacle classes.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.sprite import Sprite
from diamond import event


class AbstractObstacle(Sprite):
    """Abstract obstacle class which implements base functions and interfaces."""

    def __init__(self, *args, **kwargs):
        super(AbstractObstacle, self).__init__(*args, **kwargs)
        self._sector_pos = None
        self._tilematrix = None
        self._is_sector_visible = False

    def _on_playfield_sector_created_after_event(self, context):
        self._is_sector_visible = True

    def _on_playfield_sector_dropped_before_event(self, context):
        self._is_sector_visible = False

    def setup(self):
        self.listeners.extend([
            event.add_listener(
                self._on_playfield_sector_created_after_event,
                'playfield.sector.created.after',
                context__get_sector_pos__returns=self._sector_pos,
            ),
            event.add_listener(
                self._on_playfield_sector_dropped_before_event,
                'playfield.sector.dropped.before',
                context__get_sector_pos__returns=self._sector_pos,
            ),
        ])


class StickyObstacle(AbstractObstacle):
    """Obstacle which is not being cleaned up when its sector vanishes. It has to decide on its own."""

    pass


class SectorObstacle(AbstractObstacle):
    """Obstacle which is being cleanup up when its sector vanishes."""

    def _on_teardown_event(self, context):
        # print self, self._sector_pos, context, self._sector_pos == context
        return True

    def setup(self):
        super(SectorObstacle, self).setup()
        self.listeners.extend([
            event.add_listener(
                self._on_teardown_event,
                'playfield.sector.obstacles.clean_up',
                context__eq=self._sector_pos,
            ),
        ])
