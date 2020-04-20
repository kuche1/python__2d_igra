
import eng
set = eng.set


MAPS_DIR = 'maps/'

def str_to_int(str):
	try:
		return 0, int(str)
	except ValueError:
		return f'not an integer: {str}', 0

def str_to_float(str):
	try:
		v = float(str)
	except ValueError:
		return f'not a float: {str}', 0
	if v == float('inf'):
		return f'infinity is not a valud float', 0
	return 0, v
	
def str_to_num(str):
	try:
		int_v = int(str)
	except ValueError:
		try:
			float_v = float(str)
		except ValueError:
			return f'bad number value: {str}',0
		return 0, float_v
	else:
		return 0, int_v


def str_to_col(str):
	str = str.split(',')
	if len(str) != 3:
		return f'colors have only 3 values, bad color: {str}', 0
	col = [0,0,0]
	for ind, v in enumerate(str):
		fail, v = str_to_int(v)
		if fail: return f'bad color value: {fail}', 0
		if v < 0:
			return f'cant have a negative vanue as a color: {v}', 0
		if v > 255:
			return f'color value cant be more that 255: {v}', 0
		col[ind] = v
	#print('color: ',tuple(col))
	return 0, tuple(col)
	
	
def str_to_wall(wall_d, str):
	if wall_d == None:
		return f'you need to enter wall length first', 0
	
	data = str.split(',')
	
	args = []
	
	if len(data) < 2:
		return 'a wall needs at least 2 values', 0
	fail, x = str_to_int(data.pop(0))
	if fail: return f'bad map x: {fail}', 0
	args.append(x)
	
	fail, y = str_to_int(data.pop(0))
	if fail: return f'bad map y: {fail}', 0
	args.append(y)
	
	if len(data) >= 1:
		fail, hp = str_to_num(data.pop(0))
		if fail: return f'bad hp: {fail}', 0
		args.append(hp)
		
		if len(data) >= 1:
			fail, hardness = str_to_num(data.pop(0))
			if fail: return f'bad hardness: {fail}', 0
			args.append(hardness)
			
			if len(data) >= 3:
				str = ','.join(data[:3])
				del data[:3]
				fail, col = str_to_col( str )
				if fail: return f'bad wall color: {fail}', 0
				args.append(col)

	if len(data) != 0:
		return f'wall data contains too much properties, unneeded: {data}', 0

	return 0, Wall(wall_d, *args)
	
	
class Dict:
	def __init__(s):
		s.dict = {}
	def __setitem__(s, item, value):
		s.dict[item] = value
	def __getitem__(s, item):
		return s.dict.get(item, None)

class Wall:
	def __init__(s, d, x, y, hp=100, hardness=1, col=eng.col.black):
		s.x = x*d
		s.y = y*d
		s.hp = hp
		s.hardness = hardness
		s.col = col
	def damage(s, dmg):
		s.hp -= dmg
		if s.hp <= 0:
			map.walls[s.x,s.y] = 0
	def draw(s):
		eng.draw_rect_on_map(s.x, map.wall_d, s.y, map.wall_d, s.col)
	

