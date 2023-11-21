import numpy as np
import sys

if len(sys.argv) != 5:
    sys.exit(-1)
else:
    v_mph = int(int(sys.argv[1]))
    center_freq = float(sys.argv[2])
    Fs = float(sys.argv[3])
    N = int(sys.argv[4])

# Simulation Params, feel free to tweak these
# v_mph = 60 # velocity of either TX or RX, in miles per hour
# center_freq = 200e6 # RF carrier frequency in Hz
# Fs = 1e5 # sample rate of simulation
# N = 100 # number of sinusoids to sum

v = v_mph * 0.44704 # convert to m/s
fd = v*center_freq/3e8 # max Doppler shift
print("max Doppler shift:", fd)
t = np.arange(0, 1, 1/Fs) # time vector. (start, stop, step)
x = np.zeros(len(t))
y = np.zeros(len(t))
for i in range(N):
    alpha = (np.random.rand() - 0.5) * 2 * np.pi
    phi = (np.random.rand() - 0.5) * 2 * np.pi
    x = x + np.random.randn() * np.cos(2 * np.pi * fd * t * np.cos(alpha) + phi)
    y = y + np.random.randn() * np.sin(2 * np.pi * fd * t * np.cos(alpha) + phi)

# z is the complex coefficient representing channel, you can think of this as a phase shift and magnitude scale
z = (1/np.sqrt(N)) * (x + 1j*y) # this is what you would actually use when simulating the channel
z_mag = np.abs(z) # take magnitude for the sake of plotting
z_mag_dB = 10*np.log10(z_mag) # convert to dB