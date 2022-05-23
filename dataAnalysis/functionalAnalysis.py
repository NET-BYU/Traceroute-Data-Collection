import time


class trustedIPAddresses:
    def __init__(self):
        trusted_list = ["Hi", "By"]

    def build_trusted_list(self, data):
        pass

    def check_new_data(self):
        pass

    def clean_old_data(self):
        pass

    def trusted_list_to_string(self):
        print(self.trusted_list)


trusted = trustedIPAddresses()
with open("Outputs/byu.edu.txt") as input_file:
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

        trusted.build_trusted_list(input_data)
        trusted.trusted_list_to_string
        time.sleep(10)
