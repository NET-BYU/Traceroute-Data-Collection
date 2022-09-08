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

for i in range(len(data)):
    print("\nCalculating:", input_strings[i])
    verified_data, verify_check = initialize(start, end, data[i])
    identified_data = data[i].take([end], axis=0)
    identified_data["Truth"] = verify(data[i].take([end], axis=0), verify_check)

    previous_test = True
    total_true = 0
    total_false = 0
    total_errors = 0
    for j in data[i][end + 1 :].index:
        try:
            identified_data, verified_data, verify_check = update_variables(
                data[i].take([j], axis=0), identified_data, verified_data, verify_check
            )
        except:
            print("Error at line:", j)
            total_errors += 1
            continue
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
    print("True:", total_true, "/", total_true + total_false)
    print("False:", total_false, "/ 0")
    print("Errors:", total_errors)
