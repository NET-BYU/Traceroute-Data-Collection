from venv import create
import pandas as pd
import numpy as np
from loguru import logger


def parse_data(target, len_of_IP, text_file):
    random_list = ["a", "b"]
    # Takes the data from a txt file and parses it into a pandas dataframe in a way that will be recognizable by the machine learning algorithm
    if text_file:
        data = pd.read_csv(
            f"Outputs/{target}.txt",
            sep="\t",
            parse_dates=True,
            infer_datetime_format=True,
            names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
        )

        data = data.drop(["TTL", "Latency"], axis=1)

        data["Traceroute"] = data["Traceroute"].str.split(" ")
        data["Delay"] = data["Delay"].str.split(" ")
        logger.debug(data)
    else:
        data = target
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
            if len(data.loc[index, "Traceroute"]) > len_of_IP:
                reduced_traceroute = data.loc[index, "Traceroute"][-len_of_IP:]
            else:
                while len(data.loc[index, "Traceroute"]) < len_of_IP:
                    data.loc[index, "Traceroute"].append("0.0.0.0")
                reduced_traceroute = data.loc[index, "Traceroute"][0:]
            del data.loc[index, "Traceroute"][0:]
            # This takes the IP addresses from the ["x.x.x.x", "x.x.x.x"] format and replaces it with ["x.x.x",  "x.x.x"]
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
                    logger.debug("Can't append:", broken_ip)
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
            if len(data.loc[index, "Delay"]) > len_of_IP:
                reduced_delay = data.loc[index, "Delay"][-len_of_IP:]
            # This ensures that even if something wonkey happens with the traceroute and we don't get the amount of data that we expect, there is still 5 numbers in the array
            else:
                while len(data.loc[index, "Delay"]) < len_of_IP:
                    data.loc[index, "Delay"].append("0.0")
                reduced_delay = data.loc[index, "Delay"][
                    0:
                ]  # This Takes in all of the strings that make up the delay array and converts them into floats.
            if len(reduced_delay) == 0:
                logger.debug("reduced_delay:")
            del data.loc[index, "Delay"][0:]
            for delay in reduced_delay:
                data.loc[index, "Delay"].append(float(delay))
        else:
            logger.debug(f"Error at line {index} at {target}.txt")
            row_to_drop.append(index)
    data = data.drop(row_to_drop, axis=0)
    data = data.reset_index(drop=True)
    return data


def create_check(output):
    # Takes a list of true inputs and condences them into a dataframe of unique IP addresses and normal distribution of the delays
    # Format of verify_check [[[Array of IP Addresses], ... , ['66.219.236']], [[standard deveation, mean], ... , [0.826255166398371, 26.4456]]]
    verify_check = [[], [], []]
    for i in output.index:
        for j in range(len(output.loc[i, "Traceroute"])):
            if len(verify_check[0]) <= j:
                verify_check[0].append([output.loc[i, "Traceroute"][j]])
                if len(output.loc[i, "Delay"]) > j:
                    verify_check[2].append([output.loc[i, "Delay"][j]])
                else:
                    verify_check[2].append([0])
            else:
                if len(output.loc[i, "Delay"]) > j:
                    verify_check[2][j].append(output.loc[i, "Delay"][j])
                if not output.loc[i, "Traceroute"][j] in verify_check[0][j]:
                    verify_check[0][j].append(output.loc[i, "Traceroute"][j])
    for i in range(len(verify_check[2])):
        verify_check[1].append([np.std(verify_check[2][i])])
        verify_check[1][i].append(np.mean(verify_check[2][i]))
    del verify_check[2]
    return verify_check


def initialize(start, end, data):
    # Assumes all of the values in data[start : end] are true values and uses them to create the first intance of verify_check and verified_data
    column_user = list(data)
    output = pd.DataFrame(
        np.zeros(((end - start), len(column_user))), dtype=str, columns=column_user
    )
    output[: (end - start)] = data[start:end]
    verify_check = create_check(output)
    return output, verify_check


def test(data):
    # If more than 75% of the data is true than return true
    score = 0
    try:
        for i in data.index:
            if data.loc[i, "Truth"]:
                score += 1
        if score / len(data) > 0.75:
            return True
        else:
            return False
    except:
        logger.debug(data)
        return False


def update_variables(new_data, identified_data, verify_check, len_identified_data):
    # Checks to see if the new data it true or not
    new_data["Truth"] = verify(new_data, verify_check)
    # Adds the newly identifed data to the end of identified_data
    identified_data = pd.concat([identified_data, new_data], ignore_index=True)
    # Wait for the buffer to be 50 and then pop the first datapoint in identifed_data. If it is good data then append it to verifyed_data, otherwise get rid of it
    if len(identified_data) >= len_identified_data:
        identified_data = identified_data.drop(0, axis=0)
    return identified_data
