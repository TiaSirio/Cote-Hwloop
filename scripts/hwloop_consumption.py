import csv
import fnmatch
import os
import sys
import re


def get_job_number(filename):
    return int(filename.split('-')[-1].split('.')[0])


src = ''
dst = ''
sat_counter = 0
single = True

if len(sys.argv) == 11:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    sat_counter = int(sys.argv[3])
    execPath = sys.argv[4]
    mapper = sys.argv[5]
    single = sys.argv[6] == "s"
    job_counter = int(sys.argv[7])
    dir_to_create_task = sys.argv[8]
    dir_to_create_sat = sys.argv[9]
    tasks_used_conf = sys.argv[10]
else:
    print(
        "Usage: python3 hwloop_consumption.py /full/path/to/src/, /full/path/to/dst/, 'Number of satellites', /full/path/to/exec/, /full/path/to/mapper/, 's for Single job or m for Multiple jobs' and 'number of jobs', 'dir_task', 'dir_sat' and 'tasks used'")
    exit()

'''
onlyfiles = [f for f in listdir(execPath) if isfile(join(execPath, f)) and (f.endswith(".py") or f.endswith(".c"))]

filesInDir = []
jobExecutables = []

for task in onlyfiles:
    if task.endswith(".c"):
        filesInDir.append(task[:-2])
    else:
        filesInDir.append(task)

# print(filesInDir)
'''

filesInDir = []

with open(tasks_used_conf, "r") as fileConf:
    lines2 = fileConf.readlines()
    lines2 = [line.rstrip().split("=") for line in lines2]
    for line in lines2:
        filesInDir.append(line[1])

jobExecutables = []

with open(mapper) as file:
    lines = file.read().splitlines()

for task in lines:
    if ";" in task:
        arguments = task.split(";")
        jobExecutables.append(";".join(arguments))
    else:
        jobExecutables.append(task)

jobExecutables = [elem.split(",") for elem in jobExecutables]
jobExecutables = [[elemIn.split(";") for elemIn in elem] for elem in jobExecutables]

# Remove instance of sat
for i in range(len(jobExecutables)):
    jobExecutables[i].pop(0)

for job in jobExecutables:
    for task in job:
        for j in range(len(task)):
            if task[j].startswith("?"):
                task[j] = task[j][2:]


# Remove attributes
for job in jobExecutables:
    for i in range(len(job)):
        job[i] = job[i][0]

if not single:
    for job in jobExecutables:
        job.pop(0)
# print(jobExecutables)

all_contents = os.listdir(src)
subdirs = []

for e in all_contents:
    if os.path.isdir(src + e):
        subdirs.append(e)
subdirs.sort()

# Total consume per satellite
# for subdir in subdirs:

files = os.listdir(src)

dst_sat = os.path.join(dst[:-1], dir_to_create_sat)
if not os.path.exists(dst_sat):
    os.makedirs(dst_sat)

with open(dst_sat + 'hwloop_total_consumption_satellite.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'total_consume'])

totalSatelliteConsumption = []
mediumSatelliteConsumption = []

for j in range(sat_counter):
    totalConsumption = 0.0
    capture_pattern = 'event-cubesat-' + str(j) + '-consumption-job-*.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    capture_matches = sorted(capture_matches, key=get_job_number)
    for elem in capture_matches:
        with open(src + elem, 'r') as file:
            satelliteConsumption = list(csv.reader(file))
            satelliteConsumption = ["".join(element) for element in satelliteConsumption]
            satelliteConsumption.pop(0)
            satelliteConsumption = [float(element) for element in satelliteConsumption]
            mediumSatelliteConsumption.append(satelliteConsumption)
            for cons in satelliteConsumption:
                totalConsumption += cons
    if totalConsumption < 0:
        totalConsumption = 0
    # totalConsumption *= 1000
    with open(dst_sat + 'hwloop_total_consumption_satellite.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([j, totalConsumption])
    totalSatelliteConsumption.append(mediumSatelliteConsumption)
    mediumSatelliteConsumption = []


# Total consumption per job of each satellite
with open(dst_sat + 'hwloop_consumption_per_job.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'time-per-job'])

# Total consumption per task divided in each satellite
with open(dst_sat + 'hwloop_consumption_per_task.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'task', 'time-per-task'])


for k, job in enumerate(totalSatelliteConsumption):
    tempList = [[float(elemInner) for elemInner in elem] for elem in job]
    for p, val in enumerate(tempList):
        with open(dst_sat + 'hwloop_consumption_per_job.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([k, p, sum(val)])

if single:
    for k, job in enumerate(totalSatelliteConsumption):
        for j, lists in enumerate(job):
            # tempList = [float(elem) for elem in lists]
            for t, taskVal in enumerate(lists):
                with open(dst_sat + 'hwloop_consumption_per_task.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                    csvwriter.writerow([k, j, jobExecutables[k][t], taskVal])


consumePerTask = {}
counterPerTask = {}

for elemTask in filesInDir:
    consumePerTask[elemTask] = 0
    counterPerTask[elemTask] = 0

# Mean consume per task - Single job
files = os.listdir(src)

dst_task = os.path.join(dst[:-1], dir_to_create_task)
if not os.path.exists(dst_task):
    os.makedirs(dst_task)

with open(dst_task + "hwloop_mean_consumption_task.csv", 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['task', 'mean_consume'])

if single:
    for j in range(sat_counter):
        jobUsed = jobExecutables[j]
        capture_pattern = "event-cubesat-" + str(j) + "-consumption-job-*.csv"
        capture_matches = fnmatch.filter(files, capture_pattern)
        for elem in capture_matches:
            with open(src + elem, 'r') as file:
                satelliteConsumption = list(csv.reader(file))
                satelliteConsumption = ["".join(element) for element in satelliteConsumption]
                satelliteConsumption.pop(0)
                satelliteConsumption = [float(element) for element in satelliteConsumption]
                for idxTask, cons in enumerate(satelliteConsumption):
                    consumePerTask[jobUsed[idxTask]] += cons
                    counterPerTask[jobUsed[idxTask]] += 1

    # print(consumePerTask)
    for task, value in consumePerTask.items():
        if counterPerTask[task] == 0:
            meanConsumption = 0
        else:
            meanConsumption = value / counterPerTask[task]
        if meanConsumption < 0:
            meanConsumption = 0
        # meanConsumption *= 1000
        with open(dst_task + "hwloop_mean_consumption_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanConsumption])
else:
    for j in range(sat_counter):
        for k in range(job_counter):
            jobUsed = jobExecutables[(j * job_counter) + (k % job_counter)]
            capture_pattern = "event-cubesat-" + str(j) + "-consumption-job-" + str(k) + ".csv"
            capture_matches = fnmatch.filter(files, capture_pattern)
            if capture_matches is not None:
                for elem in capture_matches:
                    with open(src + elem, 'r') as file:
                        satelliteConsumption = list(csv.reader(file))
                        satelliteConsumption = ["".join(element) for element in satelliteConsumption]
                        satelliteConsumption.pop(0)
                        satelliteConsumption = [float(element) for element in satelliteConsumption]
                        for idxTask, cons in enumerate(satelliteConsumption):
                            consumePerTask[jobUsed[idxTask]] += cons
                            counterPerTask[jobUsed[idxTask]] += 1

    for task, value in consumePerTask.items():
        if counterPerTask[task] == 0:
            meanConsumption = 0
        else:
            meanConsumption = value / counterPerTask[task]
        if meanConsumption < 0:
            meanConsumption = 0
        # meanConsume *= 1000
        with open(dst_task + "hwloop_mean_consumption_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanConsumption])
