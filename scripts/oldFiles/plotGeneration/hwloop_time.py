import csv
import fnmatch
import os
import sys


def get_job_number(filename):
    return int(filename.split('-')[-1].split('.')[0])


src = ''
dst = ''
job_count = 0
job_per_satellite = 0
sat_counter = 0

if len(sys.argv) == 10:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    job_count = int(sys.argv[3]) * int(sys.argv[4])
    job_per_satellite = int(sys.argv[3])
    sat_counter = int(sys.argv[4])
    dir_to_create = sys.argv[5]
    execPath = sys.argv[6]
    mapper = sys.argv[7]
    single = sys.argv[8] == "s"
    tasks_used_conf = sys.argv[9]
else:
    print(
        "Usage: python3 hwloop_time.py /full/path/to/src/ /full/path/to/dst/ 'Number of jobs' 'Number of satellites' 'dir_to_create' 'executables_path' 'mapper' 'single or multiple jobs' 'tasks_used_conf'")
    exit()

dst = os.path.join(dst[:-1], dir_to_create)
if not os.path.exists(dst):
    os.makedirs(dst)

all_contents = os.listdir(src)
subdirs = []

for e in all_contents:
    if os.path.isdir(src + e):
        subdirs.append(e)
subdirs.sort()

files = os.listdir(src)
capture_matches = []
total_capture_matches = []
t = 0

for i in range(sat_counter):
    t = 0
    while True:
        capture_pattern = 'event-cubesat-' + str(i) + '-task-' + str(t) + '-duration.csv'
        t += 1
        capture_matches_temp = fnmatch.filter(files, capture_pattern)
        if len(capture_matches_temp) == 0:
            break
        else:
            capture_matches.append(capture_matches_temp)
    total_capture_matches.append(capture_matches)
    capture_matches = []


# print(total_capture_matches)

totalList = []
# Total time of each satellite
with open(dst + 'hwloop_total_time.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'time-per-sat'])

# Total time per job of each satellite
with open(dst + 'hwloop_time_per_job.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'time-per-job'])

# Total time per task divided in each satellite
with open(dst + 'hwloop_time_per_task.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job', 'task', 'time-per-task'])

tempTime = []
for capture_matches in total_capture_matches:
    tempTime = []
    for file_cap in capture_matches:
        with open(src + "".join(file_cap), 'r') as file:
            timeList = list(csv.reader(file))
            timeList = ["".join(elem) for elem in timeList]
            timeList.pop(0)
        tempTime.append(timeList)
    totalList.append(tempTime)

# print(total_capture_matches)
# print(totalList)


# Mean time per task
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

# Mean time per task
with open(dst + 'hwloop_mean_time_per_task.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['task', 'mean-time-per-task'])

timePerTask = {}
counterPerTask = {}

for elemTask in filesInDir:
    timePerTask[elemTask] = 0
    counterPerTask[elemTask] = 0


for k, job in enumerate(totalList):
    tempList = [[float(elemInner) for elemInner in elem] for elem in job]
    sumList = [sum(t) for t in tempList]
    with open(dst + 'hwloop_total_time.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([k, sum(sumList)])

# print(totalList)

if single:
    for k, job in enumerate(totalList):
        tempList = [[float(elemInner) for elemInner in elem] for elem in job]
        list_length = len(tempList[0])
        sums = []
        for i in range(list_length):
            sum_i = sum(inner_list[i] for inner_list in tempList)
            sums.append(sum_i)
        for p, val in enumerate(sums):
            with open(dst + 'hwloop_time_per_job.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                csvwriter.writerow([k, p, val])

if single:
    for k, job in enumerate(totalList):
        for j, lists in enumerate(job):
            # tempList = [float(elem) for elem in lists]
            for t, taskVal in enumerate(lists):
                with open(dst + 'hwloop_time_per_task.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                    csvwriter.writerow([k, j, jobExecutables[k][j], taskVal])

if single:
    for j in range(sat_counter):
        jobUsed = jobExecutables[j]
        tempListFloats = [[float(elemInner) for elemInner in elem] for elem in totalList[j]]
        for idxTask, cons in enumerate(tempListFloats):
            timePerTask[jobUsed[idxTask]] += sum(cons)
            counterPerTask[jobUsed[idxTask]] += 1

    for task, value in timePerTask.items():
        if counterPerTask[task] == 0:
            meanTime = 0
        else:
            meanTime = value / (counterPerTask[task] * job_per_satellite)
        with open(dst + "hwloop_mean_time_per_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanTime])
'''
else:
    for j in range(sat_counter):
        jobUsed = jobExecutables[j]
        tempListFloats = [[float(elemInner) for elemInner in elem] for elem in totalList[j]]
        for idxTask, cons in enumerate(tempListFloats):
            timePerTask[jobUsed[idxTask]] += sum(cons)
            counterPerTask[jobUsed[idxTask]] += 1

    for task, value in timePerTask.items():
        if counterPerTask[task] == 0:
            meanTime = 0
        else:
            meanTime = value / counterPerTask[task]
        with open(dst + "hwloop_mean_time_per_task.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([task, meanTime])
'''