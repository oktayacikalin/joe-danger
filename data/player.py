from pygame.locals import KEYDOWN, KEYUP

from diamond.sprite import Sprite
from diamond import event


class Player(Sprite):

    def __init__(self, *args, **kwargs):
        self.__listeners = []
        super(Player, self).__init__(*args, **kwargs)
        self.move_directions = dict()
        self.orientation = 'right'
        self.tilematrix = None
        self.passability_layer_level = None
        self.acceleration = 0.2, 0.3
        self.velocity = 0.0, 0.0
        self.velocity_max = 3.0, 15.0
        self.exact_pos = None
        self.jump_energy_max = 8
        self.jump_energy = self.jump_energy_max

    def set_controls(self, scene, move_up, move_down, move_left, move_right):
        event.remove_listeners(self.__listeners)
        self.__listeners = [
            event.add_listener(self.__on_move_up_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=move_up),
            event.add_listener(self.__on_move_down_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=move_down),
            event.add_listener(self.__on_move_left_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=move_left),
            event.add_listener(self.__on_move_right_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=move_right),
            # event.add_listener(self.__on_animation_event,
            #                    'sprite.animation.event',
            #                    context__sprite__is=self),
            # TODO shooting
            # TODO pushing
            # TODO switching
            # TODO placing bombs
        ]

    def setup_passability_layer(self, tilematrix, level):
        self.tilematrix = tilematrix
        self.passability_layer_level = level
        self.exact_pos = map(float, self.pos)

    def __del__(self):
        event.remove_listeners(self.__listeners)
        super(Player, self).__del__()

    def __on_move_up_event(self, context):
        if context.event.type == KEYDOWN:
            self.move_directions['up'] = True
        elif context.event.type == KEYUP:
            del self.move_directions['up']

    def __on_move_down_event(self, context):
        if context.event.type == KEYDOWN:
            self.move_directions['down'] = True
        elif context.event.type == KEYUP:
            del self.move_directions['down']

    def __on_move_left_event(self, context):
        if context.event.type == KEYDOWN:
            self.move_directions['left'] = True
        elif context.event.type == KEYUP:
            del self.move_directions['left']

    def __on_move_right_event(self, context):
        if context.event.type == KEYDOWN:
            self.move_directions['right'] = True
        elif context.event.type == KEYUP:
            del self.move_directions['right']

    def tick(self):
        move_directions = self.move_directions.copy()  # TODO do we need copy?

        if 'left' in move_directions and 'right' in move_directions:
            del move_directions['left']
            del move_directions['right']
        if 'up' in move_directions and 'down' in move_directions:
            del move_directions['up']
            del move_directions['down']

        v_x, v_y = self.velocity
        v_x_max, v_y_max = self.velocity_max
        a_x, a_y = self.acceleration
        action = None
        f_x, f_y = self.exact_pos
        pos_dirty = False

        if move_directions:
            # print self.pos
            # print move_directions

            if 'left' in move_directions:
                v_x -= a_x
                self.orientation = 'left'
                action = 'walk'
            elif 'right' in move_directions:
                v_x += a_x
                self.orientation = 'right'
                action = 'walk'
            if 'up' in move_directions:
                if v_y <= 0.0 and self.jump_energy > 0:
                    v_y -= a_y * 2.0
                    self.jump_energy -= 1
                    # print 'JUMP'
            elif self.jump_energy > 0:
                self.jump_energy = 0
            if v_y == 0.0:
                self.jump_energy = self.jump_energy_max

            v_x = v_x if v_x <= v_x_max else v_x_max
            v_x = v_x if v_x >= -v_x_max else -v_x_max
        elif v_y == 0.0:
            self.jump_energy = self.jump_energy_max
        else:
            self.jump_energy = 0

        if v_x < 0.0 and 'left' not in move_directions:
            v_x += a_x
            v_x = float(int(v_x * 10.0)) / 10.0
        elif v_x > 0.0 and 'right' not in move_directions:
            v_x -= a_x
            v_x = float(int(v_x * 10.0)) / 10.0

        # Remove floating point errors from velocity.
        # v_x = float(int(v_x * 10.0)) / 10.0
        # v_y = float(int(v_y * 10.0)) / 10.0

        border_radius = 10  # Player border size.
        slip_radius = 13  # Player border size for slipping around edges.
        direction_data = dict(
            right=((32 - border_radius, 0 + border_radius), (32 - border_radius, 31 - border_radius)),
            left=((-1 + border_radius, 0 + border_radius), (-1 + border_radius, 31 - border_radius)),
            fall_down=((0 + border_radius, 32), (16, 32), (31 - border_radius, 32)),
            slip_left=((0 + slip_radius, 32), (0, 32)),
            slip_right=((31 - slip_radius, 32), (32, 32)),
            up=((0 + border_radius, -1), (16, -1), (31 - border_radius, -1)),
        )

        passability_layer_level = self.passability_layer_level
        get_tile_id_at = self.tilematrix.get_tile_id_at
        x, y = self.pos  # current pos

        def can(direction):
            if direction in direction_data:
                if type(direction_data[direction]) is not bool:
                    result = True
                    for r_x, r_y in direction_data[direction]:
                        r_x = int(x + r_x + v_x) / 16
                        r_y = int(y + r_y + v_y) / 16
                        id = get_tile_id_at(r_x, r_y, passability_layer_level)
                        # print('inspected point %s has id: %s' % ((r_x, r_y), id))
                        if id == 'passability/0':
                            result = False
                            break
                    direction_data[direction] = result
                return direction_data[direction]
            else:
                return False

        if v_x > 0.0:  # Wall to the right?
            if not can('right'):
                v_x = 0.0
        if v_x < 0.0:  # Wall to the left?
            if not can('left'):
                v_x = 0.0
        if v_y < 0.0:  # Wall to the top?
            if not can('up'):
                # print 'NO GO UP'
                v_y = 0.0
                # print('bumped on ceiling at: %s' % ((x, y),))
                diff = int(round(f_y / 16.0)) * 16 - f_y
                # print(diff)
                f_y += diff
                pos_dirty = True

        if self.jump_energy in (0, self.jump_energy_max) and can('fall_down'):  # Not jumping and nothing to stand on?
            v_y += a_y
            v_y = v_y if v_y <= v_y_max else v_y_max
        if v_y > 0.0 and not can('fall_down'):  # Fallen on something?
        # if not can('fall_down'):  # Fallen on something?
            speed = v_y
            if speed > 7:
                v_y = float(int(-(speed / 5.0) * 10.0)) / 10.0
            else:
                # print 'STOP V_Y'
                v_y = 0.0
            # print('bumped on floor at: %s' % ((x, y),))
            diff = int(round(f_y / 16.0)) * 16 - f_y
            # print(diff)
            f_y += diff
            pos_dirty = True

        if v_x == 0.0 and v_y == 0.0 and not can('fall_down'):  # Not jumping or falling?
            # Down right is empty?
            if can('slip_right'):
                v_x += a_x * 2.0
                action = 'walk' if action in ('look', None) else action
            # Down left is empty?
            if can('slip_left'):
                v_x -= a_x * 2.0
                action = 'walk' if action in ('look', None) else action

        if v_x > 0.0:  # Wall to the right?
            if not can('right'):
                v_x = 0.0
        if v_x < 0.0:  # Wall to the left?
            if not can('left'):
                v_x = 0.0
        if not can('fall_down'):  # Standing on ground?
            diff = int(round(f_y / 16.0)) * 16 - f_y
            # And stuck within a wall tile?
            if diff > 0.0:
                v_y -= a_y
                # print(diff)
            elif diff < 0.0:
                v_y += a_y
                # print(diff)

        self.velocity = v_x, v_y

        # Fix animations in exotic states.
        if v_x == 0.0 and v_y == 0.0 and self.action.startswith('walk_'):
            if 'left' not in move_directions and 'right' not in move_directions:
                action = 'look'

        if action:
            # FIXME engine does not update immediately. e.g. left->right->left->right
            self.set_action('%s_%s' % (action, self.orientation))
            # print(self.action)

        # Now move sprite.
        if v_x != 0.0 or v_y != 0.0:
            f_x += v_x
            f_y += v_y
            # Remove floating point errors from exact position.
            f_x = float(int(f_x * 10.0)) / 10.0
            f_y = float(int(f_y * 10.0)) / 10.0
            pos_dirty = True

        if pos_dirty:
            self.exact_pos = f_x, f_y
            self.set_pos(int(f_x), int(f_y))
            # print(self.exact_pos, self.velocity)
