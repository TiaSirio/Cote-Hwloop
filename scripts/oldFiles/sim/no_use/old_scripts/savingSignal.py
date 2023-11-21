import numpy as np
import sys

if len(sys.argv) != 2:
    sys.exit(-1)
else:
    num_symbols = int(sys.argv[1])

x_symbols = np.random.randint(0, 2, num_symbols)*2-1 # -1 and 1's
n = (np.random.randn(num_symbols) + 1j*np.random.randn(num_symbols))/np.sqrt(2) # AWGN with unity power
r = x_symbols + n * np.sqrt(0.01) # noise power of 0.01
#print(r)

# Now save to an IQ file
#print(type(r[0])) # Check data type.  Oops it's 128 not 64!
r = r.astype(np.complex64) # Convert to 64
#print(type(r[0])) # Verify it's 64
r.tofile('bpsk_in_noise.iq') # Save to file

samples = np.fromfile('bpsk_in_noise.iq', np.complex64) # Read in file.  We have to tell it what format it is
print(samples)