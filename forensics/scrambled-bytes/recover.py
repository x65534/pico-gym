#!/usr/bin/env python3

import sys
import random
 
SEED = 1614044650
INFILE = 'data.txt'
OUTFILE = 'recovered.dat'

# Parse the source port -> payload byte file
ports = []
data = bytearray() 
with open('payload.txt', 'r') as f:
    for line in f.readlines():
        split = line.split()
        if len(split) != 2:
            print(f'Invalid payload data')
            exit(1)
        ports.append(int(split[0]))
        data.append(int(split[1], 16))

# Store an array of shuffled indices to unshuffle the data later
# Each value in the shuffled array will contain the index of its original position
indices = [*range(len(data))]
random.seed(SEED)
random.shuffle(indices)
recovered = bytearray([0] * len(data))

# Loop through each byte in the payload
for i in range(len(data)):
    # Verify that the state of the random number generator is correct
    expected_port = ports[i]
    port = random.randrange(65536)
    if port != expected_port:
        print(f'Port mismatch on line {i+1}, expected {port}, was {expected_port}')
        exit(1)
    # Decrypt and unshuffle the data
    recovered[indices[i]] = data[i] ^ random.randrange(256)

# Write out the result
with open(OUTFILE, 'wb') as f:
    f.write(recovered)

print(f'Wrote {len(recovered)} byte(s) to {OUTFILE}')

