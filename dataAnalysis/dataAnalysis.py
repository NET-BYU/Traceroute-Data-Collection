import pandas as pd
import numpy as np
import graph
import matplotlib.pyplot as plt

data = pd.read_csv(
    "Outputs/byu.edu.txt",
    sep="\t",
    parse_dates=True,
    infer_datetime_format=True,
    index_col=0,
    names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
)
data.index = pd.to_datetime((data.index.values * 1e9).astype(int))
data["Traceroute"] = data["Traceroute"].str.split(" ")
data["Delay"] = data["Delay"].str.split(" ")


graph.Traceroute(data["Traceroute"])
graph.PingLatency(data["Latency"])
