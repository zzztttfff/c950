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

    distance_traveled = 0

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
            # print('dispatch trucks')
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
    truck2.inventory.append(pkg_nearest_to_hub[1])
    unstaged_pkgs.remove(pkg_nearest_to_hub)
    return pkg_nearest_to_hub


def determine_next_pkg():
    # DETERMINE NEAREST NEIGHBOR, APPEND, REMOVE.

    current_pkg = staged_pkgs[-1]

    unstaged_min_dist_from_current = 100

    # GET CURRENT PACKAGE DIST TABLE INFO / AND COMPARE THAT TO UNSTAGED PACKAGE DIST TABLE INFO. FIND MIN DISTANCE AND APPEND THAT TO STAGED PACKAGES
    # MAKE SURE TO COMPARE AGAINST ALL DISTANCES

    # GRABS current_pkg dist_table INFO:
    current_pkg_inx = int
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            current_pkg_inx = dist_table[0].index(dest)
            # print('current_inx:', current_pkg_inx)
            # print(dist_table[current_pkg_inx - 1])

    # SHOWS ROW OF DISTANCES FOR current_pkg:
    current_pkg_dist_table_row_info = []
    for distance in dist_table[current_pkg_inx - 1]:
        if dist_table[current_pkg_inx - 1].index(distance) > 1:
            if distance != '':
                current_pkg_dist_table_row_info.append(float(distance))

    # NEED TO SHOW WHICH PKG HOLDS WHICH DISTANCE
    # THAT IS, WHICH PKG THE INDEX OF dist_table[0] THAT CORRESPONDS TO THE COLUMN DISTANCE
    # THIS BLOCK MAY NOT BE NEEDED. DON'T THINK ANY VARIABLE NEEDS TO BE MADE HERE
    # for unstaged_pkg in unstaged_pkgs:
    #     for dest in dist_table[0]:
    #         if unstaged_pkg[1].address in dest:
    #             print(unstaged_pkg[1], dist_table[0].index(dest))

    # FIND MIN DISTANCE IN THAT dist_table ROW AND SEE IF THE CORRESPONDING PKG IS IN unstaged_pkg. AFTER THIS, REMEMBER TO CHECK AGAINST ALLLL PACKAGES
    # current_pkg_dist_table_row_info.sort()
    # for distance in current_pkg_dist_table_row_info:
    #     if distance > 0:
    #         print(distance)
    nearest_neighbor = Package
    shortest_distance = 100
    # SHOWS PACKAGE AND ITS dist_table ROW INDEX! AKA ITS DISTANCE TO current_pkg
    for dest in dist_table[0]:
        for unstaged_pkg in unstaged_pkgs:
            if unstaged_pkg[1].address in dest:
                inx = dist_table[0].index(dest)
                if dist_table[current_pkg_inx - 1][inx] != '':
                    # print(dist_table[current_pkg_inx - 1][inx], unstaged_pkg[1])
                    if float(dist_table[current_pkg_inx - 1][inx]) < shortest_distance:
                        shortest_distance = float(dist_table[current_pkg_inx - 1][inx])
                        nearest_neighbor = unstaged_pkg
    # print(nearest_neighbor[1])

    # CHOOSE CLOSEST NEIGHBOR TO current_pkg AND ADD TO TRUCK. BUT FIRST, THERE ARE ONLY 30 PKGS ABOVE. FIND THE OTHER 9 AND COMPARE TO ADDRESS. THEY ARE PROBABLY IN staged_pkgs
    # NOPE. ONLY ONE IN STAGED PACKAGES, WHICH IS THE FIRST PACKAGE, SO THAT IS CORRECT. I THINK THEY ARE THE PACKAGES THAT CORRESPOND TO EMPTY INDICES IN THAT dist_table ROW.
    # FIND WAY TO ACCESS THESE DISTANCES. I SHOULD BE ABLE TO INVERT THE 2D LIST INDICES TO ACCESS THE DESIRED COLUMN BEFORE THE ROW.
    # ACCESS THE current_pkg INDEX FROM dist_table[0] AND THEN ITERATE DOWN THRU dist_table[n]
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            inx = dist_table[0].index(dest)
            for row in dist_table[1:-1]:
                if row[inx] != '':
                    # print(row[inx])
                    for unstaged_pkg in unstaged_pkgs:
                        if unstaged_pkg[1].address in row[0]:
                            # print(row[inx], unstaged_pkg[1])
                            if float(row[inx]) < shortest_distance:
                                shortest_distance = float(row[inx])
                                nearest_neighbor = unstaged_pkg
    # print(nearest_neighbor[1])

    if len(truck2.inventory) < 16:
        truck2.inventory.append(nearest_neighbor[1])
        truck2.distance_traveled += shortest_distance
        staged_pkgs.append(nearest_neighbor)
        unstaged_pkgs.remove(nearest_neighbor)
        for item in truck2.inventory:
            print(item)
        print()
        determine_next_pkg()

    elif len(truck1.inventory) < 16:
        truck1.inventory.append(nearest_neighbor[1])
        truck1.distance_traveled += shortest_distance
        staged_pkgs.append(nearest_neighbor)
        unstaged_pkgs.remove(nearest_neighbor)

        determine_next_pkg()
    # else:
    #     print('DISPATCH TRUCKS BOIIII')


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
dist_table = load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")

truck2 = Truck()
truck1 = Truck()

unstaged_pkgs = []
for bucket in myHash.table:
    for pkg in bucket:
        unstaged_pkgs.append(pkg)

truck2.load_special()
first_pkg_loaded = determine_first_pkg()
staged_pkgs = [first_pkg_loaded]

for item in unstaged_pkgs:
    determine_next_pkg()




