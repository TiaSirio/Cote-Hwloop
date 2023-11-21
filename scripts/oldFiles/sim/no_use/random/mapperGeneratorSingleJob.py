from os import listdir
from os.path import isfile, join
import os
import random
import sys
import yaml

if len(sys.argv) < 4:
    print("Needed as arguments: \"Instances of satellite\", \"Number of jobs per satellite\" and \"Maximum number of tasks for each job\"!")
    sys.exit()

satellite = int(sys.argv[1])
jobs = int(sys.argv[2])
maxNumberOfTasks = int(sys.argv[3])

# Get the name of all the files in the correct directory
execPath = os.getcwd() + "/cexec/"
mapperPath = os.getcwd() + "/cexec/mapper.txt"
onlyfiles = [f for f in listdir(execPath) if isfile(join(execPath, f)) and (f.endswith(".py") or f.endswith(".c"))]
if maxNumberOfTasks > len(onlyfiles):
    maxNumberOfTasks = len(onlyfiles)

preExec = []
# Load yaml and store the mapping of arguments for each program
with open(r'programs.yaml') as file:
    programs = yaml.load(file, Loader=yaml.FullLoader)
    for f in onlyfiles:
        for prog, arg in programs.items():
            if arg is not None and str(prog) == str(f):
                preExec.append(f + ";" + ";".join([str(elem) for elem in arg]))
                break
            elif str(prog) == str(f):
                preExec.append(f)
    #print(program)


# Remove .c to save the compiled name in the mapper
executables = []
for f in preExec:
    if ";" in f:
        arguments = f.split(";")
        if arguments[0].endswith(".c"):
            temp = arguments[0]
            arguments.pop(0)
            arguments.insert(0, temp[:-2])
            executables.append(";".join(arguments))
        else:
            executables.append(";".join(arguments))
    else:
        if f.endswith(".c"):
            executables.append(f[:-2])
        else:
            executables.append(f)

# print(executables)

tasks = []
for i in range(satellite):
    tasks.append(random.sample(executables, k=random.randint(1,maxNumberOfTasks)))

# Save mapper in a file
with open(mapperPath, "w") as file:
    for _ in range(jobs):
        for i in range(satellite):
            stringToWrite = str(i + 1) + "," + ",".join(tasks[i]) + "\n"
            # print(stringToWrite)
            file.write(stringToWrite)