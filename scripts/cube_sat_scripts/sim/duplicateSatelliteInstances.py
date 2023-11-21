import sys
import re

if len(sys.argv) != 2:
    print("Missing argument: \"Number of instance to start\"")
    sys.exit()

actual_instance = int(sys.argv[1])

with open('./satelliteInstances.yaml') as file:
    lines = [line for line in file]

pattern = r'\d+'
with open('./satelliteInstances.yaml', 'a') as file:
    file.write('\n')
    for i in range(len(lines)):
        if "Instance" in lines[i]:
            match = re.search(pattern, lines[i])
            number_to_replace = match.group(0)
            lines[i] = lines[i].replace(number_to_replace, str(actual_instance))
            actual_instance += 1
        file.write(lines[i])
