
import eng
set = eng.set

from gun import Gun


class Gun_colt(Gun):
	fire_animation_length = 0.1
	reload_animation_length = 0.6
	automatic = False
	reload_interruptable = False
	
	dmg = 3
	inaccuracy = 0.1
	inaccuracy_while_moving = 0.1
	full_clip = 20
	full_ammo = 80
	
	fire_sound = eng.load_sound(set.default_fire)
	reload_sound = eng.load_sound(set.default_reload)

