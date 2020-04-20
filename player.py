
import eng
set = eng.set

from map import map


class Player:
	
	hp_max = 100
	speed = 50
	camera_speed = 1.5
	
	d = 5
	col = eng.col.black
	
	hp_font = eng.load_font(set.hp_font, set.hp_font_size)
	clip_font = eng.load_font(set.clip_font, set.clip_font_size)
	ammo_font = eng.load_font(set.ammo_font, set.ammo_font_size)
	cooldown_font = eng.load_font(set.cooldown_font, set.cooldown_font_size)
	#
	x = 0
	y = 0
	center_x = 0
	center_y = 0
	look_direction_x = 0
	look_direction_y = 0
	
	moving = False
	def set_x(s, x):
		s.x = x
		s.center_x = x+s.d/2
	def set_y(s, y):
		s.y = y
		s.center_y = y+s.d/2
	
	def respawn(s, gun):
		s.hp = s.hp_max
		s.set_x(map.spawn_x)
		s.set_y(map.spawn_y)
		eng.camera.set_center(s.center_x, s.center_y)
		s.gun = gun
	
	def main(s):
		
		if eng.press('1'):
			eng.camera.set_zoom(eng.camera.zoom + 0.1)
		if eng.press('2'):
			eng.camera.set_zoom(eng.camera.zoom - 0.1)
		
		# keyboard movement
		x_change = 0
		if eng.hold(set.move_left):
			x_change -= s.speed
		if eng.hold(set.move_right):
			x_change += s.speed
			
		y_change = 0
		if eng.hold(set.move_up):
			y_change -= s.speed
		if eng.hold(set.move_down):
			y_change += s.speed

		if x_change == 0 and y_change == 0:
			s.moving = False
		else:
			s.moving = True
			change_x, change_y = eng.scale(x_change, y_change, s.speed*eng.dt)
			map.move(s, change_x, change_y)
			
		# look direction
		s.look_direction_x = eng.mouse.map_x - s.center_x
		s.look_direction_y = eng.mouse.map_y - s.center_y
			
		# camera movement
		change_x = s.center_x - eng.camera.center_x
		change_y = s.center_y - eng.camera.center_y
		
		#eng.camera.set_center(eng.camera.center_x+change_x*s.camera_speed*eng.dt, eng.camera.center_y+change_y*s.camera_speed*eng.dt)
		overall_change = abs(change_x) + abs(change_y)
		max_change = overall_change * s.camera_speed
		change_x, change_y = eng.scale(change_x, change_y, max_change * eng.dt)
		eng.camera.increase_center(change_x, change_y)
		#...? da izmislq po-dobre formula
		
			
		# guns
		s.gun.main(s)

	def draw(s):
		# player
		eng.draw_rect_on_map(s.x, s.d, s.y, s.d, s.col)
		# gun
		s.gun.draw()
		# hud
		eng.draw_scaled_text(x=set.hp_x, y=set.hp_y, text=f"{s.hp}/{s.hp_max}", font=s.hp_font, col=set.hp_color)
		eng.draw_scaled_text(x=set.clip_x, y=set.clip_y, text=f'{s.gun.clip}/{s.gun.full_clip}', font=s.clip_font, col=set.clip_color)
		eng.draw_scaled_text(x=set.ammo_x, y=set.ammo_y, text=f"{s.gun.ammo}/{s.gun.full_ammo}", font=s.ammo_font, col=set.ammo_color)
		
		eng.draw_scaled_text(x=0, y=14, text='%.2f%%'%s.gun.fire_animation_progress, font=s.cooldown_font, col=set.cooldown_color)
		eng.draw_scaled_text(x=0, y=18, text='%.2f%%'%s.gun.reload_animation_progress, font=s.cooldown_font, col=set.cooldown_color)

		eng.draw_scaled_text(x=0, y=24, text=f'%iFPS'%eng.FPS, font=s.hp_font, col=eng.col.red)
