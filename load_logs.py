import csv
from collections import Counter
import pickle

# bid == TRUE means it's a buy order

# jumps is the number of jumps, then range is the range so potentially could do jumps-range number of jumps
# But range can be -1 which means station so that should be changed to 0

# volRemaining and minVolume should be greater than sell volume


class marketLog:

    def __init__(self, orderID, price, volRemaining, minVolume, system_id, range, isBuyOrder):
        self.orderID = orderID
        self.price = price
        self.volRemaining = volRemaining
        self.minVolume = minVolume
        if range == -1:
            self.range = 0
        else:
            self.range = range
        self.system_id = system_id
        self.isBuyorder = isBuyOrder

    def addJumps(self, jumps):
        self.jumps = jumps

    def calcJumps(self, current_system_id, jumpMap):
        self.jumps = jumpMap.findJumps(current_system_id, self.system_id)

    def canSell_volume(self, volume):

        if self.isBuyorder == "False":
            self.canSell = False
            return

        if (volume <= self.volRemaining) & (volume >= self.minVolume):
            self.canSell = True
            return
        else:
            self.canSell = False
            return

    def calc_penalized_value(self, time_cost, jump_time, volume):
        self.needed_jumps = self.jumps - self.range
        if self.needed_jumps < 0:
            self.needed_jumps = 0

        self.value = volume * self.price

        self.jump_cost = self.needed_jumps * ((time_cost * 1000000 / 3600) * jump_time)

        self.penalized_value = self.value - self.jump_cost

# time_cost is million isk / hour made mining
# jump_time is time in seconds per jump in a system
def find_top5(filename = 'market/Kor-Azor-marketgen-2019.01.22 105804.txt',
              vol_to_sell = 200000,
              time_cost = 0.75,
              jump_time = 45):

    market_list = []

    with open(filename, 'r') as f:
        next(f) # Skip first line with headers
        reader = csv.reader(f)
        for row in reader:
            market_list.append(marketLog(orderID=row[4],
                                     price=float(row[0]),
                                     volRemaining=int(float(row[1])), # . and , as decimals not behaving nicely
                                     minVolume=int(row[6]),
                                     range=int(row[3]),
                                      isBuyOrder=row[7]
                                      ))
            # Need to update with jumps and system Id

    # Apply the canSell_volume function to each element and keep those which we can sell to
    for obj in market_list:
        obj.canSell_volume(volume = market_vol)

    market_list = [obj for obj in market_list if obj.canSell is True]

    for obj in market_list:
        obj.calc_penalized_value(volume=vol_to_sell, time_cost=time_cost, jump_time=jump_time)


    market_dict = dict()

    for obj in market_list:
        market_dict[obj] = obj.penalized_value

    market_top5 = Counter(market_dict).most_common(5)

    market_top5 = [i[0] for i in market_top5]

    return(market_top5)


# Solar system table: https://developers.eveonline.com/resource/resources


vol_to_sell = 200000
time_cost = 6
jump_time = 45
current_system_id = '30005069'


price_trit = urllib.request.urlopen("https://esi.evetech.net/latest/markets/10000065/orders/?datasource=tranquility&order_type=buy&page=1&type_id=35").read()
price_trit = json.loads(price_trit)
market_list = list()
for item in price_trit:
    market_list.append(marketLog(orderID=item['order_id'],
                                 price=item['price'],
                                 volRemaining=item['volume_remain'],  # . and , as decimals not behaving nicely
                                 minVolume=item['min_volume'],
                                 system_id=item['system_id'],
                                 range=item['range'],
                                 isBuyOrder=item['is_buy_order']
                                 ))

for obj in market_list:
    obj.canSell_volume(volume = vol_to_sell)
market_list = [obj for obj in market_list if obj.canSell is True]

kor_azor_jump_map = pickle.load( open( "jump_map/jumpMap_KorAzor.pickle", "rb" ) )

for obj in market_list:
    obj.calcJumps('30005069', kor_azor_jump_map)
