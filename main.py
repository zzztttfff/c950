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
        for self.bucket in self.table:
            for item in self.bucket:
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

    def begin_route(self, location):
        print(location)

    def __repr_id__(self):
        return f"Packages: {self.inventory[0].pkg_id}, " + ", ".join(
            [f"{x.pkg_id}" for x in self.inventory[1:len(self.inventory) - 1]]) + " ".join(
            [f", {self.inventory[len(self.inventory) - 1].pkg_id}"])
    def __repr_address__(self):
        return f"Addresses: \nID {self.inventory[0].pkg_id}: {self.inventory[0].address}\n" + "".join(
            [f"ID {x.pkg_id}: {x.address}\n" for x in self.inventory[1:len(self.inventory) - 1]]) + "".join(
            [f"ID {self.inventory[len(self.inventory) -1].pkg_id}: {self.inventory[len(self.inventory) - 1].address}"])


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


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")
truck1 = Truck()
truck2 = Truck()
truck2.load_special()

# ADD TO TRUCK2 PKGS @ LOCATIONS CLOSEST TO CURRENTLY LOADED PACKAGES
# FIND WHICH PACKAGES ARE CLOSEST TO THE ONES CURRENTLY LOADED
# DO THIS BY FINDING ADDRESSES OF CURRENTLY LOADED
print("Truck 2", truck2.__repr_address__())

# THEN FIND THE DISTANCES TO ADDRESSES OF NON-LOADED PACKAGES
# LOAD THE CLOSEST PACKAGES UNTIL TRUCK INVENTORY IS FILLED
# THEN LOAD TRUCK 1 WITH ALL OTHER VIABLE PACKAGES WITH CLOSE NEIGHBORS
# ONE OF THE TRUCKS WILL REFILL WHEN CLOSE TO HUB





