import pandas as pd
import numpy as np
from loguru import logger

length_of_true_data = (
    1008  # 7 days.     1 day = 1440 minutes      (1440 * 7) / 10 = 1008
)
seconds_per_week = 604800


def dataframe(
    target,
):
    # Takes the data from a txt file and parses it into a pandas dataframe in a way that will be recognizable by the machine learning algorithm
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
    return data


def trim_dataframe(data, len_of_IP):
    random_list = ["a", "b"]
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
            logger.debug(f"Error in data_manipulation.trim_dataframe")
            row_to_drop.append(index)
    data = data.drop(row_to_drop, axis=0)
    data = data.reset_index(drop=True)
    return data


def gap_detected(id_T, id_F, timestamp1, timestamp2, testing_data_type):
    # getting the data from the text files and throwing them in some dataframes
    IP_true_df = dataframe(id_T)
    IP_false_df = dataframe(id_F)
    if testing_data_type:
        id_Q = id_T
    else:
        id_Q = id_F
    if testing_data_type:
        IP_untested_df = IP_true_df.copy()
    else:
        IP_untested_df = IP_false_df.copy()

    # here is where I convert the times with the timestamps to lines in the data
    # the true_* and untested_* variables are meant to be index numbers in either

    # this only works well if we have more than a weeks worth of data before timestamp1
    for index, row in IP_true_df.iterrows():
        if row["Time"] > timestamp1 - seconds_per_week:
            true_start = index - 1
            break
    for index, row in IP_true_df.iterrows():
        if row["Time"] > timestamp1:
            true_end = index - 1
            break

        # If the time we get is to close to the begining of the file, then automatically just take the data from the beginning of the program
        # Lets us know about and fixes any out of bounds errors that are likley to happen
    if true_end < 0:
        logger.debug(
            f"WARNING - traceroute_collection.py\n\t Timestamp pre-dates the creation of {id_T}.txt."
        )
        true_end = length_of_true_data
    elif true_start < 0:

        logger.debug(
            f"WARNING - traceroute_collection.py:\n\t Asking for data that pre-dates the creaton of {id_T}.txt."
        )
        true_start = 0

    # Finding the start and end times for the untested data
    for index, row in IP_untested_df.iterrows():
        if row["Time"] > timestamp2:
            untested_start = index - 1
            break
    for index, row in IP_untested_df.iterrows():
        if row["Time"] > timestamp2 + seconds_per_week:
            untested_end = index - 1
            break

        # Making sure that the data is within bounds and throing errors if it isn't
    if untested_end < 0:
        logger.debug(
            f"WARNING - traceroute_collection.py\n\t Timestamp pre-dates the creation of {id_Q}.txt."
        )
        untested_end = length_of_true_data
    elif untested_start < 0:
        logger.debug(
            f"WARNING - traceroute_collection.py:\n\t Asking for data that pre-dates the creaton of {id_Q}.txt."
        )
        untested_start = 0

    # This trims down IP_untested_df to just the data that we want
    start_to_drop = [i for i in range(0, untested_start)]
    end_to_drop = [i for i in range(untested_end, len(IP_untested_df))]
    data_to_drop = start_to_drop + end_to_drop
    IP_untested_df = IP_untested_df.drop(data_to_drop, axis=0)

    # this trims down IP_true_df to just the data that we want
    begining_to_drop = [i for i in range(0, true_start)]
    end_to_drop = [i for i in range(true_end, len(IP_true_df))]
    data_to_drop = begining_to_drop + end_to_drop
    IP_true_df = IP_true_df.drop(data_to_drop, axis=0)

    # removing the time collum from both because we don't want it in the output
    IP_true_df = IP_true_df.drop(["Time"], axis=1)
    IP_untested_df = IP_untested_df.drop(["Time"], axis=1)
    return IP_true_df, IP_untested_df


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
