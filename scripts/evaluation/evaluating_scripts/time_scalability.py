import sys
import os
from statistics import mean
from statistics import stdev
import matplotlib.pyplot as plt
import numpy as np


class RedXLegendHandler(object):
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        x = width / 2
        y = height / 2
        marker = plt.Line2D([x], [y], marker='x', color='red', markersize=10, label=orig_handle.get_label())
        return [marker]


def read_files(position):
    list_to_return = []
    sorted_dirnames = sorted(os.listdir(position), key=lambda x: int(x))
    for dirname in sorted_dirnames:
        dirpath = os.path.join(position, dirname)
        for filename in os.listdir(dirpath):
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r') as file:
                file_data = file.read().split('\n')
                file_data = [str(file) for file in file_data]
                file_data = [int(file) for file in file_data if file != '']
                list_to_return.append(file_data)
    return list_to_return


def retrieve_results(list_of_data):
    results_of_data = []
    for i in range(len(list_of_data)):
        if list_of_data[i] >= list_of_data[0]:
            results_of_data.append(((list_of_data[i] - list_of_data[0]) / list_of_data[0]) * 100)
        else:
            results_of_data.append(((list_of_data[i] - list_of_data[0]) / list_of_data[i]) * 100)
        # ((list_of_data[i] - list_of_data[0])/list_of_data[0]) * 100)
    return results_of_data


def stdev_results(list_of_data):
    baseline = list_of_data[0]
    list_of_data.pop(0)
    # min_len = (min(len(list_of_data), len(baseline)))
    # list_of_data = [elem[:min_len] for elem in list_of_data]
    # baseline = baseline[:min_len]
    value_baseline = mean(baseline)
    results_of_data = []
    temp_results = []
    for elem in list_of_data:
        for i in range(len(elem)):
            if elem[i] >= value_baseline:
                temp_results.append(((elem[i] - value_baseline) / value_baseline) * 100)
            else:
                temp_results.append(((elem[i] - value_baseline) / elem[i]) * 100)
        results_of_data.append(stdev(temp_results))
        temp_results = []
    results_of_data.insert(0, 0)
    return results_of_data


jobs_scalability = ''
satellites_scalability = ''
system_scalability = ''

if len(sys.argv) == 4:
    jobs_scalability = sys.argv[1]
    if jobs_scalability[-1] != '/':
        jobs_scalability += '/'
    satellites_scalability = sys.argv[2]
    if satellites_scalability[-1] != '/':
        satellites_scalability += '/'
    system_scalability = sys.argv[3]
    if system_scalability[-1] != '/':
        system_scalability += '/'
else:
    print("Usage: python3 payload_counter.py /path/to/jobs_scalability/ /path/to/satellites_scalability/ /path/to/system_scalability/")
    exit()

jobs_scalability_list = read_files(jobs_scalability)
satellites_scalability_list = read_files(satellites_scalability)
system_scalability_list = read_files(system_scalability)

new_jobs_scalability_list = [mean(data) for data in jobs_scalability_list]
new_satellites_scalability_list = [mean(data) for data in satellites_scalability_list]
new_system_scalability_list = [mean(data) for data in system_scalability_list]

# jobs_scalability_list.reverse()
# system_scalability_list.reverse()

# print(new_jobs_scalability_list)
# print(new_satellites_scalability_list)
# print(new_system_scalability_list)

results_jobs_scalability = retrieve_results(new_jobs_scalability_list)
x_jobs_scalability = [1, 2, 4, 8, 16, 32, 64]
results_satellites_scalability = retrieve_results(new_satellites_scalability_list)
x_satellites_scalability = [1, 2, 4, 8, 10, 16]
results_system_scalability = retrieve_results(new_system_scalability_list)
x_system_scalability = [1, 2, 4, 8, 10, 16, 32, 64, 128, 256, 512, 640]
x_system_scalability_ticks = x_system_scalability.copy()
x_system_scalability_ticks[-1] = 1024
x_system_scalability_ticks.insert(-1, 1536)

print(results_jobs_scalability)
print(results_satellites_scalability)
print(results_system_scalability)

error_capsize = 8
std_err = stdev_results(jobs_scalability_list)
# std_err = [(stdev(data)/mean(data)) * 100 for data in jobs_scalability_list]
# Generate plot
xmin = 1
xmax = len(x_jobs_scalability)
xstep = 1
ymin = 0.0
ymax = max(results_jobs_scalability) + 100
ystep = max(results_jobs_scalability)/5
plt.rcParams.update({'font.size': 14})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
plt.errorbar(x_jobs_scalability, results_jobs_scalability, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation scalability - Jobs')
plt.xlabel('Number of jobs')
plt.xlim(xmin, xmax)
plt.xticks(x_jobs_scalability, x_jobs_scalability)
plt.ylabel('Percentage of time compared to the baseline')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/scalability/evaluation_jobs_scalability.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/scalability/evaluation_jobs_scalability.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

std_err = stdev_results(satellites_scalability_list)
# Generate plot
xmin = 1
xmax = len(x_satellites_scalability)
xstep = 1
ymin = min(results_satellites_scalability) - 10
ymax = max(results_satellites_scalability) + 10
ystep = (ymax - ymin) / 5
plt.rcParams.update({'font.size': 14})
plt.errorbar(x_satellites_scalability, results_satellites_scalability, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation scalability - Nano-satellites')
plt.xlabel('Number of physical nano-satellites')
plt.xlim(xmin, xmax)
plt.xticks(x_satellites_scalability, x_satellites_scalability)
plt.ylabel('Percentage of time compared to the baseline')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/scalability/evaluation_satellites_scalability.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/scalability/evaluation_satellites_scalability.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

std_err = stdev_results(system_scalability_list)
# Generate plot
xmin = 1
xmax = len(x_system_scalability)
xstep = 1
ymin = 0.0
ymax = max(results_system_scalability) + 14
ystep = (ymax - ymin) / 5
plt.rcParams.update({'font.size': 20})
#plt.rcParams.update({'font.size': 30})
plt.figure(figsize=(15, 8))
plt.errorbar(x_system_scalability, results_system_scalability, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red', capsize=error_capsize)

x_positions = [768, 1024]
plt.plot(x_positions[0], results_system_scalability[-1], 'bx', markersize=20, label='Missing MQTT messages')
plt.plot(x_positions[1], results_system_scalability[-1], 'rx', markersize=20, label='MQTT fails in creating publishers')

plt.title('Evaluation scalability - System')
plt.xlabel('Number of simulated and physical nano-satellites')
plt.xlim(xmin, xmax)
plt.xticks(x_system_scalability_ticks, x_system_scalability_ticks)
plt.ylabel('Percentage of time compared to the baseline')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.xscale('log', base=2)
plt.legend(loc='upper right')
plt.grid(True)
plt.savefig('../plots/scalability/evaluation_system_scalability.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/scalability/evaluation_system_scalability.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
