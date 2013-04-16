#!/usr/bin/env python
#
# Main entry point for the game.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.scene import SceneManager

from data.scenes.cave.scene import CaveScene


# Display options
DISPLAY_LAYOUT = {
    'screen_size': (640, 480),
    # 'screen_size': (1024, 576),
    'framerate': 60,
    'scaling': 1.00,  # 1.0 is normal; 2.0 would be double window size.
    # 'fullscreen': True,
}


def main():
    from diamond.helper import logging
    logging.LOG_LEVEL_THRESHOLD = logging.LOG_LEVEL_DEBUG

    manager = SceneManager()
    display = manager.setup_display(**DISPLAY_LAYOUT)
    display.set_caption('Joe Danger')
    manager.add_scene(CaveScene, scene_id='cave', display_layout=DISPLAY_LAYOUT)
    manager.run('cave')


if __name__ == '__main__':
    main()
