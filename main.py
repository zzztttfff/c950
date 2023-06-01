# Zachary Finegan 001122345
import csv
import math


def load_package_file(file):
    with open(file) as pkg_csv:
        reader = csv.reader(pkg_csv, delimiter=',')
        line_num = 0
        for row in pkg_csv:
            if line_num < 2:
                line_num += 1
            else:
                for pkg in reader:
                    if len(pkg) == 9:
                        pkg_id = pkg[0]
                        address = pkg[1]
                        city = pkg[2]
                        state = pkg[3]
                        zip_code = pkg[4]
                        dd = pkg[5]
                        mass = pkg[6]
                        notes = pkg[7]
                        status = pkg[8]
                        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes, status)
                    else:
                        pkg_id = pkg[0]
                        address = pkg[1]
                        city = pkg[2]
                        state = pkg[3]
                        zip_code = pkg[4]
                        dd = pkg[5]
                        mass = pkg[6]
                        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes='', status = '')

                    myHash.insert_auto(pkg_id, package)


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

    def insert_auto(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kvp in bucket_list:
            if kvp[0] == key:
                kvp[1] = item
                return True
        kvp = [key, item]
        bucket_list.append(kvp)
        return True

    def insert_manually(self, pkg_id, address, city, state, zip_code, dd, mass, notes='', status=''):
        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes, status)
        myHash.insert_auto(pkg_id, package)

    def search(self, key):
        for bucket in myHash.table:
            for item in bucket:
                if int(item[0]) == key:
                    return item[1]
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
    def __init__(self, pkg_id, address, city, state, zip_code, dd, mass, notes, status):
        self.pkg_id = pkg_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.dd = dd
        self.mass = mass
        self.notes = notes
        self.status = status

    def __str__(self):
        if self.notes != '':
            return f"ID: {self.pkg_id}, Address: {self.address}, {self.city}, {self.state} {self.zip_code}; Delivery " \
                   f"Deadline: {self.dd}; Mass: {self.mass}kg; Special Notes: {self.notes}; Status: {self.status}."
        else:
            return f"ID: {self.pkg_id}, Address: {self.address}, {self.city}, {self.state} {self.zip_code}; Delivery " \
                   f"Deadline: {self.dd}; Mass: {self.mass}kg; Status: {self.status}"


class Truck:
    def __init__(self):
        self.inventory = []
        self.manual_inventory = []
        self.manual_inventory_adjust = []
        self.route = []

    distance_traveled = 0

    def load_special(self):
        # self.inventory.append(pkg_id)
        for bucket in myHash.table:
            for pkg in bucket:
                for data in pkg:
                    if type(data) != type('string'):
                        # MANUALLY LOADS SPECIAL NOTED PACKAGES INTO truck2.inventory
                        if "Can only be on truck 2" in str(data):
                            if data not in truck2.inventory:
                                truck2.inventory.append(data)
                                truck2.manual_inventory.append(data)
                                truck2.manual_inventory_adjust.append(data)
                        if int(data.pkg_id) in {13, 14, 15, 16, 19, 20}:
                            if data not in truck2.inventory:
                                truck2.inventory.append(data)
                                truck2.manual_inventory.append(data)
                                truck2.manual_inventory_adjust.append(data)
                                # FIND WAY TO INCORPORATE MANUALLY LOADED PACKAGES INTO distance_traveled AND staged_pkg
                                # SHOULD I JUST PUT t2.distance_traveled += distance HERE? HOW WOULD I GET THE DISTANCE HERE?

        # REMOVES LOADED PKGS FROM myHash.table...MIGHT NOT BE NEEDED, OR WANTED, FOR THAT MATTER.
        # for pkg in self.inventory:
        #     pkg_in_truck = pkg.pkg_id
        #     for bucket in myHash.table:
        #         for index, item in enumerate(bucket):
        #             if item[0] == pkg_in_truck:
        #                 bucket.pop(index)

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

    # def calc_dist(self):
    #     print('calc_dist:')
    #     for box in self.manual_inventory:
    #         for staged_pkg in staged_pkgs:
    #             if box in staged_pkg:
    #                 print(box)
    #     print()

    def __repr_id__(self):
        return f"Packages: {self.inventory[0].pkg_id}, " + ", ".join(
            [f"{x.pkg_id}" for x in self.inventory[1:len(self.inventory) - 1]]) + " ".join(
            [f", {self.inventory[len(self.inventory) - 1].pkg_id}"])

    def __repr_address__(self):
        return f"Addresses: \nID {self.inventory[0].pkg_id}: {self.inventory[0].address}\n" + "".join(
            [f"ID {x.pkg_id}: {x.address}\n" for x in self.inventory[1:len(self.inventory) - 1]]) + "".join(
            [f"ID {self.inventory[len(self.inventory) - 1].pkg_id}: {self.inventory[len(self.inventory) - 1].address}"])


