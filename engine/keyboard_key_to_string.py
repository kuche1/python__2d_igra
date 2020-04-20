

keys = {

	8:'backspace',
	9:'tab',
	
	13:'enter',
	
	27:'esc',
	
	32:'space',
	
	45:'-',
	
	48:'0',
	49:'1',
	50:'2',
	51:'3',
	52:'4',
	53:'5',
	54:'6',
	55:'7',
	56:'8',
	57:'9',
	
	61:'=',
	
	91:'[',
	92:'\\',
	93:']',
	
	96:'`',
	97:'a',
	98:'b',
	99:'c',
	100:'d',
	101:'e',
	102:'f',
	103:'g',
	104:'h',
	105:'i',
	106:'j',
	107:'k',
	108:'l',
	109:'m',
	110:'n',
	111:'o',
	112:'p',
	113:'q',
	114:'r',
	115:'s',
	116:'t',
	117:'u',
	118:'v',
	119:'w',
	120:'x',
	121:'y',
	122:'z',
	
	127:'del',
	
	273:'up arrow',
	274:'down arrow',
	275:'right arrow',
	276:'left arrow',
	277:'ins',
	278:'home',
	279:'end',
	280:'pgup',
	281:'pgdn',
	
	300:'num lock',
	301:'caps lock',
	
	303:'right shift',
	304:'left shift',
	
	305:'right ctrl',
	306:'left ctrl',
	307:'right alt',
	308:'left alt',
	
}


def main(k):
	
	if k in keys:
		return keys[k]
	
	print(f"Unknown keyboard key: {k}")
	
	return f"keyboard[{k}]"
