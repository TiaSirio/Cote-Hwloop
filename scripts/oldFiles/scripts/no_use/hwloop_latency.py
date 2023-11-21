import csv
import fnmatch
import os
import sys


src = ''
dst = ''

if len(sys.argv) == 4:
  src = sys.argv[1]
  if src[-1] != '/':
    src+='/'
  dst = sys.argv[2]
  if dst[-1] != '/':
    dst+='/'
  dir_to_create = sys.argv[3]
else:
  print('Usage: python3 hwloop_latency.py /full/path/to/src/ /full/path/to/dst/ dir_to_create')
  exit()

dst = os.path.join(dst[:-1], dir_to_create)
if not os.path.exists(dst):
  os.makedirs(dst)

with open(dst + 'hwloop_latency.csv', 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
  csvwriter.writerow(['depth','avg','stdev'])
all_contents = os.listdir(src)
subdirs = []

for e in all_contents:
  if os.path.isdir(src + e):
    subdirs.append(e)
subdirs.sort()

for subdir in subdirs:
  try:
    x = int(subdir)
  except ValueError:
    pass
  y_count = 0.0
  y_total = 0.0
  latencies = []
  files = os.listdir(src + subdir)
  begin_pattern = 'event-cubesat-*-begin-work-*.csv'
  begin_matches = fnmatch.filter(files, begin_pattern)
  begin_matches.sort()
  gtf_to_begin = {}

  for i in range(0,len(begin_matches)):
    begin_dev_ix = 13
    begin_dev_id = ''

    while begin_matches[i][begin_dev_ix].isdigit():
      begin_dev_id += begin_matches[i][begin_dev_ix]
      begin_dev_ix += 1
    begin_gtf_ix = 24+len(begin_dev_id)
    begin_gtf_id = ''

    while begin_matches[i][begin_gtf_ix].isdigit():
      begin_gtf_id += begin_matches[i][begin_gtf_ix]
      begin_gtf_ix += 1
    begin_time = 0.0

    with open(src+subdir+'/'+begin_matches[i],'r',newline='') as readfile:
      csvreader = csv.reader(readfile, delimiter=',', quotechar='"')
      header = next(csvreader)
      begin_time = float(next(csvreader)[0])

    if begin_gtf_id in gtf_to_begin:
      gtf_to_begin[begin_gtf_id] = min(gtf_to_begin[begin_gtf_id],begin_time)
    else:
      gtf_to_begin[begin_gtf_id] = begin_time

  complete_pattern = 'event-cubesat-*-complete-work-*.csv'
  complete_matches = fnmatch.filter(files, complete_pattern)
  complete_matches.sort()
  gtf_to_complete = {}

  for i in range(0,len(complete_matches)):
    complete_dev_ix = 13
    complete_dev_id = ''

    while complete_matches[i][complete_dev_ix].isdigit():
      complete_dev_id += complete_matches[i][complete_dev_ix]
      complete_dev_ix += 1
    complete_gtf_ix = 27 + len(complete_dev_id)
    complete_gtf_id = ''

    while complete_matches[i][complete_gtf_ix].isdigit():
      complete_gtf_id += complete_matches[i][complete_gtf_ix]
      complete_gtf_ix += 1
    complete_time = 0.0

    with open(src+subdir+'/'+complete_matches[i],'r',newline='') as readfile:
      csvreader = csv.reader(readfile, delimiter=',', quotechar='"')
      header = next(csvreader)
      complete_time = float(next(csvreader)[0])

    if complete_gtf_id in gtf_to_complete:
      gtf_to_complete[complete_gtf_id] = max(gtf_to_complete[complete_gtf_id],complete_time)
    else:
      gtf_to_complete[complete_gtf_id] = complete_time

  for begin_key in gtf_to_begin:
    for complete_key in gtf_to_complete:
      if begin_key==complete_key:
        y_count += 1.0
        y_total += (gtf_to_complete[complete_key]-gtf_to_begin[begin_key])
        latencies.append(gtf_to_complete[complete_key]-gtf_to_begin[begin_key])

  avg = y_total/float(y_count)
  stdev = 0.0

  for latency in latencies:
    stdev += pow(latency-avg,2)
  stdev = pow(float(stdev)/float(len(latencies)),0.5)

  with open(dst + 'hwloop_latency.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    csvwriter.writerow([x,avg,stdev])