# LOAD PKG CLOSEST TO HUB
def determine_first_pkg():
    min_dist_from_hub = 100
    for dest in dist_table:
        for unstaged_pkg in unstaged_pkgs:
            if unstaged_pkg[1].address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < min_dist_from_hub:
                    min_dist_from_hub = dist_to_hub
                    pkg_nearest_to_hub = unstaged_pkg
    if pkg_nearest_to_hub[1] not in truck2.inventory:
        truck2.inventory.append(pkg_nearest_to_hub[1])

    truck2.distance_traveled += min_dist_from_hub
    truck2.route.append(min_dist_from_hub)
    unstaged_pkgs.remove(pkg_nearest_to_hub)
    return pkg_nearest_to_hub


# LOAD THE OTHER 31 PACKAGES. STILL LEAVES REMAINING PACKAGES TO BE LOADED.
def determine_next_pkg():
    # DETERMINE NEAREST NEIGHBOR, APPEND, REMOVE.

    current_pkg = staged_pkgs[-1]
    # print('current_pkg:', current_pkg)

    unstaged_min_dist_from_current = 100

    # GRABS current_pkg dist_table[0] COLUMN INDEX:
    current_pkg_inx = int
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            current_pkg_inx = dist_table[0].index(dest)

    # SHOWS ROW OF DISTANCES FOR current_pkg:
    # current_pkg_dist_table_row_info = []
    # for distance in dist_table[current_pkg_inx - 1]:
    #     if dist_table[current_pkg_inx - 1].index(distance) > 1:  # DO NOT WANT FIRST OR SECOND COLUMNS
    #         if distance != '':
    #             current_pkg_dist_table_row_info.append(float(distance))
    # FIND MIN DISTANCE IN THAT dist_table ROW AND SEE IF THE CORRESPONDING PKG IS IN unstaged_pkg. AFTER THIS, REMEMBER TO CHECK AGAINST ALLLL PACKAGES
    # current_pkg_dist_table_row_info.sort()
    # for distance in current_pkg_dist_table_row_info:
    #     if distance > 0:
    #         print(distance)

    nearest_neighbor = Package
    shortest_distance = 100
    # SHOWS PACKAGE AND ITS dist_table ROW INDEX, AKA ITS DISTANCE TO current_pkg
    for dest in dist_table[0]:
        for unstaged in unstaged_pkgs:
            if unstaged[1].address in dest:
                inx = dist_table[0].index(dest)
                if dist_table[current_pkg_inx - 1][inx] != '':
                    # print(dist_table[current_pkg_inx - 1][inx], unstaged_pkg[1])
                    if float(dist_table[current_pkg_inx - 1][inx]) < shortest_distance:
                        shortest_distance = float(dist_table[current_pkg_inx - 1][inx])
                        nearest_neighbor = unstaged
    # print(nearest_neighbor[1])

    # DETERMINE nearest_neighbor AND shortest_distance TO current_pkg:
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            inx = dist_table[0].index(dest)
            for row in dist_table[1:-1]:
                if row[inx] != '':
                    # print(row[inx])
                    for unstaged in unstaged_pkgs:
                        if unstaged[1].address in row[0]:
                            # print(row[inx], unstaged_pkg[1])
                            if float(row[inx]) < shortest_distance:
                                shortest_distance = float(row[inx])
                                nearest_neighbor = unstaged

    # ADD PACKAGES FROM manual_inventory
    if nearest_neighbor[1] in truck2.manual_inventory_adjust:
        truck2.distance_traveled += shortest_distance
        truck2.route.append(shortest_distance)
        staged_pkgs.append(nearest_neighbor)
        unstaged_pkgs.remove(nearest_neighbor)
        truck2.manual_inventory_adjust.remove(nearest_neighbor[1])
        if len(unstaged_pkgs) > 0:
            determine_next_pkg()

    # ADD TO truck2 UNTIL FILLED
    elif len(truck2.inventory) < 16:
        if nearest_neighbor[1] not in truck2.inventory:
            if nearest_neighbor[1] not in truck1.inventory:
                truck2.inventory.append(nearest_neighbor[1])
                truck2.distance_traveled += shortest_distance
                truck2.route.append(shortest_distance)
        staged_pkgs.append(nearest_neighbor)
        unstaged_pkgs.remove(nearest_neighbor)
        if len(unstaged_pkgs) > 0:
            determine_next_pkg()

    # ADD TO truck1 AFTER truck2 FILLED
    elif len(truck1.inventory) < 16:
        if nearest_neighbor[1] not in truck1.inventory:
            if nearest_neighbor[1] not in truck2.inventory:
                truck1.inventory.append(nearest_neighbor[1])
                truck1.distance_traveled += shortest_distance
                truck1.route.append(shortest_distance)
                staged_pkgs.append(nearest_neighbor)  # I MOVED THIS INTO THE TWO IF LOOPS. IF ERROR, MOVE LEFT 2 TABS
                unstaged_pkgs.remove(nearest_neighbor)
        if len(unstaged_pkgs) > 0:
            determine_next_pkg()

    # ADD PACKAGES THAT DO NOT SHOW UP IN staged_pkgs
    elif len(truck2.inventory) == 16:
        staged_boxes = []
        for staged_box in staged_pkgs:
            staged_boxes.append(staged_box[1])
        for bad_pkg in truck2.inventory:
            if bad_pkg not in staged_boxes:
                for unstaged in unstaged_pkgs:
                    if unstaged[0] == bad_pkg.pkg_id:
                        staged_pkgs.append(unstaged)
                        unstaged_pkgs.remove(unstaged)
                        truck2.distance_traveled += shortest_distance
                        truck2.route.append(shortest_distance)
                        if bad_pkg in truck2.manual_inventory_adjust:
                            truck2.manual_inventory_adjust.remove(bad_pkg)
                if len(unstaged_pkgs) > 0:
                    determine_next_pkg()

    else:
        print('DISPATCH TRUCKS BOIIII')


