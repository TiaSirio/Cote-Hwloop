import csv
import fnmatch
import os
import sys

src = ''
dst = ''
job_count = 0
job_per_satellite = 0
sat_counter = 0

if len(sys.argv) == 6:
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
else:
    print(
        "Usage: python3 hwloop_errors.py /full/path/to/src/ /full/path/to/dst/ 'Number of jobs' 'Number of satellites' 'dir_to_create'")
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

for i in range(sat_counter):
    capture_pattern = 'event-cubesat-' + str(i) + '-error-found.csv'
    capture_matches_temp = fnmatch.filter(files, capture_pattern)
    if len(capture_matches_temp) == 0:
        capture_matches.append(None)
    else:
        capture_matches.append(capture_matches_temp)

# capture_pattern = 'event-cubesat-*-error-found.csv'
# capture_matches = fnmatch.filter(files, capture_pattern)

totalList = []

if len(capture_matches) > 0:
    #capture_matches.sort()

    with open(dst + 'hwloop_errors.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow(['satellite', 'job-error'])

    with open(dst + 'hwloop_errors_per_satellite.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow(['satellite', 'job-error'])

    for file_cap in capture_matches:
        if file_cap is None:
            totalList.append(None)
        else:
            with open(src + "".join(file_cap), 'r') as file:
                errorsList = list(csv.reader(file))
                errorsList = ["".join(elem) for elem in errorsList]
                errorsList.pop(0)
                totalList.append(errorsList)

    for j, lists in enumerate(totalList):
        with open(dst + 'hwloop_errors.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            # No errors
            if lists is None:
                csvwriter.writerow([j, 0])
            else:
                csvwriter.writerow([j, len(lists)])

    for j, lists in enumerate(totalList):
        if lists is None:
            with open(dst + 'hwloop_errors_per_satellite.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                csvwriter.writerow([j, -1])
        else:
            for error_task in lists:
                with open(dst + 'hwloop_errors_per_satellite.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
                    csvwriter.writerow([j, error_task])
