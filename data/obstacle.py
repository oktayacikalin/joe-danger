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

    def set_sector_pos(self, sector_pos):
        self._sector_pos = sector_pos
        # print self, 'set sector pos', sector_pos


class StickyObstacle(AbstractObstacle):
    """Obstacle which is not being cleaned up when its sector vanishes. It has to decide on its own."""

    pass


class SectorObstacle(AbstractObstacle):
    """Obstacle which is being cleanup up when its sector vanishes."""

    def set_sector_pos(self, sector_pos):
        super(SectorObstacle, self).set_sector_pos(sector_pos)
        self.listeners.extend([
            event.add_listener(
                self._on_teardown_event,
                'playfield.sector.obstacles.clean_up',
                context__eq=sector_pos,
            ),
        ])

    def _on_teardown_event(self, context):
        # print self, self._sector_pos, context, self._sector_pos == context
        return True
