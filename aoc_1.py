import math

FILENAME = "aoc_1_input.txt"

# test cases for part 1
TESTS_1 = [
		[12, 2],
	        [14, 2],
	        [1969, 654],
	        [100756, 33583]
	]

# test cases for part 2
TESTS_2 = [
		[14, 2],
		[1969, 966],
		[100756, 50346]
	]


def fuel_for_mass(mass):
	""" Calculate the fuel required for given mass (not including the mass of the fuel)
	Where the fuel need for mass is floor(mass/3) - 2
	"""
	return math.floor(mass / 3) - 2


def fuel_for_module(mass):
	""" Calculating the fuel for a module includes the mass of the fuel and the mass of the
	fuel for that fuel, so forth, until the addition mass due to fuel is negligible. Where
	negligible means the calculate for fuel_for_mass gives zero.
	"""
	fuel = fuel_for_mass(mass)
	fuel_for_fuel = fuel_for_mass(fuel)
	while (fuel_for_fuel > 0):
		fuel += fuel_for_fuel
		fuel_for_fuel = fuel_for_mass(fuel_for_fuel)
	return fuel


def main():
	print("Checking test-cases for part #1:", end=' ')
	for t in TESTS_1:
		test_input = t[0]
		test_output = t[1]
		result = fuel_for_mass(test_input)
		assert (test_output == result)
	#	print(f'test: fuel_for_mass({test_input}) = {test_output}')
	#	print(f'real: fuel_for_mass({test_input}) = {result}')
	print("done")

	f = open(FILENAME, "r")
	lines = f.readlines()

	summation = 0
	for l in lines:
		summation = summation + fuel_for_mass(int(l))

	print(f'Total fuel for part #1: {summation}')

	print("Checking test-cases for part #2:", end=' ')
	for t in TESTS_2:
		test_input = t[0]
		test_output = t[1]
		result = fuel_for_module(test_input)
		assert (test_output == result)
	#	print(f'test: fuel_for_module({test_input}) = {test_output}')
	#	print(f'real: fuel_for_module({test_input}) = {result}')
	print("done")

	summation = 0
	for l in lines:
		summation = summation + fuel_for_module(int(l))

	print(f'Total fuel for part #2: {summation}')


if __name__ == "__main__":
	main()