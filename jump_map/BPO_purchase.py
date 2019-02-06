import sqlite3

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

    def __init__(self, typeID):
        self.typeID = typeID

    def add_originBPO(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT productTypeID FROM industryActivityProducts WHERE activityID = 8 AND typeID = " + str(self.typeID))
        self.originTypeID = cur.fetchall()[0][0]

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
        self.t1ProductID = self.name = cur.fetchall()[0][0]

        del self.t2mats[self.t1ProductID]

    def add_t1mats(self):
        conn = sqlite3.connect("jump_map/sqlite-latest.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE activityID = 1 AND typeID = " + str(self.originTypeID))
        self.t1mats = dict(cur.fetchall())


a = BPOcost(typeID=784)
a.add_name()
a.add_originBPO()
a.add_t2mats()
a.add_t1mats()
