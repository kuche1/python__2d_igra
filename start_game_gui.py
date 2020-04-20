
import eng
set = eng.set

from map import map, Wall
from guns import *
from player import Player	

		

def main():
	
	err = map.load('test map 1')
	if err:
		print(f'Map error: {err}')
		return
	
	p = Player()
	p.respawn( Gun_colt() )
	
	running = True
	while eng.next_frame() and running:
		
		if eng.press('esc'):
			running = False
		
		p.main()
		map.main()
		
		map.draw()
		p.draw()
		
		
		
		
		
		
	
