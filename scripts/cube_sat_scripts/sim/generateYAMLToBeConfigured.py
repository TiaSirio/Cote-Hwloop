import sys
import yaml

from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver



def readConfFile(pathToFile):
    listConf = []
    with open(pathToFile, "r") as fileConf:
        lines = fileConf.readlines()
        lines = [line.rstrip().split("=") for line in lines]
        for line in lines:
            listConf.append(line[1])
    return listConf



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

if len(sys.argv) != 8:
    print(
        "Needed as arguments: \"Instances of satellite\", \"Jobs per instance\", \"s for Single job or m for Multi jobs\", \"Yaml tasks file\" and \"Yaml satellite instances file\"!")
    sys.exit()

satellite = int(sys.argv[1])
jobs = int(sys.argv[2])
multipleJobs = sys.argv[3] == "m"
execPath = sys.argv[4]
tasksYamlFile = sys.argv[5]
satelliteInstanceYamlFile = sys.argv[6]
taskConf = sys.argv[7]

# satList = list(range(1, satellite + 1))
satList = list(range(0, satellite))
satList = ["Instance " + str(s) for s in satList]
jobList = []
if multipleJobs:
    jobList = list(range(0, jobs))
    jobList = ["Job " + str(j) for j in jobList]

onlyfiles = readConfFile(taskConf)

preExec = []
# Load yaml and store the mapping of arguments for each program
with open(tasksYamlFile) as file:
    programs = yaml.load(file, Loader=yaml.FullLoader)
    # print(programs)

# print(programs)

for program in programs:
    program["to_execute"] = "y"
    program["full"] = "n"
    program["sequential"] = "n"
    args = program["arguments"]
    for arg in args:
        for elem in onlyfiles:
            if arg == elem:
                if "dependencies" not in program.keys():
                    program["dependencies"] = [arg]
                else:
                    program["dependencies"].append(arg)

# Creating yaml file
yamlFile = {}

if not multipleJobs:
    yamlFile = dict.fromkeys(satList, yamlFile)
    yamlFile = dict.fromkeys(yamlFile, programs)
else:
    yamlFile = dict.fromkeys(jobList, yamlFile)
    yamlFile = dict.fromkeys(yamlFile, programs)
    yamlFile = dict.fromkeys(satList, yamlFile)

with open(satelliteInstanceYamlFile, 'w') as outfile:
    if not multipleJobs:
        outfile.write("# Instances of satellite configurator\n")
        outfile.write("# For each satellite define a DAG that represents the order of execution of the tasks\n")
        outfile.write("# For each task we have the following:\n")
        outfile.write("# - The same values as for tasksDAG.yaml\n")
        outfile.write("# - Dependencies -> Generated if we have as argument the name of another task and added to the already present dependencies.\n")
        outfile.write("# If a task have one or more dependencies, it needs to wait for the completion of the dependencies\n")
    else:
        outfile.write("# Instances of satellite configurator\n")
        outfile.write("# For each satellite define all the jobs to execute and a DAG that represents the order of execution of the tasks\n")
        outfile.write("# For each task we have the following:\n")
        outfile.write("# - The same values as for tasksDAG.yaml\n")
        outfile.write("# - Dependencies -> Generated if we have as argument the name of another task and added to the already present dependencies.\n")
        outfile.write("# If a task have one or more dependencies, it needs to wait for the completion of the dependencies\n")
    yaml.dump(yamlFile, outfile, Dumper=MyDumper, sort_keys=False)
