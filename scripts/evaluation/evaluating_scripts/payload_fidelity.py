import sys
import os
from statistics import stdev
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np


def retrieve_results(list_of_data):
    results_of_data = []
    for i in range(len(list_of_data)):
        if list_of_data[i] >= list_of_data[1]:
            results_of_data.append(((list_of_data[i] - list_of_data[1]) / list_of_data[1]) * 100)
        else:
            results_of_data.append(((list_of_data[i] - list_of_data[1]) / list_of_data[i]) * 100)
    return results_of_data


def stdev_results(list_of_data, baseline):
    # min_len = (min(len(list_of_data), len(baseline)))
    # list_of_data = list_of_data[:min_len]
    # baseline = baseline[:min_len]
    value_baseline = mean(baseline)
    results_of_data = []
    for i in range(len(list_of_data)):
        if list_of_data[i] >= value_baseline:
            results_of_data.append(((list_of_data[i] - value_baseline) / value_baseline) * 100)
        else:
            results_of_data.append(((list_of_data[i] - value_baseline) / list_of_data[i]) * 100)
    return stdev(results_of_data)


def read_files(position):
    list_to_return = []
    middle_list = []
    for filename in os.listdir(position):
        file_path = os.path.join(position, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]
            for line in lines:
                line_split = line.strip().split(';')
                middle_list.append(line_split)
        list_to_return.append(middle_list)
        middle_list = []
    return list_to_return


less_sleep = ''
more_sleep = ''
only_bus = ''
standard = ''

if len(sys.argv) == 5:
    less_sleep = sys.argv[1]
    if less_sleep[-1] != '/':
        less_sleep += '/'
    more_sleep = sys.argv[2]
    if more_sleep[-1] != '/':
        more_sleep += '/'
    only_bus = sys.argv[3]
    if only_bus[-1] != '/':
        only_bus += '/'
    standard = sys.argv[4]
    if standard[-1] != '/':
        standard += '/'
else:
    print("Usage: python3 payload_counter.py /path/to/less_sleep/ /path/to/more_sleep/ /path/to/only_bus/ /path/to/standard/")
    exit()

less_sleep_list = read_files(less_sleep)
len_less_sleep_list = [len(sublist) for sublist in less_sleep_list]
len_less_sleep = mean(len_less_sleep_list)

more_sleep_list = read_files(more_sleep)
len_more_sleep_list = [len(sublist) for sublist in more_sleep_list]
len_more_sleep = mean(len_more_sleep_list)

only_bus_list = read_files(only_bus)
len_only_bus_list = [len(sublist) for sublist in only_bus_list]
len_only_bus = mean(len_only_bus_list)

standard_list = read_files(standard)
len_standard_list = [len(sublist) for sublist in standard_list]
len_standard = mean(len_standard_list)

samples_time_list = [len_less_sleep, len_standard, len_more_sleep]
samples_relevant_elements = [len_only_bus, len_standard]

print("Number of samples less_sleep: " + str(len_less_sleep))
print("Number of samples more_sleep: " + str(len_more_sleep))
print("Number of samples only_bus: " + str(len_only_bus))
print("Number of samples standard: " + str(len_standard))

less_sleep_list = [[list_inner[0].split(',') for list_inner in list_medium] for list_medium in less_sleep_list]
more_sleep_list = [[list_inner[0].split(',') for list_inner in list_medium] for list_medium in more_sleep_list]
only_bus_list = [[list_inner[0].split(',') for list_inner in list_medium] for list_medium in only_bus_list]
standard_list = [[list_inner[0].split(',') for list_inner in list_medium] for list_medium in standard_list]

less_sleep_list = [[float(list_inner[8]) for list_inner in list_medium] for list_medium in less_sleep_list]
more_sleep_list = [[float(list_inner[8]) for list_inner in list_medium] for list_medium in more_sleep_list]
only_bus_list = [[float(list_inner[8]) for list_inner in list_medium] for list_medium in only_bus_list]
standard_list = [[float(list_inner[8]) for list_inner in list_medium] for list_medium in standard_list]

mean_less_sleep_list = [mean(sublist) for sublist in less_sleep_list]
mean_less_sleep = mean(mean_less_sleep_list)

mean_more_sleep_list = [mean(sublist) for sublist in more_sleep_list]
mean_more_sleep = mean(mean_more_sleep_list)

mean_only_bus_list = [mean(sublist) for sublist in only_bus_list]
mean_only_bus = mean(mean_only_bus_list)

mean_standard_list = [mean(sublist) for sublist in standard_list]
mean_standard = mean(mean_standard_list)

