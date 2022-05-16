import pandas as pd
import numpy as np
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


def graphPingLatency(list_of_latencys):

    array_of_latency = np.array(list_of_latencys)
    array_of_latency = np.sort(array_of_latency)

    fig, ax = plt.subplots()
    plt.hist(array_of_latency, bins=100)
    ax.set_title("Ping Latency")
    ax.set_ylabel("Instances in Range")
    ax.set_xlabel("Latency")
    plt.show()


def graphTraceroute(list_of_traceroutes):
    comprehensive_list_of_traceroutes = []

    for traceroute in list_of_traceroutes:
        for index in range(len(traceroute)):
            if (len(comprehensive_list_of_traceroutes) - 1) <= index:
                comprehensive_list_of_traceroutes.append([traceroute[index]])
            if traceroute[index] in comprehensive_list_of_traceroutes[index]:
                pass
            else:
                comprehensive_list_of_traceroutes[index].append(traceroute[index])

    print(comprehensive_list_of_traceroutes)
    x = []
    y = []
    for index in range(len(comprehensive_list_of_traceroutes)):
        x.append(index + 1)
        y.append(len(comprehensive_list_of_traceroutes[index]))

    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="white", linewidth=1)
    ax.set_title("Unique IP Addresses Across Multiple Traceroutes")
    ax.set_xlabel("Distance From Source")
    ax.set_ylabel("Number of Unique IP Addresses")
    plt.show()


graphTraceroute(data["Traceroute"])
graphPingLatency(data["Latency"])
