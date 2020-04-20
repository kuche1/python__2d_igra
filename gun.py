
import random

import eng
set = eng.set

from map import map


class Bullet:
	def __init__(s, center_x, center_y, change_x, change_y, gun):
		s.damaged_objs = []
			
		s.d = gun.bullet_d
		s.col = gun.bullet_col
		s.dmg = gun.dmg
		s.lifespan = gun.bullet_lifespan
		s.hardness = gun.bullet_hardness
		s.disappear_when_out_of_vision = gun.bullet_disappears_when_out_of_vision
		
		s.set_center_x(center_x)
		s.set_center_y(center_y)
		s.change_x = change_x
		s.change_y = change_y
	def set_x(s, new):
		s.x = new
		s.center_x = new + s.d/2
	def set_y(s, new):
		s.y = new
		s.center_y = new + s.d/2
		
	def set_center_x(s, new):
		s.x = new - s.d/2
	def set_center_y(s, new):
		s.y = new - s.d/2
		
	def damage_obj(s, obj):
		#...
		# s.hardness < 0 ?
		# s.hardness == 0 ?
		# obj.hardness == 0 ?
		if obj not in s.damaged_objs:
			if obj.hardness < s.hardness:
				s.hardness -= obj.hardness
				obj.damage(s.dmg)
				s.damaged_objs.append(obj)
			elif obj.hardness == s.hardness:
				obj.damage(s.dmg)
				return True
			else:
				proportion = s.hardness / obj.hardness
				obj.damage( s.dmg * proportion)
				return True
		
	def main(s):
		
		if s.disappear_when_out_of_vision:
			if not eng.camera.visible(s):
				return True
		
		for wall in map.move_and_collide(s, s.change_x*eng.dt, s.change_y*eng.dt):
			if s.damage_obj(wall):
				return True
			
		s.lifespan -= eng.dt
		if s.lifespan < 0:
			return True
		
	def draw(s):
		eng.draw_rect_on_map(s.x, s.d, s.y, s.d, s.col)
		

class Gun:
	### fire_animation_length = 1
	### reload_animation_length = 1
	
	automatic = False
	reload_interruptable = False
	reload_interrupt_checks_clip = True
	reload_on_fire_with_empty_clip = True
	
	### dmg = 1
	### inaccuracy = 0
	### inaccuracy_while_moving = 1
	### full_clip = 1
	### full_ammo = 1
	
	bullet_lifespan = eng.INFINITY
	bullet_hardness = 1
	bullet_speed = 100
	bullet_disappears_when_out_of_vision = False
	
	bullet_d = 1
	bullet_col = eng.col.purple
	
	fire_sound = None
	reload_sound = None
	#
	fire_animation_playing = False
	fire_animation_left = 0
	fire_animation_progress = 0
	
	reload_animation_playing = False
	reload_animation_left = 0
	reload_animation_progress = 0
	
	def __init__(s):
		s.clip = s.full_clip
		s.ammo = s.full_ammo
		
	def main(s, user):
		if s.fire_animation_playing:
			s.fire_animation_left -= eng.dt
			if s.fire_animation_left > 0:
				s.fire_animation_progress = s.fire_animation_left / s.fire_animation_length
			else:
				s.fire_animation_playing = False
				
		elif s.reload_animation_playing:
			s.reload_animation_left -= eng.dt
			if s.reload_animation_left > 0:
				s.reload_animation_progress = s.reload_animation_left / s.reload_animation_length
			else:
				s.reload_animation_playing = False
				missing = s.full_clip - s.clip
				if s.ammo >= missing:
					s.clip = s.full_clip
					s.ammo -= missing
				else:
					s.clip = s.ammo
					s.ammo = 0
		
		
		if s.automatic:
			fire_req = eng.hold
		else:
			fire_req = eng.press
		if fire_req(set.fire):
			s.fire(user)
		
		if eng.press(set.reload):
			s.reload()
			
					
	def reload(s):
		if (s.fire_animation_playing==False) and (s.reload_animation_playing==False) and s.clip != s.full_clip:
			if s.ammo > 0:
				s.reload_animation_playing = True
				s.reload_animation_left = s.reload_animation_length
				s.reload_animation_progress = 0
				
				eng.play_sound(s.reload_sound)
			else:
				pass#... play no ammo sound
					
	def fire(s, user):
		if s.fire_animation_playing:
			return
		
		if s.reload_animation_playing:
			if s.reload_interruptable:
				if s.reload_interrupt_checks_clip:
					if s.clip <= 0:
						return
				s.reload_animation_playing = False 
				eng.stop_sound(s.reload_sound)
			else:
				return
		
		if s.clip > 0:
			s.clip -= 1
			
			s.fire_animation_playing = True
			s.fire_animation_left = s.fire_animation_length
			s.fire_animation_progress = 0
			
			
			change_x = user.look_direction_x
			change_y = user.look_direction_y
			overall_change = abs(change_x) + abs(change_y)
			
			if user.moving:
				inaccuracy = s.inaccuracy + s.inaccuracy_while_moving
			else:
				inaccuracy = s.inaccuracy
				
			change_x += random.uniform(-overall_change, overall_change) * inaccuracy
			change_y += random.uniform(-overall_change, overall_change) * inaccuracy
			while change_x == 0 and change_y == 0:
				change_x = random.uniform(-1, 1)
				change_y = random.uniform(-1, 1)
				
			change_x, change_y = eng.scale(change_x, change_y, s.bullet_speed)
			bullet = Bullet( user.center_x, user.center_y, change_x, change_y, s)
			map.add_bullet( bullet )
			eng.play_sound(s.fire_sound)
			return
			
		if s.reload_on_fire_with_empty_clip:
			s.reload()
		else:
			pass#... play no clip sound

	def draw(s):#... gun model
		pass

