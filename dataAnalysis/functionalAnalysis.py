import time
import numpy as np


class Trusted:
    def __init__(self):
        self.list_IP = []
        self.list_Latency = []
        self.data_retention = (
            100  # The ammount of time that data is kept in the list in minutes
        )
        self.data_retention = (
            self.data_retention * 60
        )  # Converting minutes to epoch time

    def stars(self, data):
        for i in data:
            if i != "*":
                return False
        return True

    def build_list(self, data):
        """Store trusted information to referance later"""
        for index in range(len(data[2])):

            # stores the IP Address'
            IP_value = [data[0], data[3][index]]
            if (len(self.list_IP) - 1) < index:
                self.list_IP.append({data[2][index]: [IP_value]})

            if data[2][index] in self.list_IP[index]:
                self.list_IP[index][data[2][index]].append(IP_value)
            else:
                self.list_IP[index][data[2][index]] = [IP_value]

            # stores the latency data
            if data[3][index] == "*":
                latency_value = -1
                if len(self.list_Latency) - 1 < index:
                    self.list_Latency.append([latency_value, latency_value])
                    continue
            else:
                latency_value = float(data[3][index])
            if len(self.list_Latency) - 1 < index:
                self.list_Latency.append([latency_value, latency_value])
                continue

            if self.list_Latency[index][0] > latency_value:
                self.list_Latency[index][0] = latency_value
            elif self.list_Latency[index][1] < latency_value:
                self.list_Latency[index][1] = latency_value

            # Checks if the rest are stars, if they are stop
            if data[2][index] == "*":
                if self.stars(data[2][index:]):
                    data[2] = data[2][:index]
                    data[3] = data[3][:index]
                    break

    def pass_or_fail(self, IP_score, latency_score, length):
        if ((IP_score / length) > 0.8) or ((IP_score / length) > 0.8):
            return True
        else:
            return False

    def check_new_data(self, data):
        IP_score = 0
        latency_score = 0
        for index in range(len(data[2])):
            if (len(self.list_IP) - 1) < index:
                continue

            if data[2][index] in self.list_IP[index]:
                IP_score += 1

            if data[3][index] == "*":
                latency_value = -1
            else:
                latency_value = float(data[3][index])
            if (
                self.list_Latency[index][0] >= latency_value
                and self.list_Latency[index][1] <= latency_value
            ):
                latency_score += 1
            if data[2][index] == "*":
                if self.stars(data[2][index:]):
                    if len(data[2]) > index:
                        data[2] = data[2][: index + 1]
                        data[3] = data[3][: index + 1]
                    break

        if self.pass_or_fail(IP_score, latency_score, len(data[2])):
            self.build_list(data)
            self.clean_old_data(data[0])
        return self.pass_or_fail(IP_score, latency_score, len(data[2]))

    def clean_old_data(self, time):
        for hop in self.list_IP:
            if len(hop):
                for IP in hop:
                    if hop[IP] and hop[IP][0]:
                        # self.to_string()
                        while float(hop[IP][0][0]) < (
                            float(time) - int(self.data_retention)
                        ):
                            del hop[IP][0]
                            # print("\n\n\nindex = ", IP, " + ", hop[IP], "\n\n\n")
                            if not hop[IP]:
                                # del hop[IP]
                                break

    def to_string(self):
        the_array = np.array(self.list_IP)
        print(the_array)
        del the_array


trusted = Trusted()
with open("Outputs/136.36.62.167.txt") as input_file:
    for index, input_line in enumerate(input_file):
        try:
            input_line = input_line.strip()
        except:
            pass

        input_data = input_line.split("\t")
        input_data[2] = input_data[2].split(" ")
        while True:
            try:
                input_data[2].remove("")
            except:
                break

        input_data[3] = input_data[3].split(" ")
        while True:
            try:
                input_data[3].remove("")
            except:
                break
        if index < 100:
            trusted.build_list(input_data)
            # print(trusted.list_Latency)
        else:
            if trusted.check_new_data(input_data):
                pass
                # print("line", str(index + 1), "trusted")
            else:
                pass
                print("INTRUDER ON LINE ", str(index + 1))
                time.sleep(0.1)