class map:
	
	def load(s, name):
		s.bullets = []
		
		file = eng.get_file(MAPS_DIR+name)
		if not file:
			return f'missing map: {name}'
			
		s.out_col = None
		s.in_col = None
		s.spawn_x = None
		s.spawn_y = None
		s.wall_d = None
		s.walls = Dict()
		s.start_x = None
		s.end_x = None
		s.start_y = None
		s.end_y = None
			
		file_obj = open(file, 'r')
		while True:
			data = file_obj.readline()
			if data == '':
				break
			if data.endswith('\n'):
				data = data[:-1]
			
			if data=='':
				continue
				
			if ';' not in data:
				print(f"Warning, invalid line in mao {name}: {data}")
				
			ind = data.index(';')
			f = data[:ind]
			a = data[ind+1:]
			
			if f=='out of map color':
				fail, col = str_to_col(a)
				if fail: return fail
				s.out_col = col
			elif f=='in map color':
				fail, col = str_to_col(a)
				if fail: return fail
				s.in_col = col
			elif f=='spawn x':
				fail, num = str_to_float(a)
				if fail: return fail
				s.spawn_x = num
			elif f=='spawn y':
				fail, num = str_to_float(a)
				if fail: return fail
				s.spawn_y = num
			elif f=='wall length':
				fail, num = str_to_int(a)
				if fail: return fail
				s.wall_d = num
			elif f=='wall':
				fail, wall = str_to_wall(s.wall_d, a)
				if fail: return fail
				if s.walls[wall.x,wall.y]:
					return f'wall already exists in this position: {w.x, w.y}'
				s.walls[wall.x,wall.y] = wall
				
				if s.start_x == None or wall.x < s.start_x:
					s.start_x = wall.x
				if s.end_x == None or s.end_x < wall.x:
					s.end_x = wall.x
				if s.start_y == None or wall.y < s.start_y:
					s.start_y = wall.y
				if s.end_y == None or s.end_y < wall.y:
					s.end_y = wall.y
			else:
				return f'unknown map property: {f}, with value: {a}'
		file_obj.close()
		
		
		if s.out_col == None:
			return 'out of map color not set'
		if s.in_col == None:
			return 'map color not set'
		if s.spawn_x == None:
			return 'spawn x not set'
		if s.spawn_y == None:
			return 'spawn y not set'
		if s.wall_d == None:
			return 'wall length not set'
		
		if s.start_x == None or s.end_x == None or s.start_y == None or s.end_y == None:
			return 'map consists of no walls'
		
		
		
		start_x = int( s.start_x/s.wall_d )
		end_x = int(s.end_x/s.wall_d)
		start_y = int(s.start_y/s.wall_d)
		end_y = int(s.end_y/s.wall_d)
		
		for y in [start_y-1, end_y+1]:
			for x in range(start_x-1, end_x+2):
				wall = Wall(s.wall_d, x, y, hp=eng.INFINITY, hardness=eng.INFINITY, col=eng.col.black)
				if s.walls[wall.x,wall.y]:
					return 'i (the developer) fucked up, sorry'
				s.walls[wall.x,wall.y]= wall
				
		for x in [start_x-1, end_x+1]:
			for y in range(start_y, end_y+1):
				wall = Wall(s.wall_d, x, y, hp=eng.INFINITY, hardness=eng.INFINITY, col=eng.col.black)
				if s.walls[wall.x,wall.y]:
					return 'i (the developer) fucked up, sorry'
				s.walls[wall.x,wall.y]= wall
				
		s.start_x = s.start_x - s.wall_d
		s.end_x = s.end_x + s.wall_d*2 ### kraq na mapa, a ne poslednoto X
		s.dx = s.end_x - s.start_x
		
		s.start_y = s.start_y - s.wall_d
		s.end_y = s.end_y + s.wall_d*2
		s.dy = s.end_y - s.start_y		
		
	def multi_collide(s, x, dx, y, dy):
		xe = x + dx
		ye = y + dy
		
		x_start = int(x - (x % s.wall_d))
		x_end = int(xe - (xe % s.wall_d))
		
		y_start = int(y - (y % s.wall_d))
		y_end = int(ye - (ye % s.wall_d))

		for x in range(x_start, x_end + s.wall_d, s.wall_d):
			for y in range(y_start, y_end + s.wall_d, s.wall_d):
				wall = s.walls[x, y]
				if wall:
					yield wall
					
	def single_collide(s, x, dx, y, dy):
		for wall in s.multi_collide(x, dx, y, dy):
			return wall






	def move(s, obj, x_change, y_change):
			
		while x_change != 0 or y_change != 0:
			
			if ( biggest_change := max(abs(x_change), abs(y_change)) ) > s.wall_d:
				precent = s.wall_d / biggest_change
				temp_x = x_change * precent
				temp_y = y_change * precent
			else:
				temp_x = x_change
				temp_y = y_change
			
			if temp_x:
				wall = s.single_collide(obj.x + temp_x, obj.d, obj.y, obj.d)
				if wall:
					if temp_x > 0:
						obj.set_x((wall.x - obj.d) - eng.VERY_SMALL_NUMBER)
					else:
						obj.set_x(wall.x + s.wall_d)
					x_change = 0
				else:
					obj.set_x(obj.x + temp_x)
					x_change -= temp_x
			
			if temp_y:
				wall = s.single_collide(obj.x, obj.d, obj.y + temp_y, obj.d)
				if wall:
					if temp_y > 0:
						obj.set_y(wall.y - obj.d - eng.VERY_SMALL_NUMBER)
					else:
						obj.set_y(wall.y + s.wall_d)
					y_change = 0
				else:
					obj.set_y(obj.y + temp_y)
					y_change -= temp_y
					
	def move_and_collide(s, obj, x_change, y_change):
			
		while x_change != 0 or y_change != 0:
			
			if ( biggest_change := max(abs(x_change), abs(y_change)) ) > s.wall_d:
				precent = s.wall_d / biggest_change
				temp_x = x_change * precent
				temp_y = y_change * precent
			else:
				temp_x = x_change
				temp_y = y_change
			
			obj.set_x(obj.x + temp_x)
			obj.set_y(obj.y + temp_y)
			
			for wall in s.multi_collide(obj.x, obj.d, obj.y, obj.d):
				yield wall
				
			x_change -= temp_x
			y_change -= temp_y
				
				
				
	def add_bullet(s, bullet):
		s.bullets.append(bullet)
		
		
	def main(s):
		to_delete = []
		for bullet in s.bullets:
			if bullet.main():
				to_delete.append(bullet)
		for bullet in to_delete:
			s.bullets.remove(bullet)

		
	def draw(s):
		eng.draw_background(s.out_col)
		eng.draw_rect_on_map(s.start_x, s.dx, s.start_y, s.dy, s.in_col)
					
		for wall in s.multi_collide(eng.camera.x, eng.camera.dx, eng.camera.y, eng.camera.dy):
			wall.draw()
			
		for bullet in s.bullets:
			if eng.camera.visible(bullet):
				bullet.draw()
							
map = map()

