import json
from loguru import logger
import data_manipulation
import analizing_data


with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


for good_traceroute in IPADR:
    with open("./Outputs/CSV/" + good_traceroute + ".csv", "w") as this:
        parsed_good = data_manipulation.dataframe(good_traceroute)
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
            for test in IPADR:
                value = analizing_data.detection(
                    good_traceroute, test, current_time, current_time
                )
                this.write(f", {value * 100}")
            this.write("\n")
