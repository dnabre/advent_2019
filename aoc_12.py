import re
import numpy as np
#import aocd

scan1 = [
	'<x=-1, y=0, z=2>',
	'<x=2, y=-10, z=-7>',
	'<x=4, y=-8, z=8>',
	'<x=3, y=5, z=-1>'
]


def vector3d(x,y,z):
	return np.array([x,y,z])

def parse_scan(scan1):
	result = []
	moons = []
	for line in scan1:
		line = line[1:-1]
		p = re.findall(r'-?\d+', line)  # this is a handy little RE found in a tutorial
		vals = [int(v) for v in p]
		result.append(vals)
		moons.append(vector3d(vals[0],vals[1],vals[2]))
	return moons



class Moon:
	'''
	init_pos - save where we started
	current_pos
	velocity
	accel
	net_force - sum of forces being applied in current time step
	
	
	'''
	def __init__(self,initial_pos):
		self.init_pos = initial_pos.copy()
		self.current_pos = initial_pos.copy()
		self.net_force = np.array([0,0,0])
		self.accel = np.array([0,0,0,])
		self.velocity = np.array([0,0,0,])
	#print(" {:3d} ".format(x), end='')
	
	@staticmethod 
	def vec2str(vec):
		s = '{:5d},{:5d},{:5d}'.format(vec[0],vec[1],vec[2])
		return s

	def __str__(self):
		result = ''
		result += 'Moon @ <{:s}> with vel: <{:s}>, accel: <{:s}>, net_f: <{:s}>'.format(
			Moon.vec2str(self.current_pos),
			Moon.vec2str(self.velocity),
			Moon.vec2str(self.accel),
			Moon.vec2str(self.net_force)
		)
		return result
	def apply_gravity(self,other_moon):


		return None

	def apply_forces(self):
		
		self.net_force=np.array([0,0,0])
		return None

	def step(self):

		self.accel = np.array([0,0,0])
		return None





def print_world(moons, n):
	print(f'After {n} steps:')
	for m in moons:
		p = Moon.vec2str( m.current_pos)
		v = Moon.vec2str( m.velocity)
		print('pos=<{:s}>, vel=<{:s}>'.format(p, v), end='')
		print()
	print()








puzzle = [
	'<x=-6, y=-5, z=-8>',
	'<x=0, y=-3, z=-13>',
	'<x=-15, y=10, z=-11>',
	'<x=-3, y=-8, z=3>']


def main():
	pos = parse_scan(scan1)
	print(pos)
	world_time_step = 0

	#setup and display initial moon list
	moon_list = []
	for m in pos:
		n_m = Moon(m)
		moon_list.append(n_m)
	print_world(moon_list, world_time_step)

	#Have each moon receive the force of gravity from all moons (excluding itseslf of course)
	for m in moon_list:
		for other_m in moon_list:
			if(m==other_m): continue
			else:
				m.apply_gravity(other_m)

	#Have each moon tally all the forces being applied to it, and calculate it's new acceleration
	# NOTE: this will zero all forces which have been applied
	for m in moon_list:
		m.apply_forces()

	#Have each moon progress time one step. So it's acceleration is applied to its velocity and the moon's position to updated
	# NOTE: this will zero acceleration after it has  have been applied
	for m in moon_list:
		m.step()
	world_time_step += 1

	print_world(moon_list, world_time_step)

if __name__ == "__main__":
	main()
