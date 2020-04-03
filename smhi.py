
import requests
import time
from cachetools import cached, TTLCache
from threading import RLock
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

CACHE_MAX_ITEMS = 100
CACHE_TTL = 60*60 # enhet i sekunder

lock = RLock()

@cached(cache = TTLCache(CACHE_MAX_ITEMS,CACHE_TTL),lock = lock)
def fetch_data(subid):
    log.info("Laddar data för subid %s", subid)

    url = "http://vattenwebb.smhi.se/hydronu/data/point?subid={}".format(subid)

    res = requests.get(url)
    if res.status_code != 200:
        return None

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
