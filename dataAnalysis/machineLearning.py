from sklearn.ensemble import RandomForestClassifier
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
random_list = ["a", "b"]
with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)
for target in IPADR:

    data = pd.read_csv(
        f"Outputs/{target}.txt",
        sep="\t",
        parse_dates=True,
        infer_datetime_format=True,
        # index_col=0,
        names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
    )
    print(data.head())

    del data["Latency"]
    del data["Time"]
    data["Traceroute"] = data["Traceroute"].str.split(" ")
    data["Delay"] = data["Delay"].str.split(" ")

    for index in data.index:
        while True:
            try:
                data.loc[index, "Traceroute"].remove("*")
            except:
                break
        # print(type(data.loc[index, "Traceroute"]))
        if (
            type(data.loc[index, "Traceroute"]) == type(random_list)
            and len(data.loc[index, "Traceroute"]) > 5
        ):
            reduced_traceroute = data.loc[index, "Traceroute"][-5:]
            del data.loc[index, "Traceroute"][0:]
            for ip in reduced_traceroute:
                broken_ip = ip.split(".")
                for individual_ip in broken_ip:
                    data.loc[index, "Traceroute"].append(individual_ip)
        else:
            print(f"Error at line {index}")
            pass

        while True:
            try:
                data.loc[index, "Delay"].remove("*")
            except:
                break
        if (
            type(data.loc[index, "Delay"]) == type(random_list)
            and len(data.loc[index, "Delay"]) > 5
        ):
            reduced_delay = data.loc[index, "Delay"][-5:]
            del data.loc[index, "Delay"][0:]
            for delay in reduced_delay:
                data.loc[index, "Delay"].append(delay)

    print(data.head())
    break
