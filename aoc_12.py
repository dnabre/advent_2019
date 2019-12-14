
import re

scan1 = [
'<x=-1, y=0, z=2>',
'<x=2, y=-10, z=-7>',
'<x=4, y=-8, z=8>',
'<x=3, y=5, z=-1>'
]


def parse_scan(scan1):
	result = []
	for line in scan1:
		line= line[1:-1]
		p = re.findall(r'-?\d+', line) #this is a handy little RE found in a tutorial
		vals = [ int(v) for v in p]
		result.append(vals)
	return result

def print_world(moons, n):
	print(f'After {n} steps:')
	for (pos,vel) in moons:
		(x,y,z) = pos
		print('pos=<x={:3d}, y={:3d}, z={:3d}>, vel=<'.format(x,y,z), end='')
		(x,y,z) = vel
		print('x={:3d}, y={:3d}, z={:3d}>\n'.format(x, y, z), end='')
	print()

def calc_gravity(a,b):
	(p1,v1) = a
	(p2,v2) = b
	(x1,y1,z1) = (p1[0],p1[1],p1[2])
	(x2, y2, z2) = (p2[0], p2[1], p2[2])

	(v_x1,v_y1,v_z1) = (v1[0],v1[1],v1[2])
	(v_x2, v_y2, v_z2) = (v2[0], v2[1], v2[2])

	#x-axiz
	if (x1 < x2):
		v_x1 += 1
		v_x2 += -1
	else:
		v_x1 += -1
		v_x2 += 1

	if (y1 < y2):
		v_y1 += 1
		v_y2 += -1
	else:
		v_y1 += -1
		v_y2 += 1

	if (z1 < z2):
		v_z1 += 1
		v_z2 += -1
	else:
		v_z1 += -1
		v_z2 += 1
	return ( (v_x1, v_y1, v_z1), (v_x2, v_y2, v_z2))

def add_vel(p, v):
	(x,y,z) = p
	(a,b,c) = v
	return (x+a, y+b, c + z)




#TODO: scrap and do over
def next_time_step(moons):

	for a in range(0,len(moons)):
		for b in range(a+1,(len(moons))):
			x,y = calc_gravity(moons[a], moons[b])
			moons[a] = x
			moons[b] = y





	for i in range(len(moons)):
		(p,v) = moons[i]
		n_p = add_vel(p,v)
		moons[i] = (n_p,v)

	return moons




def main():

#	print(scan1)
#	print()
	pos =  parse_scan(scan1)
	vels = []
	for _ in pos:
		vels.append([0,0,0])
	moons =[m for m in zip(pos,vels)]

	n_max = 10
	print_world(moons,0)

	for x in range(1,n_max+1):
		moons = next_time_step(moons)
		print_world(moons, x)





if __name__ == "__main__":
	main()








