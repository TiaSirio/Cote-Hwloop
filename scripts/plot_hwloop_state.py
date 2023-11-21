import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import fnmatch

plt.set_loglevel("error")
src = ''
dst = ''
sat_counter = 0
job_total = 0
job_per_sat = 0
name_for_dir = ""
sleepPresent = True

if len(sys.argv) == 8:
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
    src_log_no_process = sys.argv[6]
    dir_state_percentage = sys.argv[7]
else:
    print(
        "Usage: python3 plot_hwloop_state.py /path/to/src/ /path/to/dst/ job_per_sat sat_counter name_for_dir src_log_no_process dir_state_percentage")
    exit()

dst_bkp = dst
dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

all_contents = os.listdir(src_log_no_process)
subdirs = []

for e in all_contents:
    if os.path.isdir(src_log_no_process + e):
        subdirs.append(e)
subdirs.sort()

files = os.listdir(src_log_no_process)
for j in range(sat_counter):
    readerSleepStart = []
    readerSleepEnd = []

    capture_pattern = 'event-cubesat-' + str(j) + '-working-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src_log_no_process + "".join(capture_matches), 'r') as file:
        readerWorkStart = list(csv.reader(file))
        readerWorkStart = ["".join(elem) for elem in readerWorkStart]
        readerWorkStart.pop(0)
        readerWorkStart = [float(elem) for elem in readerWorkStart]

    capture_pattern = 'event-cubesat-' + str(j) + '-working-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src_log_no_process + "".join(capture_matches), 'r') as file:
        readerWorkEnd = list(csv.reader(file))
        readerWorkEnd = ["".join(elem) for elem in readerWorkEnd]
        readerWorkEnd.pop(0)
        readerWorkEnd = [float(elem) for elem in readerWorkEnd]

    capture_pattern = 'event-cubesat-' + str(j) + '-idle-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src_log_no_process + "".join(capture_matches), 'r') as file:
        readerIdleStart = list(csv.reader(file))
        readerIdleStart = ["".join(elem) for elem in readerIdleStart]
        readerIdleStart.pop(0)
        readerIdleStart = [float(elem) for elem in readerIdleStart]

    capture_pattern = 'event-cubesat-' + str(j) + '-idle-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src_log_no_process + "".join(capture_matches), 'r') as file:
        readerIdleEnd = list(csv.reader(file))
        readerIdleEnd = ["".join(elem) for elem in readerIdleEnd]
        readerIdleEnd.pop(0)
        readerIdleEnd = [float(elem) for elem in readerIdleEnd]

    capture_pattern = 'event-cubesat-' + str(j) + '-sleep-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    elif (len(capture_matches) == 1):
        with open(src_log_no_process + "".join(capture_matches), 'r') as file:
            readerSleepStart = list(csv.reader(file))
            readerSleepStart = ["".join(elem) for elem in readerSleepStart]
            readerSleepStart.pop(0)
            readerSleepStart = [float(elem) for elem in readerSleepStart]
    else:
        sleepPresent = False

    capture_pattern = 'event-cubesat-' + str(j) + '-sleep-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    elif (len(capture_matches) == 1):
        with open(src_log_no_process + "".join(capture_matches), 'r') as file:
            readerSleepEnd = list(csv.reader(file))
            readerSleepEnd = ["".join(elem) for elem in readerSleepEnd]
            readerSleepEnd.pop(0)
            readerSleepEnd = [float(elem) for elem in readerSleepEnd]
    else:
        sleepPresent = False

    # Idle = 1
    # Sleep = 2
    # Working = 3

    state_sequence = []
    times = []

    sublists = [readerIdleStart, readerSleepStart, readerWorkStart]

    plt.rcParams.update({'font.size': 15})

    while readerIdleStart or readerIdleEnd or readerWorkStart or (
            readerWorkEnd) or readerSleepStart or readerSleepEnd:
        minimum_value = float('inf')
        minimumIndex = None

        for i, sublist in enumerate(sublists):
            if sublist and sublist[0] is not None and sublist[0] < minimum_value:
                minimum_value = sublist[0]
                minimumIndex = i + 1

        if minimumIndex is None:
            break

        if minimumIndex is not None:
            state_sequence.append(minimumIndex)
            if minimumIndex == 1:
                times.append(readerIdleEnd[0] - readerIdleStart[0])
                readerIdleStart.pop(0)
                readerIdleEnd.pop(0)
            elif minimumIndex == 2:
                times.append(readerSleepEnd[0] - readerSleepStart[0])
                readerSleepStart.pop(0)
                readerSleepEnd.pop(0)
            else:
                times.append(readerWorkEnd[0] - readerWorkStart[0])
                readerWorkStart.pop(0)
                readerWorkEnd.pop(0)

    # Define the states and corresponding labels
    states = [1, 2, 3]
    state_labels = ['Idle', 'Sleep', 'Working']

    # Create a list of cumulative times
    cumulative_times = [sum(times[:i + 1]) for i in range(len(times))]

    # Create bars with height defined by state_labels and states, and width defined by times
    for i in range(len(state_sequence)):
        if state_sequence[i] == 1:
            plt.bar(cumulative_times[i] - times[i], state_sequence[i], width=times[i], bottom=0, align='edge',
                    alpha=0.5, color='yellow')
        elif state_sequence[i] == 2:
            plt.bar(cumulative_times[i] - times[i], state_sequence[i], width=times[i], bottom=0, align='edge',
                    alpha=0.5, color='red')
        elif state_sequence[i] == 3:
            plt.bar(cumulative_times[i] - times[i], state_sequence[i], width=times[i], bottom=0, align='edge',
                    alpha=0.7, color='skyblue', linewidth=2)

    # Set y-axis ticks and labels
    plt.yticks(states, state_labels)

    legend_handles = [
        plt.Line2D([0], [0], color='skyblue', linewidth=1, linestyle='-', label='Working', alpha=0.7),
        plt.Line2D([0], [0], color='red', linewidth=1, linestyle='-', label='Sleep', alpha=0.5),
        plt.Line2D([0], [0], color='yellow', linewidth=1, linestyle='-', label='Idle', alpha=0.5)
    ]

    plt.legend(handles=legend_handles)

    plt.title('State machine satellite ' + str(j))
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.ylim(0, 4)

    xmin = 0
    xmax = cumulative_times[-1]
    xstep = round(cumulative_times[-1] / 4, 3)

    plt.xlim(-cumulative_times[-1] / 100, cumulative_times[-1] + cumulative_times[-1] / 100)
    x_ticks = np.linspace(0, cumulative_times[-1], 5)
    x_tick_labels = np.linspace(0, cumulative_times[-1], 5).astype(float)
    x_tick_labels = np.round(x_tick_labels, 1)

    x_tick_labels = [str(x) + " s" for x in x_tick_labels]

    plt.gca().set_xticks(x_ticks)
    plt.gca().set_xticklabels(x_tick_labels)

    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)
    plt.savefig(dst + 'hwloop_state_machine_sat_' + str(j) + '.svg', format='svg', bbox_inches="tight")
    plt.savefig(dst + 'hwloop_state_machine_sat_' + str(j) + '.eps', format='eps', bbox_inches="tight", transparent=True)
    plt.clf()

