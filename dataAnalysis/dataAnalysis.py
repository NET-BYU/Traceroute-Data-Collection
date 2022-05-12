import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(
    "136.36.62.167.txt",
    sep="\t",
    parse_dates=True,
    infer_datetime_format=True,
    index_col=0,
    names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
)
data.index = pd.to_datetime((data.index.values * 1e9).astype(int))
data["Traceroute"] = data["Traceroute"].str.split(" ")
data["Delay"] = data["Delay"].str.split(" ")


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

    plt.show()


graphTraceroute(data["Traceroute"])