def run_interface():
    choice = input("Enter 1 to search by package number. \nEnter 2 to search by time.\n")
    if choice == '1':
        pkg_num = input("Enter package number:")
        for box in staged_pkgs:
            if box[1].pkg_id == pkg_num:
                print(box[1])
    if choice == '2':
        print('welp')


# NOT SURE IF THIS WILL BE NEEDED AFTER CALC_STATUS IS IMPLEMENTED, AS CALC_STATUS WILL HAVE TO
# DETERMINE WHERE THE TRUCK IS AT A SPECIFIED TIME.
# def dispatch_trucks():
    # AT 800 TRUCKS LEAVE HUB
    # TIME = MILES / 18MPH X 60
    # start_time = time.time()
    # i = 0
    # distance_total = 0
    # for staged_pkg in staged_pkgs:
    #     for box in truck2.inventory:
    #         if staged_pkg[1] == box:
    #             distance_total += truck2.route[i]
    #             print('It took', truck2.route[i], 'miles to drop off package', box.pkg_id + '. Total distance:', round(distance_total,2), 'mi.')
    #             i += 1
    # print()


def calc_time(time):
    if time < 1000:
        if time < 800:
            print('ERROR. TRUCKS HAVE NOT YET BEEN DISPATCHED.')
            return
        time = str(time)
        if int(str(time[-2])) > 5:
            print('ERROR IN TIME < 1000')
            return
        input_minutes = int(str(time[-2])) * 10 + int(str(time[-1]))
        input_hours = (int(str(time[-3])) - 8)
        total_minutes = input_minutes + input_hours * 60
        hours = math.floor(total_minutes / 60)
        mins = total_minutes % 60
        # print(time, 'is', hours, 'hours and', mins, 'mins after 800. That\'s', total_minutes, 'minutes.')
        return total_minutes
    else:
        time = str(time)
        if int(str(time[-4])) > 2 or int(str(time[-2])) > 5 or int(str(time[-4])) == 2 and int(str(time[-3])) > 3:
            print('ERROR IN TIME >= 1000')
            return
        input_minutes = int(str(time[-2])) * 10 + int(str(time[-1]))
        input_hours = int(str(time[-4])) * 10 + (int(str(time[-3])) - 8)
        total_minutes = input_minutes + input_hours * 60
        hours = math.floor(total_minutes / 60)
        mins = total_minutes % 60
        hours_and_mins = total_minutes / 60
        # print(time, 'is', hours, 'hours and', mins, 'mins after 800. That\'s', total_minutes, 'minutes.')
        return total_minutes


