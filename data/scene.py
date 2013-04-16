# Abstract scene class.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from os.path import join
# import ConfigParser

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

from diamond.scene import Scene
from diamond.tilematrix import TileMatrix
from diamond.transition import TransitionManager
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.fps import Fps

from data.player import Player
from data.camera import Camera
from data.gfx import player as player_gfx


class AbstractScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.order_matters = False
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        # fps.set_alpha(25)  # FIXME see below
        fps.add_to(fps_node)
        fps.set_align_box(self.display_layout['screen_size'][0], 0, 'right')
        fps_node.set_order_pos(10)  # FIXME confused alpha channel in display module.

    def setup(self, display_layout, data_path):
        super(AbstractScene, self).setup()
        self.display_layout = display_layout
        self.add_default_listeners()
        self.ticker = Ticker()
        self.camera_ticker = Ticker()
        self.camera_ticker.is_threaded = False  # Keep in sync with display.
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.camera_ticker, self.transition_manager)
        self.__setup_fps()

        # self.camera_ticker.drop_outdated_msecs = 100

        config_file = join(data_path, 'matrix.ini')

        tilemap = TileMatrix()
        # tilemap.show_sector_coords = True
        tilemap.load_config(config_file)
        tilemap.add_to(self.root_node)
        # tilemap.set_pos(0, 550)

        # config = ConfigParser.ConfigParser()
        # config.read(config_file)
        # layer_names = dict([(id, int(z)) for z, id in config.items('layer.names')])
        # print layer_names

        # Search for possible entry points.
        player_entry_points = tilemap.find_in_matrix('player')
        if not player_entry_points:
            raise Exception('Missing player char in tilemap!')
        # Decide for one entry point. TODO for now we just take the first one.
        pep = player_entry_points[0]
        pos = pep[:3]
        tile_id = pep[3]
        print('Found entry point with tile_id %s at: %s' % (tile_id, pos))
        # And now remove all entry point tiles from view.
        for pep in player_entry_points:
            tilemap.set_tile_at(*(pep[:3] + [None]))
        # Create player object.
        player = Player.make(player_gfx, 'default')
        # Add it to the matrix.
        tilemap.get_layer(pos[2], auto_create=True).add(player)
        # Setup player position and orientation.
        t_w, t_h = tilemap.get_tile_size()
        player.pos = t_w * pos[0], t_h * pos[1]
        player.orientation = 'right'
        # Setup player controls.
        player.set_controls(self, **dict(
            move_up=K_UP,
            move_down=K_DOWN,
            move_left=K_LEFT,
            move_right=K_RIGHT,
        ))
        # Add player tick method to camera ticker to be in sync.
        self.camera_ticker.add(player.tick, 10)

        self.camera = Camera(tilemap, player)
        self.camera_ticker.add(self.camera.tick, 10)

        # for name in layer_names:
        #     if not name.endswith('.passability'):
        #         continue
        #     layer = tilemap.get_layer(layer_names[name], auto_create=True)
        #     if layer is not None:
        #         layer.hide()
        # player.setup_passability_layers(tilemap, layer_names, pos[2])
        player.setup_passability_layer(tilemap, 1)  # TODO query matrix for layer "passability"
