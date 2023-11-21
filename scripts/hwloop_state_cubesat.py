import csv
import fnmatch
import os
import sys

src = ''
dst = ''
sat_counter = 0
sleepPresent = True

if len(sys.argv) == 5:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    sat_counter = int(sys.argv[3])
    dir_to_create = sys.argv[4]
else:
    print(
        "Usage: python3 hwloop_state_cubesat.py /full/path/to/src/ /full/path/to/dst/ 'Number of satellites' 'dir_to_create'")
    exit()

all_contents = os.listdir(src)
subdirs = []

for e in all_contents:
    if os.path.isdir(src + e):
        subdirs.append(e)
subdirs.sort()

dst = os.path.join(dst[:-1], dir_to_create)
if not os.path.exists(dst):
    os.makedirs(dst)

with open(dst + 'hwloop_state_working.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'time-spent'])
with open(dst + 'hwloop_state_idle.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'time-spent'])
if sleepPresent:
    with open(dst + 'hwloop_state_sleep.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow(['satellite', 'time-spent'])

files = os.listdir(src)
for j in range(sat_counter):
    totalTimeSimulation = 0.0
    counterWorking = 0.0
    counterIdle = 0.0
    counterSleep = 0.0

    capture_pattern = 'event-cubesat-' + str(j) + '-working-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src + "".join(capture_matches), 'r') as file:
        readerWorkStart = list(csv.reader(file))
        readerWorkStart = ["".join(elem) for elem in readerWorkStart]
        readerWorkStart.pop(0)

    capture_pattern = 'event-cubesat-' + str(j) + '-working-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src + "".join(capture_matches), 'r') as file:
        readerWorkEnd = list(csv.reader(file))
        readerWorkEnd = ["".join(elem) for elem in readerWorkEnd]
        readerWorkEnd.pop(0)

    capture_pattern = 'event-cubesat-' + str(j) + '-idle-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src + "".join(capture_matches), 'r') as file:
        readerIdleStart = list(csv.reader(file))
        readerIdleStart = ["".join(elem) for elem in readerIdleStart]
        readerIdleStart.pop(0)

    capture_pattern = 'event-cubesat-' + str(j) + '-idle-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    with open(src + "".join(capture_matches), 'r') as file:
        readerIdleEnd = list(csv.reader(file))
        readerIdleEnd = ["".join(elem) for elem in readerIdleEnd]
        readerIdleEnd.pop(0)

    capture_pattern = 'event-cubesat-' + str(j) + '-sleep-start.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    elif (len(capture_matches) == 1):
        with open(src + "".join(capture_matches), 'r') as file:
            readerSleepStart = list(csv.reader(file))
            readerSleepStart = ["".join(elem) for elem in readerSleepStart]
            readerSleepStart.pop(0)
    else:
        sleepPresent = False

    capture_pattern = 'event-cubesat-' + str(j) + '-sleep-stop.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    # Only a file could exist with this pattern
    if (len(capture_matches) > 1):
        exit()
    elif (len(capture_matches) == 1):
        with open(src + "".join(capture_matches), 'r') as file:
            readerSleepEnd = list(csv.reader(file))
            readerSleepEnd = ["".join(elem) for elem in readerSleepEnd]
            readerSleepEnd.pop(0)
    else:
        sleepPresent = False

    totalTimeSimulation = float(readerIdleEnd[-1]) - float(readerIdleStart[0])

    for k in range(len(readerWorkStart)):
        counterWorking += float(readerWorkEnd[k]) - float(readerWorkStart[k])
    counterWorking /= totalTimeSimulation

    for k in range(len(readerIdleStart)):
        counterIdle += float(readerIdleEnd[k]) - float(readerIdleStart[k])
    counterIdle /= totalTimeSimulation

    if sleepPresent:
        for k in range(len(readerSleepStart)):
            counterSleep += float(readerSleepEnd[k]) - float(readerSleepStart[k])

    counterSleep /= totalTimeSimulation

    with open(dst + 'hwloop_state_working.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([j, counterWorking])

    with open(dst + 'hwloop_state_idle.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([j, counterIdle])

    if sleepPresent:
        with open(dst + 'hwloop_state_sleep.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([j, counterSleep])
