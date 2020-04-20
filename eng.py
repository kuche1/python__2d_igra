
import os

import pygame as pg

import engine.colors as col

import engine.mouse_key_to_string as mouse_key_to_string
mouse_key_to_string = mouse_key_to_string.main
import engine.keyboard_key_to_string as keyboard_key_to_string
keyboard_key_to_string = keyboard_key_to_string.main

import engine.settings as set


##################### maths

VERY_SMALL_NUMBER = 0.00000001
INFINITY = float('inf')

def scale(x, y, max):
	sum = abs(x) + abs(y)
	if sum:
		X = max / sum
		return x*X, y*X
	return 0, 0

##################### init stuff

PYGAME_CLOCK = pg.time.Clock()
dt = 0
FPS = 'INF'

##################### settings

STOCK_DIR = 'engine/STOCK/'
CUSTOM_DIR = 'engine/CUSTOM/'
CACHE_DIR = 'engine/CACHE/' #... oshte ne e nastroeno

def get_file(name):
	
	for (d,folders,files) in os.walk(CUSTOM_DIR):
		for folder in folders:
			dir = CUSTOM_DIR+folder+'/'+name
			if os.path.isfile(dir):
				return dir
		break
		
	if os.path.isfile(STOCK_DIR+name):
		return STOCK_DIR+name 

##################### errors

def fatal_error(info):
	print(f'FATAL ERROR: {info}')
	quit()

##################### graphics

# resolution, scaling

def resize(resx, resy):
	global SCR
	if resx <= 0 or resy <= 0:
		fatal_error(f'your resolution cant be {resx, resy}')
	
	flags = []
	if set.fullscreen:
		flags.append(pg.FULLSCREEN)
	else:
		if set.resizable:
			flags.append(pg.RESIZABLE)
	SCR = pg.display.set_mode((resx, resy), *flags)
	
	global SCALED_FORMULA_X, SCALED_FORMULA_Y
	SCALED_FORMULA_X = resx / 100
	SCALED_FORMULA_Y = resy / 100
	
	global MOUSE_SCALED_FORMULA_X, MOUSE_SCALED_FORMULA_Y
	MOUSE_SCALED_FORMULA_X =  100 / resx
	MOUSE_SCALED_FORMULA_Y =  100 / resy
	
	global MAP_RES_X, MAP_RES_Y
	#resx*X * resy*X =100*100
	X=( (100*100)/(resx*resy) )**0.5
	MAP_RES_X = resx*X
	MAP_RES_Y = resy*X
	camera.new_map_res()
		
	global MAP_FORMULA_X, MAP_FORMULA_Y
	MAP_FORMULA_X = resx / MAP_RES_X
	MAP_FORMULA_Y = resy / MAP_RES_Y

### camera

class camera:
	zoom = 1
	
	x = 0
	y = 0
	dx = 1
	dy = 1
	xe = 1
	ye = 1
	center_x = 0
	center_y = 0
	
	def new_map_res(s):
		s.dx = MAP_RES_X / s.zoom
		s.dy = MAP_RES_Y / s.zoom
		mouse.update_on_camera_change()
	
	def set_center(s, x, y):
		s.center_x = x
		s.x = x - (s.dx/2)
		s.xe = s.x + s.dx
		
		s.center_y = y
		s.y = y - (s.dy/2)
		s.ye = s.y + s.dy
		
		mouse.update_on_camera_change()
	def increase_center(s, x, y):
		s.set_center(s.center_x+x, s.center_y+y)
	
	def set_zoom(s, new):
		s.zoom = new
		s.dx = MAP_RES_X / s.zoom
		s.dy = MAP_RES_Y / s.zoom
		s.set_center_x(s.center_x)
		s.set_center_y(s.center_y)
		mouse.update_on_camera_change()
		
	def visible(s,obj):
		return (obj.x+obj.d > s.x and obj.x < s.xe) and (obj.y+obj.d > s.y and obj.y < s.ye)

### drawing

# text

FONTS_DIR = 'fonts/'

pg.font.init()

def load_font(name, size):
	file = get_file(FONTS_DIR + name)
	if not file:
		fatal_error(f"cant find font {name}")
	try:
		font = pg.font.Font(file, size)
	except RuntimeError:
		fatal_error(f'invalid font file {name}')
	return font
	
	
def draw_text_on_screen(x, y, text, font, col, center=False):
	text_surface = font.render(text, set.font_antialiasing, col)
	if center:
		text_rect = text_surface.get_rect(center=(x, y))
		SCR.blit(text_surface, text_rect)
	else:
		SCR.blit(text_surface,(x,y))

def draw_scaled_text(x, y, *ar, **kw):
	draw_text_on_screen(x*SCALED_FORMULA_X, y*SCALED_FORMULA_Y, *ar, **kw)
	
def draw_text_on_map(x, y, *ar, **kw):
	draw_text_on_screen((x-camera.x)*camera.zoom*MAP_FORMULA_X, (y-camera.y)*camera.zoom*MAP_FORMULA_Y, *ar, **kw)
	

# geometry

def draw_background(col):
	SCR.fill(col)

def draw_rect_on_screen(x, dx, y, dy, col):
	pg.draw.rect(SCR, col, (round(x), round(y), round(dx), round(dy)))#... math.ceil ?
def draw_scaled_rect(x, dx, y, dy, col):
	draw_rect_on_screen(x*SCALED_FORMULA_X, dx*SCALED_FORMULA_X, y*SCALED_FORMULA_Y, dy*SCALED_FORMULA_Y, col)
