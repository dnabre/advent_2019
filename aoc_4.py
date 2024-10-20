#Advent of Code 2019: Day Secure Container
__author__ = "dnabre"
__email__ = "dnabre@happybunnylabs.com"

RANGE = (134564,585159)


# Rule #1
def valid_six_digit_number(secret):
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
	return True

# Rule #3
def valid_doubled_digit(secret):
	"""Two adjacent digits are the same (like 22 in 122345).
	"""
	for i in range(5):
		if(secret[i] == secret[i+1]):
			return True
	return False

def valid_doubled_digit2(secret):
	#This bit (for part 2) took a bunch of tweaking and trial & error in the end
	for i in range(1,6):	#1,2,3,4,5
		if((i>1) and (secret[i-2] == secret[i])): continue
		if((i<5) and (secret[i+1] == secret[i])): continue
		if(secret[i-1] == secret[i]):
			return True
	return False


# Rule #4
def valid_monotonic(secret):
	"""Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
	"""
	for i in range(5):
		if(int(secret[i]) > int(secret[i+1])):
			return False
	return True


def valid(secret):
	if(valid_six_digit_number(secret)):
		if(valid_range(secret)):
			if(valid_doubled_digit(secret)):
				if(valid_monotonic(secret)):
					return True
	return False


def valid2(secret):
	if(valid_six_digit_number(secret)):
		if(valid_range(secret)):
			if(valid_doubled_digit2(secret)):
				if(valid_monotonic(secret)):
					return True
	return False



def main():
	

	count=0
	(good_number, max_number ) = RANGE
	print(f'Part 1: Checking from {good_number} to {max_number}')
	while (good_number <=  max_number):
		if(valid(str(good_number))):
			count= count + 1
		good_number = good_number + 1	
	print(f'        Found {count} ' )

	print('\n')	

	count=0
	(good_number, max_number ) = RANGE
	print(f'Part 2: Checking from {good_number} to {max_number}')
	while (good_number <=  max_number):
		if(valid2(str(good_number))):
			count= count + 1
		good_number = good_number + 1
	print(f'        Found {count} ')
	


if __name__ == "__main__":
	main()