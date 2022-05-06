import time
import os
from trace import getData


IPADR = ["128.187.112.26"]


if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    print("finished 1 traceroute")
    time.sleep(60 * 10)
