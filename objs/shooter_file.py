import random
from objs.constants import *
from objs.bubble_file import *
from math import sin, cos, radians, degrees, atan2
import pygame as pg


class Shooter():

	def __init__(self, image = 'images/gun.png', pos = display_rect.center):

		# center position of the image
		self.pos = pos
		self.pos_x, self.pos_y = pos

		self.initGunImage(image)
		self.initCrossHair()

		self.angle = 0

		# Setup position of 'reloads'
		self.reload1_pos = (self.pos_x + 7*BUBBLE_RADIUS, self.pos_y - 20)
		self.reload2_pos = (self.pos_x + 9.25*BUBBLE_RADIUS, self.pos_y - 20)
		self.reload3_pos = (self.pos_x + 11.5*BUBBLE_RADIUS, self.pos_y - 20)

		self.fired = Bullet(self.pos, self.angle)
		self.fired.exists = False		
		self.loaded = Bubble(self.pos)
		self.reload1 = Bubble(self.reload1_pos)
		self.reload2 = Bubble(self.reload2_pos)
		self.reload3 = Bubble(self.reload3_pos)



	def initGunImage(self, image):
		# Load image
		self.shooter = pg.image.load(image).convert_alpha()

		# Get width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]

		# Scale image
		sf = 00.20
		self.shooter = pg.transform.scale(self.shooter, (int(self.shooter_w * sf), int(self.shooter_h * sf)))

		# Get new width and height
		self.shooter_rect = self.shooter.get_rect()
		self.shooter_w = self.shooter_rect[2]
		self.shooter_h = self.shooter_rect[3]


	# I could have put this in the initialization but I wanted to emphasize the fact that the image we are actually rotating is in a box
	def putInBox(self):

		# Make a box to put shooter in
		# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
		self.shooter_box = pg.Surface((self.shooter_w, self.shooter_h*2), pg.SRCALPHA, 32)
		self.shooter_box.fill((0,0,0,0))

		# Put shooter in box
		self.shooter_box.blit(self.shooter, (0,0))

		# Since we want 90 to be when the shooter is pointing straight up, we rotate it
		self.shooter_box = pg.transform.rotate(self.shooter_box, -90)


	def initCrossHair(self):

		#invis cursor
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

		#Load and draw crosshair
		crosshair = pygame.image.load('images/crosshair.png')
		sf = 00.20
		self.crosshair = pg.transform.scale(crosshair, (int(crosshair.get_width() * sf), int(crosshair.get_height() * sf)))
		self.crosshair_rect = self.crosshair.get_rect()

	# Cuz why not
	def draw(self):
		display.blit(self.shooter_box, self.pos)

	def draw_line(self):

		# line(Surface, color, start_pos, end_pos, width=1) -> Rect
		end = ( (cos(radians(self.angle)) * AIM_LENGTH) + DISP_W/2, DISP_H - (sin(radians(self.angle)) * AIM_LENGTH))
		
		pg.draw.line(display, BLACK, self.pos, end)

	# Rotates an image and displays it
	def rotate(self, mouse_pos):
		self.draw_line()

		self.crosshair_rect.center = mouse_pos
		display.blit(self.crosshair, self.crosshair_rect)

		# Get angle of rotation (in degrees)
		self.angle = self.calcMouseAngle(mouse_pos)

		# Get a rotated version of the box to display. Note: don't keep rotating the original as that skews the image
		rotated_box = pg.transform.rotate(self.shooter_box, self.angle)

		# display the image
		display.blit(rotated_box, rotated_box.get_rect( center = self.pos))

		


	def draw_bullets(self):

		self.fired.update()
		self.loaded.draw()
		self.reload1.draw()
		self.reload2.draw()
		self.reload3.draw()
		

	def fire(self):

		if self.fired.exists: return

		else:
			rads = radians(self.angle)
			self.fired = Bullet(self.pos, rads, self.loaded.color)
			self.loaded = Bubble(self.pos, self.reload1.color)
			self.reload1 = Bubble(self.reload1_pos, self.reload2.color)
			self.reload2 = Bubble(self.reload2_pos, self.reload3.color)
			self.reload3 = Bubble(self.reload3_pos)

	def calcMouseAngle(self, mouse_pos):
		# Get mouse position and decompose it into x and y
		mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]

		# Do some quick maths and get the angle
		width = mouse_x - self.pos_x
		height = self.pos_y - mouse_y
		angle = atan2(height,width)
		degree = degrees(angle)		# convert to degrees

		# Restrict the angles, we don't want the user to be able to point all the way
		return max(min(degree , ANGLE_MAX), ANGLE_MIN)