# Obstacles.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from collections import OrderedDict


filename = 'obstacles.png'

# Replace all tiles in map and just use the definitions below.
sprites = OrderedDict((
    ('arrow', {'none': [[[0, 0, 32, 16], [0, 0], [0, 0], 60]]}),
    ('pit_bottom', {'none': [[[32, 0, 16, 16], [32, 0], [0, 0], 60]]}),
    ('wall', {'none': [[[64, 0, 32, 16], [64, 0], [0, 0], 60]]}),
    ('wall_1', {'none': [[[64, 0, 16, 16], [64, 0], [0, 0], 60]]}),
    ('wall_2', {'none': [[[80, 0, 16, 16], [80, 0], [0, 0], 60]]}),
    ('grate', {'none': [[[96, 0, 32, 16], [96, 0], [0, 0], 60]]}),
    ('stones', {'none': [[[128, 0, 32, 16], [128, 0], [0, 0], 60]]}),
    ('wall_pit_left', {'none': [[[0, 16, 32, 32], [0, 16], [0, 0], 60]]}),
    ('wall_pit_right', {'none': [[[0, 48, 32, 32], [0, 48], [0, 0], 60]]}),
    ('marble', {'none': [
        [[32, 16, 32, 32], [32, 16], [0, 0], 120],
        [[64, 16, 32, 32], [64, 16], [0, 0], 120],
    ]}),
    ('lava', {'none': [[[0, 96, 16, 16], [0, 96], [0, 0], 60]]}),
))

tile_size = [16, 16]
