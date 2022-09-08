from resources import parse_data, initialize
import dataAnalysis.graph_resorces as graph_resorces
import matplotlib.pyplot as plt
import json
import os

if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")
if not os.path.exists("./Outputs/Graphs"):
    os.makedirs("./Outputs/Graphs")

with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)

for target in IPADR:
    data = parse_data(target)
    print("Parsed:", target)
    i = 0
    time_interval = 114
    previous_check = 0
    difference = []
    while i + time_interval - 1 < len(data):
        verified_data, current_check = initialize(i, i + time_interval - 1, data[i])
        i += time_interval
        previous_check = current_check
        difference = check_difference(difference, current_check, previous_check)

    fig, ax = plt.subplots(3, figsize=(11, 10))
    fig.canvas.manager.set_window_title(f"{target}")
    fig.subplots_adjust(hspace=0.7)
    try:
        # graph_resorces.TracerouteLength(data["Traceroute"], ax[1])
        # graph_resorces.PingLatency(data["Latency"], ax[2])
        # graph_resorces.Traceroute(data["Traceroute"], ax[0], target)
        # fig.savefig(f"./Outputs/Graphs/{target}.pdf")
        print("Graphed:", target)
        plt.close()
    except:
        print("Error:", target)
