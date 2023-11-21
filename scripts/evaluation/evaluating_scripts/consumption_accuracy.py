import sys
import os
from statistics import mean
from statistics import stdev
import matplotlib.pyplot as plt
import numpy as np
import math


def read_files(position):
    list_to_return = []

    for filename in os.listdir(position):
        total_sum = 0.0
        file_path = os.path.join(position, filename)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]
            for line in lines:
                line_split = line.split(',')
                total_sum += float(line_split[1].strip())
        list_to_return.append(total_sum)
    return list_to_return


def rmse(list_of_data, benchmark_value):
    temp_result = 0
    for i in range(len(list_of_data)):
        temp_result += (list_of_data[i] - benchmark_value) ** 2
    temp_result = temp_result / len(list_of_data)
    return math.sqrt(temp_result)


src_time = ''
src_consumption = ''


if len(sys.argv) == 3:
    src_time = sys.argv[1]
    if src_time[-1] != '/':
        src_time += '/'
    src_consumption = sys.argv[2]
    if src_consumption[-1] != '/':
        src_consumption += '/'
else:
    print("Usage: python3 conversion_consumption.py /path/to/time/ /path/to/consumption/")
    exit()

rasp = 1.375
pro_micro = 0.165
bme280 = 0.00001296
gy_521 = 0.012456
ina219 = 0.010080
benchmark_consumption = [rasp, pro_micro, bme280, gy_521, ina219]

total_time_list = read_files(src_time)
total_consumption_list = read_files(src_consumption)

total_time = mean(total_time_list)
total_consumption = mean(total_consumption_list)

print("Time (s): " + str(total_time))
print("Consumption (mJ): " + str(total_consumption))

total_benchmark_consumption_j = (sum(benchmark_consumption)) * total_time
total_consumption_j = total_consumption/1000
total_consumption_list_j = [elem / 1000 for elem in total_consumption_list]

power_consumption = [total_benchmark_consumption_j, total_consumption_j]
x = ["Datasheets", "Our simulation"]

rmse_result = rmse(total_consumption_list_j, total_benchmark_consumption_j)
print("RMSE: " + str(rmse_result))

error_capsize = 8
std_err = [0, stdev(total_consumption_list_j)]
# Generate plot
xmin = 0
xmax = len(x) - 1
xstep = 1
ymin = 0
ymax = max(power_consumption) + 40
ystep = max(power_consumption)/3
plt.rcParams.update({'font.size': 11})
#plt.rcParams.update({'font.size': 14})
bar_width = 0.8
plt.bar(x, power_consumption, width=bar_width, color='skyblue', edgecolor='black', alpha=0.7, yerr=std_err, ecolor='red', capsize=error_capsize)
plt.title('Evaluation accuracy')
plt.xlabel('Type of data')
plt.xlim(xmin - 0.5, xmax + 0.5)
plt.xticks(rotation=45)
plt.xticks(x, x)
plt.ylabel('Energy consumption [J]')
plt.ylim(ymin, ymax)
plt.yticks([y for y in np.arange(ymin, ymax, ystep)], [str('{:.3f}'.format(y)) for y in np.arange(ymin, ymax, ystep)])
plt.grid(True)
plt.savefig('../plots/accuracy/evaluation_accuracy.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/accuracy/evaluation_accuracy.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