# ENSURES CORRECTNESS OF TIME AFTER ADDING MINUTES TRAVELED
def correct_time(time):
    time = str(time)
    time_list = list(time)
    if int(time_list[-2]) > 5:
        time_list[-3] = str((int(time[-3]) + 1))
        time_list[-2] = str((int(time[-2]) - 6))
        corrected_time = ''.join(time_list)
        return corrected_time
    else:
        return time


# RETURNS PACKAGE STATUS GIVEN A USER-INPUT TIME
def calc_status(given_time):

    current_time = 800
    minutes_driven = calc_time(given_time)
    working_mileage = minutes_driven * .3  # HOW FAR EACH TRUCK WILL HAVE DRIVEN BY THE given_time

    # TRUCK2:
    # ITEMS ON truck2 ORDERED BY STOP NUMBER
    t2staged = []
    for pkg in staged_pkgs:
        for item in truck2.inventory:
            if pkg[1] == item:
                t2staged.append(item)

    t2dropped_off_pkgs = {}
    distance_traveled = 0
    stop_number = 0
    for distance in truck2.route:  # Increments distance_traveled, determines and stores time in t2d{}, removes pkg from inv
        if distance_traveled + distance <= working_mileage:  # Determines last stop by given time
            distance_traveled += distance
            time_of_delivery = round(current_time + distance_traveled / .3)
            t2dropped_off_pkgs[t2staged[stop_number].pkg_id] = correct_time(time_of_delivery)
            truck2.inventory.remove(t2staged[stop_number])
            stop_number += 1
            if len(truck2.inventory) == 0:
                distance_difference = round(working_mileage - distance_traveled, 2)
                keys_list = list(t2dropped_off_pkgs.keys())
                keys_except_last = keys_list[:-1]
                keys_except_last_str = ', '.join(keys_except_last)
                key_last = keys_list[-1]
                print('At', given_time, 'truck2 has dropped off packages', keys_except_last_str, 'and', str(key_last) +
                      '. No packages en route')
                break
        else:  # Shows status
            distance_difference = round(working_mileage - distance_traveled, 2)
            keys_list = list(t2dropped_off_pkgs.keys())
            keys_except_last = keys_list[:-1]
            keys_except_last_str = ', '.join(keys_except_last)
            key_last = keys_list[-1]
            en_route = []
            for pkg in truck2.inventory:
                en_route.append(str(pkg.pkg_id))
            en_route_str = ', '.join(en_route)
            print('At', given_time, 'truck2 has dropped off packages', keys_except_last_str, 'and', str(key_last),
                  'and is', distance_difference, 'miles into the next delivery.')
            print('Packages en route:', en_route_str)
            break
    how_to_access_value = t2dropped_off_pkgs.get('14')

    # TRUCK1:
    # ITEMS ON truck1 ORDERED BY STOP NUMBER
    t1staged = []
    for pkg in staged_pkgs:
        for item in truck1.inventory:
            if pkg[1] == item:
                t1staged.append(item)

    t1dropped_off_pkgs = {}
    distance_traveled = 0
    stop_number = 0
    for distance in truck1.route:  # Increments distance_traveled, determines and stores time in t1d{}, removes pkg from inv
        if distance_traveled + distance <= working_mileage:  # Determines last stop by given time
            distance_traveled += distance
            time_of_delivery = round(current_time + distance_traveled / .3)
            t1dropped_off_pkgs[t1staged[stop_number].pkg_id] = correct_time(time_of_delivery)
            if len(truck1.inventory) == 1:
                last_pkg = truck1.inventory[0]
            truck1.inventory.remove(t1staged[stop_number])
            stop_number += 1
            if len(truck1.inventory) == 0:
                if len(truck2.inventory) != 0:
                    # RETURN TO HUB, LOAD UP, DISPATCH
                    # DETERMINE DISTANCE FROM LAST PACKAGE TO HUB
                    last_address = last_pkg.address
                    return_to_hub(last_address)
                    print('get to hub, reload, dispatch')
                    break
                distance_difference = round(working_mileage - distance_traveled, 2)
                keys_list = list(t1dropped_off_pkgs.keys())
                keys_except_last = keys_list[:-1]
                keys_except_last_str = ', '.join(keys_except_last)
                key_last = keys_list[-1]
                en_route = []
                for pkg in truck2.inventory:
                    en_route.append(str(pkg.pkg_id))
                en_route_str = ', '.join(en_route)
                print('At', given_time, 'truck1 has dropped off packages', keys_except_last_str, 'and',
                      str(key_last) + '. No packages en route.')
                break
        else:  # Shows status
            distance_difference = round(working_mileage - distance_traveled, 2)
            keys_list = list(t1dropped_off_pkgs.keys())
            keys_except_last = keys_list[:-1]
            keys_except_last_str = ', '.join(keys_except_last)
            key_last = keys_list[-1]
            en_route = []
            for pkg in truck1.inventory:
                en_route.append(str(pkg.pkg_id))
            en_route_str = ', '.join(en_route)
            print('At', given_time, 'truck1 has dropped off packages', keys_except_last_str, 'and', str(key_last),
                  'and is', distance_difference, 'miles into the next delivery.')
            print('Packages en route:', en_route_str)
            break
    how_to_access_value = t1dropped_off_pkgs.get('32')

    # PRESENTS ALL PACKAGES NOT YET DELIVERED BY THE GIVEN TIME
    # for bucket in myHash.table:
    #     for pkg in bucket:
    #


