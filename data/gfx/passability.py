# Passability types.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from json import load
from collections import OrderedDict
from os.path import splitext, dirname, join


locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
filename = join(dirname(__file__), filename)

# TODO replace all tiles in map and just use the definitions below.
sprites.update(OrderedDict((
    ('wall', {'none': [[[0, 0, 16, 16], [0, 0], [0, 0], 60]]}),
    ('platform', {'none': [[[48, 0, 16, 16], [48, 0], [0, 0], 60]]}),
    ('climb_platform', {'none': [[[16, 0, 16, 16], [16, 0], [0, 0], 60]]}),
    ('climb', {'none': [[[32, 0, 16, 16], [32, 0], [0, 0], 60]]}),
)))
