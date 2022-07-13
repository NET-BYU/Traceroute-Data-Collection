from operator import index
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import graph
import matplotlib.pyplot as plt
import json
import os
import time


if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")
if not os.path.exists("./Outputs/Graphs"):
    os.makedirs("./Outputs/Graphs")
random_list = ["a", "b"]
with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


def parse_data(target):
    data = pd.read_csv(
        f"Outputs/{target}.txt",
        sep="\t",
        parse_dates=True,
        infer_datetime_format=True,
        names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
    )

    del data["Latency"]
    del data["Time"]
    data["Traceroute"] = data["Traceroute"].str.split(" ")
    data["Delay"] = data["Delay"].str.split(" ")

    for index in data.index:
        if type(data.loc[index, "Traceroute"]) == type(random_list):
            while True:
                try:
                    data.loc[index, "Traceroute"].remove("*")
                except:
                    break

            if len(data.loc[index, "Traceroute"]) > 5:
                reduced_traceroute = data.loc[index, "Traceroute"][-5:]
            else:
                reduced_traceroute = data.loc[index, "Traceroute"]
            del data.loc[index, "Traceroute"][0:]

            for ip in reduced_traceroute:
                broken_ip = ip.split(".")
                for individual_ip in broken_ip:
                    if individual_ip != "*" and individual_ip != "":
                        data.loc[index, "Traceroute"].append(float(individual_ip))
                    else:
                        data.loc[index, "Traceroute"].append(0.0)
            while len(data.loc[index, "Traceroute"]) < 20:
                data.loc[index, "Traceroute"].append(-1.0)
        else:
            print(f"Error at line {index} at {target}.txt")
            data.drop(index, axis=0)

        if (
            type(data.loc[index, "Delay"]) == type(random_list)
            and len(data.loc[index, "Delay"]) >= 5
        ):
            reduced_delay = data.loc[index, "Delay"][-5:]
            del data.loc[index, "Delay"][0:]
            for delay in reduced_delay:
                if delay != "*" and delay != "":
                    data.loc[index, "Delay"].append(float(delay))
                    data.loc[index, "Traceroute"].append(float(delay))
                else:
                    data.loc[index, "Traceroute"].append(0.0)

        if type(data.loc[index, "Traceroute"]) == type(random_list):
            if data.loc[index, "TTL"] != "*":
                data.loc[index, "Traceroute"].append(float(data.loc[index, "TTL"]))
            else:
                data.loc[index, "Traceroute"].append(0.0)

        while len(data.loc[index, "Traceroute"]) < 26:
            data.loc[index, "Traceroute"].append(0.0)

    data = data.drop(["TTL", "Delay"], axis=1)
    return data


def MLIP(array, length):
    for i in range(len(array)):
        if i == 0:
            value = [True for x in range(len(array[i]))]
            array[i]["Correct"] = value
        else:
            value = [False for x in range(len(array[i]))]
            array[i]["Correct"] = value
            if i == 1:
                output = array[i]
            else:
                output = pd.concat([output, array[i]], ignore_index=True)
    output = shuffle(output)
    output.reset_index(inplace=True, drop=True)
    if len(array[0]) > length:
        array[0] = array[0][:length]
    if len(output) > len(array[0]):
        output = output[: len(array[0])]
    output = pd.concat([output, array[0]], ignore_index=True)
    output = shuffle(output)
    output.reset_index(inplace=True, drop=True)
    return output


def inline(array, length, percent):
    for i in range(len(array)):
        if i == 0:
            value = [True for x in range(len(array[i]))]
            array[i]["Correct"] = value
            good_data = array[i]
        else:
            value = [False for x in range(len(array[i]))]
            array[i]["Correct"] = value
            if i == 1:
                bad_data = array[i]
            else:
                bad_data = pd.concat([bad_data, array[i]], ignore_index=True)

    bad_data = shuffle(bad_data)
    bad_data.reset_index(inplace=True, drop=True)

    train = pd.concat(
        [bad_data[: int(length * percent)], good_data[:length]], ignore_index=True
    )
    test = pd.concat(
        [bad_data[int(length * percent) :], good_data[length:]], ignore_index=True
    )
    X_train = train["Traceroute"]
    y_train = train["Correct"]
    X_test = test["Traceroute"]
    y_test = test["Correct"]

    return X_train, X_test, y_train, y_test


array = [
    parse_data(IPADR[0]),
    parse_data(IPADR[1]),
    parse_data(IPADR[2]),
    parse_data(IPADR[3]),
    parse_data(IPADR[4]),
    parse_data(IPADR[5]),
    parse_data(IPADR[6]),
]

x = 0
for i in array[3]["Traceroute"]:
    x += 1
    try:
        if len(i) != 26:
            print(f"line: {x}\n{len(i)}: {i}")
    except:
        print("TypeError: object of type 'float' has no len()", i, "line:", x)


X_train, X_test, y_train, y_test = inline(array, 30, 0.5)
X_train = X_train.to_list()
y_train = y_train.to_list()
X_test = X_test.to_list()
y_test = y_test.to_list()

print(f"Training: {len(X_train)}")
print(f"Test: {len(X_test)}")

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)
pred_rfc = rfc.predict(X_test)


print(classification_report(y_test, pred_rfc))
