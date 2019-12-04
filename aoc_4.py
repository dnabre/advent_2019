#Advent of Code 2019: Day Secure Container
__author__ = "dnabre"
__email__ = "dnabre@happybunnylabs.com"

RANGE = (134564,585159)

TESTS_1 = [
# Secret, Validity, Rule (1-4) Broken (0 being no rules)
	('111111',False ,1),
	('223450',False ,4),
	('123789',False ,3)
]

"""
TESTS_2 = [
	('R8,U5,L5,D3\nU7,R6,D4,L4',30),
	('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83',610),
	('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7',410)
]
"""


# Password rules given by problem

# Rule #1
def valid_six_digit_number(secret):
#	print("valid_six_digit_number")
	""" It is a six-digit number.
	"""
	if(len(secret)!=6):
		return False
	if(not secret.isnumeric()):
		return False
#	print(f'{secret} is a six digit number')
	return True

# Rule #2
def valid_range(secret):
#	print("valid_range")
	""" The value is within the range given in your puzzle input.
	"""
	(low,high) = RANGE
	int_secret = int(secret)
	if(int_secret < low):
		return False
	if(int_secret > high):
		return False

#	print(f'{secret} is within range {low} to {high}')	
	return True

# Rule #3
def valid_doubled_digit(secret):
#	print("valid_doubled_digit")
	"""Two adjacent digits are the same (like 22 in 122345).
	"""
	for i in range(5):
	#print(f'{secret}\t secret[{i}]={secret[i]} \t secret[{i+1}]={secret[i+1]} \t {secret[i] == secret[i+1]}')
		if(secret[i] == secret[i+1]):
		#	print(f'{secret} has doubled digit {secret[i]}')
			return True
	return False

# Rule #4
def valid_monotonic(secret):
#	print("valid_monotonic")
	"""Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
	"""
	for i in range(5):
#		print(f'{secret}\t secret[{i}]={secret[i]} \t secret[{i+1}]={secret[i+1]} \t {secret[i] > secret[i+1]}')
		if(int(secret[i]) > int(secret[i+1])):
			return False
#	print(f'{secret}\t secret[{i}]={secret[i]} \t secret[{i+1}]={secret[i+1]} \t {secret[i] > secret[i+1]}')
	return True

rules = [valid_six_digit_number, valid_range, valid_doubled_digit, valid_monotonic]

def valid_only_doubled(secret):

	i = 0
	while (i < 5):
	#print(f'{secret}\t secret[{i}]={secret[i]} \t secret[{i+1}]={secret[i+1]} \t {secret[i] == secret[i+1]}')
		if(secret[i] == secret[i+1]):
		#	print(f'{secret} has doubled digit {secret[i]}')
			return True
	return False

def valid(secret):
	

	if(valid_six_digit_number(secret)):
		if(valid_range(secret)):
			if(valid_doubled_digit(secret)):
				if(valid_monotonic(secret)):
					return True
	return False

def main():
	print('Part 1 : running given examples: ')
	
	print(rules)


	for t in TESTS_1:
		(s, v, rule) = t
		rule_no = valid(s)
		print(f'\t Secret: {s} \t Valid: {v} \t Rule Number Broken: {rule} => ')
		print(f'\t Secret: {s} \t Valid: {rule_no==0} \t Rule Number Broken: {rule_no}')
		#assert(rule_no == r)
		print()
	print(' done')
	
	count=0
	(good_number, max ) = RANGE
	
	while (good_number <=  max):
		if(valid(str(good_number))):
			count= count + 1
			print(good_number)
		good_number = good_number + 1
	
	print(count)







if __name__ == "__main__":
	main()

