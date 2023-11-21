import sys
import time

if len(sys.argv) != 3:
    print("Missing argument: \"seconds\" and \"printVal\"!")
    sys.exit()

seconds = float(sys.argv[1])
printVal = sys.argv[2]

time.sleep(seconds)
print(printVal)
