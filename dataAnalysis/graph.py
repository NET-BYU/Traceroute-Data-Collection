from inspect import trace
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def PingLatency(list_of_latencys, ax):

    array_of_latency = np.array(list_of_latencys)
    array_of_latency = np.sort(array_of_latency)

    ax.hist(array_of_latency, bins=100)
    ax.set_title("Ping Latency")
    ax.set_ylabel("Instances in Range")
    ax.set_xlabel("Latency")


def Traceroute(list_of_traceroutes, ax, target):
    comprehensive_list_of_traceroutes = []
    comprehensive_ammount_of_traceroutes = []

    for traceroute in list_of_traceroutes:
        for index in range(len(traceroute)):
            if (len(comprehensive_list_of_traceroutes) - 1) <= index:
                comprehensive_list_of_traceroutes.append([traceroute[index]])
                comprehensive_ammount_of_traceroutes.append([1])
            if traceroute[index] in comprehensive_list_of_traceroutes[index]:
                for index_of_traceroute in range(
                    len(comprehensive_list_of_traceroutes[index])
                ):
                    if (
                        traceroute[index]
                        == comprehensive_list_of_traceroutes[index][index_of_traceroute]
                    ):
                        comprehensive_ammount_of_traceroutes[index][
                            index_of_traceroute
                        ] += 1

            else:
                comprehensive_list_of_traceroutes[index].append(traceroute[index])
                comprehensive_ammount_of_traceroutes[index].append(1)
                break

    x = []
    y = []
    for index in range(len(comprehensive_list_of_traceroutes)):
        x.append(index + 1)
        y.append(len(comprehensive_list_of_traceroutes[index]))

    ax.bar(x, y, width=1, edgecolor="white", linewidth=1)
    ax.set_title("Unique IP Addresses Across Multiple Traceroutes")
    ax.set_xlabel("Distance From Source")
    ax.set_ylabel("Number of Unique IP Addresses")

    TracerouteSteps(
        comprehensive_ammount_of_traceroutes, comprehensive_list_of_traceroutes, target
    )


def TracerouteSteps(
    comprehensive_ammount_of_traceroutes, comprehensive_list_of_traceroutes, target
):
    row = 5
    if int(len(comprehensive_ammount_of_traceroutes) / row) == (
        len(comprehensive_ammount_of_traceroutes) / row
    ):
        collum = int(len(comprehensive_ammount_of_traceroutes) / row)
    else:
        collum = int(len(comprehensive_ammount_of_traceroutes) / row) + 1

    figure, axis = plt.subplots(row, collum, figsize=(40, 20))

    for index in range(len(comprehensive_list_of_traceroutes)):
        axis[(index) % row][int((index) / row)].bar(
            comprehensive_list_of_traceroutes[index],
            comprehensive_ammount_of_traceroutes[index],
        )
    plt.subplots_adjust(hspace=0.08, left=0.03, right=0.99, bottom=0.03)
    figure.canvas.manager.set_window_title(f"{target}_traceroute_step")
    figure.savefig(f"./Outputs/Graphs/{target}_traceroute_step.pdf")


def TracerouteLength(list_of_traceroutes, ax):
    length_of_traceroutes = []
    for traceroot in list_of_traceroutes:
        length_of_traceroutes.append(len(traceroot))

    ax.hist(length_of_traceroutes, range=(0, 30), bins=30)
    ax.set_title("Hops in Traceroot")
    ax.set_ylabel("Instances in Range")
    ax.set_xlabel("Number of Hops")
