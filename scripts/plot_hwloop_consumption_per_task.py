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
    print("Usage: python3 plot_hwloop_consumption_per_task.py /path/to/src/ /path/to/dst/ sat_counter job_counter name_for_dir")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

if not os.path.exists(src + 'hwloop_consumption_per_task.csv'):
    sys.exit(-1)

# Coverage
base_xvalues = []
base_yvalues = []
temp = 0
medium_xvalues = []
medium_yvalues = []
temp_2 = 0
total_xvalues = []
total_yvalues = []

with open(src + 'hwloop_consumption_per_task.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        if temp != int(line_split[1]):
            temp = int(line_split[1])
            medium_xvalues.append(base_xvalues)
            medium_yvalues.append(base_yvalues)
            base_xvalues = []
            base_yvalues = []
        if temp_2 != int(line_split[0]):
            temp_2 = int(line_split[0])
            total_xvalues.append(medium_xvalues)
            total_yvalues.append(medium_yvalues)
            medium_xvalues = []
            medium_yvalues = []
        base_xvalues.append(str(line_split[2].strip()))
        base_yvalues.append(float(line_split[3].strip()))

medium_xvalues.append(base_xvalues)
medium_yvalues.append(base_yvalues)
total_xvalues.append(medium_xvalues)
total_yvalues.append(medium_yvalues)
# print(total_xvalues)

# Generate plot
for j in range(sat_counter):
    base_xvalues = total_xvalues[j] # [[sublist[j] for sublist in subsublist] for subsublist in total_xvalues]
    base_yvalues = total_yvalues[j] # [[sublist[j] for sublist in subsublist] for subsublist in total_yvalues]
    # print(base_xvalues)
    for m, elem in enumerate(base_xvalues):
        # totVal = sum(base_yvalues[m])
        # percentageVal = [(el/totVal)*100 for el in base_yvalues[m]]
        # xvalues_new = [i for i in range(len(elem))]
        # base_yvalues[m] = [k/1000 for k in base_yvalues[m]]
        xmin = 0
        xmax = len(elem) - 1
        xstep = 1
        ymin = 0.0
        ymax = max(base_yvalues[m]) + min(base_yvalues[m]) / 4
        ystep = max(base_yvalues[m]) / 3
        plt.rcParams.update({'font.size': 15})
        plt.figure(figsize=(max(len(elem) - 4, 7), 7))
        # plt.plot(xvalues_new, base_yvalues[m], color='black', linestyle='solid', marker='o')
        # plt.pie(percentageVal, labels=base_yvalues[m], autopct='%1.1f%%', startangle=140)
        bar_width = 0.8
        plt.bar(elem, base_yvalues[m], width=bar_width, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title('Consumption per task of satellite ' + str(j) + ' for job ' + str(m))
        plt.xlabel('Tasks')
        plt.xlim(xmin - 0.5, xmax + 0.5)
        plt.xticks(rotation=45)
        plt.xticks(elem, elem)
        # plt.xticks([x for x in np.arange(xmin, xmax + xstep, xstep)], [str(int(x)) for x in np.arange(xmin, xmax + xstep, xstep)])
        plt.ylabel('Consumption [mJ]')
        plt.ylim(ymin, ymax)
        plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
        plt.grid(True)
        plt.savefig(dst + 'hwloop_consumption_per_task_of_satellite_' + str(j) + '_for_job_' + str(m) + '.svg', format='svg', bbox_inches="tight")
        plt.savefig(dst + 'hwloop_consumption_per_task_of_satellite_' + str(j) + '_for_job_' + str(m) + '.eps', format='eps', bbox_inches="tight", transparent=True)
        plt.clf()
        plt.close('all')