print("Mean less_sleep: " + str(mean_less_sleep))
print("Mean more_sleep: " + str(mean_more_sleep))
print("Mean only_bus: " + str(mean_only_bus))
print("Mean standard: " + str(mean_standard))

'''
stdev_less_sleep_list = [stdev(sublist) for sublist in less_sleep_list]
stdev_less_sleep = mean(stdev_less_sleep_list)
stdev_more_sleep_list = [stdev(sublist) for sublist in more_sleep_list]
stdev_more_sleep = mean(stdev_more_sleep_list)
stdev_only_bus_list = [stdev(sublist) for sublist in only_bus_list]
stdev_only_bus = mean(stdev_only_bus_list)
stdev_standard_list = [stdev(sublist) for sublist in standard_list]
stdev_standard = mean(stdev_standard_list)
print("Standard deviation less_sleep: " + str(stdev_less_sleep))
print("Standard deviation more_sleep: " + str(stdev_more_sleep))
print("Standard deviation only_bus: " + str(stdev_only_bus))
print("Standard deviation standard: " + str(stdev_standard))
'''

min_less_sleep_list = [min(sublist) for sublist in less_sleep_list]
min_less_sleep = mean(min_less_sleep_list)

min_more_sleep_list = [min(sublist) for sublist in more_sleep_list]
min_more_sleep = mean(min_more_sleep_list)

min_only_bus_list = [min(sublist) for sublist in only_bus_list]
min_only_bus = mean(min_only_bus_list)

min_standard_list = [min(sublist) for sublist in standard_list]
min_standard = mean(min_standard_list)

print("Min less_sleep: " + str(min_less_sleep))
print("Min more_sleep: " + str(min_more_sleep))
print("Min only_bus: " + str(min_only_bus))
print("Min standard: " + str(min_standard))

max_less_sleep_list = [max(sublist) for sublist in less_sleep_list]
max_less_sleep = mean(max_less_sleep_list)

max_more_sleep_list = [max(sublist) for sublist in more_sleep_list]
max_more_sleep = mean(max_more_sleep_list)

max_only_bus_list = [max(sublist) for sublist in only_bus_list]
max_only_bus = mean(max_only_bus_list)

max_standard_list = [max(sublist) for sublist in standard_list]
max_standard = mean(max_standard_list)

print("Max less_sleep: " + str(max_less_sleep))
print("Max more_sleep: " + str(max_more_sleep))
print("Max only_bus: " + str(max_only_bus))
print("Max standard: " + str(max_standard))

# Evaluation
results_samples_time = retrieve_results(samples_time_list)
x_samples_time = ["24 ms", "100 ms\nBaseline", "415 ms"]
results_relevant_elements = retrieve_results(samples_relevant_elements)
x_relevant_elements = ["12 ms\nOnly relevant information", "100 ms\nStandard"]

