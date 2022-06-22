from sklearn.ensemble import RandomForestClassifier


with open("Outputs/76.8.213.221.txt") as input_file:
    total_data = []
    for index, input_line in enumerate(input_file):
        output = []
        try:
            input_line = input_line.strip()
        except:
            pass
        input_data = input_line.split("\t")

        output.append(input_data[1])

        input_data[2] = input_data[2].split(" ")
        while True:
            try:
                input_data[2].remove("")
            except:
                break

        output.append(len(input_data[2]))

        while True:
            try:
                input_data[2].remove("*")
            except:
                break

        for x in range(len(input_data[2]) - 5, len(input_data[2])):
            temp = input_data[2][x].split(".")
            for y in temp:
                output.append(y)

        input_data[3] = input_data[3].split(" ")
        while True:
            try:
                input_data[3].remove("")
            except:
                try:
                    input_data[3].remove("*")
                except:
                    break
        for x in range(len(input_data[3]) - 5, len(input_data[3])):
            output.append(input_data[3][x])
        # print(output)
        total_data.append(output)
        if index > 10:
            break
print(total_data)
