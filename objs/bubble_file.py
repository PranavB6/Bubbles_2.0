from objs.constants import *
from math import sin, cos
import random, time
import pygame.gfxdraw

class Bubble():

	def __init__(self, pos, color = None):

		if color is None: self.color = random.choice(BUBBLE_COLORS)
		else:			  self.color = color

		self.pos = pos
		self.radius = BUBBLE_RADIUS

		self.shake_options = [-1, 0, 1]

	def shake(self):
		if self.color == BG_COLOR: return

		x, y = self.pos[0], self.pos[1]

		self.pos = ( x + random.choice(self.shake_options), y + random.choice(self.shake_options))
		self.draw()
		self.pos = (x, y)

	def draw(self):

		if self.color == BG_COLOR: return

		x, y = int(self.pos[0]), int(self.pos[1])

		# pg.draw.circle(display, self.color, (x,y), self.radius)

		pg.gfxdraw.filled_circle(display, x, y, BUBBLE_RADIUS, self.color)

		r, g, b = self.color
		offset = 110
		outline_color = (max(r - offset, 0), max(g - offset, 0), max(b - offset, 0))
		pg.gfxdraw.aacircle(display, x, y, BUBBLE_RADIUS, outline_color)



class Bullet(Bubble):

	def __init__(self, pos, angle, color = None):
		super().__init__(pos, color)

		self.dx = cos(angle) * BUBBLE_VEL
		self.dy = -sin(angle) * BUBBLE_VEL

		self.pos = pos
		self.exists = True

	def update(self):

		if self.exists:

			x, y = self.pos

			if   (x - BUBBLE_RADIUS) <= WALL_BOUND_L: self.dx *= -1
			elif (x + BUBBLE_RADIUS) >= WALL_BOUND_R: self.dx *= -1

			self.pos = (x + self.dx, y + self.dy)

			self.draw()


class GridBubble(Bubble):

	def __init__(self, row, col, pos, exists = True, color = None):

		super().__init__(pos, color)

		self.row = row
		self.col = col
		self.exists = exists

		self.L = None
		self.R = None
		self.UL = None
		self.UR = None
		self.DL = None
		self.DR = None 

	def getComrades(self):

		comrades = [self.UR, self.UL, self.R, self.L, self.DR, self.DL]
		alive_comrades = []

		for comrade in comrades: 
			if comrade: 
				alive_comrades.append(comrade)

		return alive_comrades

	def pop(self):
		if self.exists == False: raise ValueError('Trying to pop bubble that doesn\'t exist: ({}, {})'.format(self.row, self.col))

		frames = []
		x, y = int(self.pos[0]), int(self.pos[1])
		dy = 1
		dyy = 0.5

		while (y - BUBBLE_RADIUS) < DISP_H:
			dy += dyy
			y += dy
			frames.append(Bubble((x, y), self.color))

		frames = frames[::-1]

		self.exists = False
		self.color = BG_COLOR
		return frames