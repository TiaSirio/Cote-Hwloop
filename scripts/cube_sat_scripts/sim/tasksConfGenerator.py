import yaml
import sys
import os



def read_schedule_file(schedule_file):
    with open(schedule_file, 'r') as file:
        schedule_data = yaml.safe_load(file)
    return schedule_data


# Filling the TasksUsed and TasksExecDir conf files.

if len(sys.argv) != 4:
    print("Missing argument: \"Tasks file conf\", \"Tasks exec dir conf\" and \"Instance satellite file DAG\"")
    sys.exit()

tasksFile = sys.argv[1]
tasksExecDirFile = sys.argv[2]
satelliteInstances = sys.argv[3]

python_dir = "python_tasks"
c_dir = "c_tasks"

schedule_data = read_schedule_file(satelliteInstances)
programs = []

with open(tasksFile, "w") as file:
    taskVal = 1
    for elem in schedule_data:
        programs.append(elem['name'])
        file.write("task" + str(taskVal) + "=" + elem['name'] + "\n")
        taskVal += 1

with open(tasksExecDirFile, "w") as file:
    for prog in programs:
        for root, dirs, files in os.walk("."):
            if prog in files:
                file.write(prog + "=" + os.path.join(root, prog)[2:] + "\n")
