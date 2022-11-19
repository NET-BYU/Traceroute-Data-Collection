from traceroute_resources import (
    verify,
)
from resources import (
    parse_data,
    create_check,
)
import pandas as pd
from loguru import logger

start = 0
end = 1008  # 7 days.     1 days = 10080 minutes      (1440 * 7) / 10 = 1008
len_identified_data = 25
data = []
# Parses all of the data and puts it in a variable called data


def traceroute_analysis(good_data, unverified_data):
    good_data = parse_data(good_data, 6, False)
    unverified_data = parse_data(unverified_data, 6, False)
    verify_check = create_check(good_data)
    verified_data = []
    total_true = 0
    for i in unverified_data.index:
        verified_data.append(verify(unverified_data.take([i], axis=0), verify_check))
        total_true += verified_data[i]
    reliability_percent = total_true / len(verified_data)

    return reliability_percent
