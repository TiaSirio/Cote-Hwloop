import matplotlib.pyplot as plt
import os
import sys

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
    print("Usage: python3 plot_hwloop.py /path/to/src/ /path/to/dst/ sat_counter job_per_sat name_for_dir")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

# Latency
base_xvalues = []
base_yvalues = []
with open(src + 'hwloop_latency.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        base_xvalues.append(int(line_split[0]))
        base_yvalues.append(float(line_split[1]))

# Generate latency plot
xmin = 0
xmax = sat_counter * 2
xstep = 50
ymin = 0
ymax = 400
ystep = 50
fig = plt.figure()
ax = plt.axes( \
    title='HWLoop', \
    xlabel='Instance of satellite', \
    xlim=(xmin, xmax), xscale='linear', \
    xticks=[x for x in range(xmin, xmax + xstep, xstep)], \
    xticklabels=[str(x) for x in range(xmin, xmax + xstep, xstep)], \
    ylabel='Seconds', \
    ylim=(ymin, ymax), yscale='linear', \
    yticks=[y for y in range(ymin, ymax + ystep, ystep)], \
    yticklabels=[str(y) for y in range(ymin, ymax + ystep, ystep)] \
    )
ax.plot(base_xvalues, base_yvalues, color='#000000', linestyle='solid', marker='2', label='HWLoop')
ax.legend()
fig.savefig(dst + 'hwloop_latency.pdf', bbox_inches='tight')
fig.savefig(dst + 'hwloop_latency.png', bbox_inches='tight')
plt.close(fig)
