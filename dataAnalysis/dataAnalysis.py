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

    fig, ax = plt.subplots(2, figsize=(11, 10))
    fig.canvas.manager.set_window_title(f"{target}")
    plt.subplots_adjust(hspace=0.7)

    graph.Traceroute(data["Traceroute"], ax[0])
    graph.PingLatency(data["Latency"], ax[1])
    plt.savefig(f"./Outputs/Graphs/{target}.pdf")
