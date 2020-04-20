

import eng

import start_game_gui
import options_gui


def main():
	
	font = eng.load_font(eng.set.main_menu_font, eng.set.main_menu_font_size)
	
	while eng.next_frame():
		
		if eng.press('esc'):
			eng.quit()
		
		eng.draw_background(eng.col.white)
		
		eng.btn(text='start', text_col=eng.col.green, act=start_game_gui.main, x=20, dx=60, y=30, dy=15, col=eng.col.red, font=font)
		eng.btn(text='options', text_col=eng.col.blue, act=options_gui.main,   x=20, dx=60, y=50, dy=15, col=eng.col.green, font=font)
		eng.btn(text='quit', text_col=eng.col.red, act=eng.quit,               x=20, dx=60, y=70, dy=15, col=eng.col.blue, font=font)
		
		
	
