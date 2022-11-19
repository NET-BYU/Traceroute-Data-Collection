import pandas as pd
import numpy as np
from loguru import logger


def parse_data(
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


def verify(data, verify_check):
    traceroute_score = 0.0
    delay_score = 0.0
    if len(data.iat[0, 0]) <= len(verify_check[0]):
        for i in range(len(data.iat[0, 0])):
            # Checks every datapoint in Traceroute to see if it is in verify check. If it is in the exact same place, give it a higher score
            # print("this is data:")
            # print(data.iat[0, 0])
            # print("This is length of traceroute:")
            # print(len(data.iat[0, 0]))
            if data.iat[0, 0][i] in verify_check[0][i]:
                # print(data.iat[0, 0][i])
                traceroute_score += 1
            # elif data.iat[0, 0][i] in verify_check[0]:
            #     traceroute_score += 1
    else:
        for i in range(len(verify_check[0])):
            # Does the same thing as the if statement, just not going out of bounds. I am not convinced this redundancy is nessisary, however I put it in here because I was having problems
            if data.iat[0, 0][i] in verify_check[0][i]:
                traceroute_score += 1
            # elif data.iat[0, 0][i] in verify_check[0]:
            #     traceroute_score += 1
    # try:
    # Checks to see if the delay we have gotten is within 1 standard deveations of the verify_check data
    # Once again there is the length redudnancy because I am having mysterious errors sometimes
    # sandard_deviations = 1
    # if len(data.iat[1, 0]) <= len(verify_check[1]):
    #     for i in range(len(data.iat[0, 1])):
    #         if data.iat[0, 1][i] >= (
    #             verify_check[1][i][1] - sandard_deviations * verify_check[1][i][0]
    #         ) and data.iat[0, 1][i] <= (
    #             verify_check[1][i][1] + sandard_deviations * verify_check[1][i][0]
    #         ):
    #             delay_score += 1
    # else:
    #     for i in range(len(verify_check[1])):
    #         if data.iat[0, 1][i] >= (
    #             verify_check[1][i][1] - sandard_deviations * verify_check[1][i][0]
    #         ) and data.iat[0, 1][i] <= (
    #             verify_check[1][i][1] + sandard_deviations * verify_check[1][i][0]
    #         ):
    #             delay_score += 1
    # except:
    #     logger.debug("Error comparing delay data")
    #     return "Two"
    total_score = traceroute_score / len(
        data.iat[0, 0]
    )  # * 0.8 + (delay_score / len(data)) * 0.2
    return total_score
    # logger.debug("total_score:", total_score)
    # if total_score >= 0.75:
    #     return True
    # else:
    #     return False
