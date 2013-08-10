#!/usr/bin/env python
#
# Main entry point for the game.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from diamond.cli import Cli
from diamond.scene import SceneManager

from data.scenes.cave.scene import CaveScene


def main():
    cli = Cli(
        app_name='Joe Danger',
        app_version=0.1,
        app_description='An adventurous jump\'n\'run.',
        prog_name=__file__,
    )
    cli.add_screen_size(default='640x480')
    cli.add_fullscreen()
    cli.add_debug_logging()
    cli.add_profiler()
    args = cli.parse_args()

    manager = SceneManager()
    width, height = map(int, args.screen_size.split('x'))
    manager.setup_window(
        width=width, height=height,
        adapt_height=True, resizable=True,
        fullscreen=args.fullscreen,
        caption='Joe Danger'
    )
    manager.add_scene(CaveScene, scene_id='cave')

    cli.run(manager.run, 'cave')


if __name__ == '__main__':
    main()
