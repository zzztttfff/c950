# Zachary Finegan 001122345


import csv


class HashTable:
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kvp in bucket_list:
            if kvp[0] == key:
                kvp[1] = item
                return True
        kvp = [key, item]
        bucket_list.append(kvp)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kvp in bucket_list:
            if kvp[0] == key:
                return kvp[1]
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kvp in bucket_list:
            if kvp[0] == key:
                bucket_list.remove([kvp[0], kvp[1]])

    def __repr__(self):
        for bucket in self.table:
            for item in bucket:
                print(item[1])


class Package:
    def __init__(self, pkg_id, address, city, state, zip_code, dd, mass, notes):
        self.pkg_id = pkg_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.dd = dd
        self.mass = mass
        self.notes = notes

    def __str__(self):
        if self.notes != '':
            return f"ID: {self.pkg_id}, Address: {self.address}, {self.city}, {self.state} {self.zip_code}; Delivery " \
                   f"Deadline: {self.dd}; Mass: {self.mass}kg; Special Notes: {self.notes}."
        else:
            return f"ID: {self.pkg_id}, Address: {self.address}, {self.city}, {self.state} {self.zip_code}; Delivery " \
                   f"Deadline: {self.dd}; Mass: {self.mass}kg"


class Truck:
    def __init__(self):
        self.inventory = []

    def load_special(self):
        # self.inventory.append(pkg_id)
        for bucket in myHash.table:
            for pkg in bucket:
                for data in pkg:
                    if type(data) != type('string'):
                        # MANUALLY LOADS SPECIAL NOTED PACKAGES
                        if "Can only be on truck 2" in str(data):
                            truck2.inventory.append(data)
                        if int(data.pkg_id) in {13, 14, 15, 16, 19, 20}:
                            truck2.inventory.append(data)

        for pkg in self.inventory:
            pkg_in_truck = pkg.pkg_id
            for bucket in myHash.table:
                for index, item in enumerate(bucket):
                    if item[0] == pkg_in_truck:
                        bucket.pop(index)

    def load(self, pkg_id):
        # self.inventory.append(pkg_id)
        for bucket in myHash.table:
            for pkg in bucket:
                for data in pkg:
                    print(data)

        for pkg in self.inventory:
            pkg_in_truck = pkg.pkg_id
            for bucket in myHash.table:
                for index, item in enumerate(bucket):
                    if item[0] == pkg_in_truck:
                        bucket.pop(index)

    # def begin_route(self, location):
    #     print(location)

    def __repr_id__(self):
        return f"Packages: {self.inventory[0].pkg_id}, " + ", ".join(
            [f"{x.pkg_id}" for x in self.inventory[1:len(self.inventory) - 1]]) + " ".join(
            [f", {self.inventory[len(self.inventory) - 1].pkg_id}"])

    def __repr_address__(self):
        return f"Addresses: \nID {self.inventory[0].pkg_id}: {self.inventory[0].address}\n" + "".join(
            [f"ID {x.pkg_id}: {x.address}\n" for x in self.inventory[1:len(self.inventory) - 1]]) + "".join(
            [f"ID {self.inventory[len(self.inventory) - 1].pkg_id}: {self.inventory[len(self.inventory) - 1].address}"])


