from trace import traceRoute
data = {
    "IPADR1": [ 
        "google.com",
        ["2022-5-3 13:54", [], -1],
        ["2022-5-3 13:54", [], -1]],
    "IPADR2": [ 
        "yahoo.com",
        ["2022-5-3 13:54", [], -1],
        ["2022-5-3 13:54", [], -1]
    ]
}


data["IPADR1"][1][1] = traceRoute(data["IPADR1"][0])