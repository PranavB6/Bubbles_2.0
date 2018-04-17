import time, random
from constants import *
from bubble_file import *
from math import sqrt
import pygame as pg

class GridManager():

	def __init__(self):
		self.rows = GRID_ROWS
		self.cols = GRID_COLS
		self.even_offset = True
		self.targets = []

		self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]

		for row in range(self.rows):
			for col in range(self.cols):
				pos = self.calcPos(row, col, self.even_offset)
				self.grid[row][col] = GridBubble(row, col, pos)


		for row in range(self.rows):
			for col in range(self.cols):
				self.findComrades(self.grid[row][col])

		self.appendBottom()
		self.findTargets()
		self.collided = False
		self.collision_counter = 0
		self.animations = []
		self.paths = []
		self.prev_time = 0

	def view(self, gun, game):

		if gun.fired.exists: self.checkCollision(gun.fired)

		if self.collided: 
			self.collision_counter += 1
			bubble = self.reviveBubble(gun.fired)			
			self.updateRows()
			self.popCluster(bubble, game)
			self.findTargets()
			self.checkGameOver(game)
			self.collided = False

		self.draw()

	def checkGameOver(self, game):

		if self.rows < GAMEOVER_ROWS: return

		for col in range(self.cols):
			if self.grid[GAMEOVER_ROWS - 1][col].exists:
				game.over = True
				return	


	def checkCollision(self, bullet):

		bullet_x, bullet_y = bullet.pos
		bullet_x += bullet.dx
		bullet_y += bullet.dy

		for target in self.targets:
			target_x, target_y = target.pos

			L = target_x - (HITBOX_SIZE/2)
			R = target_x + (HITBOX_SIZE/2)
			U = target_y - (HITBOX_SIZE/2)
			D = target_y + (HITBOX_SIZE/2)

			if (bullet_y - (HITBOX_SIZE/2)) < D:		
				if (bullet_x + (HITBOX_SIZE/2)) > L:	
					if (bullet_x - (HITBOX_SIZE/2)) < R:			
						if (bullet_y + (HITBOX_SIZE/2)) > U:
							bullet.exists = False
							self.collided = True

		if bullet_y < 0: 
			bullet.exists = False
			self.collided = True

	def reviveBubble(self, bullet):

		collide_point = bullet.pos

		imaginary = []
		dists = []

		for row in range(self.rows):
			for col in range(self.cols):
				if not self.grid[row][col].exists:
					imaginary.append(self.grid[row][col])

		for bubble in imaginary:
			x,y = collide_point
			bubble_x, bubble_y = bubble.pos

			dist = sqrt( (((x - bubble_x) ** 2) + (y - bubble_y) ** 2) )
			dists.append(dist)

		idx = dists.index(min(dists))
		replacement = imaginary[idx]

		replacement.exists = True
		replacement.color = bullet.color

		return replacement

	def updateRows(self):

		if (self.collision_counter % APPEND_COUNTDOWN == 0) and (self.collision_counter != 0): self.appendTop()

		for col in range(self.cols):
			if self.grid[self.rows-1][col].exists:
				self.appendBottom()
				return

		for col in range(self.cols):
			if self.grid[self.rows - 2][col].exists:
				return

		self.deleteBottom()


	def appendTop(self):

		for row in range(self.rows):
			for col in range(self.cols):
				self.grid[row][col].row += 1

		new_row = []
		self.rows += 1
		self.even_offset = not self.even_offset

		for col in range(self.cols):
			pos = self.calcPos(0, col, self.even_offset)
			new_row.append(GridBubble(0, col, (0,0)))

		self.grid.insert(0, new_row)

		for row in range(self.rows):
			for col in range(self.cols):
				self.grid[row][col].pos = self.calcPos(row, col, self.even_offset)
				if (row == 0) or (row == 1): self.findComrades(self.grid[row][col])	

	def appendBottom(self):

		row = []

		for col in range(self.cols):
			pos = self.calcPos(self.rows, col, self.even_offset)
			row.append(GridBubble(self.rows, col, pos, exists = False, color = BG_COLOR))

		self.grid.append(row)

		self.rows += 1

		for row in range(self.rows - 3, self.rows):
			for col in range(self.cols):
				self.findComrades(self.grid[row][col])

	def deleteBottom(self):
		self.grid.pop()
		self.rows -= 1

		for col in range(self.cols):
			self.findComrades(self.grid[self.rows - 1][col])



	def popCluster(self, bubble, game):

		cluster = self.findCluster(bubble)

		if (len(cluster) >= 3) or (bubble.color == BLACK):			
			while len(cluster) > 0:
				bubble = cluster.pop()

				frames = bubble.pop()
				self.animations.append(frames)

				game.score += 1

				for comrade in bubble.getComrades():
					if comrade.exists and (comrade not in cluster):
						rooted = self.findRoot(comrade)
						if not rooted: cluster.append(comrade)


	def findCluster(self, bubble, reached = None):
		
		if reached == None: reached = []

		for comrade in bubble.getComrades():
			if comrade.exists:
				if (comrade not in reached) and ((comrade.color == bubble.color) or (bubble.color == BLACK)):
					reached.append(comrade)
					reached = self.findCluster(comrade, reached)

		return reached

	def findRoot(self, bubble, reached = None, rooted = False):

		# print('row, col = ({}, {})'.format(bubble.row, bubble.col))

		if reached == None:	reached = []

		if bubble.row == 0:
			self.paths.append(reached)
			return True

		for comrade in bubble.getComrades():
			if comrade.exists and (comrade not in reached):
				reached.append(comrade)

				rooted = self.findRoot(comrade, reached)
				if rooted:	return True



		return rooted
		

	def findComrades(self, bubble):
		bubble.L = None
		bubble.R = None
		bubble.UL = None
		bubble.UR = None
		bubble.DL = None
		bubble.DR = None

		even_offset = self.even_offset
		row = bubble.row
		col = bubble.col

		if col > 0: bubble.L = self.grid[row][col - 1]
		if col < (self.cols - 1): bubble.R = self.grid[row][col + 1]
		
		if not ((row % 2) == even_offset):  
			if row > 0:
				bubble.UL = self.grid[row - 1][col]

				if col < (self.cols - 1):
					bubble.UR = self.grid[row - 1][col + 1]

			if row < (self.rows - 1):
				bubble.DL = self.grid[row + 1][col]

				if col < (self.cols - 1):
					bubble.DR = self.grid[row + 1][col + 1]

		else:
			if row > 0:
				bubble.UR = self.grid[row - 1][col]

				if col > 0:
					bubble.UL = self.grid[row - 1][col - 1]

			if row < (self.rows - 1):
				bubble.DR = self.grid[row + 1][col]

				if col > 0:
					bubble.DL = self.grid[row + 1][col - 1]


	def updateComrades(self, bubble):

		for comrade in bubble.getComrades():
			self.findComrades(comrade)

			
	def findTargets(self):
		self.targets = []

		for row in range(self.rows):
			for col in range(self.cols):
				bubble = self.grid[row][col]

				if not bubble.exists:
					for comrade in bubble.getComrades():
						if (comrade not in self.targets) and comrade.exists:
							self.targets.append(comrade)

		# for target in self.targets: print('row, col = {}, {}'.format(target.row, target.col))


	def calcPos(self, row, col, even_offset):

		x = (col * ((ROOM_WIDTH - BUBBLE_RADIUS) / (GRID_COLS))) + WALL_BOUND_L + BUBBLE_RADIUS

		if not ((row % 2) == even_offset): 
			x += BUBBLE_RADIUS

		y = BUBBLE_RADIUS + (row * BUBBLE_RADIUS * 2) 

		return (x,y)

	def draw(self):

		for row in range(self.rows):
			for col in range(self.cols):

				if ((self.collision_counter + 1) % APPEND_COUNTDOWN == 0):
						self.grid[row][col].shake()

				else: self.grid[row][col].draw()

		for animation in self.animations:
			if not animation: 
				self.animations.remove(animation)
				continue
			frame = animation.pop()
			frame.draw()

		if SHOW_COMRADES or VISUALIZATIONS:
			for row in range(self.rows):
				for col in range(self.cols):
					bubble = self.grid[row][col]
					bubble_x, bubble_y = bubble.pos

					for comrade in bubble.getComrades():
						comrade_x, comrade_y = comrade.pos
						x_vec = (comrade_x - bubble_x)/2
						y_vec = (comrade_y - bubble_y)/2


						pg.draw.line(display, BLACK, bubble.pos, (bubble_x + x_vec, bubble_y + y_vec))

		if SHOW_TARGETS or VISUALIZATIONS:
			for target in self.targets:
				x, y = int(target.pos[0]), int(target.pos[1])
				# circle(Surface, color, pos, radius, width=0) -> Rect
				pg.draw.circle(display, BLACK, (x,y), 5)

		if SHOW_HITBOXES or VISUALIZATIONS:
			for target in self.targets:
				x, y = target.pos
				hitbox = pg.Surface((HITBOX_SIZE, HITBOX_SIZE), pg.SRCALPHA, 32)
				hitbox.fill((50, 50, 50, 180))
				display.blit(hitbox, (x - HITBOX_SIZE/2, y - HITBOX_SIZE/2))


		if SHOW_ROOT_PATH or VISUALIZATIONS:
			for path in self.paths:
				for idx in range(len(path)):
					if idx == 0: continue
					pg.draw.line(display, BLACK, path[idx-1].pos, path[idx].pos, 3)


			if time.time() - self.prev_time > 0.01:
				self.prev_time = time.time()
				if self.paths:
					del self.paths[0][0]
					if not self.paths[0]: del self.paths[0]