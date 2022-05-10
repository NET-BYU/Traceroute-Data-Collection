import time
import os
from trace import getData


IPADR = ["byu.edu", "72.160.10.9", "97.117.140.93", "136.36.62.167", "76.8.213.221"]


if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    time.sleep(60 * 10)
