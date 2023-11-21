import sys
import os
import math

if len(sys.argv) != 1:
    print("Usage: python3 temp_test.py")
    exit()

non_func_data = "1684916665207,3.308,-0.200,3.536,0.000,3.936,0.000,5.028,-1.900,2.884,-0.100,0.984,-0.100,1.044,-0.300,2.968,-0.200,40.780;1684916665110,3.312,-0.200,3.528,0.000,3.936,0.000,5.028,-1.800,2.900,-0.100,0.984,-0.100,1.044,-0.300,2.944,-0.100,41.318;1684916665014,3.328,-0.100,3.524,0.000,3.936,0.100,5.012,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916664917,3.336,-0.100,3.516,0.000,3.936,0.000,5.032,-1.800,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.944,-0.200,41.318;1684916664821,3.332,-0.100,3.508,0.000,3.936,0.000,5.032,-1.600,2.884,-0.100,0.988,-0.200,1.044,-0.300,2.968,-0.200,41.318;1684916664726,3.316,-0.100,3.504,0.000,3.936,0.000,5.024,-1.700,2.896,-0.100,0.988,-0.100,1.044,-0.300,2.940,-0.100,40.780;1684916664629,3.308,-0.200,3.516,0.000,3.936,0.000,5.032,-1.700,2.912,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916664533,3.308,-0.100,3.524,0.000,3.936,0.000,5.032,-1.700,2.912,-0.100,0.988,-0.200,1.044,-0.300,2.948,-0.100,41.318;1684916664437,3.320,-0.100,3.532,0.000,3.936,0.000,5.008,-1.800,2.896,-0.200,0.984,-0.200,1.044,-0.300,2.972,-0.200,40.780;1684916664341,3.332,-0.100,3.536,0.000,3.936,0.000,5.016,-1.700,2.884,-0.100,0.984,-0.100,1.044,-0.300,2.972,-0.200,41.318;1684916664245,3.336,-0.100,3.540,0.000,3.936,0.000,5.004,-1.800,2.888,-0.100,0.984,-0.100,1.044,-0.300,2.948,-0.100,40.780;1684916664149,3.304,-0.100,3.540,0.000,3.936,0.000,5.008,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916664053,3.308,-0.200,3.540,0.000,3.936,0.000,5.000,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.940,-0.200,41.318;1684916663956,3.324,-0.100,3.536,0.000,3.936,0.000,5.008,-1.800,2.908,0.000,0.988,-0.100,1.044,-0.300,2.968,-0.200,40.780;1684916663860,3.336,-0.100,3.532,0.000,3.936,0.000,5.008,-1.800,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.972,-0.200,41.318;1684916663764,3.332,-0.200,3.528,0.000,3.936,0.000,5.016,-1.800,2.880,-0.100,0.988,-0.100,1.044,-0.300,2.952,-0.200,40.780;1684916663667,3.320,-0.100,3.496,0.000,3.936,0.000,5.012,-1.800,2.892,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916663571,3.308,-0.100,3.500,0.000,3.936,0.100,5.000,-1.800,2.912,-0.100,0.988,-0.200,1.044,-0.300,2.936,-0.200,41.318;1684916663475,3.308,-0.100,3.504,0.000,3.936,0.000,5.012,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.964,-0.200,40.780;1684916663379,3.316,-0.200,3.512,0.000,3.936,0.000,5.012,-1.800,2.880,-0.100,0.984,-0.100,1.044,-0.300,2.976,-0.200,41.318;1684916663283,3.332,-0.100,3.520,0.000,3.936,0.000,5.012,-1.800,2.892,-0.200,0.984,-0.100,1.044,-0.300,2.960,-0.200,41.318;1684916663187,3.336,-0.100,3.528,0.000,3.936,0.000,5.012,-1.800,2.912,-0.100,0.984,-0.100,1.044,-0.300,2.940,-0.200,40.780;1684916663091,3.324,-0.200,3.532,0.000,3.936,0.000,5.008,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.968,-0.200,41.318;1684916662995,3.312,-0.100,3.536,0.000,3.936,0.000,5.012,-1.800,2.900,-0.100,0.988,-0.100,1.044,-0.300,2.976,-0.100,40.780;1684916662899,3.308,-0.100,3.540,0.000,3.936,0.100,5.004,-1.800,2.884,-0.100,0.988,-0.200,1.044,-0.300,2.956,-0.200,40.780;1684916662802,3.312,-0.100,3.540,0.000,3.936,0.000,5.012,-1.900,2.884,-0.100,0.988,-0.100,1.044,-0.300,2.932,-0.200,41.856;1684916662706,3.336,-0.100,3.504,0.000,3.936,0.000,5.028,-1.600,2.900,-0.100,0.988,-0.100,1.044,-0.300,2.936,-0.200,40.780;1684916662610,3.320,-0.100,3.500,0.000,3.936,0.000,5.032,-1.600,2.916,-0.100,0.988,-0.200,1.044,-0.300,2.960,-0.100,40.780;1684916662514,3.308,-0.200,3.496,0.000,3.936,0.000,5.032,-1.600,2.912,-0.100,0.984,-0.200,1.044,-0.300,2.976,-0.200,41.318;1684916662418,3.308,-0.100,3.496,0.000,3.936,0.000,5.028,-1.600,2.892,-0.100,0.984,-0.200,1.044,-0.300,2.960,-0.200,41.856;1684916662321,3.312,-0.100,3.500,0.000,3.936,0.000,5.016,-1.800,2.880,-0.100,0.988,-0.100,1.044,-0.300,2.936,-0.100,41.318;1684916662225,3.328,-0.200,3.504,0.000,3.936,0.000,5.008,-1.600,2.888,-0.100,0.988,-0.100,1.044,-0.300,2.932,-0.200,41.318;1684916662129,3.336,-0.100,3.508,0.000,3.936,0.000,5.016,-1.600,2.908,-0.100,0.988,-0.100,1.044,-0.400,2.952,-0.200,41.318;1684916662032,3.324,-0.200,3.516,0.000,3.936,0.000,5.016,-1.600,2.916,-0.100,0.988,-0.100,1.044,-0.300,2.976,-0.200,40.780;1684916661936,3.308,-0.100,3.524,0.000,3.936,0.000,5.012,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.400,2.964,-0.200,40.780;1684916661839,3.300,-0.200,3.528,0.000,3.936,0.000,5.008,-1.800,2.888,-0.100,0.988,-0.200,1.044,-0.300,2.940,-0.200,40.780;1684916661675,3.332,-0.200,3.536,0.000,3.936,0.000,4.996,-1.800,2.904,-0.100,0.988,-0.100,1.044,-0.300,2.928,-0.200,41.318;1684916661578,3.316,-0.200,3.500,0.000,3.936,0.000,5.004,-1.800,2.904,-0.100,0.984,-0.200,1.044,-0.300,2.960,-0.200,40.780;1684916661482,3.304,-0.100,3.508,0.000,3.936,0.000,5.012,-1.800,2.884,-0.100,0.984,-0.200,1.044,-0.300,2.936,-0.100,40.780;1684916661385,3.300,-0.100,3.512,0.000,3.936,0.000,5.004,-1.800,2.904,-0.100,0.984,-0.100,1.044,-0.300,2.932,-0.100,40.780;1684916661287,3.308,-0.100,3.520,0.000,3.936,0.000,4.964,-1.800,2.916,-0.100,0.984,-0.100,1.044,-0.300,2.952,-0.200,40.780"

