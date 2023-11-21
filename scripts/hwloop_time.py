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

if len(sys.argv) == 10:
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
    dir_to_create_time = sys.argv[8]
    tasks_used_conf = sys.argv[9]
else:
    print(
        "Usage: python3 hwloop_time.py /full/path/to/src/, /full/path/to/dst/, 'Number of satellites', /full/path/to/exec/, /full/path/to/mapper/, 's for Single job or m for Multiple jobs' and 'number of jobs', 'dir_time', and 'tasks used'")
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

dst_sat = os.path.join(dst[:-1], dir_to_create_time)
if not os.path.exists(dst_sat):
    os.makedirs(dst_sat)

with open(dst_sat + 'hwloop_total_time_satellite.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'total_consume'])

totalSatelliteTime = []
mediumSatelliteTime = []

for j in range(sat_counter):
    totalTime = 0.0
    capture_pattern = 'event-cubesat-' + str(j) + '-time-job-*.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    capture_matches = sorted(capture_matches, key=get_job_number)
    for elem in capture_matches:
        with open(src + elem, 'r') as file:
            satelliteTime = list(csv.reader(file))
            satelliteTime = ["".join(element) for element in satelliteTime]
            satelliteTime.pop(0)
            satelliteTime = [float(element) for element in satelliteTime]
            mediumSatelliteTime.append(satelliteTime)
            for cons in satelliteTime:
                totalTime += cons
    if totalTime < 0:
        totalTime = 0
    # totalTime *= 1000
    with open(dst_sat + 'hwloop_total_time_satellite.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([j, totalTime])
    totalSatelliteTime.append(mediumSatelliteTime)
    mediumSatelliteTime = []


# Total time per job of each satellite
with open(dst_sat + 'hwloop_time_per_job.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'time-per-job'])

# Total time per task divided in each satellite
with open(dst_sat + 'hwloop_time_per_task.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'task', 'time-per-task'])


for k, job in enumerate(totalSatelliteTime):
    tempList = [[float(elemInner) for elemInner in elem] for elem in job]
    for p, val in enumerate(tempList):
        with open(dst_sat + 'hwloop_time_per_job.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([k, p, sum(val)])

if single:
    for k, job in enumerate(totalSatelliteTime):
        for j, lists in enumerate(job):
            # tempList = [float(elem) for elem in lists]
            for t, taskVal in enumerate(lists):
                with open(dst_sat + 'hwloop_time_per_task.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                    csvwriter.writerow([k, j, jobExecutables[k][t], taskVal])


consumePerTask = {}
counterPerTask = {}

for elemTask in filesInDir:
    consumePerTask[elemTask] = 0
    counterPerTask[elemTask] = 0

# Mean consume per task - Single job
files = os.listdir(src)

dst_task = os.path.join(dst[:-1], dir_to_create_time)
if not os.path.exists(dst_task):
    os.makedirs(dst_task)

with open(dst_task + "hwloop_mean_time_task.csv", 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['task', 'mean_consume'])

if single:
    for j in range(sat_counter):
        jobUsed = jobExecutables[j]
        capture_pattern = "event-cubesat-" + str(j) + "-time-job-*.csv"
        capture_matches = fnmatch.filter(files, capture_pattern)
        for elem in capture_matches:
            with open(src + elem, 'r') as file:
                satelliteTime = list(csv.reader(file))
                satelliteTime = ["".join(element) for element in satelliteTime]
                satelliteTime.pop(0)
                satelliteTime = [float(element) for element in satelliteTime]
                for idxTask, cons in enumerate(satelliteTime):
                    consumePerTask[jobUsed[idxTask]] += cons
                    counterPerTask[jobUsed[idxTask]] += 1

    # print(consumePerTask)
    for task, value in consumePerTask.items():
        if counterPerTask[task] == 0:
            meanTime = 0
        else:
            meanTime = value / counterPerTask[task]
        if meanTime < 0:
            meanTime = 0
        # meanTime *= 1000
        with open(dst_task + "hwloop_mean_time_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanTime])
else:
    for j in range(sat_counter):
        for k in range(job_counter):
            jobUsed = jobExecutables[(j * job_counter) + (k % job_counter)]
            capture_pattern = "event-cubesat-" + str(j) + "-time-job-" + str(k) + ".csv"
            capture_matches = fnmatch.filter(files, capture_pattern)
            if capture_matches is not None:
                for elem in capture_matches:
                    with open(src + elem, 'r') as file:
                        satelliteTime = list(csv.reader(file))
                        satelliteTime = ["".join(element) for element in satelliteTime]
                        satelliteTime.pop(0)
                        satelliteTime = [float(element) for element in satelliteTime]
                        for idxTask, cons in enumerate(satelliteTime):
                            consumePerTask[jobUsed[idxTask]] += cons
                            counterPerTask[jobUsed[idxTask]] += 1

    for task, value in consumePerTask.items():
        if counterPerTask[task] == 0:
            meanTime = 0
        else:
            meanTime = value / counterPerTask[task]
        if meanTime < 0:
            meanTime = 0
        # meanConsume *= 1000
        with open(dst_task + "hwloop_mean_time_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanTime])