# def nearest_neighbor():
#     # ADD TO TRUCK2 PKGS @ LOCATIONS CLOSEST TO CURRENTLY LOADED PACKAGES
#     # FIND WHICH PACKAGES ARE CLOSEST TO THE ONES CURRENTLY LOADED
#     # DO THIS BY FINDING ADDRESSES OF CURRENTLY LOADED PACKAGES:
#     # print("Truck 2", truck2.__repr_address__())
#     # THEN FIND THE DISTANCES TO ADDRESSES OF NON-LOADED PACKAGES
#     # FIND CLOSEST LOCATION VIA DISTANCE TABLE:
#     # ITERATE CURRENT PACKAGE ADDRESS AGAINST ALL OTHER ADDRESSES
#     # CHOOSE THE MINIMUM DISTANCE. CLOSEST NEIGHBOR ALGORITHM
#     row = 4
#     col = 0
#     # for pkg in truck2.inventory:
#     #     for index, item in enumerate(dist_table[0]):
#     #         if pkg.address in item:
#     #             col = item
#     #             print(col, ' index:', index)
#     #             row = index
#     #         print(pkg.address, 'is ',dist_table[row][2], 'miles from ', dist_table[2][row-1])
#
#     for i in range()
#
#     # THE ABOVE INDICATES THE COLUMN (AND ITS CORRESPONDING INDEX) THAT WE WILL COMPARE AGAINST
#     print()
#     print('heya', dist_table[row][3])
#     # NOW ITERATE THRU ALL ROWS TO FIND SHORTEST DISTANCE
#
#     # LOAD THE CLOSEST PACKAGES UNTIL TRUCK INVENTORY IS FILLED
#     # THEN LOAD TRUCK 1 WITH ALL OTHER VIABLE PACKAGES WITH CLOSE NEIGHBORS
#     # ONE OF THE TRUCKS WILL REFILL WHEN CLOSE TO HUB

# Find and deliver package closest to hub
def nearest_neighbor():
    # PACKAGES THAT HAVE YET TO BE LOADED
    pkgs_at_hub = []
    for pkg in myHash.table:
        for item in pkg:
            pkgs_at_hub.append(item[1])

    # DESTINATIONS FOR UNLOADED PACKAGES
    # hub_pkg_destinations = []
    # hub_pkg_destinations.append(pkg.address)

    min_dist = 10
    for dest in dist_table:
        # hub_pkg_destinations.append(pkg.address)
        for pkg in pkgs_at_hub:
            if pkg.address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < min_dist:
                    min_dist = dist_to_hub
    print(min_dist)

    # For pkg in pkgs_at_hub:
    # Find dest from dist_table,
    # Find dest distance from hub
    # After all iterations, determine shortest distance from hub
    # The above pkg will be first.
    # Then find shortest distance from there to find second pkg
    # Continue...


def load_package_file(file):
    with open(file) as pkg_csv:
        reader = csv.reader(pkg_csv, delimiter=',')
        line_num = 0
        for row in pkg_csv:
            if line_num < 2:
                line_num += 1
            else:
                for pkg in reader:
                    if len(pkg) == 8:
                        pkg_id = pkg[0]
                        address = pkg[1]
                        city = pkg[2]
                        state = pkg[3]
                        zip_code = pkg[4]
                        dd = pkg[5]
                        mass = pkg[6]
                        notes = pkg[7]
                        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes)
                    else:
                        pkg_id = pkg[0]
                        address = pkg[1]
                        city = pkg[2]
                        state = pkg[3]
                        zip_code = pkg[4]
                        dd = pkg[5]
                        mass = pkg[6]
                        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes='')

                    myHash.insert(pkg_id, package)
        # for bucket in myHash.table:
        #     for pkg in bucket:
        #         for data in pkg:
        #             if type(data) != type('string'):
        #                 print(data)
        # print('\n')


def load_dist_file(file):
    with open(file) as dist_csv:
        reader = csv.reader(dist_csv, delimiter=',')
        arr = [[]]

        for row in reader:
            if len(arr) == 1:
                arr.insert(0, row)
            else:
                arr.insert(len(arr) - 1, row)
        del arr[len(arr) - 1]
        # for element in arr:
        # print(element)
        # print(arr[2][0], arr[2][1], ' is ', arr[2][2], ' miles from ', arr[0][2])
        # print()
        return arr


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
dist_table = load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")
truck1 = Truck()
truck2 = Truck()
truck2.load_special()
nearest_neighbor()  # EVENTUALLY THIS CAN TAKE AN ARGUMENT TO MAKE PROGRAM SELF-ADJUSTING
