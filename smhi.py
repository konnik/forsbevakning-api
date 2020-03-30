
import requests
import time


def fetch_data(subid):
    url = "http://vattenwebb.smhi.se/hydronu/data/point?subid={}".format(subid)

    res = requests.get(url)
    chartData = res.json()["chartData"]

    data = {
        "subid": chartData["subid"],
        "mq": chartData["mq"],
        "mlq": chartData["mlq"],
        "mhq": chartData["mhq"],
        "hindcast": chartData["hindcast"]["data"],
        "forecast": chartData["forecast"]["data"]
    }

    return data
