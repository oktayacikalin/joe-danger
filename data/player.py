# Defines the player object, it's capabilities and actions.
#
# @author    Oktay Acikalin <oktay.acikalin@gmail.com>
# @copyright Oktay Acikalin
# @license   MIT (LICENSE.txt)

from pygame.locals import KEYDOWN, KEYUP

from diamond.sprite import Sprite
from diamond import event
from diamond.sound import Sound, ChannelArray
from diamond.decorators import dump_args, time


class Player(Sprite):

    def __init__(self, *args, **kwargs):
        self.__listeners = []
        super(Player, self).__init__(*args, **kwargs)
        self.active_commands = dict()
        self.orientation = 'right'
        self.tilematrix = None
        self.passability_layer_level = None
        self.directions = None
        self.mode = 'fall'
        self.float_pos = None
        self.velocity = (0.0, 0.0)
        self.velocity_max = (3.0, 15.0)
        self.acceleration = None
        self.jump_energy = None
        self.mode_methods = dict(
            walk=self.__tick_mode_walk,
            jump=self.__tick_mode_jump,
            crouch=self.__tick_mode_crouch,
            climb=self.__tick_mode_climb,
            fall=self.__tick_mode_fall,
        )
        self.track_animation_events = True
        sound = Sound.get_instance()
        self.sound_array = ChannelArray(2)
        self.walk_sound = sound.load('data/sfx/walk.ogg', volume=48)

    def set_controls(self, scene, up, down, left, right, action):
        event.remove_listeners(self.__listeners)
        self.__listeners = [
            event.add_listener(self.__on_up_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=up),
            event.add_listener(self.__on_down_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=down),
            event.add_listener(self.__on_left_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=left),
            event.add_listener(self.__on_right_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=right),
            event.add_listener(self.__on_action_event,
                               'scene.event.system',
                               context__scene__is=scene,
                               context__event__key__eq=action),
            event.add_listener(self.__on_animation_event,
                               'sprite.animation.event',
                               context__sprite__is=self),
        ]

    def setup_passability_layer(self, tilematrix, level):
        self.tilematrix = tilematrix
        self.passability_layer_level = level
        self.__switch_to_mode(self.mode, force=True)
        self.float_pos = map(float, self.pos)

    def teardown(self):
        # print 'Player.teardown(%s)' % self
        event.remove_listeners(self.__listeners)
        self.mode_methods.clear()
        self.tilematrix = None

    def __on_up_event(self, context):
        if context.event.type == KEYDOWN:
            self.active_commands['up'] = True
        elif context.event.type == KEYUP:
            del self.active_commands['up']

    def __on_down_event(self, context):
        if context.event.type == KEYDOWN:
            self.active_commands['down'] = True
        elif context.event.type == KEYUP:
            del self.active_commands['down']

    def __on_left_event(self, context):
        if context.event.type == KEYDOWN:
            self.active_commands['left'] = True
        elif context.event.type == KEYUP:
            del self.active_commands['left']

    def __on_right_event(self, context):
        if context.event.type == KEYDOWN:
            self.active_commands['right'] = True
        elif context.event.type == KEYUP:
            del self.active_commands['right']

    def __on_action_event(self, context):
        if context.event.type == KEYDOWN:
            self.active_commands['action'] = True
        elif context.event.type == KEYUP:
            del self.active_commands['action']

    def __on_animation_event(self, context):
        if context.event == 'walk_step':
            self.sound_array.play(self.walk_sound)

    def __can_switch_to_mode(self, mode, direction=None):
        if mode == 'walk':
            return True  # Should always be possible.
        elif mode == 'climb':
            return self.__has_climb('climb_%s' % direction) and not self.__has_barrier('down')
        elif mode == 'jump':
            return not self.__has_barrier('up')
        else:
            raise Exception('Unknown mode: %s' % mode)

    # @time
    def __switch_to_mode(self, mode, force=False):
        if mode == self.mode and not force:
            print('Already in mode: %s' % mode)
            return
        self.directions = dict(
            up=[(8, -1), (16, -1), (23, -1)],
            down=[(8, 32), (16, 32), (23, 32)],
            left=[(7, 8), (7, 16), (7, 31)],
            right=[(24, 8), (24, 16), (24, 31)],
            center=[
                # (8, 8), (16, 8), (23, 8),
                # (16, 16),
                # (8, 31), (16, 31), (23, 31),
                (15, 8), (16, 8), (17, 8),
                (16, 16),
                (15, 31), (16, 31), (17, 31),
            ],
            up_left=[(8, -1), (8, 16)],
            up_right=[(23, -1), (23, 16)],
            down_left=[(8, 32), (8, 16)],
            down_right=[(23, 32), (23, 16)],
            slip_up_left=[(8, -1), (8, 16)],
            slip_up_right=[(23, -1), (23, 16)],
            slip_down_left=[(13, 32), (8, 16)],
            slip_down_right=[(18, 32), (23, 16)],
            climb_center=[
                # (8, 8), (16, 8), (23, 8),
                # (16, 16),
                # (8, 31), (16, 31), (23, 31),
                (15, 8), (16, 8), (17, 8),
                (16, 16),
                (15, 31), (16, 31), (17, 31),
            ],
            climb_down=[(15, 32), (16, 32), (17, 32)],
        )
        if mode == 'walk':
            self.set_action('look_%s' % self.orientation)
            self.acceleration = (0.2, 0.3)
            self.velocity_max = (3.0, 15.0)
        elif mode == 'jump':
            self.set_action('jump_%s' % self.orientation)
            self.acceleration = (0.2, 0.6)
            self.velocity_max = (3.0, 10.0)
            self.jump_energy = 8
        elif mode == 'crouch':
            self.set_action('crouch_look_%s' % self.orientation)
            self.acceleration = (0.2, 0.2)
            self.velocity_max = (1.0, 1.0)
            self.directions = dict(
                up=[(4, 15), (16, 15), (27, 15)],
                down=[(4, 32), (16, 32), (27, 32)],
                left=[(3, 16), (3, 31)],
                right=[(28, 16), (28, 31)],
                center=[
                    (4, 16), (16, 16), (27, 16),
                    (16, 24),
                    (4, 31), (16, 31), (27, 31),
                ]
            )
        elif mode == 'climb':
            self.set_action('climb_look_%s' % self.orientation)
            self.acceleration = (0.2, 0.2)
            self.velocity_max = (1.0, 1.0)
        elif mode == 'fall':
            self.set_action('fall_%s' % self.orientation)
            self.acceleration = (0.2, 0.3)
            self.velocity_max = (3.0, 15.0)
        else:
            raise Exception('Unknown mode: %s' % mode)
        self.mode = mode

    def __get_tiles(self, direction, off_x=0.0, off_y=0.0):
        pos_x, pos_y = self.float_pos
        vel_x, vel_y = self.velocity
        passability_layer_level = self.passability_layer_level
        get_tile_id_at = self.tilematrix.get_tile_id_at
        directions = self.directions
        ids = []
        # This fixes a problem when jumping into walls and suddenly see
        # ground below the player because of the velocity.
        if 'down' in direction:
            vel_x = 0.0
        for r_x, r_y in directions[direction]:
            r_x = int(pos_x + r_x + vel_x + off_x) / 16
            r_y = int(pos_y + r_y + vel_y + off_y) / 16
            ids.append(get_tile_id_at(r_x, r_y, passability_layer_level))
        return ids

    def __has_barrier(self, direction):
        ids = self.__get_tiles(direction)
        return 'passability/0,0' in ids

    def __has_platform(self, direction):
        ids = self.__get_tiles(direction)
        return 'passability/1,0' in ids or 'passability/3,0' in ids

    def __has_ground(self, direction):
        return self.__has_barrier(direction) or self.__has_platform(direction)

    def __has_climb(self, direction):
        ids = self.__get_tiles(direction)
        return 'passability/1,0' in ids or 'passability/2,0' in ids

    def __tick_mode_walk(self, state):
        active_commands = state['active_commands']
        vel_x = state['vel_x']
        vel_y = state['vel_y']
        vel_x_max = state['vel_x_max']
        acc_x = state['acc_x']
        acc_y = state['acc_y']
        if 'left' in active_commands:
            vel_x -= acc_x
            self.orientation = 'left'
        elif 'right' in active_commands:
            vel_x += acc_x
            self.orientation = 'right'
        elif not self.__has_ground('slip_down_left') and self.__has_ground('down_right'):
            vel_x -= acc_x
        elif not self.__has_ground('slip_down_right') and self.__has_ground('down_left'):
            vel_x += acc_x
        else:
            if vel_x < 0.0:
                vel_x += acc_x
            elif vel_x > 0.0:
                vel_x -= acc_x
            vel_x = float(int(vel_x * 10.0)) / 10.0
        if 'up' in active_commands:
            if self.__can_switch_to_mode('climb', 'center'):
                self.__switch_to_mode('climb')
            elif self.__can_switch_to_mode('jump'):
                self.__switch_to_mode('jump')
        elif 'down' in active_commands:
            if self.__can_switch_to_mode('climb', 'down'):
                vel_y += acc_y * 2
                self.__switch_to_mode('climb')
            else:
                self.__switch_to_mode('crouch')
        elif 'action' in active_commands:
            self.__switch_to_mode('action')
        if vel_x > 0.0:
            vel_x = vel_x if vel_x <= vel_x_max else vel_x_max
        elif vel_x < 0.0:
            vel_x = vel_x if vel_x >= -vel_x_max else -vel_x_max
        state['vel_x'] = vel_x
        state['vel_y'] = vel_y
        if vel_x != 0.0:
            state['action'] = 'walk'
        else:
            state['action'] = 'look'
        # If player has no ground below start falling.
        if not self.__has_ground('down'):
            self.__switch_to_mode('fall')

    def __tick_mode_jump(self, state):
        active_commands = state['active_commands']
        vel_x = state['vel_x']
        vel_x_max = state['vel_x_max']
        vel_y = state['vel_y']
        vel_y_max = state['vel_y_max']
        acc_x = state['acc_x']
        acc_y = state['acc_y']
        if 'left' in active_commands and not self.__has_barrier('up_left'):
            vel_x -= acc_x
            self.orientation = 'left'
            state['action'] = 'jump'
        elif 'right' in active_commands and not self.__has_barrier('up_right'):
            vel_x += acc_x
            self.orientation = 'right'
            state['action'] = 'jump'

        if not self.__has_barrier('slip_up_left') and self.__has_barrier('up_right'):
            vel_x -= acc_x
            if vel_y < 0.0:
                vel_y += acc_y
        elif not self.__has_barrier('slip_up_right') and self.__has_barrier('up_left'):
            vel_x += acc_x
            if vel_y < 0.0:
                vel_y += acc_y
        # If player has ground above and velocity <= 0.0 set JUMP
        # energy and velocity to 0.0.
        elif self.__has_barrier('up'):
            vel_y = 0.0
            # print('bumped on ceiling at: %s, %s' % (state['pos_x'], state['pos_y']))
            pos_y = state['pos_y']
            diff = int(round(pos_y / 16.0)) * 16 - pos_y
            # print(diff)
            pos_y += diff
            state['pos_y'] = pos_y
            state['pos_dirty'] = True
            self.__switch_to_mode('fall')
        elif 'up' in active_commands:
            if self.__can_switch_to_mode('climb', 'center'):
                self.__switch_to_mode('climb')
            elif self.jump_energy > 0:
                vel_y -= acc_y
                self.jump_energy -= 1
            else:
                self.__switch_to_mode('fall')
        else:
            self.__switch_to_mode('fall')
        if vel_x > 0.0:
            vel_x = vel_x if vel_x <= vel_x_max else vel_x_max
        elif vel_x < 0.0:
            vel_x = vel_x if vel_x >= -vel_x_max else -vel_x_max
        if vel_y > 0.0:
            vel_y = vel_y if vel_y <= vel_y_max else vel_y_max
        elif vel_y < 0.0:
            vel_y = vel_y if vel_y >= -vel_y_max else -vel_y_max
        state['vel_x'] = vel_x
        state['vel_y'] = vel_y

    def __tick_mode_crouch(self, state):
        active_commands = state['active_commands']
        vel_x = state['vel_x']
        vel_x_max = state['vel_x_max']
        acc_x = state['acc_x']
        if 'left' in active_commands:
            vel_x -= acc_x
            self.orientation = 'left'
        elif 'right' in active_commands:
            vel_x += acc_x
            self.orientation = 'right'
        # TODO implement this?
        # elif not self.__has_ground('slip_down_left') and self.__has_ground('down_right'):
        #     vel_x -= acc_x
        # elif not self.__has_ground('slip_down_right') and self.__has_ground('down_left'):
        #     vel_x += acc_x
        else:
            if vel_x < 0.0:
                vel_x += acc_x
            elif vel_x > 0.0:
                vel_x -= acc_x
            vel_x = float(int(vel_x * 10.0)) / 10.0
        if not 'down' in active_commands:
            if not self.__has_barrier('up'):
                self.__switch_to_mode('walk')
        if vel_x > 0.0:
            vel_x = vel_x if vel_x <= vel_x_max else vel_x_max
        elif vel_x < 0.0:
            vel_x = vel_x if vel_x >= -vel_x_max else -vel_x_max
        state['vel_x'] = vel_x
        if vel_x != 0.0:
            state['action'] = 'crouch'
        else:
            state['action'] = 'crouch_look'
        # If player has no ground below start falling.
        if not self.__has_ground('down'):
            self.__switch_to_mode('fall')

    def __tick_mode_climb(self, state):
        active_commands = state['active_commands']
        vel_x = state['vel_x']
        vel_x_max = state['vel_x_max']
        vel_y = state['vel_y']
        vel_y_max = state['vel_y_max']
        acc_x = state['acc_x']
        acc_y = state['acc_y']
        if 'left' in active_commands:
            vel_x -= acc_x
            self.orientation = 'left'
        elif 'right' in active_commands:
            vel_x += acc_x
            self.orientation = 'right'
        else:
            if vel_x < 0.0:
                vel_x += acc_x
            elif vel_x > 0.0:
                vel_x -= acc_x
            vel_x = float(int(vel_x * 10.0)) / 10.0
        if 'up' in active_commands:
            vel_y -= acc_y
        elif 'down' in active_commands:
            vel_y += acc_y
        else:
            if vel_y < 0.0:
                vel_y += acc_y
            elif vel_y > 0.0:
                vel_y -= acc_y
            vel_y = float(int(vel_y * 10.0)) / 10.0
        if vel_x > 0.0:
            vel_x = vel_x if vel_x <= vel_x_max else vel_x_max
        elif vel_x < 0.0:
            vel_x = vel_x if vel_x >= -vel_x_max else -vel_x_max
        if vel_y > 0.0:
            vel_y = vel_y if vel_y <= vel_y_max else vel_y_max
        elif vel_y < 0.0:
            vel_y = vel_y if vel_y >= -vel_y_max else -vel_y_max
        if self.__has_barrier('up') and vel_y < 0.0:
            vel_y = 0.0
            state['pos_dirty'] = True
        if self.__has_ground('down') and not self.__has_climb('climb_down') and vel_y > 0.0:
            vel_y = 0.0
            state['pos_dirty'] = True
            self.__switch_to_mode('walk')
        if not self.__has_climb('center'):
            self.__switch_to_mode('fall')
            vel_y -= acc_y * 3
        state['vel_x'] = vel_x
        state['vel_y'] = vel_y
        if vel_x != 0.0 or vel_y != 0.0:
            state['action'] = 'climb_up' if vel_y <= 0.0 else 'climb_down'
        else:
            state['action'] = 'climb_look'

    def __tick_mode_fall(self, state):
        active_commands = state['active_commands']
        pos_y = state['pos_y']
        vel_x = state['vel_x']
        vel_x_max = state['vel_x_max']
        vel_y = state['vel_y']
        vel_y_max = state['vel_y_max']
        acc_x = state['acc_x']
        acc_y = state['acc_y']
        if 'left' in active_commands:
            vel_x -= acc_x
            self.orientation = 'left'
            state['action'] = 'jump'
        elif 'right' in active_commands:
            vel_x += acc_x
            self.orientation = 'right'
            state['action'] = 'jump'
        elif not self.__has_ground('slip_down_left') and self.__has_ground('down_right'):
            vel_x -= acc_x
        elif not self.__has_ground('slip_down_right') and self.__has_ground('down_left'):
            vel_x += acc_x
        else:
            if vel_x < 0.0:
                vel_x += acc_x / 2.0
            elif vel_x > 0.0:
                vel_x -= acc_x / 2.0
            vel_x = float(int(vel_x * 10.0)) / 10.0
        if 'up' in active_commands:
            if self.__can_switch_to_mode('climb', 'center'):
                self.__switch_to_mode('climb')
        elif 'down' in active_commands:
            if self.__can_switch_to_mode('climb', 'down'):
                vel_y += acc_y * 2
                self.__switch_to_mode('climb')
        elif 'action' in active_commands:
            self.__switch_to_mode('action')
        # If player has ground above and velocity <= 0.0 set velocity to 0.0.
        if vel_y < 0.0 and self.__has_barrier('up'):
            vel_y = 0.0
            # print('bumped on ceiling at: %s' % ((state['pos_x'], pos_y),))
            diff = int(round(pos_y / 16.0)) * 16 - pos_y
            # print(diff)
            state['pos_y'] += diff + 1
            state['pos_dirty'] = True
        else:
            # If player is falling and has ground below...
            if vel_y >= 0.0 and self.__has_ground('down'):
                # print('bumped on floor at: %s' % ((state['pos_x'], pos_y),))
                # ...and velocity >= 7.0 set velocity to -y/5 and
                if vel_y >= 7.0:
                    vel_y = -vel_y / 5
                    # switch to JUMP mode. TODO really? I like fall mode more...
                    # self.__switch_to_mode('jump')
                else:
                    # ...set velocity to 0.0.
                    vel_y = 0.0
                    # Pull player out of barrier.
                    diff = int(round(pos_y / 16.0)) * 16 - pos_y
                    state['pos_y'] += diff
                    state['pos_dirty'] = True
                    self.__switch_to_mode('walk')  # TODO best choice?
            # If player has no ground below accelerate downwards.
            else:
                vel_y += acc_y
                # FIXME very tiny jump locks into an endless loop of -0.3 and 0.0.
        if vel_x > 0.0:
            vel_x = vel_x if vel_x <= vel_x_max else vel_x_max
        elif vel_x < 0.0:
            vel_x = vel_x if vel_x >= -vel_x_max else -vel_x_max
        if vel_y > 0.0:
            vel_y = vel_y if vel_y <= vel_y_max else vel_y_max
        elif vel_y < 0.0:
            vel_y = vel_y if vel_y >= -vel_y_max else -vel_y_max
        state['vel_x'] = vel_x
        state['vel_y'] = vel_y

    def tick(self):
        active_commands = self.active_commands.copy()  # Don't break code above.

        if 'left' in active_commands and 'right' in active_commands:
            del active_commands['left']
            del active_commands['right']
        if 'up' in active_commands and 'down' in active_commands:
            del active_commands['up']
            del active_commands['down']

        pos_x, pos_y = self.float_pos
        vel_x, vel_y = self.velocity
        vel_x_max, vel_y_max = self.velocity_max
        acc_x, acc_y = self.acceleration
        pos_dirty = False
        has_barrier = self.__has_barrier

        # TODO If player gets hit by an enemy switch to DIE mode.

        try:
            method = self.mode_methods[self.mode]
        except KeyError:
            raise Exception('Unknown mode: %s' % self.mode)
        state = dict(
            active_commands=active_commands,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_dirty=pos_dirty,
            vel_x=vel_x,
            vel_y=vel_y,
            vel_x_max=vel_x_max,
            vel_y_max=vel_y_max,
            acc_x=acc_x,
            acc_y=acc_y,
            action=None,
        )
        method(state)
        vel_x, vel_y, action = state['vel_x'], state['vel_y'], state['action']
        pos_x, pos_y, pos_dirty = state['pos_x'], state['pos_y'], state['pos_dirty']

        # If player has ground at left or right set velocity to 0.0.
        if has_barrier('left') and vel_x < 0.0:
            vel_x = 0.0
            pos_dirty = True
            # diff = int(round(pos_x / 16.0)) * 16 - pos_x - 7
            # print pos_x, diff
            # pos_x += diff
            # print pos_x
        elif has_barrier('right') and vel_x > 0.0:
            vel_x = 0.0
            pos_dirty = True

        if action and action != self.action:
            self.set_action('%s_%s' % (action, self.orientation))

        # print vel_x, vel_y, self.action, self.mode

        if vel_x != 0.0 or vel_y != 0.0 or pos_dirty:
            pos_x += vel_x
            pos_y += vel_y
            pos_dirty = True
        self.velocity = (vel_x, vel_y)

        if pos_dirty:
            self.float_pos = (pos_x, pos_y)
            self.set_pos(*map(int, self.float_pos))
