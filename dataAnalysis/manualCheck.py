from resources import parse_data, initialize, verify, test, create_check
import pandas as pd
import json


with open("Input.json", "r") as input_file:
    input_strings = json.load(input_file)

start = 0
end = 50
size = 50
data = []
for i in input_strings:
    print("Parsing:", i)
    data.append(parse_data(i))
# print(data[0])
for i in range(len(data)):
    print("\nCalculating:", input_strings[i])
    verified_data, verify_check = initialize(start, end, data[i])
    identified_data = pd.DataFrame(
        [
            [
                data[i].at[end, "Traceroute"],
                data[i].at[end, "Delay"],
                verify(data[i].loc[end], verify_check),
            ]
        ],
        columns=["Traceroute", "Delay", "Truth"],
    )

    previous_test = True
    total_true = 0
    total_false = 0
    for j in data[i][end + 1 :].index:
        try:
            temp = pd.DataFrame(
                [
                    [
                        data[i].loc[j, "Traceroute"],
                        data[i].loc[j, "Delay"],
                        verify(data[i].loc[j], verify_check),
                    ]
                ],
                columns=["Traceroute", "Delay", "Truth"],
            )
        except:
            print("Error at", input_strings[i], "on line", j)
            print(data[i].loc[j])
        identified_data = pd.concat([identified_data, temp], ignore_index=True)
        if len(identified_data) >= size:
            if identified_data.loc[len(identified_data) - 1, "Truth"]:
                try:
                    temp = pd.DataFrame(
                        [
                            [
                                identified_data.loc[
                                    len(identified_data) - 1, "Traceroute"
                                ],
                                identified_data.loc[len(identified_data) - 1, "Delay"],
                            ]
                        ],
                        columns=["Traceroute", "Delay"],
                    )
                    verified_data = pd.concat(
                        [verified_data, temp],
                        ignore_index=True,
                    )
                except:
                    print("Something's broken:")
                verified_data = verified_data.drop(0, axis=0)
            identified_data = identified_data.drop(0, axis=0)
            verify_check = create_check(identified_data)
        current_test = test(identified_data)
        if current_test:
            total_true += 1
        else:
            total_false += 1
        if previous_test != current_test:
            if previous_test:
                print("False from: ", j)
            else:
                print("To: ", j)
    # except:
    #     print("its just not working")
    print("True:", total_true, "/", total_true + total_false)
    print("Flase:", total_false, "/ 0")
    for k in range(len(data)):
        if i == k:
            continue
        print("\tChecking:", input_strings[k])
        total_true = 0
        total_false = 0
        for l in data[k].index:
            try:
                temp = pd.DataFrame(
                    [
                        [
                            data[k].loc[l, "Traceroute"],
                            data[k].loc[l, "Delay"],
                            verify(data[k].loc[l], verify_check),
                        ]
                    ],
                    columns=["Traceroute", "Delay", "Truth"],
                )
            except:
                print("\tError at", input_strings[k], "on line", l)
                print("\t", data[k].loc[l])
            identified_data = pd.concat([identified_data, temp], ignore_index=True)
            if len(identified_data) >= size:
                if identified_data.loc[len(identified_data) - 1, "Truth"]:
                    try:
                        temp = pd.DataFrame(
                            [
                                [
                                    identified_data.loc[
                                        len(identified_data) - 1, "Traceroute"
                                    ],
                                    identified_data.loc[
                                        len(identified_data) - 1, "Delay"
                                    ],
                                ]
                            ],
                            columns=["Traceroute", "Delay"],
                        )
                        verified_data = pd.concat(
                            [verified_data, temp],
                            ignore_index=True,
                        )
                    except:
                        print("\tSomething's broken:")
                    verified_data = verified_data.drop(0, axis=0)
                identified_data = identified_data.drop(0, axis=0)
                verify_check = create_check(identified_data)
            current_test = test(identified_data)
            if current_test:
                total_true += 1
            else:
                total_false += 1
        print("\tTrue:", total_true, "/ 0")
        print("\tFlase:", total_false, "/", total_true + total_false)
