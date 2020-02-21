import numpy as np

# Number of levels
m = 4

# Size of population
N = 4**m

# Probability for geometric distribution
p = 1/10

# Array of infection
infected_history = [set({(2,2)})]
total_infected = set({(2,2)})

# Returns x+1 in base b
def next_in_base(x, b):
	nxt = x.copy()
	i=1
	while x[-i] == b-1:
		nxt[-i] = 0
		i-=1
	nxt[-i] = nxt[-i]+1
	return nxt

# Get same height everytime we sample
def get_height (x,y):
	x1 = bin_to_dec(x)
	y1 = bin_to_dec(y)
	idx = x1*(4**(m/2)) + y1
	np.random.seed(int(idx))
	return np.random.geometric(p=p)%(m+1)

# The range will be 2**h
# return starting point for range
# x and y are binary strings
def find_range (x, y, h):
	x1 = x[:-h] + "0"*h
	y1 = y[:-h] + "0"*h
	return (x1, y1, 2**h)

def dec_to_bin (x, digits):
	b = bin(x)[2:]
	b = "0"*(digits-len(b)) + b
	return b

def bin_to_dec (b):
	return int(b,2)

def next_in_bin(b):
	if b == "1"*(len(b)):
		return "1" + "0"*len(b)
	nxt = ''
	i=1
	while b[-i] == '1':
		nxt = '0' + nxt
		i+=1
	nxt = '1' + nxt
	nxt = b[:len(b)-len(nxt)]+ nxt
	return nxt

def infect_iteration_h (x, y, h):
	start_x, start_y, length =  find_range(x,y,h)
	compare_x, compare_y = start_x, start_y
	for i in range(length):
		if i>0: compare_y = next_in_bin(compare_y)
		for j in range(length):
			if j>0: compare_x = next_in_bin(compare_x)
			print(compare_x, compare_y)
			compare_h = get_height(compare_x, compare_y)
			# got_infected = try_to_infect(x, y, h, compare_x, compare_y)
			# if got_infected:
			# 	#append com_x and comp_y to infected list
			# 	pass
		compare_x = start_x

def infect_iteration (x, y, h):
	for i in range (1,h+1):
		infect_iteration_h (x,y,i)
	# Check nearest neighbors (height 0) separately

def try_to_infect(x, y, h, compare_x, compare_y):
	# Check if height of comp_x, comp_y is at least h
	#
	pass





x=37
y=255
xbin = dec_to_bin(x, m)
ybin = dec_to_bin(y, m)
print(xbin,ybin)
print(find_range(xbin, ybin, 3))


print(next_in_bin(xbin), next_in_bin(ybin))

x=0
y=0
xbin = dec_to_bin(x, m)
ybin = dec_to_bin(y, m)
infect_iteration(xbin,ybin,3)
