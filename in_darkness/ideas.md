## Goal of the game:

To collect as many coins as possible

## Player challenges:

1) There are monsters roaming around (using simple vertical and horizontal movement)
2) When a coin is grabbed, all monsters move towards that coin for a few frames
3) The game is in darkness, except for a cone of light and an area around the player

## Technical challenges:

1) Smooth movement. Because there is a light cone, I'd like for movement to be available outside of a grid
2) Enemy movement. So far we've done all movement along x,y axis. This will require diagonal movement.
3) The biggest issue I anticipate is the use of darkness. From what I understand, I can use a PNG file as a mask for the darkness, but if I am limited to the coin, door, monster, and robot PNGs then it might be difficult to pull off.

## Plan:

1) Establish a playable surface area
2) Create a playable character
	1) Establish movement
3) Place coins in random spots
	1) Implement grabbing coins
4) Place monsters in random spots
	1) Add randomized movement
	2) Get collisions with player
5) Add darkness and light
	1) Stretch: add fading mechanic for light area
	2) Stretch: and flashlight
