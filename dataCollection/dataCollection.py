import time
import os
from trace import getData
import sentry_sdk
import json

# sentry_sdk.init(
#     "https://2fbbdb1dd9ce4472853649ed421fca5f@o1245655.ingest.sentry.io/6402901",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
# )

with open("Input.json", "r") as input_file:
    IPADR = json.load(input_file)

if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    time.sleep(60 * 10)
