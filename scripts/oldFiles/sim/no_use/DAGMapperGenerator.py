import yaml
import sys

def read_schedule_file(schedule_file):
    with open(schedule_file, 'r') as file:
        schedule_data = yaml.safe_load(file)
    return schedule_data


def addPriorityToTask(prioritiesTasks, elem, job):
    for program in job:
        if program['name'] == elem:
            prioritiesTasks[elem] = program['priority']
    return prioritiesTasks


def create_dependency_graph(schedule_data):
    dependency_graph = {}
    arguments_name = {}
    priorities = {}

    for program in schedule_data:
        program_name = program['name']
        dependencies = program.get('dependencies', [])
        arguments = program.get('arguments', [])
        priority = program.get('priority', [])
        check_if_used = program['to_execute'] == 'y'

        if check_if_used:
            if program_name not in dependency_graph:
                dependency_graph[program_name] = set()
            for dependency in dependencies:
                dependency_graph[program_name].add(dependency)

            if program_name not in arguments_name:
                arguments_name[program_name] = set()
            for arg in arguments:
                if arg is not None:
                    arguments_name[program_name].add(arg)

            if program_name not in priorities:
                priorities[program_name] = set()
            priorities[program_name].add(priority)

    return dependency_graph, arguments_name, priorities


def find_initial_programs(dependency_graph):
    initial_programs = []

    for program, dependencies in dependency_graph.items():
        if len(dependencies) == 0:
            initial_programs.append(program)

    return initial_programs


def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack


def topological_sort_with_groups(dependency_graph, priorities):
    in_degree = {node: 0 for node in dependency_graph}

    # Count the in-degrees of the nodes
    for node in dependency_graph:
        in_degree[node] = len(dependency_graph[node])


    node_to_delete = []
    queue = []
    # Take the first elements to be executed
    for node in dependency_graph:
        if in_degree[node] == 0:
            queue.append(node)
            in_degree.pop(node)
            node_to_delete.append(node)

    # Remove them from the dependency graph
    for node in node_to_delete:
        dependency_graph.pop(node)
    sorted_nodes = []

    # Sort queue by priorities
    queue = sorted(queue, key=lambda x: -min(priorities[x]))

    while queue:
        next_queue = []
        current_group = []
        node_to_delete = []
        for node_deleted in queue:
            dependency_to_delete = []
            current_group.append(node_deleted)
            for node in dependency_graph:
                for dependency in dependency_graph[node]:
                    # If I find in a node in the dependency graph, the node eliminated, I remove its dependency
                    if dependency == node_deleted:
                        in_degree[node] -= 1
                        dependency_to_delete.append([node, dependency])
                    # If a node has no dependency, should be eliminated from the DAG in the next iteration
                    # It will represent the next sub-list of tasks to be executed
                    if in_degree[node] == 0:
                        next_queue.append(node)
                        if node not in node_to_delete:
                            node_to_delete.append(node)
            for elem in dependency_to_delete:
                value_set = dependency_graph.get(elem[0], set())
                value_set.discard(elem[1])
                dependency_graph[elem[0]] = value_set

        for node_del in node_to_delete:
            dependency_graph.pop(node_del)
            in_degree.pop(node_del)

        # Sort by priorities
        current_group = sorted(current_group, key=lambda x: -min(priorities[x]))

        sorted_nodes.append(current_group)
        queue = next_queue

    return sorted_nodes




if len(sys.argv) != 4:
    print("Missing argument: \"s for SingleJob or m for MultipleJobs\", \"MapperDAG file\" and \"Instance satellite file DAG\"")
    sys.exit()

if sys.argv[1] == "s":
    single = True
else:
    single = False

mapperDAG = sys.argv[2]
satelliteInstancesDAG = sys.argv[3]
#mapperPriorityDAG = sys.argv[4]

schedule_data = read_schedule_file(satelliteInstancesDAG)

#prioritiesTasks = {}
#first = True
'''
with open(mapperPriorityDAG, 'w') as fileClear:
    fileClear.write("")
'''
if single:
    with open(mapperDAG, 'w') as file:
        for sat, job in schedule_data.items():
            #first = True
            dependency_graph, arguments_name, priorities = create_dependency_graph(job)
            sorted_graph = topological_sort(dependency_graph)
            #print(priorities)
            #for elem in sorted_graph:
            #    prioritiesTasks = addPriorityToTask(prioritiesTasks, elem, job)
            par_and_seq_groups = topological_sort_with_groups(dependency_graph, priorities)


            #print(prioritiesTasks)
            #print(par_and_seq_groups)
            #print(arguments_name)
            for prog, arguments in arguments_name.items():
                for listArgs in par_and_seq_groups:
                    for i in range(len(listArgs)):
                        if listArgs[i] == prog:
                            if arguments != set():
                                temp = str(listArgs[i]) + ";" + ";".join(arguments)
                                listArgs[i] = temp


            #print(par_and_seq_groups)
            par_and_seq_groups = [",".join(elem) for elem in par_and_seq_groups]

            #print(arguments_name)
            line = str(sat[-1]) + "|" + "|".join(par_and_seq_groups) + "\n"
            file.write(line)
            '''
            with open(mapperPriorityDAG, 'a') as file2:
                file2.write(str(prioritiesTasks))
                file2.write("\n")
            '''

else:
    with open(mapperDAG, 'w') as file:
        for sat, jobs in schedule_data.items():
            for job, tasks in jobs.items():
                #first = True
                dependency_graph, arguments_name, priorities = create_dependency_graph(tasks)
                sorted_graph = topological_sort(dependency_graph)
                #for elem in sorted_graph:
                #    prioritiesTasks = addPriorityToTask(prioritiesTasks, elem, tasks)
                par_and_seq_groups = topological_sort_with_groups(dependency_graph, priorities)


                #print(par_and_seq_groups)
                #print(arguments_name)
                for prog, arguments in arguments_name.items():
                    for listArgs in par_and_seq_groups:
                        for i in range(len(listArgs)):
                            if listArgs[i] == prog:
                                if arguments != set():
                                    temp = str(listArgs[i]) + ";" + ";".join(arguments)
                                    listArgs[i] = temp


                #print(par_and_seq_groups)
                par_and_seq_groups = [",".join(elem) for elem in par_and_seq_groups]

                #print(arguments_name)
                line = str(sat[-1]) + "|" + "|".join(par_and_seq_groups) + "\n"
                file.write(line)

                '''
                with open(mapperPriorityDAG, 'a') as file2:
                    file2.write(str(prioritiesTasks))
                    file2.write("\n")
                '''