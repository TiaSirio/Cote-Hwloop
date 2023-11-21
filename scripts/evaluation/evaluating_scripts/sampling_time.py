import sys
import os
from statistics import stdev
from statistics import mean


def sampling_time(list_of_data):
    time_slot = []
    data_to_use = [sublist[0].split(",") for sublist in list_of_data]
    data_to_use = [[float(element) for element in sublist] for sublist in data_to_use]
    data_to_use = [int(sublist[0]) for sublist in data_to_use]
    for t in range(0, len(data_to_use) - 1):
        time_slot.append((data_to_use[t + 1] - data_to_use[t]))
    time = mean(time_slot)
    return time


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


position = ''

if len(sys.argv) == 2:
    position = sys.argv[1]
    if position[-1] != '/':
        position += '/'
else:
    print("Usage: python3 sampling_time.py /path/to/position/")
    exit()

position_list = read_files(position)

all_sampling_times = [sampling_time(sublist) for sublist in position_list]
general_sampling_time = mean(all_sampling_times)
print(general_sampling_time)
