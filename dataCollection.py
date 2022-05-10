import time
import os
from trace import getData


IPADR = ["byu.edu", "97.117.140.93", "72.160.10.9"]


if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    time.sleep(60 * 10)
