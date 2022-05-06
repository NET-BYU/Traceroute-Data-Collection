import time
from trace import getData


IPADR = ["8.8.8.8", "yahoo.com", "google.com", "firefox.com"]


while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    print("finished 1 traceroute")
    time.sleep(60 * 10)
