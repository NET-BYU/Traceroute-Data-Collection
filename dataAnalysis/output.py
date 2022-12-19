import json
from loguru import logger
import data_manipulation
import analizing_data
import pandas as pd
from yaml import safe_load


with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


def load_all_data(ip_addresses, server):
    return {
        ip: data_manipulation.dataframe(ip, server, start="2022-08-08 16:37:25.480")
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

with open("servers.yaml") as f:
    config = safe_load(f)

hosts = config["servers"]
north_hosts = config["clients"]["north"]
provo_hosts = config["clients"]["provo"]
south_hosts = config["clients"]["south"]

all_results = {}
for host in hosts:
    all_data = load_all_data(IPADR, host)
    all_results[host] = {}
    all_results[host]["north"] = []
    all_results[host]["provo"] = []
    all_results[host]["south"] = []

    for good_ip, good_data in all_data.items():
        logger.info(f"Testing {good_ip}...")

        results = dict(
            analyze_data(good_data, test_data, test_ip)
            for test_ip, test_data in all_data.items()
        )
        # Average all the values in the time period
        results = pd.DataFrame(results).apply(pd.DataFrame.mean).to_frame()

        # Filter out values and only compare them to those in their group
        if good_ip in north_hosts:
            logger.debug("North")
            results = results[results.index.isin(north_hosts)]
            all_results[host]["north"].append(results)
        elif good_ip in provo_hosts:
            logger.debug("Provo")
            results = results[results.index.isin(provo_hosts)]
            all_results[host]["provo"].append(results)
        elif good_ip in south_hosts:
            logger.debug("South")
            results = results[results.index.isin(south_hosts)]
            all_results[host]["south"].append(results)
        else:
            logger.critical("Found IP out of zones!!!")

        # results.to_csv(f"Outputs/CSV/{host}/{good_ip}.csv")

for host in all_results.keys():
    for zone in all_results[host].keys():
        all_results[host][zone] = pd.concat(all_results[host][zone], axis=1)

print(all_results)
