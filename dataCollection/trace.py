import subprocess
import time
import os


def traceRoute(target):
    p = subprocess.run(
        ["traceroute", target, "-I", "-n", "-q", "1"], stdout=subprocess.PIPE, text=True
    )
    return ParseTraceRouteOutput(p)


def ParseTraceRouteOutput(input):

    output = ""
    traceroute = []
    latency = []

    splitter = input.stdout.split("\n")
    del splitter[0]

    for x in splitter:
        x = x[4 : len(x)]

        if x == "":
            continue

        if x == "*":
            traceroute.append("*")
            latency.append("*")
        else:
            smallSplitter = x.split(" ")
            traceroute.append(smallSplitter[0])
            latency.append(smallSplitter[2])

    for x in traceroute:
        output = output + x + " "
    output = output[0 : len(output) - 2]
    output = output + "\t"

    for x in latency:
        output = output + x + " "
    output = output[0 : len(output) - 2]

    return output


def GetTTL(ip):
    result = os.popen("ping -c 1 " + ip).read()
    n = result.find("ttl=")
    if n >= 0:
        ttl = result[n + 4 :]
        n = ttl.find(" ")
        if n > 0:
            return int(ttl[:n])
    return -1


def getData(target):
    output = str(time.time()) + "\t" + str(GetTTL(target)) + "\t" + traceRoute(target)
    return output
