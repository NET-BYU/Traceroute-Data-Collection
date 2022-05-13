import time
import os
from trace import getData
import sentry_sdk

sentry_sdk.init(
    "https://2fbbdb1dd9ce4472853649ed421fca5f@o1245655.ingest.sentry.io/6402901",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


IPADR = [
    "byu.edu",
    "136.36.62.167",
    "76.8.213.221",
    "97.117.140.93",
    "72.160.10.9",
    "75.174.31.107",
    "69.73.60.141",
]


if not os.path.exists("./Outputs"):
    os.makedirs("./Outputs")

while True:
    for target in IPADR:
        with open("./Outputs/" + target + ".txt", "a") as this:
            this.write(getData(target) + "\n")
    time.sleep(60 * 10)
