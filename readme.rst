Player modes
============

The player can have one of the following modes:
* WALK
* JUMP
* CROUCH
* CLIMB
* ACTION
* FALL
* DIE

Use "switch_to_mode" methods to handle transitions and setup of each mode.
Use "can_switch_to_mode" to test if e.g. CLIMB is possible and makes sense.
If player gets hit by an enemy switch to DIE mode.
If player has no ground below and not in CLIMB, DIE or JUMP mode accelerate downwards.
If player has ground below and velocity >= 7.0 set velocity to -x/5 and switch to JUMP mode.
If player has ground below set velocity to 0.0.
If player has ground above and velocity <= 0.0 set JUMP energy and velocity to 0.0.
If player has ground at left or right set velocity to 0.0.

1. WALK mode

1.1 Enter indicators
* Default mode.

1.2 Possible commands
* LEFT => Move left.
* RIGHT => Move right.
* UP => Try to CLIMB up, else switch to JUMP mode.
* DOWN => Try to CLIMB down, else switch to CROUCH mode.
* ACTION => Switch to ACTION mode.

1.3 Exit indicators
* If player looses ground switch to FALL mode.

2. JUMP mode

2.1 Enter indicators
* Switch from WALK (full jump) or CLIMB (half jump) mode or bump on ground.

2.2 Possible commands
* LEFT => Move left.
* RIGHT => Move right.
* UP => Try to CLIMB up, else accelerate upwards if possible.

2.3 Exit indicators
* If player cannot jump higher anymore switch to FALL mode.
* If UP is not being pressed switch to FALL mode.

3. CROUCH mode

3.1 Enter indicators
* Switch from WALK mode.

3.2 Possible commands
* LEFT => Move left.
* RIGHT => Move right.

4. CLIMB mode

4.1 Enter indicators
* Switch from other mode.

4.2 Possible commands
* LEFT => Move left.
* RIGHT => Move right.
* UP => Move up if possible, else switch to JUMP mode.
* DOWN => Move down.

4.3 Exit indicators
* If player leaves climb passabiity tiles switch to FALL mode.

5. ACTION mode

5.1 Enter indicators
* Switch from other mode (ACTION key pressed down).

5.2 Possible commands
* SAME AS ORIENTATION => Try to press button.
* AGAINST ORIENTATION => Try to drag some box/boulder.
* UP => Try to shoot.
* DOWN => Try to place a bomb.

5.3 Exit indicators
* If ACTION key released switch to last mode.

6. FALL mode

6.1 Enter indicators
* Switch from other mode.

6.2 Possible commands
* LEFT => Move left.
* RIGHT => Move right.
* UP => Try to CLIMB up.
* DOWN => Try to CLIMB down.

6.3 Exit indicators
* If player has ground below switch to WALK mode.

7. DIE mode

7.1 Enter indicators
* Switch from other mode.

7.2 Possible commands
-

7.3 Exit indicators
* If animation is done, respawn on last save point.
