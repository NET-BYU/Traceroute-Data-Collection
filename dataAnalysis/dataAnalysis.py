import pandas as pd
import numpy as np
import graph
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

    data = pd.read_csv(
        f"Outputs/{target}.txt",
        sep="\t",
        parse_dates=True,
        infer_datetime_format=True,
        index_col=0,
        names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
    )
    data.index = pd.to_datetime((data.index.values * 1e9).astype(int))
    data["Traceroute"] = data["Traceroute"].str.split(" ")
    data["Delay"] = data["Delay"].str.split(" ")
    for stuff in data["Traceroute"]:
        while True:
            try:
                stuff.remove("")
            except:
                break
    for stuff in data["Delay"]:
        while True:
            try:
                stuff.remove("")
            except:
                break

    fig, ax = plt.subplots(3, figsize=(11, 10))
    fig.canvas.manager.set_window_title(f"{target}")
    fig.subplots_adjust(hspace=0.7)
    try:
        graph.TracerouteLength(data["Traceroute"], ax[1])
        graph.PingLatency(data["Latency"], ax[2])
        graph.Traceroute(data["Traceroute"], ax[0], target)
        fig.savefig(f"./Outputs/Graphs/{target}.pdf")
        print("Graphed:", target)
        plt.close()
    except:
        print("Error:", target)
