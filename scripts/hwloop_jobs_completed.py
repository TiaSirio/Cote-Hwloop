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
        "Usage: python3 hwloop_jobs_completed.py /full/path/to/src/ /full/path/to/dst/ 'Number of jobs' 'Number of satellites' 'dir_to_create'")
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

with open(dst + 'hwloop_jobs_completed.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow(['satellite', 'job-coverage'])

files = os.listdir(src)
for j in range(sat_counter):
    counter = 0
    capture_pattern = 'event-cubesat-' + str(j) + '-complete-work-*.csv'
    capture_matches = fnmatch.filter(files, capture_pattern)
    for i in range(0, len(capture_matches)):
        counter += 1.0
    y_sat = int(counter)
    with open(dst + 'hwloop_jobs_completed.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerow([j, y_sat])
