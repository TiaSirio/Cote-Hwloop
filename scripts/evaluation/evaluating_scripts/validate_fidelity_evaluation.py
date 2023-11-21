import sys
import os
from statistics import stdev
from statistics import mean


def read_files(position):
    list_to_return = []
    middle_list = []
    # sorted_dirnames = sorted(os.listdir(position), key=lambda x: int(x))

    # for dirname in sorted_dirnames:
    #     dirpath = os.path.join(position, dirname)
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
    print("Usage: python3 validate_fidelity_evaluation.py /path/to/position/")
    exit()

position_list = read_files(position)

len_list = [len(sublist) for sublist in position_list]

# print(len_list)
# print(min(len_list))
# print(max(len_list))
perc_std = (stdev(len_list)/mean(len_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Number of samples OK!")
else:
    print("Number of samples - NOT OK!")
    exit(1)

mean_list = []
std_list = []
min_list = []
max_list = []
for sublist in position_list:
    temp_list = [list_medium[0].split(',') for list_medium in sublist]
    temp_list = [float(list_medium[8]) for list_medium in temp_list]
    mean_list.append(mean(temp_list))
    std_list.append(stdev(temp_list))
    min_list.append(min(temp_list))
    max_list.append(max(temp_list))

perc_std = (stdev(mean_list)/mean(mean_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Mean OK!")
else:
    print("Mean - NOT OK!")
    exit(1)

perc_std = (stdev(std_list)/mean(std_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Standard deviation OK!")
else:
    print("Standard deviation - NOT OK!")
    exit(1)

perc_std = (stdev(min_list)/mean(min_list)) * 100
print(perc_std)
if perc_std < 10:
    print("Min OK!")
else:
    print("Min - NOT OK!")
    exit(1)

perc_std = (stdev(max_list)/mean(max_list)) * 100
print(perc_std)
if perc_std < 6:
    print("Max OK!")
else:
    print("Max - NOT OK!")
    exit(1)
