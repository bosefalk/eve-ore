import sqlite3
from jump_map.prices import amarr_price_avg
import math

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

class BPOcost:

    def __init__(self, typeID, mat_research = 0.93):
        self.typeID = typeID
        self.mat_research = mat_research

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

    def add_t1mats(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE activityID = 1 AND typeID = " + str(self.originTypeID))
        self.t1mats = dict(cur.fetchall())

    def cost_t1mats(self, mat_research = 0.93):

        # Look up yesterdays average prices in Amarr for the t1 product, adjusted for the assumed materials
        # research modifier on the t1 BPO (default 7%)
        t1cost = list()

        for key, value in self.t1mats.items():
            amarr_price = amarr_price_avg(key) * (value * 0.93)
            t1cost.append(amarr_price)

        self.t1cost = round(sum(t1cost))

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

        amarr_sale_price = amarr_price_avg(self.outputItem)
        self.price = round(amarr_sale_price)

a = BPOcost(typeID=784)
a.add_name()
a.add_originBPO()
a.add_t2mats()
a.add_t1mats()
a.cost_t1mats()
a.cost_t2mats()
a.total_cost()
a.add_outputItem()
a.add_price()

print(a.cost)
print(a.price)
print(a.price - a.cost)