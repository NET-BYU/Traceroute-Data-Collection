import subprocess
import re


import datetime
from threading import currentThread

from trace import traceRoute, GetTTL


data = {
    "IPADR1": [ 
        "8.8.8.8",
        ["2022-5-3 13:54", [], -1],
        ["2022-5-3 13:54", [], -1]],
    "IPADR2": [ 
        "yahoo.com",
        ["2022-5-3 13:54", [], -1],
        ["2022-5-3 13:54", [], -1]
    ]
}

data["IPADR1"][1][0] = datetime.datetime.now()
data["IPADR1"][1][1] = traceRoute(data["IPADR1"][0])
data["IPADR1"][1][2] = GetTTL(data["IPADR1"][0])

print("\nTime:", data["IPADR1"][1][0], "\n")
print("Traceroute:")
for x in data["IPADR1"][1][1]:
    print(x)
print("\nTTL:", data["IPADR1"][1][2])







p = subprocess.run(["traceroute", data["IPADR1"][0]], stdout=subprocess.PIPE, text=True)
# res=p.communicate()[0]
# if p.returncode > 0:
#     print('server error')
# else:
#     pattern = re.compile('TTL=\d*')
#     print(pattern.search(str(res)).group())
print(p.stdout)