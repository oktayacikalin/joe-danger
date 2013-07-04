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
from diamond.fps import Fps
from diamond.collision import Collision
from diamond import event

from data.player import Player
from data.camera import Camera
from data.obstacle import SectorObstacle
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
        width = self.root_node.display.screen_size[0]
        fps.set_align_box(width, 0, 'right')
        fps_node.set_order_pos(10)

    def __hide_passability(self):
        layer = self.tilematrix.get_layer(self.layer_names['passability'], auto_create=True)
        layer.hide()

    def __collision_state_changed(self, context):
        # print(context)
        player = context['source']
        targets = filter(lambda item: not item.is_hidden, context['targets'])
        if targets:
            p_rect = player.get_bounding_rect()
            # print(p_rect)
            p_x, p_y = p_rect.center
            # print(p_x, p_y)
            vel_x, vel_y = player.velocity
            vel_x_max, vel_y_max = 3.0, 3.0  # player.velocity_max
            vel_x, vel_y = 0.0, 0.0
            for target in targets:
                name = target.vault.name
                # print(name)
                t_rect = target.get_bounding_rect()
                # print(t_rect)
                t_x, t_y = t_rect.center
                d_x, d_y = p_x - t_x, p_y - t_y
                if name == 'wall_pit_left':
                    d_x = max(1, abs(d_x))
                elif name == 'wall_pit_right':
                    d_x = min(-1, abs(d_x) * -1)
                # print(d_x, d_y)
                vel_x += d_x
                vel_y += d_y
            if vel_x:
                vel_x = (min(abs(vel_x), vel_x_max)) * (vel_x / abs(vel_x))
            if vel_y:
                vel_y = (min(abs(vel_y), vel_y_max)) * (vel_y / abs(vel_y))
            player.set_tint(r=100, g=50, b=50)
            player.velocity = vel_x, vel_y
            player.switch_to_mode('fall')
            self.energy -= 10
            event.emit('player.energy.changed', player)
        else:
            player.set_tint(r=100, g=100, b=100)

    def __setup_collision_detection(self):
        self.collision = Collision()
        self.ticker.add(self.collision.tick, 16)
        self.bind(
            event.add_listener(self.__collision_state_changed, 'collision.state'),
        )

    def __on_player_energy_changed(self, context):
        player = context
        print('energy = %d' % self.energy)

        if self.energy <= 0:
            print('player dies. respawn.')
            self.energy = 100
            pep = self.last_player_entry_point
            pos = pep[:3]
            player.set_pos(*self.tilematrix.translate_to_pos(*pos[:2]))

    def __setup_player(self):
        tilematrix = self.tilematrix

        # Search for possible entry points.
        player_entry_points = tilematrix.find_in_matrix_by_tilesheet('player')
        if not player_entry_points:
            raise Exception('Missing player char in tilematrix!')
        # Decide for one entry point.
        # TODO for now we just take the first one.
        pep = player_entry_points[0]
        pos = pep[:3]
        tile_id = pep[3]
        print('Found entry point with tile_id %s at: %s' % (tile_id, pos))
        # Save the list for later (e.g. respawn)
        self.last_player_entry_point = pep
        self.player_entry_points = player_entry_points
        # And now remove all entry point tiles from view.
        for pep in player_entry_points:
            tilematrix.set_tiles_at([(pep[:3] + [None])])

        # Create player object.
        player = Player.make(player_gfx, 'default')
        # Add it to the matrix.
        tilematrix.get_layer(pos[2], auto_create=True).add(player)
        # Setup player position and orientation.
        player.pos = tilematrix.translate_to_pos(*pos[:2])
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
        self.camera = Camera(tilematrix, player)
        self.camera_ticker.add(self.camera.tick, 15)

        player.setup_passability_layer(tilematrix, self.layer_names['passability'])

        # Put player into collision detection.
        self.collision.set_source(player)

        # Now put player in hands of scene itself. It will call teardown later on.
        self.manage(player)

        self.energy = 100
        self.bind(
            event.add_listener(self.__on_player_energy_changed, 'player.energy.changed'),
        )
        event.emit('player.energy.changed', player)

    def __add_obstacles_to_sector(self, context):
        sector = context
        sector_pos = sector.get_sector_pos()
        obstacles = self.sector_obstacles.get(sector_pos, [])
        # print obstacles
        tilematrix = self.tilematrix
        vault = tilematrix.get_sheet('obstacles')
        new_sprites = {}
        new_layers = {}
        # Group sprites by id for faster generation.
        for x, y, z, id in obstacles:
            pos = (tilematrix.translate_to_pos(x, y), z, (x, y, z))
            try:
                new_sprites[id].append(pos)
            except KeyError:
                new_sprites[id] = [pos]
        # Create all sprites.
        for id, sprites in new_sprites.iteritems():
            cls = self._obstacle_classes.get(id, SectorObstacle)
            _sprites = cls.make_many(vault, id, len(sprites))
            # print 'generated new sprites:', _sprites
            for pos, z, tile_pos in sprites:
                # Don't recreate already existing obstacles.
                if tile_pos in self._active_obstacles:
                    print tile_pos
                    continue
                sprite = _sprites.pop()
                sprite.pos = pos
                sprite._sector_pos = sector_pos
                sprite._tile_pos = tile_pos
                sprite._tilematrix = tilematrix
                sprite.setup()
                try:
                    new_layers[z].append(sprite)
                except KeyError:
                    new_layers[z] = [sprite]
                self._active_obstacles[tile_pos] = sprite
        # Add them to the layers.
        for z, sprites in new_layers.iteritems():
            # print 'adding %s to layer %s' % (sprites, z)
            tilematrix.get_layer(z, auto_create=True).add_children(sprites)
            self.collision.add_targets(sprites)
        event.emit('playfield.sector.created.after', sector)

    def __remove_obstacles_from_sector(self, context):
        sector = context
        event.emit('playfield.sector.dropped.before', sector)
        sector_pos = sector.get_sector_pos()
        # Let's search for sprites to be removed.
        results = event.emit('playfield.sector.obstacles.clean_up', sector_pos)
        # Extract objects of event methods.
        sprites = [meth.im_self for meth, ret in results]
        # Group them by layer.
        groups = dict()
        for sprite in sprites:
            if not sprite.parent_node:
                continue
            try:
                groups[sprite.parent_node].append(sprite)
            except KeyError:
                groups[sprite.parent_node] = [sprite]
            index = self._active_obstacles.keys()[self._active_obstacles.values().index(sprite)]
            del self._active_obstacles[index]
        # Clean everything up.
        for layer, sprites in groups.iteritems():
            # print 'removing %s from layer %s' % (sprites, layer)
            layer.remove_children(sprites)
            self.collision.remove_targets(sprites)

    def __remove_obstacle(self, context):
        print('__remove_obstacle(%s, %s)' % (self, context))
        obstacle = context
        obstacle.remove_from_parent()
        self.collision.remove_targets([obstacle])
        index = self._active_obstacles.keys()[self._active_obstacles.values().index(obstacle)]
        del self._active_obstacles[index]

    def __setup_obstacles(self):
        tilematrix = self.tilematrix
        obstacles = {}
        # Search for obstacles.
        obst_coords = tilematrix.find_in_matrix_by_tilesheet('obstacles')
        # print obst_coords
        # Now remove them from the map.
        # TODO move tile "lava" into normal tilesheet and remove filtering here.
        tiles_to_remove = []
        tilematrix__get_sector_pos = tilematrix.get_sector_pos
        for obst in obst_coords:
            x, y, z, id = obst
            if id == 'lava':
                continue
            # print obst
            tiles_to_remove.append(([x, y, z, None]))
            key = tilematrix__get_sector_pos(x, y)
            obst = [x, y, z, id]
            try:
                obstacles[key].append(obst)
            except KeyError:
                obstacles[key] = [obst]
        tilematrix.set_tiles_at(tiles_to_remove)
        # And cache them for later "recovery".
        self.sector_obstacles = obstacles
        self._obstacle_classes = {}
        self._active_obstacles = {}
        # print obstacles
        self.bind(
            event.add_listener(self.__add_obstacles_to_sector, 'tilematrix.sector.created.after'),
            event.add_listener(self.__remove_obstacles_from_sector, 'tilematrix.sector.dropped.before'),
            event.add_listener(self.__remove_obstacle, 'tilematrix.obstacle.ready_for_cleanup'),
        )

    def setup(self, data_path):
        super(AbstractScene, self).setup()
        self.add_default_listeners()
        self.ticker = Ticker()
        self.camera_ticker = Ticker()
        # self.camera_ticker = Ticker(limit=2, timeout=10)
        self.camera_ticker.is_threaded = False  # Keep in sync with display.
        self.transition_manager = TransitionManager()
        self.bind(self.ticker, self.camera_ticker, self.transition_manager)
        self.__setup_fps()

        config_file = join(data_path, 'matrix.ini')

        tilematrix = TileMatrix()
        # tilematrix.show_sector_coords = True
        tilematrix.load_config(config_file)
        # tilematrix.set_pos(0, 550)
        self.tilematrix = tilematrix

        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.layer_names = dict([(id, int(z)) for z, id in config.items('layer.names')])
        # print self.layer_names

        self.__hide_passability()
        self.__setup_collision_detection()
        self.__setup_player()
        self.__setup_obstacles()

        tilematrix.add_to(self.root_node)
        # TODO implement prefetching of tilematrix sectors if event display.update.cpu_is_idle is being emitted.
