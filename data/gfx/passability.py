# Passability types.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from collections import OrderedDict


filename = 'passability.png'

# Replace all tiles in map and just use the definitions below.
sprites = OrderedDict((
    ('wall', {'none': [[[0, 0, 16, 16], [0, 0], [0, 0], 60]]}),
    ('platform', {'none': [[[48, 0, 16, 16], [48, 0], [0, 0], 60]]}),
    ('climb_platform', {'none': [[[16, 0, 16, 16], [16, 0], [0, 0], 60]]}),
    ('climb', {'none': [[[32, 0, 16, 16], [32, 0], [0, 0], 60]]}),
))

tile_size = [16, 16]
