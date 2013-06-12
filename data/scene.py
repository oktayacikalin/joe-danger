# Abstract scene class.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from os.path import join
import ConfigParser

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

from diamond.scene import Scene
from diamond.tilematrix import TileMatrix
from diamond.transition import TransitionManager
from diamond.ticker import Ticker
from diamond.node import Node
from diamond.sprite import Sprite
from diamond.fps import Fps
from diamond.collision import Collision
from diamond import event

from data.player import Player
from data.camera import Camera
from data.gfx import player as player_gfx


class AbstractScene(Scene):

    def __setup_fps(self):
        fps_node = Node('fps node')
        fps_node.order_matters = False
        fps_node.add_to(self.root_node)
        fps = Fps(ticker=self.ticker, details=True)
        fps.set_alpha(75)
        fps.set_background_color(0, 0, 0, 230)
        fps.set_background_border(3)
        fps.add_to(fps_node)
        fps.set_align_box(self.display_layout['screen_size'][0], 0, 'right')
        fps_node.set_order_pos(10)

    def __hide_passability(self):
        layer = self.tilemap.get_layer(self.layer_names['passability'], auto_create=True)
        layer.hide()

    def __collision_state_changed(self, context):
        print(context)

    def __setup_collision_detection(self):
        self.collision = Collision()
        self.ticker.add(self.collision.tick, 60)
        self.bind(
            event.add_listener(self.__collision_state_changed, 'collision.state.changed'),
        )

    def __setup_player(self):
        tilemap = self.tilemap

        # Search for possible entry points.
        player_entry_points = tilemap.find_in_matrix_by_tilesheet('player')
        if not player_entry_points:
            raise Exception('Missing player char in tilemap!')
        # Decide for one entry point.
        # TODO for now we just take the first one.
        pep = player_entry_points[0]
        pos = pep[:3]
        tile_id = pep[3]
        print('Found entry point with tile_id %s at: %s' % (tile_id, pos))
        # And now remove all entry point tiles from view.
        for pep in player_entry_points:
            tilemap.set_tiles_at([(pep[:3] + [None])])
        # Save the list for later (e.g. respawn)
        self.player_entry_points = player_entry_points

        # Create player object.
        player = Player.make(player_gfx, 'default')
        # Add it to the matrix.
        tilemap.get_layer(pos[2], auto_create=True).add(player)
        # Setup player position and orientation.
        player.pos = tilemap.translate_to_pos(*pos[:2])
        player.orientation = 'right'
        # Setup player controls.
        player.set_controls(self, **dict(
            up=K_UP,
            down=K_DOWN,
            left=K_LEFT,
            right=K_RIGHT,
            action=K_SPACE,
        ))
        # Add player tick method to camera ticker to be in sync.
        self.camera_ticker.add(player.tick, 15)

        # Setup camera.
        self.camera = Camera(tilemap, player)
        self.camera_ticker.add(self.camera.tick, 15)

        player.setup_passability_layer(tilemap, self.layer_names['passability'])

        # Put player into collision detection.
        self.collision.set_source(player)

        # Now put player in hands of scene itself. It will call teardown later on.
        self.manage(player)

    def __add_obstacles_to_sector(self, context):
        sector = context
        sector_pos = sector.get_sector_pos()
        obstacles = self.sector_obstacles.get(sector_pos, [])
        # print obstacles
        tilemap = self.tilemap
        vault = tilemap.get_sheet('obstacles')
        new_sprites = {}
        new_layers = {}
        # Group sprites by id for faster generation.
        for x, y, z, id in obstacles:
            pos = (tilemap.translate_to_pos(x, y), z)
            try:
                new_sprites[id].append(pos)
            except KeyError:
                new_sprites[id] = [pos]
        # Create all sprites.
        for id, sprites in new_sprites.iteritems():
            _sprites = Sprite.make_many(vault, id, len(sprites))
            # print 'generated new sprites:', _sprites
            for pos, z in sprites:
                sprite = _sprites.pop()
                sprite.pos = pos
                try:
                    new_layers[z].append(sprite)
                except KeyError:
                    new_layers[z] = [sprite]
        # Add them to the layers.
        for z, sprites in new_layers.iteritems():
            # print 'adding %s to layer %s' % (sprites, z)
            tilemap.get_layer(z, auto_create=True).add_children(sprites)
            self.collision.add_targets(sprites)
        # And save the list for later removal.
        self.active_sector_obstacles[sector_pos] = new_layers

    def __remove_obstacles_from_sector(self, context):
        sector = context
        sector_pos = sector.get_sector_pos()
        tilemap = self.tilemap
        for z, sprites in self.active_sector_obstacles[sector_pos].iteritems():
            # print 'removing %s from layer %s' % (sprites, z)
            tilemap.get_layer(z, auto_create=True).remove_children(sprites)
            self.collision.remove_targets(sprites)
        del self.active_sector_obstacles[sector_pos]

    def __setup_obstacles(self):
        tilemap = self.tilemap
        obstacles = {}
        # Search for obstacles.
        obst_coords = tilemap.find_in_matrix_by_tilesheet('obstacles')
        # print obst_coords
        # Now remove them from the map.
        # TODO move tile "lava" into normal tilesheet and remove filtering here.
        tiles_to_remove = []
        tilemap__get_sector_pos = tilemap.get_sector_pos
        for obst in obst_coords:
            x, y, z, id = obst
            if id == 'lava':
                continue
            # print obst
            tiles_to_remove.append(([x, y, z, None]))
            key = tilemap__get_sector_pos(x, y)
            obst = [x, y, z, id]
            try:
                obstacles[key].append(obst)
            except KeyError:
                obstacles[key] = [obst]
        tilemap.set_tiles_at(tiles_to_remove)
        # And cache them for later "recovery".
        self.sector_obstacles = obstacles
        self.active_sector_obstacles = {}
        # print obstacles
        self.bind(
            event.add_listener(self.__add_obstacles_to_sector, 'tilematrix.sector.created.after'),
            event.add_listener(self.__remove_obstacles_from_sector, 'tilematrix.sector.dropped.before'),
        )

    def setup(self, display_layout, data_path):
        super(AbstractScene, self).setup()
        self.display_layout = display_layout
        self.add_default_listeners()
        self.ticker = Ticker()
        self.camera_ticker = Ticker()
        # self.camera_ticker = Ticker(limit=2, timeout=10)
        self.camera_ticker.is_threaded = False  # Keep in sync with display.
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.camera_ticker, self.transition_manager)
        self.__setup_fps()

        config_file = join(data_path, 'matrix.ini')

        tilemap = TileMatrix()
        # tilemap.show_sector_coords = True
        tilemap.load_config(config_file)
        # tilemap.set_pos(0, 550)
        self.tilemap = tilemap

        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.layer_names = dict([(id, int(z)) for z, id in config.items('layer.names')])
        # print self.layer_names

        self.__hide_passability()
        self.__setup_collision_detection()
        self.__setup_player()
        self.__setup_obstacles()

        tilemap.add_to(self.root_node)
        # TODO implement prefetching of tilemap sectors if event display.update.cpu_is_idle is being emitted.
