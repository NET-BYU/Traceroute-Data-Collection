import json
from loguru import logger
import data_manipulation
import analizing_data


with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


def load_all_data(ip_addresses):
    return {
        ip: data_manipulation.dataframe(ip, start="2022-08-08 16:37:25.480")
        for ip in ip_addresses
    }


all_data = load_all_data(IPADR)

for good_ip, good_data in all_data.items():
    logger.info(f"Testing {good_ip}...")

    for test_ip, test_data in all_data.items():
        logger.info(f"\tComparing against {test_ip}...")

        groups = list(good_data.groups.keys())
        for true_week_name, questionable_week_name in zip(groups, groups[1:]):
            score = analizing_data.traceroute_analysis(
                good_data.get_group(true_week_name),
                test_data.get_group(questionable_week_name),
            )

            # Do something with score???

        # for good, test in zip(good_data, test_data[1:]):
        #     print(good)
        #     print(test)
        # for good_data_week, test_data_next_week in "???":
        # value = analizing_data.detection(good_data_week, test_data_next_week)


# for good_traceroute in IPADR:
#     with open("./Outputs/CSV/" + good_traceroute + ".csv", "w") as this:
#         logger.info(f"Testing {good_traceroute}...")
#         parsed_good = data_manipulation.dataframe(good_traceroute)
#         good_info = [
#             good_traceroute,
#             parsed_good.at[0, "Time"],
#             parsed_good.at[len(parsed_good) - 1, "Time"],
#         ]
#         if good_info[1] < 1659998245.480082:
#             good_info[1] = 1659998245.480082
#         current_time = good_info[1]
#         for i in IPADR:
#             this.write(f", {i}")
#         this.write("\n")

#         while current_time + (2 * 604800) < good_info[2]:
#             current_time = current_time + 604800
#             this.write(str(current_time))
#             for test in IPADR:
#                 logger.info(f"Comparing against {test}...")
#                 value = analizing_data.detection(
#                     good_traceroute, test, current_time, current_time
#                 )
#                 this.write(f", {value * 100}")
#             this.write("\n")
