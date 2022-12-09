import json
from loguru import logger
import data_manipulation
import analizing_data
import pandas as pd


with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


def load_all_data(ip_addresses):
    return {
        ip: data_manipulation.dataframe(ip, start="2022-08-08 16:37:25.480")
        for ip in ip_addresses
    }


def analyze_data(good_data, test_data, test_ip):
    logger.info(f"\tComparing against {test_ip}...")

    results = []
    times = []
    groups = list(good_data.groups.keys())
    for true_week_name, questionable_week_name in zip(groups, groups[1:]):
        percent = analizing_data.traceroute_analysis(
            good_data.get_group(true_week_name),
            test_data.get_group(questionable_week_name),
        )

        results.append(percent)
        times.append(true_week_name)

    return test_ip, pd.Series(results, index=times)


all_data = load_all_data(IPADR)
all_results = {}

for good_ip, good_data in all_data.items():
    logger.info(f"Testing {good_ip}...")

    results = dict(
        analyze_data(good_data, test_data, test_ip)
        for test_ip, test_data in all_data.items()
    )
    results = pd.DataFrame(results)
    results.to_csv(f"Outputs/CSV/{good_ip}.csv")
    all_results[good_ip] = results

print(all_results)
