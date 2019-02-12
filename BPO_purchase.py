import sqlite3
from prices import amarr_price_avg, base_price
import math
import csv
from tqdm import tqdm

conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
cur = conn.cursor()
# Laser Physics: 20413
# Mechanical Engineering: 20424
cur.execute("SELECT typeID FROM industryActivityMaterials WHERE materialTypeID = 20413")
dc_laser = cur.fetchall()
dc_laser = [a[0] for a in dc_laser]

cur.execute("SELECT typeID FROM industryActivityMaterials WHERE materialTypeID = 20424")
dc_mecheng = cur.fetchall()
dc_mecheng = [a[0] for a in dc_mecheng]

BPOs = list(set(dc_laser) & set(dc_mecheng))
BPOs = tuple(BPOs)


cur.execute("SELECT typeID, productTypeID FROM industryActivityProducts WHERE activityID == 8 AND typeID IN {}".format(BPOs))
BPCs = cur.fetchall()
BPCs = dict(BPCs)
BPCs = list(BPCs.values())

class BPOcost:

    def __init__(self, typeID, mat_research = 0.93, batch_size = 10, system_index = 0.01, tax_rate = 0.05):
        self.typeID = typeID
        self.mat_research = mat_research
        self.batch_size = batch_size
        self.system_index = system_index
        self.tax_rate = tax_rate

    def add_originBPO(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT typeID FROM industryActivityProducts WHERE activityID = 8 AND productTypeID = " + str(self.typeID))
        self.originTypeID = cur.fetchall()[0][0]

    def add_outputItem(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT productTypeID FROM industryActivityProducts WHERE activityID = 1 AND typeID = " + str(self.typeID))
        self.outputItem = cur.fetchall()[0][0]


    def add_name(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT typeName FROM invTypes WHERE typeID = " + str(self.typeID))
        self.name = cur.fetchall()[0][0]

    def add_t2mats(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE typeID = " + str(self.typeID))
        self.t2mats = dict(cur.fetchall())

        cur.execute("SELECT productTypeID FROM industryActivityProducts WHERE activityID = 1 AND typeID = " + str(self.originTypeID))
        self.t1ProductID = cur.fetchall()[0][0]

        del self.t2mats[self.t1ProductID]

        for key in self.t2mats:
            self.t2mats[key] *= self.batch_size

    def add_t1mats(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE activityID = 1 AND typeID = " + str(self.originTypeID))
        self.t1mats = dict(cur.fetchall())

        for key in self.t1mats:
            self.t1mats[key] *= self.batch_size

    def cost_t1mats(self):

        # Look up yesterdays average prices in Amarr for the t1 product, adjusted for the assumed materials
        # research modifier on the t1 BPO (default 7%)
        t1cost = list()

        for key, value in self.t1mats.items():
            amarr_price = amarr_price_avg(key) * (value * self.mat_research)
            t1cost.append(amarr_price)

        self.t1cost = round(sum(t1cost))

    def cost_t2mats(self):

        # Look up yesterdays average prices in Amarr for the t1 product, adjusted for the assumed materials
        # research modifier on the t1 BPO (default 7%)
        t2cost = list()

        for key, value in self.t2mats.items():
            amarr_price = amarr_price_avg(key) * math.ceil((value * self.mat_research))
            t2cost.append(amarr_price)

        self.t2cost = round(sum(t2cost))

    def total_cost(self):

        self.cost = self.t1cost + self.t2cost

    def add_price(self):

        amarr_sale_price, self.total_volume = amarr_price_avg(self.outputItem, return_volume=True)
        if amarr_sale_price is None:
            self.price = None
        else:
            self.price = round(amarr_sale_price * self.batch_size)

    def calc_prod_cost(self):

        b_price = base_price(self.outputItem)

        self.prod_cost = round(((b_price * self.batch_size) * self.system_index) * (1 + self.tax_rate))


BPC_obj = dict()
for bpc in BPCs:
    BPC_obj[bpc] = BPOcost(typeID=bpc)

for key, value in tqdm(BPC_obj.items()):
    value.add_name()
    value.add_originBPO()
    value.add_t2mats()
    value.add_t1mats()
    value.cost_t1mats()
    value.cost_t2mats()
    value.total_cost()
    value.add_outputItem()
    value.add_price()
    value.calc_prod_cost()

for key, value in list(BPC_obj.items()):

    if value.price is None:
        del BPC_obj[key]


header = ['typeID', 'name', 'material cost', 'production cost', 'total cost', 'sale price', 'profit', 'volume']

with open('Excel/bpos.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(header)
    for key, value in BPC_obj.items():
        row = [value.typeID,
               value.name,
               value.cost,
               value.prod_cost,
               value.cost + value.prod_cost,
               value.price,
               value.price - value.cost - value.prod_cost,
               value.total_volume]
        writer.writerow(row)