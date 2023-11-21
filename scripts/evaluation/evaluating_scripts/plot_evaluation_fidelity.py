import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np


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

    value_to_return = random.choice(list_to_return)
    return value_to_return


def calculate_slot(data):
    list_to_return = []
    for i in range(len(data)):
        list_to_return.append((data[i] - data[0])/1000)
    return list_to_return


position_standard = ''
position_less = ''
position_more = ''
position_bus = ''

if len(sys.argv) == 5:
    position_standard = sys.argv[1]
    if position_standard[-1] != '/':
        position_standard += '/'
    position_less = sys.argv[2]
    if position_less[-1] != '/':
        position_less += '/'
    position_more = sys.argv[3]
    if position_more[-1] != '/':
        position_more += '/'
    position_bus = sys.argv[4]
    if position_bus[-1] != '/':
        position_bus += '/'
else:
    print("Usage: python3 plot_evaluation_fidelity.py /path/to/position/ /path/to/position/ /path/to/position/ /path/to/position/")
    exit()

position_list_standard = read_files(position_standard)
position_list_less = read_files(position_less)
position_list_more = read_files(position_more)
position_list_bus = read_files(position_bus)

position_list_standard = [list_medium[0].split(',') for list_medium in position_list_standard]
x_standard = [int(list_medium[0]) for list_medium in position_list_standard]
position_list_standard = [float(list_medium[8]) for list_medium in position_list_standard]
position_list_less = [list_medium[0].split(',') for list_medium in position_list_less]
x_less = [int(list_medium[0]) for list_medium in position_list_less]
position_list_less = [float(list_medium[8]) for list_medium in position_list_less]
position_list_more = [list_medium[0].split(',') for list_medium in position_list_more]
x_more = [int(list_medium[0]) for list_medium in position_list_more]
position_list_more = [float(list_medium[8]) for list_medium in position_list_more]
position_list_bus = [list_medium[0].split(',') for list_medium in position_list_bus]
x_bus = [int(list_medium[0]) for list_medium in position_list_bus]
position_list_bus = [float(list_medium[8]) for list_medium in position_list_bus]

x_standard = calculate_slot(x_standard)
x_less = calculate_slot(x_less)
x_more = calculate_slot(x_more)
x_bus = calculate_slot(x_bus)

# Create a Matplotlib figure and plot the data
plt.rcParams.update({'font.size': 32.5})
plt.figure(figsize=(30, 7))
plt.plot(x_standard, position_list_standard, label='Standard - 100 ms', color='blue', alpha=0.5)
plt.plot(x_less, position_list_less, label='Faster - 24 ms', color='green', alpha=0.5)
plt.plot(x_more, position_list_more, label='Slower - 415 ms', color='red', alpha=0.5)
plt.plot(x_bus, position_list_bus, label='Only bus - 12 ms', color='orange', alpha=0.5)
plt.xlim(-10, 830)
plt.xlabel('Time [s]')
plt.ylabel('Current draw in PSU [mA]')
plt.title('Current draw comparison between sampling times')
plt.legend(loc='upper right')
plt.grid(True)

# Show the plot
plt.savefig('../plots/fidelity/visual_comparison.svg', format='svg', bbox_inches="tight")
plt.savefig('../plots/fidelity/visual_comparison.eps', format='eps', bbox_inches="tight", transparent=True)
plt.clf()
