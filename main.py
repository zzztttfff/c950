# Zachary Finegan 001122345
import csv


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
                            if data not in truck2.inventory:
                                truck2.inventory.append(data)
                        if int(data.pkg_id) in {13, 14, 15, 16, 19, 20}:
                            if data not in truck2.inventory:
                                truck2.inventory.append(data)
        # REMOVES LOADED PKGS FROM myHash.table
        for pkg in self.inventory:
            pkg_in_truck = pkg.pkg_id
            for bucket in myHash.table:
                for index, item in enumerate(bucket):
                    if item[0] == pkg_in_truck:
                        bucket.pop(index)

    def load(self, pkg_to_load):
        if len(self.inventory) > 16:
            print('Too many packages in truck.')
            # dispatch truck
            # try loading other truck
            return 'Too many packages in truck.'

        # ADD TO TRUCK INVENTORY
        self.inventory.append(pkg_to_load)
        # for pkg in self.inventory:
        #     # if pkg_to_load not in pkg:
        #     self.inventory.append(pkg_to_load)

        # REMOVE FROM HUB
        for bucket in myHash.table:
            for pkg in bucket:
                if pkg[0] == pkg_to_load.pkg_id:
                    # print('load() pkg[0]: ', pkg[0])
                    return
        return

    def __repr_id__(self):
        return f"Packages: {self.inventory[0].pkg_id}, " + ", ".join(
            [f"{x.pkg_id}" for x in self.inventory[1:len(self.inventory) - 1]]) + " ".join(
            [f", {self.inventory[len(self.inventory) - 1].pkg_id}"])

    def __repr_address__(self):
        return f"Addresses: \nID {self.inventory[0].pkg_id}: {self.inventory[0].address}\n" + "".join(
            [f"ID {x.pkg_id}: {x.address}\n" for x in self.inventory[1:len(self.inventory) - 1]]) + "".join(
            [f"ID {self.inventory[len(self.inventory) - 1].pkg_id}: {self.inventory[len(self.inventory) - 1].address}"])


