

def main(k):
	
	#print("mouse button: ", k)
	
	if k==1:
		return "mouse1"
	if k==2:
		return "mouse3"
	if k==3:
		return "mouse2"
	if k==4:
		return "wheelup"
	if k==5:
		return "wheeldown"
		
	if k==8:
		return "mouse4"
	if k==9:
		return "mouse5"
	
	print(f"Unknown mouse key: {k}")
	
	return f"mouse[{k}]"
