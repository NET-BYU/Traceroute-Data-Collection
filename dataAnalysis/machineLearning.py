from operator import index
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import os


# Making sure that the output file even exists
if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

    # Will be used to check to make sure that the inputs we are getting are the type we expect
random_list = ["a", "b"]

# IPADR stands for IP Addresses and is a list of all of the IP Addresses that ./dataCollection/dataCollection.py has been collecting data for
with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)


def parse_data(target):
    # Takes the data from a txt file and parses it into a pandas dataframe in a way that will be recognizable by the machine learning algorithm

    data = pd.read_csv(
        f"Outputs/{target}.txt",
        sep="\t",
        parse_dates=True,
        infer_datetime_format=True,
        names=["Time", "TTL", "Traceroute", "Delay", "Latency"],
    )

    del data["Latency"]
    del data["Time"]
    data["Traceroute"] = data["Traceroute"].str.split(" ")
    data["Delay"] = data["Delay"].str.split(" ")

    for index in data.index:
        if type(data.loc[index, "Traceroute"]) == type(random_list):

            # I decided that we don't want to include any instances of * into the data. This is in an effort to provide more specificity to the data
            while True:
                try:
                    data.loc[index, "Traceroute"].remove("*")
                except:
                    break

                # We need a consistant sized array to pass into sklearn, so i decided that the last 5 nodes in the traceroute's path. I belived this would be sort enough almost any route would have then but long enough to get accurate results
            if len(data.loc[index, "Traceroute"]) > 5:
                reduced_traceroute = data.loc[index, "Traceroute"][-5:]
            else:
                reduced_traceroute = data.loc[index, "Traceroute"]
            del data.loc[index, "Traceroute"][0:]

            # This takes the IP addresses from the ["x.x.x.x", "x.x.x.x"] notation and replaces it with [x, x, x, x,  x, x, x, x]
            for ip in reduced_traceroute:
                broken_ip = ip.split(".")
                for individual_ip in broken_ip:
                    if individual_ip != "*" and individual_ip != "":
                        data.loc[index, "Traceroute"].append(float(individual_ip))
                    else:
                        data.loc[index, "Traceroute"].append(0.0)
                # In the event that there is less than 5 traceroutes we fill the rest with zero's in order to keep the size of the array consistant
            while len(data.loc[index, "Traceroute"]) < 20:
                data.loc[index, "Traceroute"].append(-1.0)
        else:
            print(f"Error at line {index} at {target}.txt")
            del data.loc[index, "Traceroute"][0:]
            data.drop(index, axis=0)

            # This takes the last 5 delay values and appends them to "Traceroute"
        if (
            type(data.loc[index, "Delay"]) == type(random_list)
            and len(data.loc[index, "Delay"]) >= 5
        ):
            reduced_delay = data.loc[index, "Delay"][-5:]
            del data.loc[index, "Delay"][0:]
            for delay in reduced_delay:
                if delay != "*" and delay != "":
                    data.loc[index, "Delay"].append(float(delay))
                    data.loc[index, "Traceroute"].append(float(delay))
                else:
                    data.loc[index, "Traceroute"].append(0.0)

        if type(data.loc[index, "Traceroute"]) == type(random_list):
            if data.loc[index, "TTL"] != "*":
                data.loc[index, "Traceroute"].append(float(data.loc[index, "TTL"]))
            else:
                data.loc[index, "Traceroute"].append(0.0)

            # In the event that something goes wrong this fills the array so that it is still a consitant size
        while len(data.loc[index, "Traceroute"]) < 26:
            data.loc[index, "Traceroute"].append(0.0)

    data = data.drop(["TTL", "Delay"], axis=1)
    return data


def add_identifier(data, identifier):
    output = data
    value = [identifier for x in range(len(data))]
    output["Correct"] = value
    return output


def MLIP(array, length):
    # Defines the first dataset in the array as true and the rest as false
    # Outputs in a single dataset an even ammount of true and false data
    # The false data is a random sample from all the available false data cut down to the same length of true data

    for i in range(len(array)):
        if i == 0:
            good_data = add_identifier(array[i], True)
        else:
            array[i] = add_identifier(array[i], False)
            if i == 1:
                output = array[i]
            else:
                output = pd.concat([output, array[i]], ignore_index=True)
    output = shuffle(output)
    output.reset_index(inplace=True, drop=True)
    if len(array[0]) > length:
        array[0] = array[0][:length]
    if len(output) > len(array[0]):
        output = output[: len(array[0])]
    output = pd.concat([output, array[0]], ignore_index=True)
    output = shuffle(output)
    output.reset_index(inplace=True, drop=True)
    return output


def inline(array, length, percent):
    # Takes the first {length} of data from the first dataset in array and sets it to True
    # Then it takes {percent * length} number of data points randomly from all of the other datasets from the array and sets them to False
    # Randomizes the dataset and returns it in the same format as sklearn's train_test_split function
    for i in range(len(array)):
        if i == 0:
            good_data = add_identifier(array[i], True)
        else:
            array[i] = add_identifier(array[i], False)
            if i == 1:
                bad_data = array[i]
            else:
                bad_data = pd.concat([bad_data, array[i]], ignore_index=True)

    bad_data = shuffle(bad_data)
    bad_data.reset_index(inplace=True, drop=True)

    train = pd.concat(
        [bad_data[: int(length * percent)], good_data[:length]], ignore_index=True
    )
    test = pd.concat(
        [bad_data[int(length * percent) :], good_data[length:]], ignore_index=True
    )
    X_train = train["Traceroute"]
    y_train = train["Correct"]
    X_test = test["Traceroute"]
    y_test = test["Correct"]

    return X_train, X_test, y_train, y_test


initial_good_data = IPADR[0]
print(f"Testing {initial_good_data}.txt")
training_data = [initial_good_data]
false_test = []
for i in IPADR:
    if i in training_data:
        continue
    if len(training_data) < 7:
        training_data.append(i)
    else:
        if len(false_test) == 0:
            false_test = add_identifier(parse_data(i), False)
        else:
            false_test = pd.concat(
                [false_test, add_identifier(parse_data(i), False)],
                ignore_index=True,
            )
for i in range(len(training_data)):
    training_data[i] = parse_data(training_data[i])

x = 0
for i in training_data[0]["Traceroute"]:
    x += 1
    try:
        if len(i) != 26:
            print(f"line: {x}\n{len(i)}: {i}")
    except:
        print("TypeError: object of type 'float' has no len()", i, "line:", x)

good_data = 30
X_train, X_test, y_train, y_test = inline(training_data, good_data, 1)
X_train = X_train.to_list()
y_train = y_train.to_list()
X_test = X_test.to_list()
y_test = y_test.to_list()

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)
pred_rfc = rfc.predict(X_test)

print(
    f"Training data: good-{good_data}, bad-{len(X_train) - good_data}, total-{len(X_train)}"
)
print(f"Testing data: {len(X_test)}")
print("Accuracy:", accuracy_score(y_test, pred_rfc))
print(classification_report(y_test, pred_rfc))

# testing false data the algorith wasn't trained on

false_test_X = false_test["Traceroute"]
false_test_y = false_test["Correct"]

X_test = sc.transform(false_test_X.to_list())
pred_rfc = rfc.predict(X_test)

print(f"\n\nFalse untrained data: {len(false_test_X)}")
print("Accuracy:", accuracy_score(false_test_y, pred_rfc))
print(classification_report(false_test_y, pred_rfc))
