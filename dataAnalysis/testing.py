from traceroute_analysis import traceroute_analysis
from traceroute_collection import gap_detected
from traceroute_resources import parse_data

import json
from loguru import logger


def detection(id1, id2, t1, t2, truth):
    # print("Re started traceroute data colleciton to id:", id1)
    # when doing in real time pause while traceroute collects data
    testing1, testing2 = gap_detected(id1, id2, t1, t2, truth)
    # print(testing1)
    # print(testing2)
    score = traceroute_analysis(testing1, testing2)
    # Score will show how many trigered true of false. If we are checking for true values that is the accuracy. If we are checking against false data we have to invert the score. (score = 0 means that it was 100% accurate)
    return score


# def stop_traceroute(id):
#     print("Stoped tracerouting to id:", id)


with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)
# for good in IPADR:
#     parsed_good = parse_data(good)
#     # Getting the range of the good data. How long has this been running?
#     if latest_time < parsed_good.at[0, "Time"]:
#         latest_time = parsed_good.at[0, "Time"]
#     good_info = [
#         good,
#         parsed_good.at[0, "Time"],
#         parsed_good.at[len(parsed_good) - 1, "Time"],
#     ]

for good_traceroute in IPADR:
    with open("./Outputs/CSV/" + good_traceroute + ".csv", "w") as this:
        parsed_good = parse_data(good_traceroute)
        good_info = [
            good_traceroute,
            parsed_good.at[0, "Time"],
            parsed_good.at[len(parsed_good) - 1, "Time"],
        ]
        if good_info[1] < 1659998245.480082:
            good_info[1] = 1659998245.480082
        current_time = good_info[1]
        for i in IPADR:
            this.write(f", {i}")
        this.write("\n")

        while current_time + (2 * 604800) < good_info[2]:
            current_time = current_time + 604800
            this.write(str(current_time))
            # value = detection(
            #     good_traceroute, good_traceroute, current_time, current_time, False
            # )
            # this.write(f", {value * 100}")
            for test in IPADR:
                value = detection(
                    good_traceroute, test, current_time, current_time, False
                )
                this.write(f", {value * 100}")
            this.write("\n")
