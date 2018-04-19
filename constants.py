import pygame as pg

# visualizations
VISUALIZATIONS = False
SHOW_COMRADES = False
SHOW_TARGETS = False
SHOW_HITBOXES = False
SHOW_ROOT_PATH = False

APPEND_COUNTDOWN = 5


DISP_W = 900
DISP_H = 700
BOTTOM_CENTER = (450,700)
DISP_CENTER = (DISP_W/2, DISP_H/2)


# create display
display = pg.display.set_mode((DISP_W,DISP_H))
display_rect = display.get_rect()
pg.display.set_caption('Bubbles 2.0')
clock = pg.time.Clock()

# colours
BLACK = (0, 0, 0 )
LIGHT_GRAY = (122, 122, 122)
DARK_GRAY = (60,60,60)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
VIOLET = (127, 0, 255)

# Ball colours
BUBBLE_COLORS = [RED,YELLOW,GREEN,BLUE,VIOLET]
BG_COLOR = 'No color'

AIM_LENGTH = 200

ANGLE_MAX = 180 - 15
ANGLE_MIN = 15

# Moving Bubble Constants
BUBBLE_VEL = 15
BUBBLE_RADIUS = 15

# Grid Constants
GRID_COLS = 20
GRID_ROWS = 10
GAMEOVER_ROWS = 20


HITBOX_SIZE = (BUBBLE_RADIUS * 2) - 4



#Game environment constants
WALL_WIDTH = 120
FLOOR_HEIGHT = DISP_H - (2 * BUBBLE_RADIUS * (GAMEOVER_ROWS - 1))
ROOM_WIDTH = DISP_W - (2 * WALL_WIDTH)
WALL_BOUND_L = WALL_WIDTH
WALL_BOUND_R = DISP_W - WALL_WIDTH
WALL_BOUND_FLOOR = DISP_H - FLOOR_HEIGHT
# WALL_RECT_L = pg.Rect(0,0,WALL_WIDTH,DISP_H)
# WALL_RECT_R = pg.Rect(WALL_BOUND_R,0,WALL_WIDTH,DISP_H)