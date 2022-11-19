from traceroute_resources import parse_data
import pandas as pd
from loguru import logger

# IP_true_file = "24.49.163.147"
# IP_false_file = "50.243.6.69"
path_to_data = "/home/carter/Research/Traceroute-Data-Collection/Outputs/"
length_of_true_data = (
    1008  # 7 days.     1 day = 1440 minutes      (1440 * 7) / 10 = 1008
)
seconds_per_week = 604800
number_of_test_IPs = 1008


def gap_detected(id_T, id_F, timestamp1, timestamp2, testing_data_type):
    # getting the data from the text files and throwing them in some dataframes
    IP_true_df = parse_data(id_T)
    IP_false_df = parse_data(id_F)
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
        # TODO: throw an actual error here to let us know that this triggered

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
    # logger.debug(f"\t\t\t\t\ttested[{true_start}:{true_end}]")
    # logger.debug(f"\t\t\t\t\tuntested[{untested_start}:{untested_end}]")
    return IP_true_df, IP_untested_df
