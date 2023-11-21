import sys
import re

if len(sys.argv) != 3:
    print("Missing argument: \"Number of instance to start\" \"Number to reach\"")
    sys.exit()

actual_instance = int(sys.argv[1])
instance_to_reach = int(sys.argv[2])

with open('./satelliteInstances.yaml') as file:
    lines = [line for line in file]

exit_val = False
pattern = r'\d+'
with open('./satelliteInstances.yaml', 'a') as file:
    file.write('\n')
    for i in range(len(lines)):
        if exit_val:
            break
        if "Instance" in lines[i]:
            match = re.search(pattern, lines[i])
            number_to_replace = match.group(0)
            lines[i] = lines[i].replace(number_to_replace, str(actual_instance))
            actual_instance += 1
        file.write(lines[i])
        if (actual_instance - 1) == instance_to_reach:
            exit_val = True

