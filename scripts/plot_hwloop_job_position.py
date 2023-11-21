import matplotlib.pyplot as plt
import numpy as np
import os
import sys

plt.set_loglevel("error")
src = ''
dst = ''
name_for_dir = ""

if len(sys.argv) == 6:
    src = sys.argv[1]
    if src[-1] != '/':
        src += '/'
    dst = sys.argv[2]
    if dst[-1] != '/':
        dst += '/'
    name_for_dir = sys.argv[3]
    sat_counter = int(sys.argv[4])
    orbit_duration = float(sys.argv[5])
else:
    print("Usage: python3 plot_hwloop_job_position.py /path/to/src/ /path/to/dst/ name_for_dir sat_counter orbit_duration")
    exit()

dst = os.path.join(dst[:-1], name_for_dir)
if not os.path.exists(dst):
    os.makedirs(dst)

for j in range(sat_counter):
    positions = []
    label_durations = []
    with open(src + 'hwloop_position_' + str(j) + '.csv', 'r') as infile:
        lines = infile.readlines()
        lines = lines[1:]
        for line in lines:
            line_split = line.split(',')
            positions.append(float(line_split[0]))
            label_durations.append(float(line_split[1]))

    # print(positions)
    # print(label_durations)
    # Generate data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    # Calculate start and end positions for each duration
    start_positions = positions
    end_positions = [(start + duration / orbit_duration * 2 * np.pi) % (2 * np.pi) for start, duration in
                     zip(start_positions, label_durations)]
    # end_positions = [start + duration / orbit_duration * 2 * np.pi for start, duration in zip(start_positions, label_durations)]

    # labels = list(range(0, len(positions)))
    # labels = ["Job " + str(elem) for elem in labels]

    # print(start_positions)
    # print(end_positions)

    # Generate plot
    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(14, 6))
    plt.plot(x, y, color='black', linestyle='solid')

    label_text = 'Jobs zone'
    label_position = np.pi / 2
    plt.text(label_position, 0, label_text, ha='center', va='center', color='black', fontsize=12, alpha=0.5)

    label_text = 'Not jobs zone'
    label_position = 3 * (np.pi / 2)
    plt.text(label_position, 0, label_text, ha='center', va='center', color='black', fontsize=12, alpha=0.5)

    legend_handles = [
        plt.Line2D([0], [0], color='blue', linewidth=1, linestyle='-', label='Working', alpha=0.7),
        plt.Line2D([0], [0], color='yellow', linewidth=1, linestyle='-', label='Not working', alpha=0.3)
    ]

    plt.legend(handles=legend_handles)

    # Shade the regions for working and non-working periods
    for i in range(len(start_positions)):
        start = start_positions[i]
        end = end_positions[i]

        # Check for overlap with blue shading
        if i > 0 and start < end_positions[i - 1]:
            start = end_positions[i - 1]

        width = end - start
        plt.axvspan(start, start + width, facecolor='blue', alpha=1, linewidth=2)
        # plt.axvspan(start, end, facecolor='blue', alpha=0.8)

        # Shade non-working periods
        if i < len(start_positions) - 1:
            non_working_start = end
            non_working_end = start_positions[i + 1]
            width = non_working_end - non_working_start
            plt.axvspan(non_working_start, non_working_start + width, facecolor='yellow', alpha=0.3)
            # plt.axvspan(non_working_start, non_working_end, facecolor='yellow', alpha=0.3)

    if not np.isclose(end_positions[-1], np.pi, atol=1e-2):
        plt.axvspan(end_positions[-1], np.pi, facecolor='yellow', alpha=0.3)

    plt.xlabel('Time - Longitude (s)')
    plt.ylabel('Latitude')
    plt.title('Orbital jobs position')

    xmin = 0
    xmax = orbit_duration
    xstep = round(orbit_duration / 4, 3)

    x_ticks = np.linspace(0, 2 * np.pi, 5)
    x_tick_labels = np.linspace(0, orbit_duration, 5).astype(float)

    x_tick_labels = [str(x) for x in x_tick_labels]

    plt.gca().set_xticks(x_ticks)
    plt.gca().set_xticklabels(x_tick_labels)

    plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    # plt.savefig(dst + 'hwloop_job_position_' + str(j) + '.png', format='png', dpi=400, bbox_inches="tight")
    plt.savefig(dst + 'hwloop_job_position_' + str(j) + '.svg', format='svg', bbox_inches="tight")
    plt.savefig(dst + 'hwloop_job_position_' + str(j) + '.eps', format='eps', bbox_inches="tight", transparent=True)
    plt.clf()
