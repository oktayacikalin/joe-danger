# Player animations.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

# from json import load
# from collections import OrderedDict
# from os.path import splitext, dirname, join
from os.path import dirname, join


# locals().update(load(open('%s.json' % splitext(__file__)[0], 'rb'), object_pairs_hook=OrderedDict))
# filename = join(dirname(__file__), filename)
filename = join(dirname(__file__), 'player.png')

sprites = {
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
        'jump_left': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 32, 32, 32), (  0, 32), (0, 0), 360],
            [( 32, 32, 32, 32), ( 32, 32), (0, 0), 360],
            [( 64, 32, 32, 32), ( 64, 32), (0, 0), 360],
            -1,
        ],
        'jump_right': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 64, 32, 32), (  0, 64), (0, 0), 360],
            [( 32, 64, 32, 32), ( 32, 64), (0, 0), 360],
            [( 64, 64, 32, 32), ( 64, 64), (0, 0), 360],
            -1,
        ],
        'fall_left': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 32, 32, 32), (  0, 32), (0, 0), 360],
            # [( 32, 32, 32, 32), ( 32, 32), (0, 0), 360],
            # [( 64, 32, 32, 32), ( 64, 32), (0, 0), 360],
            -1,
        ],
        'fall_right': [
            #        rect     ,  hotspot , delta , msecs
            [(  0, 64, 32, 32), (  0, 64), (0, 0), 360],
            # [( 32, 64, 32, 32), ( 32, 64), (0, 0), 360],
            # [( 64, 64, 32, 32), ( 64, 64), (0, 0), 360],
            -1,
        ],
        'crawl_look_left': [
            #       rect     ,  hotspot , delta , msecs
            [(128, 32, 32, 32), (128, 32), (0, 0), 120],
        ],
        'crawl_look_right': [
            #       rect     ,  hotspot , delta , msecs
            [(128, 64, 32, 32), (128, 64), (0, 0), 120],
        ],
        'crawl_left': [
            #        rect     ,  hotspot , delta , msecs
            [( 96, 32, 32, 32), ( 96, 32), (0, 0), 120],
            [(128, 32, 32, 32), (128, 32), (0, 0), 120, 'crawl_step'],
            [(160, 32, 32, 32), (160, 32), (0, 0), 120],
            -1,
        ],
        'crawl_right': [
            #        rect     ,  hotspot , delta , msecs
            [( 96, 64, 32, 32), ( 96, 64), (0, 0), 120],
            [(128, 64, 32, 32), (128, 64), (0, 0), 120, 'crawl_step'],
            [(160, 64, 32, 32), (160, 64), (0, 0), 120],
            -1,
        ],
        'climb_look_left': [
            #       rect     ,  hotspot , delta , msecs
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120],
        ],
        'climb_look_right': [  # Same as left!
            #       rect     ,  hotspot , delta , msecs
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120],
        ],
        'climb_up_left': [
            #        rect     ,  hotspot  , delta , msecs
            [(  0, 96, 32, 32), (  0, 96), (0, 0), 120],
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120, 'climb_step'],
            [( 64, 96, 32, 32), ( 64, 96), (0, 0), 120],
            -1,
        ],
        'climb_up_right': [  # Same as left!
            #        rect     ,  hotspot  , delta , msecs
            [(  0, 96, 32, 32), (  0, 96), (0, 0), 120],
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120, 'climb_step'],
            [( 64, 96, 32, 32), ( 64, 96), (0, 0), 120],
            -1,
        ],
        'climb_down_left': [
            #        rect     ,  hotspot , delta , msecs
            [( 64, 96, 32, 32), ( 64, 96), (0, 0), 120],
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120, 'climb_step'],
            [(  0, 96, 32, 32), (  0, 96), (0, 0), 120],
            -1,
        ],
        'climb_down_right': [  # Same as left!
            #        rect     ,  hotspot , delta , msecs
            [( 64, 96, 32, 32), ( 64, 96), (0, 0), 120],
            [( 32, 96, 32, 32), ( 32, 96), (0, 0), 120, 'climb_step'],
            [(  0, 96, 32, 32), (  0, 96), (0, 0), 120],
            -1,
        ],
    }
}

# Set fake tilesize so that we match our matrix tiles if necessary.
tile_size = [16, 16]