dst_bkp = os.path.join(dst_bkp[:-1], dir_state_percentage)
if not os.path.exists(dst_bkp):
    os.makedirs(dst_bkp)

base_xvalues_idle = []
base_yvalues_idle = []
with open(src + 'hwloop_state_idle.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        base_xvalues_idle.append(int(line_split[0]))
        base_yvalues_idle.append(float(line_split[1]))

# Generate plot
xmin = 0
xmax = sat_counter - 1
xstep = 1
ymin = 0.0
ymax = 1.12
ystep = 0.25
plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(max(len(base_yvalues_idle) - 4, 7), 7))
bar_width = 0.8
plt.bar(base_xvalues_idle, base_yvalues_idle, width=bar_width, color='yellow', edgecolor='black', alpha=0.5)
# plt.plot(base_xvalues_idle, base_yvalues_idle, color='black', linestyle='solid', marker='o')
# plt.bar(base_xvalues, base_yvalues, color='blue', width=0.8)
plt.title('Percentage in idle state')
plt.xlabel('Instance of satellite')
plt.xlim(xmin, xmax)
plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
plt.ylabel('Percentage')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y * 100)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
# plt.savefig(dst_bkp + 'hwloop_state_idle.pdf', format='pdf')
plt.savefig(dst_bkp + 'hwloop_state_idle.svg', format='svg', bbox_inches="tight")
plt.savefig(dst_bkp + 'hwloop_state_idle.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

base_xvalues_sleep = []
base_yvalues_sleep = []
with open(src + 'hwloop_state_sleep.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        base_xvalues_sleep.append(int(line_split[0]))
        base_yvalues_sleep.append(float(line_split[1]))

if base_xvalues_sleep and base_yvalues_sleep:
    # Generate plot
    xmin = 0
    xmax = sat_counter - 1
    xstep = 1
    ymin = 0.0
    ymax = 1.12
    ystep = 0.25
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize=(max(len(base_yvalues_sleep) - 4, 7), 7))
    bar_width = 0.8
    plt.bar(base_xvalues_sleep, base_yvalues_sleep, width=bar_width, color='red', edgecolor='black', alpha=0.5)
    # plt.plot(base_xvalues_sleep, base_yvalues_sleep, color='blue', linestyle='solid', marker='o')
    # plt.bar(base_xvalues, base_yvalues, color='blue', width=0.8)
    plt.title('Percentage in sleep state')
    plt.xlabel('Instance of satellite')
    plt.xlim(xmin, xmax)
    plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
    plt.ylabel('Percentage')
    plt.ylim(ymin, ymax)
    plt.yticks([y for y in np.arange(ymin, ymax, ystep)],
               [str(int(y * 100)) + "%" for y in np.arange(ymin, ymax, ystep)])
    plt.grid(True)
    # plt.savefig(dst_bkp + 'hwloop_state_sleep.pdf', format='pdf')
    plt.savefig(dst_bkp + 'hwloop_state_sleep.svg', format='svg', bbox_inches="tight")
    plt.savefig(dst_bkp + 'hwloop_state_sleep.eps', format='eps', bbox_inches="tight", transparent=True)
    plt.clf()

base_xvalues_working = []
base_yvalues_working = []
with open(src + 'hwloop_state_working.csv', 'r') as infile:
    lines = infile.readlines()
    lines = lines[1:]
    for line in lines:
        line_split = line.split(',')
        base_xvalues_working.append(int(line_split[0]))
        base_yvalues_working.append(float(line_split[1]))

# Generate plot
xmin = 0
xmax = sat_counter - 1
xstep = 1
ymin = 0.0
ymax = 1.12
ystep = 0.25
plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(max(len(base_yvalues_working) - 4, 7), 7))
bar_width = 0.8
plt.bar(base_xvalues_working, base_yvalues_working, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7)
# plt.plot(base_xvalues_working, base_yvalues_working, color='blue', linestyle='solid', marker='o')
# plt.bar(base_xvalues, base_yvalues, color='blue', width=0.8)
plt.title('Percentage in working state')
plt.xlabel('Instance of satellite')
plt.xlim(xmin, xmax)
plt.xticks([x for x in range(xmin, xmax + xstep, xstep)], [str(x) for x in range(xmin, xmax + xstep, xstep)])
plt.ylabel('Percentage')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y * 100)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
# plt.savefig(dst_bkp + 'hwloop_state_working.pdf', format='pdf')
plt.savefig(dst_bkp + 'hwloop_state_working.svg', format='svg', bbox_inches="tight")
plt.savefig(dst_bkp + 'hwloop_state_working.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
