from resources import (
    parse_data,
    initialize,
    verify,
    test,
    create_check,
    update_variables,
)
import pandas as pd
import json


with open("Input.json", "r") as input_file:
    input_strings = json.load(input_file)

start = 0
end = 50
size = 50
data = []
# Parses all of the data and puts it in a variable called data
for i in input_strings:
    print("Parsing:", i)
    data.append(parse_data(i))

# Inside this for loop we go though each of the IP addresses and first check it against itself and then check against every other IP address in the list
for true_dataframe in range(len(data)):
    # Initializes variables based on the assumption that the data points from [start, end] are trustworty
    print("\nCalculating:", input_strings[true_dataframe])
    verified_data, verify_check = initialize(start, end, data[true_dataframe])
    identified_data = data[true_dataframe].take([end], axis=0)
    identified_data["Truth"] = verify(
        data[true_dataframe].take([end], axis=0), verify_check
    )

    previous_test = True
    total_true = 0
    total_false = 0
    total_errors = 0

    # itterates through every line of data after [end] in the IP address, keeping a buffer of 50 datapoints that are known to be correct as well as a buffer of 50 tested variables who's truth is averaged and used to determine if an error should be sent or not
    for j in data[true_dataframe][end + 1 :].index:
        try:
            # Tests the next datapoint and appends it to the end of identified_data. Pops off the first data point of identified_data and if it was previously determined to be true it appends it to the end of verified_data and pops off the first datapoint
            identified_data, verified_data, verify_check = update_variables(
                data[true_dataframe].take([j], axis=0),
                identified_data,
                verified_data,
                verify_check,
            )
        except:
            print("Error at line:", j)
            total_errors += 1
            continue
        # Test returns true if more than 75% of the datapoints in identified_data were previously determined to be true
        current_test = test(identified_data)
        if current_test:
            total_true += 1
        else:
            total_false += 1
        if previous_test != current_test:
            if not current_test:
                print("\tFalse from: ", j)
            else:
                print("\tTo: ", j)
            previous_test = current_test
    print("True positives:", total_true, "/", total_true + total_false + total_errors)
    print("False negatives:", total_false, "/ 0")
    print("Errors:", total_errors)

    previous_test = False
    total_true = 0
    total_false = 0
    total_errors = 0
    # Itterates throught every other IP address with the original set of
    for false_dataframe in range(len(data)):
        if false_dataframe != true_dataframe:
            verified_data, verify_check = initialize(start, end, data[true_dataframe])
            identified_data = data[true_dataframe].take([end], axis=0)
            identified_data["Truth"] = verify(
                data[true_dataframe].take([end], axis=0), verify_check
            )
            print("\tChecking against:", input_strings[false_dataframe])
            # itterates through every line in the IP address in the same way as before
            for j in data[false_dataframe][end + 1 :].index:
                try:
                    identified_data, verified_data, verify_check = update_variables(
                        data[false_dataframe].take([j], axis=0),
                        identified_data,
                        verified_data,
                        verify_check,
                    )
                except:
                    print("\t\tline:", j)
                    total_errors += 1
                    continue
                current_test = test(identified_data)
                if current_test:
                    total_true += 1
                else:
                    total_false += 1
                if previous_test != current_test:
                    if current_test:
                        print("\tTrue from: ", j)
                    else:
                        print("\tTo: ", j)
                    previous_test = current_test
    print("False positives:", total_true, "/ 0")
    print("True Negatives:", total_false, "/", total_true + total_false + total_errors)
    print("Errors:", total_errors)
