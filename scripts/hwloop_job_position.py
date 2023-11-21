import csv
import fnmatch
import os
import sys

src = ''
dst = ''

if len(sys.argv) == 5:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    dir_to_create = sys.argv[3]
    sat_counter = int(sys.argv[4])
else:
    print(
        "Usage: python3 hwloop_job_position.py /full/path/to/src/ /full/path/to/dst/ 'dir_to_create' 'Instances of satellite'")
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

for j in range(sat_counter):
    files = os.listdir(src)

    working_times = []
    # Working time
    capture_pattern_start = 'event-cubesat-' + str(j) + '-working-start.csv'
    capture_matches_start = fnmatch.filter(files, capture_pattern_start)
    # Only a file could exist with this pattern
    if (len(capture_matches_start) > 1):
        exit()
    with open(src + "".join(capture_matches_start), 'r') as file:
        readerWorkStart = list(csv.reader(file))
        readerWorkStart = ["".join(elem) for elem in readerWorkStart]
        readerWorkStart.pop(0)

    capture_pattern_stop = 'event-cubesat-' + str(j) + '-working-stop.csv'
    capture_matches_stop = fnmatch.filter(files, capture_pattern_stop)
    # Only a file could exist with this pattern
    if (len(capture_matches_stop) > 1):
        exit()
    with open(src + "".join(capture_matches_stop), 'r') as file:
        readerWorkEnd = list(csv.reader(file))
        readerWorkEnd = ["".join(elem) for elem in readerWorkEnd]
        readerWorkEnd.pop(0)

    for k in range(len(readerWorkStart)):
        working_times.append(float(readerWorkEnd[k]) - float(readerWorkStart[k]))

    with open(dst + 'hwloop_position_' + str(j) + '.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow(['position,' 'duration'])
    capture_pattern = 'event-cubesat-' + str(j) + '-found-job.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    if len(capture_matches) > 1:
        sys.exit()
    with open(src + "".join(capture_matches), 'r') as file:
        positions = list(csv.reader(file))
        positions = ["".join(elem) for elem in positions]
        positions.pop(0)
    # capture_matches.pop(0)
    for idx, pos in enumerate(positions):
        with open(dst + 'hwloop_position_' + str(j) + '.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            csvwriter.writerow([pos, working_times[idx]])
