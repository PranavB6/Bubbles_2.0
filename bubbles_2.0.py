import time, random
from constants import *
from bubble_file import *
from grid_file import *
from shooter_file import *
from game_objects import *
import pygame as pg
pg.init()


def main():

	# --------------- Initialization ----------------
	background = Background()

	gun = Shooter(pos = BOTTOM_CENTER)
	gun.putInBox()	

	grid_manager = GridManager()
	game = Game()	
	cheat_manager = CheatManager(grid_manager, gun)

	mouse_pos = (DISP_W/2, DISP_H/2)

	# ---------------------------------------------
	
	while not game.over:

		background.draw()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()

			if event.type == pg.MOUSEMOTION:
				mouse_pos = pg.mouse.get_pos()

				
			if event.type == pg.MOUSEBUTTONDOWN:
				gun.fire()

			# Ctrl+C to quit
			if event.type == pg.KEYDOWN:
				cheat_manager.view(event)

				if event.key == pg.K_c and pg.key.get_mods() & pg.KMOD_CTRL:
					pg.quit()
					quit()


		grid_manager.view(gun, game)

		gun.rotate(mouse_pos)
		gun.draw_bullets()

		game.drawScore()

		pg.display.update()
		clock.tick(60)

	game.gameOverScreen(grid_manager, background)

	return

if __name__ == '__main__': 
	while True: main()