error_capsize = 8
std_err = [stdev_results(len_less_sleep_list, len_standard_list), stdev_results(len_standard_list, len_standard_list), stdev_results(len_more_sleep_list, len_standard_list)]
# std_err = [(stdev(len_less_sleep_list)/mean(len_less_sleep_list)) * 100, (stdev(len_standard_list)/mean(len_standard_list)) * 100, (stdev(len_more_sleep_list)/mean(len_more_sleep_list)) * 100]
# Generate plot
xmin = 0
xmax = len(x_samples_time) - 1
xstep = 1
ymin = min(results_samples_time) - 40
ymax = max(results_samples_time) + 40
ystep = max(results_samples_time)/3
plt.rcParams.update({'font.size': 14})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_samples_time, results_samples_time, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red')
plt.errorbar(x_samples_time, results_samples_time, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red', capsize=error_capsize)
# bar_width = 0.8
# plt.bar(x_samples_time, results_samples_time, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7,)
plt.title('Evaluation fidelity - Number of samples')
plt.xlabel('Sampling time')
plt.xlim(xmin - 0.2, xmax + 0.2)
plt.xticks(rotation=45)
plt.xticks(x_samples_time, x_samples_time)
plt.ylabel('Percentage of samples compared to the baseline')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_samples_fidelity.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/evaluation_samples_fidelity.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

std_err = [stdev_results(len_only_bus_list, len_standard_list), stdev_results(len_standard_list, len_standard_list)]
# Generate plot
xmin = 0
xmax = len(x_relevant_elements) - 1
xstep = 1
ymin = min(results_relevant_elements)
ymax = max(results_relevant_elements) + 100
ystep = max(1, (max(results_relevant_elements) - min(results_relevant_elements)) / 5)
plt.rcParams.update({'font.size': 14})
# ystep = max(results_relevant_elements)/5
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_relevant_elements, results_relevant_elements, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red')
plt.errorbar(x_relevant_elements, results_relevant_elements, color='black', linestyle='solid', marker='o', yerr=std_err, ecolor='red', capsize=error_capsize)
# bar_width = 0.8
# plt.bar(x_relevant_elements, results_relevant_elements, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err, ecolor='red')
plt.title('Evaluation fidelity - Relevant data recorded')
plt.xlabel('Sampling time')
plt.xlim(xmin - 0.2, xmax + 0.2)
plt.xticks(rotation=45)
plt.xticks(x_relevant_elements, x_relevant_elements)
plt.ylabel('Percentage of samples compared to the baseline')
plt.ylim(ymin - 10, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str(int(y)) + "%" for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_relevant_data_fidelity.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/evaluation_relevant_data_fidelity.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

x_statistics = ["12 ms\nOnly relevant information", "24 ms", "100 ms\nBaseline", "415 ms"]
mean_list = [mean_only_bus, mean_less_sleep, mean_standard, mean_more_sleep]
# stdev_list = [stdev_only_bus, stdev_less_sleep, stdev_standard, stdev_more_sleep]
min_list = [min_only_bus, min_less_sleep, min_standard, min_more_sleep]
max_list = [max_only_bus, max_less_sleep, max_standard, max_more_sleep]

std_err = [stdev(mean_only_bus_list), stdev(mean_less_sleep_list), stdev(mean_standard_list), stdev(mean_more_sleep_list)]
# Generate plot
xmin = 0
xmax = len(x_statistics) - 1
xstep = 1
ymin = 0.0
ymax = max(mean_list) + 30
ystep = max(mean_list)/5
plt.rcParams.update({'font.size': 14})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_statistics, mean_list, color='black', linestyle='solid', marker='o')
bar_width = 0.8
plt.bar(x_statistics, mean_list, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation fidelity - Mean')
plt.xlabel('Sampling time')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks(rotation=45)
plt.xticks(x_statistics, x_statistics)
plt.ylabel('Current draw in PSU [mA]')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_mean_fidelity.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/evaluation_mean_fidelity.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

'''
std_err = [stdev(stdev_only_bus_list), stdev(stdev_less_sleep_list), stdev(stdev_standard_list), stdev(stdev_more_sleep_list)]
# Generate plot
xmin = 0
xmax = len(x_statistics) - 1
xstep = 1
ymin = 0.0
ymax = max(stdev_list) + 2
ystep = max(stdev_list)/5
plt.rcParams.update({'font.size': 15})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_statistics, stdev_list, color='black', linestyle='solid', marker='o')
bar_width = 0.8
plt.bar(x_statistics, stdev_list, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err)
plt.title('Evaluation fidelity - Standard deviations')
plt.xlabel('Sampling')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks(rotation=45)
plt.xticks(x_statistics, x_statistics)
plt.ylabel('Standard deviation values')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_stdev_fidelity.svg', format='svg', bbox_inches="tight")
plt.clf()
'''

'''
std_err = [stdev(min_only_bus_list), stdev(min_less_sleep_list), stdev(min_standard_list), stdev(min_more_sleep_list)]
# Generate plot
xmin = 0
xmax = len(x_statistics) - 1
xstep = 1
ymin = 0.0
ymax = max(min_list) + 30
ystep = max(min_list)/4
plt.rcParams.update({'font.size': 15})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_statistics, min_list, color='black', linestyle='solid', marker='o')
bar_width = 0.8
plt.bar(x_statistics, min_list, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation fidelity - Min')
plt.xlabel('Sampling')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks(rotation=45)
plt.xticks(x_statistics, x_statistics)
plt.ylabel('Min values')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_min_fidelity.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/evaluation_min_fidelity.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()

std_err = [stdev(max_only_bus_list), stdev(max_less_sleep_list), stdev(max_standard_list), stdev(max_more_sleep_list)]
# Generate plot
xmin = 0
xmax = len(x_statistics) - 1
xstep = 1
ymin = 0.0
ymax = max(max_list) + 30
ystep = max(max_list)/5
plt.rcParams.update({'font.size': 15})
# plt.figure(figsize=(max(len(base_xvalues) - 4, 7), 7))
# plt.plot(x_statistics, max_list, color='black', linestyle='solid', marker='o')
bar_width = 0.8
plt.bar(x_statistics, max_list, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation fidelity - Max')
plt.xlabel('Sampling')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks(rotation=45)
plt.xticks(x_statistics, x_statistics)
plt.ylabel('Max values')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/fidelity/evaluation_max_fidelity.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/evaluation_max_fidelity.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
'''