import subprocess
from trace import getData


IPADR = ["8.8.8.8", "yahoo.com", "google.com", "firefox.com", ""]


for target in IPADR:
    with open("./Outputs/" + target + ".txt", "a") as this:
        this.write(getData(target) + "\n")