temp = non_func_data.split(";")

nonFuncListToModify = []
for elem in temp:
    split_elements = elem.split(',')
    float_elements = [float(e) for e in split_elements]
    nonFuncListToModify.append(float_elements)
initialNonFuncTimestamp = str(nonFuncListToModify[-1][0])[:-2]
finalNonFuncTimestamp = str(nonFuncListToModify[0][0])[:-2]
transposed_matrix = list(map(list, zip(*nonFuncListToModify)))
column_means = [sum(column) / len(column) for column in transposed_matrix]
column_means.pop(0)
finalNonFuncListToTransfer = [[finalNonFuncTimestamp], [initialNonFuncTimestamp]]
for q in range(2):
    for elem in column_means:
        finalNonFuncListToTransfer[q].append(elem)
listNonFuncWithStrings = finalNonFuncListToTransfer
print(listNonFuncWithStrings)

watts = []
for t in listNonFuncWithStrings:
    watts.append(math.fabs(float(t[7])) * math.fabs(float(t[8])/1000))
print(watts)

time = []
for t in listNonFuncWithStrings:
    time.append(int(t[0]))
print(time)

avgWatts = []
for w in range(0, len(watts) - 1):
    avgWatts.append((watts[w] + watts[w + 1])/2)
print(avgWatts)

timeSlot = []
for t in range(0, len(time) - 1):
    timeSlot.append((time[t] - time[t + 1]))
print(timeSlot)

energy = []
for w in range(0, len(avgWatts)):
    energy.append(avgWatts[w] * timeSlot[w])
print(energy)

totEnergy = sum(energy)
print("Energy consumption (mJ): " + str(totEnergy))

'''
for t in range(0, len(temp)):
    temp[t] = temp[t].split(',')
    temp[t] = [float(e) for e in temp[t]]

watts = []
for t in temp:
    watts.append(math.fabs(float(t[7])) * math.fabs(float(t[8])/1000))
print(watts)

time = []
for t in temp:
    time.append(int(t[0]))

avgWatts = []
for w in range(0, len(watts) - 1):
    avgWatts.append((watts[w] + watts[w + 1])/2)
print(avgWatts)

timeSlot = []
for t in range(0, len(time) - 1):
    timeSlot.append((time[t] - time[t + 1]))
print(timeSlot)

energy = []
for w in range(0, len(avgWatts)):
    energy.append(avgWatts[w] * timeSlot[w])
print(energy)

totEnergy = sum(energy)
print("Energy consumption (mJ): " + str(totEnergy))
'''

# print(";".join(listNonFuncWithStrings))
'''
watts = []
for t in temp:
    watts.append(math.fabs(float(t[7])) * math.fabs(float(t[8])/1000))
print(watts)

time = []
for t in temp:
    time.append(int(t[0]))

avgWatts = []
for w in range(0, len(watts) - 1):
    avgWatts.append((watts[w] + watts[w + 1])/2)
print(avgWatts)

timeSlot = []
for t in range(0, len(time) - 1):
    timeSlot.append((time[t] - time[t + 1]))
print(timeSlot)

energy = []
for w in range(0, len(avgWatts)):
    energy.append(avgWatts[w] * timeSlot[w])
print(energy)

totEnergy = sum(energy)
print("Energy consumption (mJ): " + str(totEnergy))
'''