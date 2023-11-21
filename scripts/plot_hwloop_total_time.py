import matplotlib.pyplot as plt
import numpy as np
import os
import sys

plt.set_loglevel("error")
src = ''
dst = ''
sat_counter = 0
job_total = 0
job_per_sat = 0
name_for_dir = ""

if len(sys.argv) == 6:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    sat_counter = int(sys.argv[4])
    job_total = int(sys.argv[4]) * int(sys.argv[3])
    job_per_sat = int(sys.argv[3])
    name_for_dir = sys.argv[5]
else:
    print("Usage: python3 plot_hwloop_total_time.py /path/to/src/ /path/to/dst/ job_per_sat sat_counter name_for_dir")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

# Coverage
base_xvalues = []
base_yvalues = []
with open(src + 'hwloop_total_time_satellite.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        base_xvalues.append(int(line_split[0]))
        base_yvalues.append(float(line_split[1]))

# base_yvalues = [k/1000 for k in base_yvalues]

# Generate plot
xmin = 0
xmax = sat_counter - 1
xstep = 1
ymin = 0.0
ymax = 1 if max(base_yvalues) <= 0 else max(base_yvalues) + max(base_yvalues) / 10
ystep = 0.25 if max(base_yvalues) <= 0 else max(base_yvalues) / 4
plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
bar_width = 0.8
plt.bar(base_xvalues, base_yvalues, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7)
# plt.plot(base_xvalues, base_yvalues, color='black', linestyle='solid', marker='o')
# plt.bar(base_xvalues, base_yvalues, color='blue', width=0.8)
plt.title('Total time per satellite')
plt.xlabel('Instance of satellite')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
plt.ylabel("Total time [s]")
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)],
           [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
# plt.savefig(dst + 'hwloop_consume_sat.pdf', format='pdf')
plt.savefig(dst + 'hwloop_total_time.svg', format='svg', bbox_inches="tight")
plt.savefig(dst + 'hwloop_total_time.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
