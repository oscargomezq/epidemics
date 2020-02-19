import numpy as np

# Size of groups
b = 4

# Number of levels
m = 4

# Size of population
N = b**m

# Probability for geometric distribution
p = 1/10

# Number of communities each person belongs to
heights = np.random.geometric(p=p, size=N)%(m+1)

# Array of infection
infected = [[np.zeros(N, dtype=int)]]
infected = [0][0] = 1

# Base b representations
base_b = np.zeros((N, b), dtype=int)

# Returns x+1 in base b
def next_in_base(x, b):
	nxt = x.copy()
	i=1
	while x[-i] == b-1:
		nxt[-i] = 0
		i-=1
	nxt[-i] = nxt[-i]+1
	return nxt

for i in range(1,N):
	base_b[i] = next_in_base(base_b[i-1], b)

print(base_b)


