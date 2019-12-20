import re
import numpy as np
import math
# import aocd

scan1 = [
	'<x=-1, y=0, z=2>',
	'<x=2, y=-10, z=-7>',
	'<x=4, y=-8, z=8>',
	'<x=3, y=5, z=-1>'
]

scan2 = [
	'<x=-8, y=-10, z=0>',
	'<x=5, y=5, z=10>',
	'<x=2, y=-7, z=3>',
	'<x=9, y=-8, z=-3>'
]


def vector3d(x, y, z):
	return np.array([x, y, z])


def vec3d_equal(x,y):
	if(x[0] != y[0]):
		return False
	if(x[1] != y[1]):
		return False
	if(x[2] != y[2]):
		return False
	return True

def lcm3(x,y,z):
	gcd2 = math.gcd(y,z)
	lcm2 = y*z // gcd2
	lcm3 = x * lcm2 // math.gcd(x,lcm2)
	return lcm3




def parse_scan(scan1):
	result = []
	moons = []
	for line in scan1:
		line = line[1:-1]
		p = re.findall(r'-?\d+', line)  # this is a handy little RE found in a tutorial
		vals = [int(v) for v in p]
		result.append(vals)
		moons.append(vector3d(vals[0], vals[1], vals[2]))
	return moons


class Moon:
	'''
	init_pos - save where we started
	current_pos
	velocity
	accel
	net_force - sum of forces being applied in current time step
	
	
	'''

	def __init__(self, initial_pos):
		self.init_pos = initial_pos.copy()
		self.current_pos = initial_pos.copy()
		self.net_force = np.array([0, 0, 0])
		self.accel = np.array([0, 0, 0, ])
		self.velocity = np.array([0, 0, 0, ])
		self.history = []

	@staticmethod
	def vec2str(vec):
		s = '{:5d},{:5d},{:5d}'.format(vec[0], vec[1], vec[2])
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

	def apply_gravity(self, other_moon):
		unit_vectors = [
			np.array([1, 0, 0]),
			np.array([0, 1, 0]),
			np.array([0, 0, 1])
		]

		for axis in [0, 1, 2]:
			my_val = self.current_pos[axis]
			other_value = other_moon.current_pos[axis]
			if (my_val < other_value):
				self.net_force += unit_vectors[axis]
			elif (my_val > other_value):
				self.net_force -= unit_vectors[axis]

	def apply_forces(self):
		self.accel = self.net_force.copy()
		self.net_force = np.array([0, 0, 0])


	def repeated(self, new_pos, new_vel):
		pos_repeated= False
		vel_repeated = False
		if(
			(self.init_pos[0] == new_pos[0]) and
				(self.init_pos[1] == new_pos[1]) and
				(self.init_pos[2] == new_pos[2])):
			pos_repeated = True

		if (
			(0 == new_vel[0]) and
			(0 == new_vel[1]) and
			(0 == new_vel[2])):
			vel_repeatd = True
		return (pos_repeated and vel_repeated)




	def step(self):
		#		self.history += (self.current_pos.copy(), self.velocity.copy())
		self.velocity += self.accel
		self.current_pos += self.velocity
		self.accel = np.array([0, 0, 0])
		return (self.repeated(self.current_pos, self.velocity))


def total_energy(self):
	p_e = 0
	p_e = abs(self.current_pos[0]) + abs(self.current_pos[1]) + abs(self.current_pos[2])
	k_e = abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])
	return p_e * k_e


def print_world(moons, n):
	print(f'After {n} steps:')
	for m in moons:
		p = Moon.vec2str(m.current_pos)
		v = Moon.vec2str(m.velocity)
		print('pos=<{:s}>, vel=<{:s}>'.format(p, v), end='')
		print()


def print_energy(moons):
	result = 'Sum of total energy:'
	sum_of_te = 0
	for m in moons:
		t_e = m.total_energy()
		sum_of_te += t_e
		result += f' {t_e} +'
	result = result[:-1]
	result += "= " + str(sum_of_te)
	print(result)


def step_world(moon_list):
	# Have each moon receive the force of gravity from all moons (excluding itseslf of course)
	for m in moon_list:
		for other_m in moon_list:
			if (m == other_m):
				continue
			else:
				m.apply_gravity(other_m)

	# Have each moon tally all the forces being applied to it, and calculate it's new acceleration
	# NOTE: this will zero all forces which have been applied
	for m in moon_list:
		m.apply_forces()

	# Have each moon progress time one step. So it's acceleration is applied to its velocity and the moon's position to updated
	# NOTE: this will zero acceleration after it has  have been applied
	found = False
	for m in moon_list:
		m.step()

ZERO_VECTOR = vector3d(0,0,0)

def check_for_repeat(moons):
	for m in moons:
		if (not vec3d_equal(m.init_pos, m.current_pos)):
			return False
		if (not vec3d_equal(ZERO_VECTOR, m.velocity)):
			return False
	return True

def check_for_repeat_axis(moon_list,axis):
	for m in moon_list:
		if ( m.init_pos[axis] != m.current_pos[axis]):
			return False
		if (m.velocity[axis] != 0):
			return False
	return True


axis_found = [0,0,0]





# Part 1 Solution: 5937
# Part 2 Solution: 376203951569712


puzzle = [
	'<x=-6, y=-5, z=-8>',
	'<x=0, y=-3, z=-13>',
	'<x=-15, y=10, z=-11>',
	'<x=-3, y=-8, z=3>']


def main():
	pos = parse_scan(puzzle)
	print(pos)
	world_time_step = 0

	# setup and display initial moon list
	moon_list = []
	for m in pos:
		n_m = Moon(m)
		moon_list.append(n_m)
	print_world(moon_list, world_time_step)

	while ( world_time_step < 1_000_000_000) :
		step_world(moon_list)
		world_time_step += 1
	#	if(world_time_step % 100 == 0): print(world_time_step)
		for axis in [0,1,2]:
			if(axis_found[axis] > 0):
				continue
			ax_result = check_for_repeat_axis(moon_list,axis)
			if(ax_result):
				axis_found[axis] = world_time_step
				print(f'repeat on axis: {axis} at step # {world_time_step}')
				print_world(moon_list, world_time_step)
				r = axis_found[0] * axis_found[1] * axis_found[2]
				if (r > 0):
					l3 = lcm3(axis_found[0] , axis_found[1] , axis_found[2])
					print(f'Predicted repeat step is: {l3}')



		result = check_for_repeat(moon_list)
		if (result):
			print(f"\nState Repeat found at step #{world_time_step}")
			break
	print_world(moon_list, world_time_step)


#			print_energy(moon_list)


if __name__ == "__main__":
	main()
