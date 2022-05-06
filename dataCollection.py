import datetime
import subprocess
from trace import traceRoute, GetTTL


IPADR = [
    "8.8.8.8",
    "yahoo.com",
    "google.com",
    "firefox.com",
    "miniclip.com"]

def getData(target):
    output = str(datetime.datetime.now().strftime("%x")) + " " + str(datetime.datetime.now().strftime("%X"))+ "\t" + traceRoute(target) + "\t" + str(GetTTL(target))
    return output

for target in IPADR:
    with open("./Outputs/" + target + ".txt", "a") as this:
        this.write(getData(target) + "\n")
    



