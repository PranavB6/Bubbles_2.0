from constants import *
import pygame as pg
import time
pg.font.init()




class Game():
	def __init__(self):
		self.over = False
		self.score = 0
		self.prev_score = self.score

		self.font = pg.font.Font("pixel.otf", 30)

		self.score_label = self.font.render('Score:{}'.format(self.score), False, BLACK)
		self.score_label_x, self.score_label_y, _, _ = self.score_label.get_rect(center = DISP_CENTER)


		self.end_msg = self.font.render('You Fucked Up!', False, BLACK)
		self.end_msg_x, self.end_msg_y, _, _ = self.end_msg.get_rect(center = DISP_CENTER)

		self.restart_msg = self.font.render('Press R to restart', False, BLACK)
		self.restart_msg_x, self.restart_msg_y, _, _ = self.restart_msg.get_rect(center = DISP_CENTER)
		# Surface((width, height), flags=0, depth=0, masks=None) -> Surface


	def gameOverScreen(self, grid_manager, background):

		for row in range(grid_manager.rows):
			for col in range(grid_manager.cols):
				bubble = grid_manager.grid[row][col]

				if bubble.exists: 
					frames = bubble.pop()
					grid_manager.animations.append(frames)

		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN:

					if chr(event.key) == 'r':
						return

					if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
						pg.quit()
						quit()

			background.draw()
			self.drawGameOver()			
			grid_manager.draw()
			pg.display.update()
			clock.tick(60)


		return

	def drawScore(self):

		self.updateScore()

		display.blit(self.score_label,(WALL_BOUND_L + 20, DISP_H - 40))

	def drawGameOver(self):

		display.blit(self.end_msg, (self.end_msg_x, DISP_H/2 - 60))
		display.blit(self.restart_msg,(self.restart_msg_x, DISP_H/2 - 30))
		display.blit(self.score_label,(self.score_label_x, DISP_H/2 - 0))

	def updateScore(self):
		if self.prev_score == self.score: return

		self.prev_score = self.score
		self.score_label = self.font.render('Score: {}'.format(self.score), False, BLACK)
		self.score_label_x, self.score_label_y, _, _ = self.score_label.get_rect(center = DISP_CENTER)




class Background():
	def __init__(self):
		self.image = self.getImage()

		self.wall = pg.Surface((WALL_WIDTH, DISP_H), pg.SRCALPHA, 32)
		self.wall.fill((122,122,122,122))

		self.floor = pg.Surface((ROOM_WIDTH,FLOOR_HEIGHT), pg.SRCALPHA, 32)
		self.floor.fill((200,0,0,90))


	def getImage(self):
		# Load and draw background image
		bg = pg.image.load('bg.png').convert()
		_, _, bg_w, bg_h = bg.get_rect()
		sf = 0.8
		bg = pg.transform.scale(bg, (int(bg_w * sf), int(bg_h * sf)))
		return bg


	def draw(self):
		display.blit(self.image, (0,0))

		pg.draw.line(display, BLUE, (WALL_BOUND_L, 0), (WALL_BOUND_L, DISP_H))
		pg.draw.line(display, BLUE, (WALL_BOUND_R, 0), (WALL_BOUND_R, DISP_H))
		pg.draw.line(display, RED, (WALL_BOUND_L, DISP_H - FLOOR_HEIGHT), (WALL_BOUND_R, DISP_H - FLOOR_HEIGHT))

		display.blit(self.floor, (WALL_BOUND_L, WALL_BOUND_FLOOR))
		display.blit(self.wall, (0,0))
		display.blit(self.wall, (WALL_BOUND_R, 0))


class StateMachine():

	def __init__(self):

		self.states = ['begin', 'next_key', 'final_key', 'reset']
		self.state = 'begin'
		self.idx = 0

	def set(self, state):

		if state not in self.states: raise ValueError('{} not a valid state'.format(state))
		else: self.state = state

		# print('State set to', self.state)

	def get_state(self):
		return self.state



class CheatManager():


	def __init__(self, grid_manager, gun):
		self.grid_manager = grid_manager
		self.gun = gun 

		#----------------------------------- Put you cheat codes here --------------------------------#
		self.cheats = ['god', 'explosion', 'blue', 'violet', 'green', 'yellow', 'red']
		self.machines = [StateMachine() for cheat in self.cheats]

	def view(self, event):

		for idx in range(len(self.cheats)):
			self.check(event, self.cheats[idx], self.machines[idx])

	def check(self, event, cheat, machine):

		if not chr(event.key).isalpha(): return

		char = chr(event.key)

		if machine.get_state() == 'begin':
			machine.idx = 0
			if char == cheat[machine.idx]:
				machine.set('next_key') 
				machine.idx += 1
			return

		if machine.get_state() == 'next_key':

			# print('char', char)
			# print('cheat[{}] = {}'.format(machine.idx, cheat[machine.idx] ))
			if char == cheat[machine.idx]:
				machine.idx += 1

				if machine.idx + 1 == len(cheat):
					machine.set('final_key')
					

			else: machine.set('begin')
				
			return

		if machine.get_state() == 'final_key':
			if char == cheat[machine.idx]:

				for machine in self.machines:
					machine.set('begin')

				#-------------------------------- Put cheat functions here --------------------------#
				if cheat == 'god': self.god_cheat()
				elif cheat == 'explosion': self.explosion_cheat()
				elif cheat == 'red': self.red()
				elif cheat == 'green': self.green()
				elif cheat == 'yellow': self.yellow()
				elif cheat == 'blue': self.blue()
				elif cheat == 'violet': self.violet()

				else: raise ValueError('Cheat function for \'{}\' not called'.format(cheat))
				#------------------------------------------------------------------------------------#

			else: machine.set('begin')

			return

	#-------------------------------------------------- Put what the cheat function do here -------------------------- #

	def blue(self): self.gun.loaded.color = BLUE
	def red(self): self.gun.loaded.color = RED
	def yellow(self): self.gun.loaded.color = YELLOW
	def green(self): self.gun.loaded.color = GREEN
	def violet(self): self.gun.loaded.color = VIOLET


	def god_cheat(self):
		print('Activated God Mode')

		for row in range(self.grid_manager.rows):
			for col in range(self.grid_manager.cols):
				if self.grid_manager.grid[row][col].exists:
					self.grid_manager.grid[row][col].color = self.gun.loaded.color

	def explosion_cheat(self):
		print('Activated Cheat: Explosion')
		self.gun.loaded.color = BLACK

	def bubbles_cheat(self):
		print('bubbles')
		return