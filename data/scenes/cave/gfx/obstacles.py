# Obstacles.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

# from json import load
from collections import OrderedDict
# from os.path import splitext, dirname, join
from os.path import dirname, join


# locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
# filename = join(dirname(__file__), filename)
filename = join(dirname(__file__), 'obstacles.png')

# TODO replace all tiles in map and just use the definitions below.
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
