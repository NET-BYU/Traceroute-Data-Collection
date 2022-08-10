import pandas as pd
import numpy as np
import json
import os


def parse_data(target):
    # print(target)
    random_list = ["a", "b"]
    # Takes the data from a txt file and parses it into a pandas dataframe in a way that will be recognizable by the machine learning algorithm

    data = pd.read_csv(
        f"Outputs/{target}.txt",
        sep="\t",
        parse_dates=True,
        infer_datetime_format=True,
        names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
    )

    data = data.drop(["TTL", "Time", "Latency"], axis=1)

    data["Traceroute"] = data["Traceroute"].str.split(" ")
    data["Delay"] = data["Delay"].str.split(" ")
    row_to_drop = []
    for index in data.index:
        if type(data.loc[index, "Traceroute"]) == type(random_list):

            # I decided that we don't want to include any instances of * into the data. This is in an effort to provide more specificity to the data
            while True:
                try:
                    data.loc[index, "Traceroute"].remove("*")
                except:
                    break
            while True:
                try:
                    data.loc[index, "Traceroute"].remove("")
                except:
                    break
            # We need a consistant sized array to pass into sklearn, so i decided that the last 5 nodes in the traceroute's path. I belived this would be sort enough almost any route would have then but long enough to get accurate results
            if len(data.loc[index, "Traceroute"]) > 5:
                reduced_traceroute = data.loc[index, "Traceroute"][-5:]
            else:
                reduced_traceroute = data.loc[index, "Traceroute"][0:]
            del data.loc[index, "Traceroute"][0:]

            # This takes the IP addresses from the ["x.x.x.x", "x.x.x.x"] notation and replaces it with ["x.x.x",  "x.x.x"]
            # print(data.loc[index, "Traceroute"])
            for ip in range(len(reduced_traceroute)):
                broken_ip = reduced_traceroute[ip].split(".")
                while True:
                    try:
                        broken_ip.remove("")
                    except:
                        break
                try:
                    data.loc[index, "Traceroute"].append(
                        broken_ip[0] + "." + broken_ip[1] + "." + broken_ip[2]
                    )
                except:
                    print("Can't append:", broken_ip)

            if len(reduced_traceroute) == 0:
                row_to_drop.append(index)

                # This takes the last 5 delay values and converts them to floats
            while True:
                try:
                    data.loc[index, "Delay"].remove("*")
                except:
                    break
            while True:
                try:
                    data.loc[index, "Delay"].remove("")
                except:
                    break

            if len(data.loc[index, "Delay"]) >= 5:
                reduced_delay = data.loc[index, "Delay"][-5:]
            else:
                reduced_delay = data.loc[index, "Delay"][0:]
            del data.loc[index, "Delay"][0:]

            for delay in reduced_delay:
                data.loc[index, "Delay"].append(float(delay))

        else:
            print(f"Error at line {index} at {target}.txt")
            row_to_drop.append(index)
    data = data.drop(row_to_drop, axis=0)
    return data


def create_check(output):
    verify_check = [[], [], []]
    for i in output.index:
        for j in range(len(output.loc[i, "Traceroute"])):
            try:
                if len(verify_check[0]) <= j:
                    verify_check[0].append([output.loc[i, "Traceroute"][j]])
                    verify_check[2].append([output.loc[i, "Delay"][j]])
                else:
                    already_here = False
                    verify_check[2][j].append(output.loc[i, "Delay"][j])
                    if not output.loc[i, "Traceroute"][j] in verify_check[0][j]:
                        verify_check[0][j].append(output.loc[i, "Traceroute"][j])
            except:
                print("Error of some kind")
                verify_check[0][j].append("0.0.0")
    for i in range(len(verify_check[2])):
        verify_check[1].append([np.std(verify_check[2][i])])
        verify_check[1][i].append(np.mean(verify_check[2][i]))
    del verify_check[2]
    return verify_check


def initialize(start, end, data):
    column_user = list(data)
    output = pd.DataFrame(
        np.zeros(((end - start), len(column_user))), dtype=str, columns=column_user
    )
    output[: (end - start)] = data[start:end]
    verify_check = create_check(output)
    return output, verify_check


def verify(data, verify_check):
    score = 0
    if len(data["Traceroute"]) <= len(verify_check[0]):
        for i in range(len(data["Traceroute"])):
            # print('data["Traceroute_data"][i]', data["Traceroute"][i])
            # print("verify_check[0][i]", verify_check[0][i])
            if data["Traceroute"][i] in verify_check[0][i]:
                score += 2
            elif data["Traceroute"][i] in verify_check[0]:
                score += 1
    else:
        for i in range(len(verify_check[0])):
            # print('data["Traceroute_data"][i]', data["Traceroute"][i])
            # print("verify_check[0][i]", verify_check[0][i])
            if data["Traceroute"][i] in verify_check[0][i]:
                score += 2
            elif data["Traceroute"][i] in verify_check[0]:
                score += 1

    if score >= len(data) * 1.75:
        # print("True", score)
        return True
    else:
        # print("False", score)
        return False


def test(data):
    score = 0
    # print("\n\n\tdata:\n", data)
    # print("\tfirst index:")
    for i in data.index:
        if data.loc[i, "Truth"]:
            score += 1
    if score / len(data) > 0.75:
        # print("True:", score)
        return True
    else:
        print("False")
        return False


def updata_variables(new_data, identified_data, verified_data, verify_check):
    temp = pd.DataFrame(
        [
            [
                new_data["Traceroute"],
                new_data["Delay"],
                verify(new_data, verify_check),
            ]
        ],
        columns=["Traceroute", "Delay", "Truth"],
    )
    return new_data, identified_data, verified_data, verify_check
