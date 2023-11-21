from os import listdir
from os.path import isfile, join
import os
import sys
import yaml

from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver

class MyRepresenter(Representer):
    def represent_none(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:null',
                                     u'')

class MyDumper(Emitter, Serializer, MyRepresenter, Resolver):
    def ignore_aliases(self, data):
        return True

    def __init__(self, stream,
                 default_style=None, default_flow_style=None,
                 canonical=None, indent=None, width=None,
                 allow_unicode=None, line_break=None,
                 encoding=None, explicit_start=None, explicit_end=None,
                 version=None, tags=None, sort_keys=False):
        Emitter.__init__(self, stream, canonical=canonical,
                         indent=indent, width=width,
                         allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding,
                            explicit_start=explicit_start, explicit_end=explicit_end,
                            version=version, tags=tags)
        MyRepresenter.__init__(self, default_style=default_style,
                               default_flow_style=default_flow_style, sort_keys=sort_keys)
        Resolver.__init__(self)


MyRepresenter.add_representer(type(None),
                              MyRepresenter.represent_none)


if len(sys.argv) != 10:
    print("Needed as arguments: \"Instances of satellite\", \"Jobs per instance\", \"s for Single job or m for Multi jobs\", \"Mapper file position\", \"Yaml tasks file\""
          ", \"Yaml tasks directory\", \"Yaml satellite instances file\" and \"Yaml satellite instances directory\"!")
    sys.exit()


satellite = int(sys.argv[1])
jobs = int(sys.argv[2])
multipleJobs = sys.argv[3] == "m"
mapperPath = sys.argv[4]
execPath = sys.argv[5]
tasksYamlFile = sys.argv[6]
tasksYamlDir = sys.argv[7]
satelliteInstanceYamlFile = sys.argv[8]
satelliteInstanceYamlDir = sys.argv[9]


#satList = list(range(1, satellite + 1))
satList = list(range(0, satellite))
satList = ["Instance " + str(s) for s in satList]
jobList = []
if multipleJobs:
    #jobList = list(range(1, jobs + 1))
    jobList = list(range(0, jobs))
    jobList = ["Job " + str(j) for j in jobList]
arguments = [None]


# Get the name of all the files in the correct directory
onlyfiles = [f for f in listdir(execPath) if isfile(join(execPath, f)) and (f.endswith(".py") or f.endswith(".c"))]
onlyfiles.sort()
#print(onlyfiles)


# Creating yaml file
# yamlFile = {k: {} for i, k in enumerate(set(onlyfiles))}
yamlFile = {}

if not multipleJobs:
    yamlFile = dict.fromkeys(onlyfiles, yamlFile)
    yamlFile = dict.fromkeys(yamlFile, arguments)
    yamlFile = dict.fromkeys(satList, yamlFile)
else:
    yamlFile = dict.fromkeys(onlyfiles, yamlFile)
    yamlFile = dict.fromkeys(yamlFile, arguments)
    yamlFile = dict.fromkeys(jobList, yamlFile)
    yamlFile = dict.fromkeys(satList, yamlFile)
# print(yamlFile)


preExec = []
# Load yaml and store the mapping of arguments for each program
os.chdir(tasksYamlDir)
with open(tasksYamlFile) as file:
    programs = yaml.load(file, Loader=yaml.FullLoader)
    #print(programs)


# Adding arguments with mapping from programs.yaml
if not multipleJobs:
    for sat, taskElems in yamlFile.items():
        for taskElem in taskElems:
            #print(sat)
            for prog, arg in programs.items():
                if taskElem == prog:
                    taskElems[taskElem] = arg
else:
    for sat, jobElems in yamlFile.items():
        for job, taskElems in jobElems.items():
            for taskElem in taskElems:
                for prog, arg in programs.items():
                    if taskElem == prog:
                        taskElems[taskElem] = arg

os.chdir(satelliteInstanceYamlDir)
with open(satelliteInstanceYamlFile, 'w') as outfile:
    if not multipleJobs:
        outfile.write("# Instances of satellite configurator\n")
        outfile.write("# For each satellite define the order of execution of the tasks\n")
        outfile.write("# The arguments given in input for a task must be defined in the bullet points below that task\n")
        outfile.write("# If an argument takes as input the output of the previous task, leave the bullet point blank\n")
    else:
        outfile.write("# Instances of satellite configurator\n")
        outfile.write("# For each satellite define all the jobs to execute and the order of execution of the tasks of each job\n")
        outfile.write("# The arguments given in input for a task must be defined in the bullet points below that task\n")
        outfile.write("# If an argument takes as input the output of the previous task, leave the bullet point blank\n")
    yaml.dump(yamlFile, outfile, Dumper=MyDumper, sort_keys=False)
    #yaml.dump(yamlFile, outfile, Dumper=NoAliasDumper, sort_keys=False)


#with open('satelliteInstances.yaml', 'w') as file:


'''
preExec = []
# Load yaml and store the mapping of arguments for each program
with open(r'satellitesInstances.yaml', 'r') as file:
    programs = yaml.load(file, Loader=yaml.FullLoader)
    print(programs)
'''