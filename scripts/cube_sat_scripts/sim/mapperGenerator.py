import yaml
import sys
import networkx as nx


def read_schedule_file(schedule_file):
    with open(schedule_file, 'r') as file:
        schedule_data = yaml.safe_load(file)
    return schedule_data


def retrieve_arguments(schedule_data):
    arguments_name = {}

    for program in schedule_data:
        program_name = program['name']
        arguments_val = program.get('arguments', [])
        check_if_used = program['to_execute'] == 'y'

        if check_if_used:
            if program_name not in arguments_name:
                arguments_name[program_name] = []
            if arguments_val is not None:
                for arg in arguments_val:
                    arguments_name[program_name].append(arg)

    return arguments_name


def retrieve_if_use_bash_script(schedule_data):
    bash_name = {}

    for program in schedule_data:
        program_name = program['name']

        # If the program name is not already in the dictionary and a bash script is specified
        if program_name not in bash_name:
            if 'run_bash_script' in program:
                bash_name[program_name] = program['run_bash_script']
    return bash_name


def create_graph_and_topological_sort(data):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes with their priority as an attribute
    for item in data:
        if item['to_execute'] == 'y':
            graph.add_node(item['name'], priority=item['priority'])

    # Add edges representing dependencies
    for item in data:
        if item['to_execute'] == 'y':
            if 'dependencies' in item:
                for dep in item['dependencies']:
                    if not graph.has_node(dep):
                        sys.exit("Added a not existent dependency!")
                    graph.add_edge(dep, item['name'])

    # Perform topological sort based on priority values and dependencies
    return nx.lexicographical_topological_sort(graph, key=lambda x: (-graph.nodes[x]['priority'], x))


if len(sys.argv) != 4:
    print(
        "Missing argument: \"s for SingleJob or m for MultipleJobs\", \"Mapper file\" and \"Instance satellite file DAG\"")
    sys.exit()

if sys.argv[1] == "s":
    # Check if the first command-line argument is "s" (for SingleJob)
    single = True
else:
    single = False

mapperDAG = sys.argv[2]
satelliteInstancesDAG = sys.argv[3]

schedule_data = read_schedule_file(satelliteInstancesDAG)
equalToProgram = False

if single:
    with open(mapperDAG, 'w') as file:
        for sat, job in schedule_data.items():
            # Check if correct configuration
            if 'Job 0' in job:
                sys.exit("Started single job simulation, with multiple jobs configuration!")
            sorted_nodes = create_graph_and_topological_sort(job)
            arguments_name = retrieve_arguments(job)
            sorted_node_list = ",".join(sorted_nodes).split(",")
            sorted_node_list_copy = sorted_node_list.copy()
            bash_scripts = retrieve_if_use_bash_script(job)

            # Bad, but done to add "" where there is a string and not a program
            for i in range(len(sorted_node_list)):
                for task in arguments_name:
                    if sorted_node_list[i] == task:
                        if arguments_name[task] != [None]:
                            tempList = []
                            for elem in arguments_name[task]:
                                for generic_task in sorted_node_list_copy:
                                    if elem == generic_task:
                                        equalToProgram = True
                                        break
                                if equalToProgram:
                                    tempList.append(elem)
                                else:
                                    stringToAppend = '"' + str(elem) + '"'
                                    tempList.append(stringToAppend)
                                equalToProgram = False
                            temp = str(sorted_node_list[i]) + ";" + ";".join(tempList)
                            sorted_node_list[i] = temp

            # Check if instead of running the task for a single input,
            # is used the bash script that will execute for every input in the database
            checkForScriptInsteadOfExec = []
            for task in sorted_node_list:
                arguments_temp = task.split(";")
                if arguments_temp[0] in bash_scripts:
                    if bash_scripts[arguments_temp[0]] != 0:
                        arguments_temp[0] = "?" + str(bash_scripts[arguments_temp[0]]) + str(arguments_temp[0])
                        checkForScriptInsteadOfExec.append(";".join(arguments_temp))
                    else:
                        checkForScriptInsteadOfExec.append(task)
                else:
                    checkForScriptInsteadOfExec.append(task)
            sorted_node_list = checkForScriptInsteadOfExec.copy()

            line = str(sat[9:]) + "," + ",".join(sorted_node_list) + "\n"
            file.write(line)
else:
    with open(mapperDAG, 'w') as file:
        for sat, jobs in schedule_data.items():
            numberOfJobOfInstance = 0
            # Check if correct configuration
            if not 'Job 0' in jobs:
                sys.exit("Started multiple jobs simulation, with single job configuration!")
            for job, tasks in jobs.items():
                sorted_nodes = create_graph_and_topological_sort(tasks)
                arguments_name = retrieve_arguments(tasks)
                sorted_node_list = ",".join(sorted_nodes).split(",")
                sorted_node_list_copy = sorted_node_list.copy()
                bash_scripts = retrieve_if_use_bash_script(tasks)

                # Bad, but done to add "" where there is a string and not a program
                for i in range(len(sorted_node_list)):
                    for task in arguments_name:
                        if sorted_node_list[i] == task:
                            if arguments_name[task] != [None]:
                                tempList = []
                                for elem in arguments_name[task]:
                                    for generic_task in sorted_node_list_copy:
                                        if elem == generic_task:
                                            equalToProgram = True
                                            break
                                    if equalToProgram:
                                        tempList.append(elem)
                                    else:
                                        stringToAppend = '"' + str(elem) + '"'
                                        tempList.append(stringToAppend)
                                    equalToProgram = False
                                temp = str(sorted_node_list[i]) + ";" + ";".join(tempList)
                                sorted_node_list[i] = temp

                # Check if instead of running the task for a single input,
                # is used the bash script that will execute for every input in the database
                checkForScriptInsteadOfExec = []
                for task in sorted_node_list:
                    arguments_temp = task.split(";")
                    if arguments_temp[0] in bash_scripts:
                        if bash_scripts[arguments_temp[0]] != 0:
                            arguments_temp[0] = "?" + str(bash_scripts[arguments_temp[0]]) + str(arguments_temp[0])
                            checkForScriptInsteadOfExec.append(";".join(arguments_temp))
                        else:
                            checkForScriptInsteadOfExec.append(task)
                    else:
                        checkForScriptInsteadOfExec.append(task)
                sorted_node_list = checkForScriptInsteadOfExec.copy()

                line = str(sat[-1]) + "," + str(numberOfJobOfInstance) + "," + ",".join(sorted_node_list) + "\n"
                numberOfJobOfInstance += 1
                file.write(line)