# Find and deliver package closest to hub
def stage_trucks():
    # SHOW PACKAGES THAT HAVE YET TO BE LOADED
    pkgs_at_hub = []
    for pkg in myHash.table:
        for item in pkg:
            pkgs_at_hub.append(item[1])

    # LOOK AT ALL POSSIBLE PKG LOCATIONS, DETERMINE WHICH SET HAS CLOSEST PKG TO HUB:
    # DETERMINE MIN DIST TO HUB FOR UNLOADED PACKAGES:
    unloaded_min_dist_from_hub = 100
    nearest_unloaded_pkg = Package
    for dest in dist_table:
        for pkg in pkgs_at_hub:
            if pkg.address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < unloaded_min_dist_from_hub:
                    unloaded_min_dist_from_hub = dist_to_hub
                    nearest_unloaded_pkg = pkg

    # DETERMINE MIN DIST TO HUB FOR TRUCK2 LOADED PACKAGES:
    t2loaded_min_dist_from_hub = 100
    nearest_t2_loaded_pkg = Package
    for dest in dist_table:
        for pkg in truck2.inventory:
            if pkg.address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < t2loaded_min_dist_from_hub:
                    t2loaded_min_dist_from_hub = dist_to_hub
                    nearest_t2_loaded_pkg = pkg

    # DETERMINE MIN DIST TO HUB FOR TRUCK1 LOADED PACKAGES:
    t1loaded_min_dist_from_hub = 100
    nearest_t1_loaded_pkg = Package
    for dest in dist_table:
        for pkg in truck1.inventory:
            if pkg.address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < t1loaded_min_dist_from_hub:
                    t1loaded_min_dist_from_hub = dist_to_hub
                    nearest_t1_loaded_pkg = pkg

    if t2loaded_min_dist_from_hub < t1loaded_min_dist_from_hub:
        loaded_min_dist_from_hub = t2loaded_min_dist_from_hub
        nearest_loaded_pkg = nearest_t2_loaded_pkg
    else:
        loaded_min_dist_from_hub = t1loaded_min_dist_from_hub
        nearest_loaded_pkg = nearest_t1_loaded_pkg

    if loaded_min_dist_from_hub < unloaded_min_dist_from_hub:
        min_dist_from_hub = loaded_min_dist_from_hub
        nearest_pkg_to_hub = nearest_loaded_pkg
    else:
        min_dist_from_hub = unloaded_min_dist_from_hub
        nearest_pkg_to_hub = nearest_unloaded_pkg

    t2count = 0
    for box in truck2.inventory:
        t2count += 1
    while t2count < 16:
        # truck2.load(nearest_pkg_to_hub)
        if nearest_pkg_to_hub not in truck2.inventory:
            truck2.inventory.append(nearest_pkg_to_hub)
        # REMOVE FROM unstaged_pkgs LIST:
        for thing in unstaged_pkgs:
            if thing[1] == nearest_pkg_to_hub:
                unstaged_pkgs.remove(thing)
        # IF PKG WAS AT HUB, REMOVE FROM pkgs_at_hub LIST:
        if nearest_pkg_to_hub in pkgs_at_hub:
            pkgs_at_hub.remove(nearest_pkg_to_hub)
        t2count += 1
        if len(unstaged_pkgs) < 40:
            current_location = nearest_pkg_to_hub.address
            current_pkg = nearest_pkg_to_hub
            # determine_next_pkg(current_pkg)
    if t2count == 16:
        t1count = 0
        for box in truck1.inventory:
            t1count += 1
        while t1count < 16:
            truck1.load(nearest_pkg_to_hub)
            # print('LOAD THE PACKAGES: nearest_pkg_to_hub: ', nearest_pkg_to_hub)
            t1count += 1
        if t1count == 16:
            print('dispatch trucks')
            return

    # # LOAD THE PACKAGES
    # for dest in dist_table:
    #     # HUB:
    #     for pkg in pkgs_at_hub:
    #         if pkg.address in dest[0]:
    #             if float(dest[2]) == min_dist_from_hub:
    #
    #                 t2count = 0
    #                 for box in truck2.inventory:
    #                     t2count += 1
    #                 while t2count < 16:
    #                     # truck2.load(nearest_pkg_to_hub)
    #                     truck2.inventory.append(nearest_pkg_to_hub)
    #                     # IF IT WAS AT HUB, THIS 'IF' REMOVES IT FROM HUB LIST:
    #                     if nearest_pkg_to_hub in pkgs_at_hub:
    #                         pkgs_at_hub.remove(nearest_pkg_to_hub)
    #                     t2count += 1
    #                 if t2count == 16:
    #
    #                     t1count = 0
    #                     for box in truck1.inventory:
    #                         t1count += 1
    #                     while t1count < 16:
    #                         truck1.load(nearest_pkg_to_hub)
    #                         # print('LOAD THE PACKAGES: nearest_pkg_to_hub: ', nearest_pkg_to_hub)
    #                         t1count += 1
    #                     if t1count == 16:
    #                         print('dispatch trucks')
    #
    # # THIS HELPS THE ABOVE TO SHOW WHERE PKG CLOSEST TO HUB IS LOCATED
    # # TRUCK2:
    # for pkg in truck2.inventory:
    #     if pkg.address in dest[0]:
    #         if float(dest[2]) == min_dist_from_hub:
    #             count = 0
    #             for box in truck2.inventory:
    #                 count += 1
    #                 while count < 16:
    #                     # truck2.load(pkg)
    #                     truck2.inventory.append(nearest_pkg_to_hub)
    #                     unstaged_pkgs.remove(nearest_pkg_to_hub)  # IF LENGTH < 40 FIND ADDRESS OF LAST ELEMENT (unstaged_pkgs[-1?]
    #                     count += 1
    #     # # TRUCK1:
    #     # for pkg in truck1.inventory:
    #     #     if pkg.address in dest[0]:
    #     #         if float(dest[2]) == min_dist_from_hub:
    #     #             count = 0
    #     #             for box in truck2.inventory:
    #     #                 if count < 15:
    #     #                     count += 1
    #     #                 while count < 15:
    #     #                     truck2.load(pkg)
    #     #                     count += 1


# LOAD PKG WITH DESTINATION CLOSEST TO HUB
def determine_first_pkg():
    min_dist_from_hub = 100
    for dest in dist_table:
        for unstaged_pkg in unstaged_pkgs:
            if unstaged_pkg[1].address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < min_dist_from_hub:
                    min_dist_from_hub = dist_to_hub
                    pkg_nearest_to_hub = unstaged_pkg
    return pkg_nearest_to_hub

def determine_next_pkg(current_pkg):
    # SHOW PACKAGES THAT HAVE YET TO BE LOADED
    # for pkg in unstaged_pkgs:
    #     print('determine_next_pkg: ', pkg)

    t2count = 0
    unloaded_min_dist_from_current = 100

    while t2count < 16:
        t2count += 1
        nearest_unloaded_pkg = Package
        for pkg in unstaged_pkgs:
            if pkg == current_pkg:
                print('here')
                dist_to_current = 2
                if dist_to_current < unloaded_min_dist_from_current:
                    unloaded_min_dist_from_current = dist_to_current
                    nearest_unloaded_pkg = pkg


def deliver_pkg(pkg, truck):
    for box in truck.inventory:
        print(box)
    print()
    curr_address = pkg.address
    for box in truck.inventory:
        if pkg.address == box.address:
            truck.inventory.remove(pkg)
    for box in truck.inventory:
        print(box)


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
dist_table = load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")

unstaged_pkgs = []
for bucket in myHash.table:
    for pkg in bucket:
        unstaged_pkgs.append(pkg)

determine_first_pkg()

ordered_route = []  # SORT TRUCK INVENTORIES
for stop in ordered_route:
    print(stop)

truck2 = Truck()
truck1 = Truck()

truck2.load_special()

# for box in truck2.inventory:
#     print('t2before: ', box)
stage_trucks()
# for box in truck2.inventory:
#     print('t2after: ', box)

countss = 0
for pkg in unstaged_pkgs:
    countss += 1
    # print(pkg)
print('countss', countss)