def draw_rect_on_map(x, dx, y, dy, col):
	draw_rect_on_screen((x-camera.x)*camera.zoom*MAP_FORMULA_X, dx*camera.zoom*MAP_FORMULA_X, (y-camera.y)*camera.zoom*MAP_FORMULA_Y, dy*camera.zoom*MAP_FORMULA_Y, col)

def draw_flip():
	pg.display.flip()

##################### buttons

BUTTONS = []

class Button:
	def __init__(s, act, x, dx, y, dy, col, text=None, font=None, text_col=None):
		s.act = act
		s.x = x
		s.dx = dx
		s.y = y
		s.dy = dy
		s.col = col
		
		s.text = text
		s.font = font
		s.text_col = text_col
		
		s.xe = x+dx
		s.ye = y+dy

def btn(*args, **kwargs):
	b = Button(*args, **kwargs)
	BUTTONS.append(b)

def buttons_draw():
	for b in BUTTONS:
		draw_scaled_rect(b.x, b.dx, b.y, b.dy, b.col)
		if b.text:
			draw_scaled_text(x=b.x+b.dx/2, y=b.y+b.dy/2, text=b.text, font=b.font, col=b.text_col, center=True)
		
def buttons_main():
	global BUTTONS
	if press(set.click):
		#todo = []
		BUTTONS.reverse()
		for b in BUTTONS:
			if b.x <= mouse.scaled_x <= b.xe and b.y <= mouse.scaled_y <= b.ye:
				#todo.append(b.act)
				BUTTONS = []
				b.act()
				break
		else:
			BUTTONS = []
		#BUTTONS = []
		#for action in todo:
		#	action()
	else:
		BUTTONS = []

##################### keypresses

class mouse:
	x = 0
	y = 0
	screen_x = 1
	screen_y = 1
	scaled_x = 0
	scaled_y = 0
	def set_screen_pos(s, screen_pos):
		s.screen_x = screen_pos[0]
		s.screen_y = screen_pos[1]
		
		s.scaled_x = s.screen_x * MOUSE_SCALED_FORMULA_X
		s.scaled_y = s.screen_y * MOUSE_SCALED_FORMULA_Y
		
		s.update_on_camera_change()
	def update_on_camera_change(s,):
		s.map_x = camera.x + ((s.scaled_x * camera.dx)/100)
		s.map_y = camera.y + ((s.scaled_y * camera.dy)/100)

#

PRESSED_KEYS = []
HELD_KEYS = []

def press(k):
	return k in PRESSED_KEYS
def hold(k):
	return k in HELD_KEYS

def keydown(k):
	PRESSED_KEYS.append(k)
	HELD_KEYS.append(k)
def keyup(k):
	if k in HELD_KEYS:
		HELD_KEYS.remove(k)

def handle_events():
	global PRESSED_KEYS
	
	PRESSED_KEYS = []
	
	for e in pg.event.get():
		
		if e.type == pg.MOUSEMOTION:
			mouse.set_screen_pos(e.pos) 
		elif e.type == pg.MOUSEBUTTONDOWN:
			keydown( mouse_key_to_string(e.button) )
		elif e.type == pg.MOUSEBUTTONUP:
			keyup( mouse_key_to_string(e.button) )
			
		elif e.type == pg.KEYDOWN:
			keydown( keyboard_key_to_string(e.key) )
		elif e.type == pg.KEYUP:
			keyup( keyboard_key_to_string(e.key) )
			
		elif e.type == pg.VIDEORESIZE:
			resize(e.w, e.h)
			
		elif e.type == pg.ACTIVEEVENT:
			pass
			
		elif e.type == pg.QUIT:
			quit()
			
		else:
			print(e)
			
			
##################### on frame

ENGINE_RUNNING = 1

def next_frame():
	global dt, FPS
	
	dt = PYGAME_CLOCK.tick(set.fps_limit) / 1000
	if dt == 0:
		FPS = 2000
	else:
		FPS = 1/dt
	
	buttons_draw()
	draw_flip()
	
	handle_events()
	
	buttons_main()

	return ENGINE_RUNNING

def quit():
	global ENGINE_RUNNING
	ENGINE_RUNNING = 0

##################### audio

SOUNDS_DIR = 'sounds/'

def init_audio():
	global AUDIO_CHANNELS, CHANNEL_IND
	
	pg.mixer.quit()
	pg.mixer.init(set.audio_frequency, set.audio_size, set.audio_channels, set.audio_buffer)

	AUDIO_CHANNELS = []
	CHANNEL_IND = 0

	for x in range(set.audio_virtual_channels):
		AUDIO_CHANNELS.append(pg.mixer.Channel(x))
		
	if len(AUDIO_CHANNELS) < 1:
		print("ERROR: cant have less than one audio channel")
		quit()

def load_sound(name):
	file = get_file(SOUNDS_DIR + name)
	if not file:
		fatal_error(f"missing sound file: {name}")
	try:
		sound = pg.mixer.Sound(file)
	except pg.error:
		fatal_error(f"invalid sound file: {name}")
	return sound

def play_sound(sound):
	global CHANNEL_IND
	sound.set_volume(set.sound_volume)
	
	AUDIO_CHANNELS[CHANNEL_IND].play(sound)
	CHANNEL_IND += 1
	if CHANNEL_IND >= len(AUDIO_CHANNELS):
		CHANNEL_IND = 0

def stop_sound(sound):
	sound.stop()

init_audio()

##################### init

mouse = mouse()
camera = camera()
resize(set.resx,set.resy)

