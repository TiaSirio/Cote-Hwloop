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
    print("Usage: python3 plot_hwloop_errors_per_job.py /path/to/src/ /path/to/dst/ sat_counter job_counter name_for_dir")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

if not os.path.exists(src + 'hwloop_errors_per_satellite.csv'):
    sys.exit(-1)

# Coverage
base_xvalues = []
base_yvalues = []
temp = 0
total_xvalues = []
total_yvalues = []
with open(src + 'hwloop_errors_per_satellite.csv', 'r') as infile:
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
        base_xvalues.append(int(line_split[0]))
        base_yvalues.append(int(line_split[1]))

total_xvalues.append(base_xvalues)
total_yvalues.append(base_yvalues)

precedentElem = 0
counter = 0
total_errors = []
temp_errors = []

for lists in total_yvalues:
    # No errors
    if lists[0] == -1:
        temp_errors = [0 for _ in range(job_counter)]
        total_errors.append(temp_errors)
        temp_errors = []
    else:
        precedentElem = 0
        j = 0
        while j < len(lists):
            while precedentElem != lists[j]:
                precedentElem += 1
                temp_errors.append(0)
                counter = 0
            while precedentElem == lists[j]:
                counter += 1
                j += 1
                if j == len(lists):
                    break
            precedentElem += 1
            temp_errors.append(counter)
            counter = 0
        while precedentElem < job_counter:
            precedentElem += 1
            temp_errors.append(0)
            counter = 0
        total_errors.append(temp_errors)
        temp_errors = []

# Generate plot
for j in range(sat_counter):
    jobs_sat = list(range(0, job_counter))
    list_yvalues = total_errors[j]
    xmin = 0
    xmax = job_counter - 1
    xstep = 1
    ymin = 0.0
    ymax = max(list_yvalues) + 1
    ystep = 1
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize=(max(len(list_yvalues) - 4, 7), 7))
    plt.plot(jobs_sat, list_yvalues, color='black', linestyle='solid', marker='o')
    plt.title('Errors per jobs for satellite ' + str(j))
    plt.xlabel('Jobs')
    plt.xlim(xmin, xmax)
    plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
    plt.ylabel('Errors')
    plt.ylim(ymin, ymax)
    plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) for y in np.arange(ymin, ymax, ystep)])
    plt.grid(True)
    # plt.savefig(dst + 'hwloop_coverage.pdf', format='pdf', dpi=300, bbox_inches="tight")
    plt.savefig(dst + 'hwloop_errors_' + str(j) + '.svg', format='svg', bbox_inches="tight")
    plt.savefig(dst + 'hwloop_errors_' + str(j) + '.eps', format='eps', bbox_inches="tight", transparent=True)
    plt.clf()
