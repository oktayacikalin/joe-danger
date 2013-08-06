#!/usr/bin/env python
#
# Main entry point for the game.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.scene import SceneManager

from data.scenes.cave.scene import CaveScene


def main():
    from diamond.helper import logging
    logging.LOG_LEVEL_THRESHOLD = logging.LOG_LEVEL_DEBUG

    manager = SceneManager()
    display = manager.setup_window(
        width=640, height=480,
        adapt_width=True, resizable=True,
        caption='Joe Danger'
    )
    manager.add_scene(CaveScene, scene_id='cave')
    manager.run('cave')

    from diamond.decorators import print_time_stats
    print_time_stats()


if __name__ == '__main__':
    main()
