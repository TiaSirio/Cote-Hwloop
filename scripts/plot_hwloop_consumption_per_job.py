import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

plt.set_loglevel("error")
src = ''
dst = ''
sat_counter = 0
job_counter = 0
name_for_dir = ""

if len(sys.argv) == 6:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    sat_counter = int(sys.argv[3])
    job_counter = int(sys.argv[4])
    name_for_dir = sys.argv[5]
else:
    print("Usage: python3 plot_hwloop_consumption_per_job.py /path/to/src/ /path/to/dst/ sat_counter job_per_sat name_for_dir")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

if not os.path.exists(src + 'hwloop_consumption_per_job.csv'):
    sys.exit(-1)

# Coverage
base_xvalues = []
base_yvalues = []
temp = 0
total_xvalues = []
total_yvalues = []
with open(src + 'hwloop_consumption_per_job.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        if temp != int(line_split[0]):
            temp = int(line_split[0])
            total_xvalues.append(base_xvalues)
            total_yvalues.append(base_yvalues)
            base_xvalues = []
            base_yvalues = []
        base_xvalues.append(int(line_split[1].strip()))
        base_yvalues.append(float(line_split[2].strip()))

total_xvalues.append(base_xvalues)
total_yvalues.append(base_yvalues)

# Generate plot
for j in range(sat_counter):
    jobs_sat = list(range(0, job_counter))
    base_xvalues = total_xvalues[j]
    base_yvalues = total_yvalues[j]
    # Generate plot
    # base_yvalues = [k/1000 for k in base_yvalues]
    xmin = 0
    xmax = base_xvalues[-1]
    xstep = 1
    ymin = 0.0
    ymax = max(base_yvalues) + min(base_yvalues) / 4
    ystep = max(base_yvalues) / 3
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
    plt.plot(base_xvalues, base_yvalues, color='black', linestyle='solid', marker='o')
    plt.title('Consumption per job for satellite ' + str(j))
    plt.xlabel('Jobs')
    plt.xlim(xmin, xmax)
    plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
    plt.ylabel('Consumption [mJ]')
    plt.ylim(ymin, ymax)
    plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
    plt.grid(True)
    plt.savefig(dst + 'hwloop_consumption_per_job_for_satellite_' + str(j) + '.svg', format='svg', bbox_inches="tight")
    plt.savefig(dst + 'hwloop_consumption_per_job_for_satellite_' + str(j) + '.eps', format='eps', bbox_inches="tight", transparent=True)
    plt.clf()

