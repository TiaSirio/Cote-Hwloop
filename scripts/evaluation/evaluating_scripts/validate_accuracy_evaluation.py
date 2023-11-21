import sys
import os
from statistics import stdev
from statistics import mean


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

total_time_list = read_files(src_time)
total_consumption_list = read_files(src_consumption)

perc_std = (stdev(total_time_list)/mean(total_time_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Time OK!")
else:
    print("Time - NOT OK!")
    exit()

perc_std = (stdev(total_consumption_list)/mean(total_consumption_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Consumption OK!")
else:
    print("Consumption - NOT OK!")
    exit()



