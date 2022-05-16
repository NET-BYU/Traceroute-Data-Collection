import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def PingLatency(list_of_latencys, ax):

    array_of_latency = np.array(list_of_latencys)
    array_of_latency = np.sort(array_of_latency)

    plt.hist(array_of_latency, bins=100)
    ax.set_title("Ping Latency")
    ax.set_ylabel("Instances in Range")
    ax.set_xlabel("Latency")


def Traceroute(list_of_traceroutes, ax):
    comprehensive_list_of_traceroutes = []

    for traceroute in list_of_traceroutes:
        for index in range(len(traceroute)):
            if (len(comprehensive_list_of_traceroutes) - 1) <= index:
                comprehensive_list_of_traceroutes.append([traceroute[index]])
            if traceroute[index] in comprehensive_list_of_traceroutes[index]:
                pass
            else:
                comprehensive_list_of_traceroutes[index].append(traceroute[index])

    x = []
    y = []
    for index in range(len(comprehensive_list_of_traceroutes)):
        x.append(index + 1)
        y.append(len(comprehensive_list_of_traceroutes[index]))

    ax.bar(x, y, width=1, edgecolor="white", linewidth=1)
    ax.set_title("Unique IP Addresses Across Multiple Traceroutes")
    ax.set_xlabel("Distance From Source")
    ax.set_ylabel("Number of Unique IP Addresses")
