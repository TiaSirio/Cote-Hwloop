import os
import sys
import yaml

if len(sys.argv) != 5:
    print("Needed as arguments: \"s for SingleJob or m for MultiJobs\", \"Mapper file position\", \"Yaml satellite instances file\" and \"Yaml satellite instances directory\"!")
    sys.exit()

multiJobs = sys.argv[1] == "m"
# Name of the mapper file
mapperPath = sys.argv[2]
satelliteInstanceYamlFile = sys.argv[3]
satelliteInstanceYamlDir = sys.argv[4]
os.chdir(satelliteInstanceYamlDir)



job = []
satInstances = []
multipleJobsSim = []
temp = []



# Load yaml and store the mapping of arguments for each program
with open(satelliteInstanceYamlFile) as file:
    yamlFile = yaml.load(file, Loader=yaml.FullLoader)
    #print(yamlFile)
    if not multiJobs:
        for sat, taskElems in yamlFile.items():
            for taskElem in taskElems:
                if taskElems[taskElem] is not None:
                    for elem in taskElems[taskElem]:
                        if elem is not None:
                            temp.append(str(elem))
                        else:
                            temp.append("")
                    job.append(taskElem + ";" + ";".join(temp.copy()))
                    temp = []
                else:
                    job.append(taskElem)
            satInstances.append(job.copy())
            job = []
    else:
        for sat, jobElems in yamlFile.items():
            for jobElem, taskElems in jobElems.items():
                for taskElem in taskElems:
                    if taskElems[taskElem] is not None:
                        for elem in taskElems[taskElem]:
                            if elem is not None:
                                temp.append(str(elem))
                            else:
                                temp.append("")
                        job.append(taskElem + ";" + ";".join(temp.copy()))
                        temp = []
                    else:
                        job.append(taskElem)
                satInstances.append(job.copy())
                job = []
            multipleJobsSim.append(satInstances.copy())
            satInstances = []
#print(multipleJobsSim)



jobExecutables = []
satExecutables = []
multipleExecutables = []

# Remove .c to save the compiled name in the mapper
if not multiJobs:
    for sat in satInstances:
        for task in sat:
            if ";" in task:
                arguments = task.split(";")
                if arguments[0].endswith(".c"):
                    temp = arguments[0]
                    arguments.pop(0)
                    arguments.insert(0, temp[:-2])
                    jobExecutables.append(";".join(arguments))
                else:
                    jobExecutables.append(";".join(arguments))
            else:
                if task.endswith(".c"):
                    jobExecutables.append(task[:-2])
                else:
                    jobExecutables.append(task)
        satExecutables.append(jobExecutables.copy())
        jobExecutables = []
else:
    for sat in multipleJobsSim:
        for job in sat:
            for task in job:
                if ";" in task:
                    arguments = task.split(";")
                    if arguments[0].endswith(".c"):
                        temp = arguments[0]
                        arguments.pop(0)
                        arguments.insert(0, temp[:-2])
                        jobExecutables.append(";".join(arguments))
                    else:
                        jobExecutables.append(";".join(arguments))
                else:
                    if task.endswith(".c"):
                        jobExecutables.append(task[:-2])
                    else:
                        jobExecutables.append(task)
            satExecutables.append(jobExecutables.copy())
            jobExecutables = []
        multipleExecutables.append(satExecutables.copy())
        satExecutables = []
#print(multipleExecutables)

# Save mapper in a file
with open(mapperPath, "w") as file:
    if not multiJobs:
        for i in range(len(satExecutables)):
            stringToWrite = str(i) + "," + ",".join(satExecutables[i]) + "\n"
            file.write(stringToWrite)
    else:
        for i in range(len(multipleExecutables)):
            for j in range(len(multipleExecutables[i])):
                stringToWrite = str(i) + "," + ",".join(multipleExecutables[i][j]) + "\n"
                #print(stringToWrite)
                file.write(stringToWrite)