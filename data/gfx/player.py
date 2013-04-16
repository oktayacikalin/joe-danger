# Player animations.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from json import load
from collections import OrderedDict
from os.path import splitext, dirname, join


locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
filename = join(dirname(__file__), filename)

sprites.update({
    'default': {
        'none': [
            #       rect     ,  hotspot , delta , msecs
            [( 32, 64, 32, 32), ( 32, 64), (0, 0), 120],
        ],
        'look_left': [
            #       rect     ,  hotspot , delta , msecs
            [( 32, 32, 32, 32), ( 32, 32), (0, 0), 120],
        ],
        'look_right': [
            #       rect     ,  hotspot , delta , msecs
            [( 32, 64, 32, 32), ( 32, 64), (0, 0), 120],
        ],
        'walk_left': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 32, 32, 32), (  0, 32), (0, 0), 120],
            [( 32, 32, 32, 32), ( 32, 32), (0, 0), 120, 'walk_step'],
            [( 64, 32, 32, 32), ( 64, 32), (0, 0), 120],
            -1,
        ],
        'walk_right': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 64, 32, 32), (  0, 64), (0, 0), 120],
            [( 32, 64, 32, 32), ( 32, 64), (0, 0), 120, 'walk_step'],
            [( 64, 64, 32, 32), ( 64, 64), (0, 0), 120],
            -1,
        ],
        # 'climb_up': [
        #     #        rect     ,  hotspot  , delta , msecs
        #     [(  0, 96, 32, 32), (  0, 96), (0, 0), 120],
        #     [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120, 'climb_step'],
        #     [( 64, 96, 32, 32), ( 64, 96), (0, 0), 120],
        #     -1,
        # ],
        # 'climb_down': [
        #     #        rect     ,  hotspot , delta , msecs
        #     [(  0, 0, 32, 32), (  0,  0), (0, 0), 120],
        #     [( 32, 0, 32, 32), ( 32,  0), (0, 0), 120, 'climb_step'],
        #     [( 64, 0, 32, 32), ( 64,  0), (0, 0), 120],
        #     -1,
        # ],
        # 'jump_left': [
        #     #        rect     ,  hotspot , delta , msecs
        #     [(  0, 32, 32, 32), (  0, 32), (0, 0), 90, 'jump'],
        #     [(  0, 32, 32, 32), (  0, 32), (0, 0), 90],
        #     [( 32, 32, 32, 32), ( 32, 32), (0, 0), 150],
        #     [( 32, 32, 32, 32), ( 32, 32), (0, 0), 150, ['bump_on_ground', 'walk_step']],
        # ],
        # 'jump_right': [
        #     #        rect     ,  hotspot , delta , msecs
        #     [(  0, 64, 32, 32), (  0, 64), (0, 0), 90, 'jump'],
        #     [(  0, 64, 32, 32), (  0, 64), (0, 0), 90],
        #     [( 32, 64, 32, 32), ( 32, 64), (0, 0), 150],
        #     [( 32, 64, 32, 32), ( 32, 64), (0, 0), 150, ['bump_on_ground', 'walk_step']],
        # ],
    }
})



# from os.path import join, dirname


# filename = join(dirname(__file__), 'r1sprites-00.png')

# sprites = {
#     'default': {
#         'none': [
#             #       rect     ,  hotspot, delta , msecs
#             [(85, 60, 32, 32), (85, 60), (0, 0), 120],
#         ],
#         'look_left': [
#             #       rect     ,  hotspot, delta , msecs
#             [(255, 102, 32, 32), (255, 102), (0, 0), 120],
#         ],
#         'look_right': [
#             #       rect     ,  hotspot, delta , msecs
#             [(85, 60, 32, 32), (85, 60), (0, 0), 120],
#         ],
#         'walk_left': [
#             #       rect     ,  hotspot, delta , msecs
#             [(297, 102, 32, 32), (297, 102), (0, 0), 120],
#             [(340, 102, 32, 32), (340, 102), (0, 0), 120],
#             [(42, 145, 32, 32), (42, 145), (0, 0), 120],
#             [(85, 145, 32, 32), (85, 145), (0, 0), 120],
#             [(127, 145, 32, 32), (127, 145), (0, 0), 120],
#         ],
#         'walk_right': [
#             #       rect     ,  hotspot, delta , msecs
#             [(127, 60, 32, 32), (127, 60), (0, 0), 120],
#             [(170, 60, 32, 32), (170, 60), (0, 0), 120],
#             [(212, 60, 32, 32), (212, 60), (0, 0), 120],
#             [(255, 60, 32, 32), (255, 60), (0, 0), 120],
#             [(297, 60, 32, 32), (297, 60), (0, 0), 120],
#         ],
#     },
# }

# tile_size = [16, 16]
