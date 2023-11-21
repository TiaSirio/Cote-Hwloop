import sys
from statistics import stdev
from statistics import mean


def read_data(position):
    with open(position, 'r') as file:
        file_data = file.read().split('\n')
        file_data = [str(file) for file in file_data]
        file_data = [int(file) for file in file_data if file != '']
        data_file = file_data
    return data_file


position = ''

if len(sys.argv) == 2:
    position = sys.argv[1]
else:
    print("Usage: python3 validate_scalability_evaluation.py /path/to/position/")
    exit()

data_list = read_data(position)

perc_std = (stdev(data_list)/mean(data_list)) * 100
print(perc_std)
if perc_std < 5:
    print("Simulation times OK!")
else:
    print("Simulation times - NOT OK!")
    exit(1)