def return_to_hub(last_address):
    print('return:')
    i = 0
    for row in dist_table:
        if last_address in row[2]:
            selected = dist_table[i]
            print('what', selected)



# RUN PROGRAM STUFF


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
dist_table = load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")

truck2 = Truck()
truck1 = Truck()
# delivered_pkgs = []

# STARTS AS ALL PACKAGES; PACKAGES GET REMOVED AS THEY ARE STAGED
unstaged_pkgs = []
for bucket in myHash.table:
    for pkg in bucket:
        unstaged_pkgs.append(pkg)

# ADDS SPECIAL PACKAGES TO truck2.inventory
truck2.load_special()

# CREATE staged_pkgs, DETERMINE FIRST PACKAGE IN ROUTE, ADD IT TO staged_pkgs, REMOVE IT FROM unstaged_pkgs, REMOVE FROM truck2.manual_inventory_adjust
staged_pkgs = [determine_first_pkg()]
if staged_pkgs[0][1] in truck2.manual_inventory_adjust:
    truck2.manual_inventory_adjust.remove(staged_pkgs[0][1])

# FULLY LOAD BOTH TRUCKS, ADJUST staged_pkgs AND unstaged_pkgs
for item in unstaged_pkgs:
    determine_next_pkg()

# dispatch_trucks()

# PRINTSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

# # truck2
# c = 0
# print('truck2.inventory:')
# for item in truck2.inventory:
#     print(item)
#     c += 1
# print(c)
# print()
#
# # truck1
# c = 0
# print('truck1.inventory:')
# for item in truck1.inventory:
#     print(item)
#     c += 1
# print(c)
# print()
#
# # staged_pkgs
# c = 0
# print('staged_pkgs:')
# for item in staged_pkgs:
#     print(item)
#     c += 1
# print(c)
# print()
#
# # unstaged_pkgs
# c = 0
# print('unstaged packages:')
# for unstaged_pkg in unstaged_pkgs:
#     print(unstaged_pkg)
#     c += 1
# print(c)
# print()

# distances
# print('t2distance', truck2.distance_traveled)
# print('t1distance', truck1.distance_traveled)

# run_interface()
# calc_time(2359)

calc_status(900)
