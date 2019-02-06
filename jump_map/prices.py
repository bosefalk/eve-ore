# Get mineral prices from eve swagger: https://esi.evetech.net/latest/#!/Market/get_markets_region_id_orders

import urllib.request
import json
import datetime

ID = 35

def amarr_price_now(ID):
    # Domain is region ID 10000043
    price_json = urllib.request.urlopen("https://esi.evetech.net/latest/markets/10000043/orders/?datasource=tranquility&order_type=sell&page=1&type_id=" + str(ID)).read()
    price_dict = json.loads(price_json)

    # Amarr has solarsystem ID 30002187

    price_dict = [dict for dict in price_dict if dict['system_id'] == 30002187]
    prices = [dict['price'] for dict in price_dict]
    min_price = min(prices)
    return(min_price)

def amarr_price_avg(ID):

    # Domain is region ID 10000043
    price_json = urllib.request.urlopen("https://esi.evetech.net/latest/markets/10000043/history/?datasource=tranquility&type_id=" + str(ID)).read()
    price_dict = json.loads(price_json)

    yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    yesterday_avg = [dict['average'] for dict in price_dict if dict['date'] == yesterday_str]

    while len(yesterday_avg) == 0:
        yesterday = yesterday - datetime.timedelta(days = 1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        yesterday_avg = [dict['average'] for dict in price_dict if dict['date'] == yesterday_str]

    return(yesterday_avg[0])

#
#
#
# price_json = urllib.request.urlopen("https://esi.evetech.net/latest/markets/prices/?datasource=tranquility").read()
#
#
#
# # Type IDs are from the sqlite-lastest.sqlite database, downloaded from https://www.fuzzwork.co.uk/dump/
#
# mineral_ids = {"Tritanium": 34,
#                "Pyerite": 35}
#
#
# l = list()
# types = [32774, 32780]
#
# l = [id_dict for id_dict in price_dict if id_dict['type_id'] in mineral_ids.values()]
#
# volume = 10000
# time_cost = 5,
# jump_time = 45)
#
# price_trit = urllib.request.urlopen("https://esi.evetech.net/latest/markets/10000065/orders/?datasource=tranquility&order_type=buy&page=1&type_id=35").read()
# price_trit = json.loads(price_trit)
#
# # Filter sales orders which can accept this volume of minerals
# price_trit = [l for l in price_trit if (volume <= l['volume_remain']) and (volume >= l['min_volume'])]
#
#
# calc_penalized_value(time_cost, jump_time, volume):
#     needed_jumps = jumps - range
#     if self.needed_jumps < 0:
#         self.needed_jumps = 0
#
#     self.value = volume * self.price
#
#     self.jump_cost = self.needed_jumps * ((time_cost * 1000000 / 3600) * jump_time)
#
#     self.penalized_value = self.value - self.jump_cost
#
#
#
# i['type_id'] is