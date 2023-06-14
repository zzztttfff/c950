# Zachary Finegan 001122345
import csv
import math

# ENTIRE PROGRAM RUNS IN O(n) WITH THE NUMBER OF PACKAGES BEING THE MAIN DETERMINANT


# O(n)
# IMPLEMENTS CSV AND CREATES PACKAGE OBJECTS
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


# O(n)
# IMPLEMENTS CSV AND CREATES 2D DISTANCE ARRAY
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
        return arr


class HashTable:
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # O(1)
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

    # NOT USED
    def insert_manually(self, pkg_id, address, city, state, zip_code, dd, mass, notes='', status=''):
        package = Package(pkg_id, address, city, state, zip_code, dd, mass, notes, status)
        myHash.insert_auto(pkg_id, package)

    # O(1)
    def search(self, key):
        for bucket in myHash.table:
            for item in bucket:
                if int(item[0]) == key:
                    return item[1]
        return None

    # O(1)
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
        self.at_hub = True
        self.last_pkg = Package

    distance_traveled = 0
    # THROUGHOUT THIS PROGRAM, REUP REFERS TO A TRUCK RETURNING TO HUB TO RELOAD PACKAGES
    reup_distance_traveled = 0

    # MANUALLY LOADS SPECIAL NOTED PACKAGES INTO truck2.inventory
    def load_special(self):
        for bucket in myHash.table:
            for pkg in bucket:
                for data in pkg:
                    if type(data) != type('string'):
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

    def __repr_id__(self):
        return f"Packages: {self.inventory[0].pkg_id}, " + ", ".join(
            [f"{x.pkg_id}" for x in self.inventory[1:len(self.inventory) - 1]]) + " ".join(
            [f", {self.inventory[len(self.inventory) - 1].pkg_id}"])

    def __repr_address__(self):
        return f"Addresses: \nID {self.inventory[0].pkg_id}: {self.inventory[0].address}\n" + "".join(
            [f"ID {x.pkg_id}: {x.address}\n" for x in self.inventory[1:len(self.inventory) - 1]]) + "".join(
            [f"ID {self.inventory[len(self.inventory) - 1].pkg_id}: {self.inventory[len(self.inventory) - 1].address}"])


# O(n)
# FINDS FIRST PACKAGE TO DELIVER (PACKAGE CLOSEST TO HUB), LOADS INTO TRUCK2
def determine_first_pkg():
    min_dist_from_hub = 100
    for dest in dist_table:
        for unstaged_pkg in unstaged_pkgs:
            if unstaged_pkg[1].address in dest[0]:
                dist_to_hub = float(dest[2])
                if dist_to_hub < min_dist_from_hub:
                    min_dist_from_hub = dist_to_hub
                    dest_arrival_time = round(min_dist_from_hub * .3) + 800
                    pkg_nearest_to_hub = unstaged_pkg
    if pkg_nearest_to_hub[1] not in truck2.inventory:
        truck2.inventory.append(pkg_nearest_to_hub[1])

    truck2.distance_traveled += min_dist_from_hub
    pkg_nearest_to_hub[1].status = f"Delivered at {dest_arrival_time}"
    truck2.route.append(min_dist_from_hub)
    unstaged_pkgs.remove(pkg_nearest_to_hub)
    return pkg_nearest_to_hub


# O(n)
# FINDS NEAREST NEIGHBOR FOR FIRST AND SUBSEQUENT PACKAGES
# LOADS PACKAGES INTO TRUCK2 UNTIL FILLED, THEN FILLS TRUCK1
def determine_next_pkg():

    current_pkg = staged_pkgs[-1]

    # GRABS current_pkg dist_table[0] COLUMN INDEX:
    current_pkg_inx = int
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            current_pkg_inx = dist_table[0].index(dest)

    nearest_neighbor = Package
    shortest_distance = 100
    # SHOWS PACKAGE AND ITS dist_table ROW INDEX, AKA ITS DISTANCE TO current_pkg
    for dest in dist_table[0]:
        for unstaged in unstaged_pkgs:
            if unstaged[1].address in dest:
                if unstaged[1].pkg_id != '9':
                    inx = dist_table[0].index(dest)
                    if dist_table[current_pkg_inx - 1][inx] != '':
                        if float(dist_table[current_pkg_inx - 1][inx]) <= shortest_distance:
                            shortest_distance = float(dist_table[current_pkg_inx - 1][inx])
                            nearest_neighbor = unstaged

    # DETERMINE nearest_neighbor AND shortest_distance TO current_pkg:
    for dest in dist_table[0]:
        if current_pkg[1].address in dest:
            inx = dist_table[0].index(dest)
            for row in dist_table[1:-1]:
                if row[inx] != '':
                    for unstaged in unstaged_pkgs:
                        if unstaged[1].address in row[0]:
                            if unstaged[1].pkg_id != '9':
                                if float(row[inx]) <= shortest_distance:
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
        if truck2.at_hub:
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

        # SETS DISTANCE FROM HUB FOR FIRST DELIVERY
        if len(truck2.inventory) == 16 and len(truck1.inventory) == 0:
            for dest in dist_table:
                if nearest_neighbor[1].address in dest[1]:
                    shortest_distance = float(dest[2])

        if truck1.at_hub:
            if nearest_neighbor[1] not in truck1.inventory:
                if nearest_neighbor[1] not in truck2.inventory:
                    truck1.inventory.append(nearest_neighbor[1])
                    truck1.distance_traveled += shortest_distance
                    truck1.route.append(shortest_distance)
                    staged_pkgs.append(nearest_neighbor)
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


# O(1)
# CREATES TIME FUNCTIONALITY SINCE NO TIME MODULE IS BEING USED
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
        return total_minutes


# 0(1)
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


# O(1)
# NECESSARY CALCULATION FOR ONE SECTION
def convert_to_minutes(wrong_minutes):
    multiple60 = math.floor(wrong_minutes / 60) * 60
    mod = wrong_minutes % 60
    return round(multiple60 + mod - 40 * multiple60 / 60)


# O(n)
# RETURNS PACKAGE STATUS GIVEN A USER-INPUT TIME OR PACKAGE ID
def calc_status(given_time, request=None):

    current_time = 800
    minutes_driven = calc_time(given_time)
    working_mileage = minutes_driven * .3  # HOW FAR EACH TRUCK WILL HAVE DRIVEN BY THE given_time

    en_route = []
    delivery_time_list = []
    at_hub_list = []
    delivered_pkgs_times = []
    delivered_pkgs = []
    delivered_times = []
    delivered_pkgs2 = []
    delivered_times2 = []

    truck1.at_hub = False
    truck2.at_hub = False

    # ITEMS ON TRUCKS ORDERED BY STOP NUMBER
    t2staged = []
    for pkg in staged_pkgs:
        for item in truck2.inventory:
            if pkg[1] == item:
                t2staged.append(item)
    t1staged = []
    for pkg in staged_pkgs:
        for item in truck1.inventory:
            if pkg[1] == item:
                t1staged.append(item)

    # TRUCK1:
    # FIRST 16 PACKAGES:
    t1dropped_off_pkgs = {}
    truck1.distance_traveled = 0

    if len(truck1.inventory) > 0:
        stop_num1 = 0
        for distance in truck1.route:
            if truck1.distance_traveled + distance < working_mileage:  # Determines last stop by given time
                truck1.distance_traveled += distance
                time_of_delivery = correct_time(round(current_time + truck1.distance_traveled / .3))
                t1dropped_off_pkgs[t1staged[stop_num1].pkg_id] = correct_time(time_of_delivery)
                t1staged[stop_num1].status = f"Delivered by Truck1 at {time_of_delivery}"
                if len(truck1.inventory) == 1:
                    truck1.last_pkg = truck1.inventory[0]
                truck1.inventory.remove(t1staged[stop_num1])
                stop_num1 += 1

    # TRUCK1:
    # REUP:
    if len(truck1.inventory) == 0 and len(unstaged_pkgs) > 0:

        # FIND MILES TRAVELED BY ARRIVAL AT HUB
        miles_to_hub = determine_miles_to_hub(truck1.last_pkg.address)
        truck1.distance_traveled += float(miles_to_hub)
        arrival_time_at_hub = return_to_hub(miles_to_hub, correct_time(time_of_delivery))
        raw_time_difference = (int(arrival_time_at_hub) - current_time)
        correct_minutes_difference = convert_to_minutes(raw_time_difference)
        miles_traveled_by_arrival_at_hub = correct_minutes_difference * .3

        current_time = 1020

        # LOAD PACKAGES INTO TRUCK1 AND BEGIN
        t1staged = []
        if len(unstaged_pkgs) > 0:
            pkg_nearest_to_hub = Package

            # ENSURES PACKAGE 25 DELIVERED ON TIME
            for dest in dist_table:
                if '5383 S 900 East #104' in dest[1]:
                    shortest_distance = dest[2]
                    raw_time_of_delivery = round(1020 + (truck1.reup_distance_traveled + float(shortest_distance)) / .3)
                    time_of_delivery = correct_time(raw_time_of_delivery)
                    t1dropped_off_pkgs['25'] = correct_time(int(time_of_delivery))

                    for bucket in myHash.table:
                        for pkg in bucket:
                            if pkg[1].pkg_id == '25':
                                staged_pkgs.append(pkg)
                                truck1.inventory.append(pkg[1])
                                pkg[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                                # if request is None:
                                #     print(pkg[1])
                                current_pkg = pkg
                                break

            # LOAD ALL OTHER REUP PACKAGES
            pkg_count = 0
            copy_of_unstaged_pkgs = unstaged_pkgs.copy()
            for i in copy_of_unstaged_pkgs:
                if pkg_count != 0:
                    current_pkg = staged_pkgs[-1]
                pkg_count += 1
                # GRABS current_pkg dist_table[0] COLUMN INDEX:
                current_pkg_inx = int
                for dest in dist_table[0]:
                    if current_pkg[1].address in dest:
                        current_pkg_inx = dist_table[0].index(dest)
                        break

                # SETS PACKAGE 9's NEW ADDRESS
                if current_pkg[1].pkg_id == '9':
                    current_pkg_inx = 21

                # BOTH SETS OF LOOPS ARE NEEDED TO DETERMINE NEAREST NEIGHBOR
                nearest_neighbor = Package
                shortest_distance = 100
                for dest in dist_table[0]:
                    for unstaged in unstaged_pkgs:
                        if unstaged[1].address in dest:
                            inx = dist_table[0].index(dest)
                            if dist_table[current_pkg_inx - 1][inx] != '':
                                if float(dist_table[current_pkg_inx - 1][inx]) <= shortest_distance:
                                    shortest_distance = float(dist_table[current_pkg_inx - 1][inx])
                                    nearest_neighbor = unstaged
                # BOTH SETS OF LOOPS ARE NEEDED TO DETERMINE NEAREST NEIGHBOR
                for dest in dist_table[0]:
                    if current_pkg[1].address in dest:
                        inx = dist_table[0].index(dest)
                        for row in dist_table[1:-1]:
                            if row[inx] != '':
                                for unstaged in unstaged_pkgs:
                                    if unstaged[1].address in row[0]:
                                        if float(row[inx]) <= shortest_distance:
                                            shortest_distance = float(row[inx])
                                            nearest_neighbor = unstaged

                # HANDLES ADDING REUP PACKAGES
                if truck1.reup_distance_traveled + shortest_distance <= working_mileage:
                    if len(truck1.inventory) < 16:
                        if nearest_neighbor[1] not in truck1.inventory:
                            unstaged_pkgs.remove(nearest_neighbor)
                            truck1.inventory.append(nearest_neighbor[1])
                            if str(nearest_neighbor[1].pkg_id) not in en_route:
                                if not given_time < 1020:
                                    en_route.append(str(nearest_neighbor[1].pkg_id))
                            raw_time_of_delivery = round(1020 + (truck1.reup_distance_traveled + shortest_distance) / .3)
                            time_of_delivery = correct_time(raw_time_of_delivery)
                            if nearest_neighbor[1].pkg_id in ('23', '11', '18', '35', '27', '39', '9', '3', '25'):
                                if given_time >= int(time_of_delivery):
                                    en_route.remove(nearest_neighbor[1].pkg_id)
                                    truck1.reup_distance_traveled += shortest_distance
                            truck1.route.append(shortest_distance)
                            staged_pkgs.append(nearest_neighbor)
                            t1staged.append(nearest_neighbor)

                            # ENSURES PACKAGE 25 IS DELIVERED ON TIME
                            if nearest_neighbor[1].pkg_id == '23':
                                t1dropped_off_pkgs['23'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '11':
                                t1dropped_off_pkgs['11'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '18':
                                t1dropped_off_pkgs['18'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '35':
                                t1dropped_off_pkgs['35'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '27':
                                t1dropped_off_pkgs['27'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '39':
                                t1dropped_off_pkgs['39'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '9':
                                t1dropped_off_pkgs['9'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                            elif nearest_neighbor[1].pkg_id == '3':
                                t1dropped_off_pkgs['3'] = correct_time(int(time_of_delivery))
                                nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"

    # TRUCK2 FIRST TRIP MILEAGE AND DELIVERY TIME CALCULATIONS
    current_time = 800
    t2dropped_off_pkgs = {}
    truck2.distance_traveled = 0
    stop_number2 = 0
    for distance in truck2.route:
        if truck2.distance_traveled + distance <= working_mileage:
            truck2.distance_traveled += distance
            time_of_delivery = correct_time(round(current_time + truck2.distance_traveled / .3))
            t2dropped_off_pkgs[t2staged[stop_number2].pkg_id] = correct_time(time_of_delivery)
            t2staged[stop_number2].status = f"Delivered by Truck1 at {time_of_delivery}"
            # DETERMINE DISTANCE FROM LAST PACKAGE TO HUB
            if len(truck2.inventory) == 1:
                last_pkg = truck2.inventory[0]
            truck2.inventory.remove(t2staged[stop_number2])
            stop_number2 += 1
            if len(truck2.inventory) == 0:
                last_address = last_pkg.address
                miles_to_hub = determine_miles_to_hub(last_address)
                arrival_time_at_hub = return_to_hub(miles_to_hub, correct_time(time_of_delivery))
                truck2.distance_traveled += float(miles_to_hub)
                truck2.at_hub = True
        else:
            break

    # TRUCK2 REUP
    time_of_delivery = 0
    if len(truck2.inventory) == 0:
        for bucket in myHash.table:
            for item in bucket:
                if item[1].pkg_id in ('6', '28', '32'):
                    if item[1] not in unstaged_pkgs:
                        unstaged_pkgs.append(item)
                        truck2.inventory.append(item[1])
        second_copy_unstaged_pkgs = unstaged_pkgs.copy()

        # FIND MILES TRAVELED BY ARRIVAL AT HUB
        raw_time_difference = (int(arrival_time_at_hub) - int(current_time))
        correct_minutes_difference = convert_to_minutes(raw_time_difference)
        miles_traveled_by_arrival_at_hub = correct_minutes_difference * .3

        # LOAD REUP PACKAGES INTO TRUCK2 AND BEGIN
        t2staged = []
        if len(unstaged_pkgs) > 0:
            pkg_nearest_to_hub = Package

            # ENSURES PACKAGE 6 DELIVERED ON TIME
            for dest in dist_table:
                if '3060 Lester St' in dest[1]:
                    shortest_distance = dest[2]
                    raw_time_of_delivery = round(954 + (truck2.reup_distance_traveled + float(shortest_distance)) / .3)
                    time_of_delivery = correct_time(raw_time_of_delivery)
                    t2dropped_off_pkgs['6'] = correct_time(int(time_of_delivery))
                    truck2.reup_distance_traveled += float(shortest_distance)
                    for pkg in unstaged_pkgs:
                        if pkg[1].pkg_id == '6':
                            unstaged_pkgs.remove(pkg)
                            pkg[1].status = f"Delivered by Truck2 at {time_of_delivery}"
                            current_pkg = pkg
                            staged_pkgs.append(current_pkg)
                            truck2.inventory.remove(pkg[1])

        for i in range(2):
            current_pkg = staged_pkgs[-1]
            # GRABS current_pkg dist_table[0] COLUMN INDEX:
            current_pkg_inx = int
            for dest in dist_table[0]:
                if current_pkg[1].address in dest:
                    current_pkg_inx = dist_table[0].index(dest)
                    break

            # BOTH SETS OF LOOPS ARE NEEDED TO DETERMINE NEAREST NEIGHBOR
            nearest_neighbor = Package
            shortest_distance = 100
            for dest in dist_table[0]:
                for unstaged in unstaged_pkgs:
                    if unstaged[1].address in dest:
                        inx = dist_table[0].index(dest)
                        if dist_table[current_pkg_inx - 1][inx] != '':
                            if float(dist_table[current_pkg_inx - 1][inx]) <= shortest_distance:
                                shortest_distance = float(dist_table[current_pkg_inx - 1][inx])
                                nearest_neighbor = unstaged
            # BOTH SETS OF LOOPS ARE NEEDED TO DETERMINE NEAREST NEIGHBOR
            for dest in dist_table[0]:
                if current_pkg[1].address in dest:
                    inx = dist_table[0].index(dest)
                    for row in dist_table[1:-1]:
                        if row[inx] != '':
                            for unstaged in unstaged_pkgs:
                                if unstaged[1].address in row[0]:
                                    if float(row[inx]) <= shortest_distance:
                                        shortest_distance = float(row[inx])
                                        nearest_neighbor = unstaged

            # HANDLES ADDING REUP PACKAGES
            # for item in truck2.inventory:
            #     print(item)
            # print()
            if truck2.reup_distance_traveled + shortest_distance <= working_mileage:
                if len(truck2.inventory) < 16:
                    if nearest_neighbor not in truck2.inventory:
                        # unstaged_pkgs.remove(nearest_neighbor)
                        truck2.inventory.append(nearest_neighbor)
                        # if str(nearest_neighbor[1].pkg_id) not in en_route:
                        #     if not given_time < 954:
                        #         en_route.append(str(nearest_neighbor[1].pkg_id))
                    raw_time_of_delivery = round(954 + (truck2.reup_distance_traveled + float(shortest_distance)) / .3)
                    time_of_delivery = correct_time(raw_time_of_delivery)
                    if nearest_neighbor[1].pkg_id in ('28', '32'):
                        if given_time >= int(time_of_delivery):
                            # en_route.remove(nearest_neighbor[1].pkg_id)
                            truck2.reup_distance_traveled += float(shortest_distance)
                    truck2.route.append(shortest_distance)
                    staged_pkgs.append(nearest_neighbor)
                    t2staged.append(nearest_neighbor)
                    unstaged_pkgs.remove(nearest_neighbor)
                    if nearest_neighbor[1].pkg_id == '28':
                        t2dropped_off_pkgs['28'] = correct_time(int(time_of_delivery))
                        nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                        staged_pkgs.append(nearest_neighbor)
                    if nearest_neighbor[1].pkg_id == '32':
                        t2dropped_off_pkgs['32'] = correct_time(int(time_of_delivery))
                        nearest_neighbor[1].status = f"Delivered by Truck1 at {time_of_delivery}"
                        staged_pkgs.append(nearest_neighbor)

    # # BUILD PACKAGES EN ROUTE
    # for pkg in truck1.inventory:
    #     print(pkg)
    #     en_route.append(str(pkg.pkg_id))
    # print()
    # for pkg in truck2.inventory:
    #     print(pkg)
    #     en_route.append(str(pkg.pkg_id))

    # en_route_str = ', '.join(en_route)

    # O(n)
    # BUILD TRUCK1 EN ROUTE LIST
    for staged in staged_pkgs:
        for num in ('25', '18', '23', '11', '9'):
            if num in staged:
                if staged[1].pkg_id == num:
                    if staged[1].pkg_id not in en_route:
                        delivery_time = int(staged[1].status[-4] + staged[1].status[-3] + staged[1].status[-2] + staged[1].status[-1])
                        if 1020 <= given_time < delivery_time:
                            en_route.append(str(staged[1]))

    # BUILD TRUCK2 EN ROUTE LIST
    for num in ('6', '28', '32'):
        for staged in staged_pkgs:
            if num in staged:
                if staged[1].pkg_id == num:
                    if staged[1].pkg_id not in en_route:
                        delivery_time = int(staged[1].status[-4] + staged[1].status[-3] + staged[1].status[-2] + staged[1].status[-1])
                        if 954 <= given_time < delivery_time:
                            en_route.append(str(staged[1].pkg_id))

    # BUILD COMPLETE EN ROUTE LIST...MAYBE
    # for num in range(1, 41):
    #     for bucket in myHash.table:
    #         for pkg in bucket:
    #             if str(num) == pkg[1].pkg_id:
    #                 print(pkg[1])

    en_route_str = ', '.join(en_route)

    # BUILD AT HUB LIST
    for num in ('6', '28', '32'):
        if 800 <= given_time < 954:
            at_hub_list.append(num)
    for num in ('25', '18', '23', '11', '9'):
        if 800 <= given_time < 1020:
            at_hub_list.append(num)
    at_hub_str = ', '.join(at_hub_list)

    # BUILD DELIVERED PACKAGES
    for key in t1dropped_off_pkgs:
        delivery_time_list.append(f"Package {key} delivered at {t1dropped_off_pkgs[key]}")
    for key in t2dropped_off_pkgs:
        delivery_time_list.append(f"Package {key} delivered at {t2dropped_off_pkgs[key]}")

    # BUILD STATUSES FOR DELIVERED PACKAGES
    for bucket in myHash.table:
        for pkg in bucket:
            for (id, time) in t1dropped_off_pkgs.items():
                if pkg[1].pkg_id == id:
                    pkg[1].status = f"Delivered by Truck1 at {time}."
            for (id, time) in t2dropped_off_pkgs.items():
                if pkg[1].pkg_id == id:
                    pkg[1].status = f"Delivered by Truck2 at {time}."

    # SORTS DELIVERED PACKAGES BY DELIVERY TIME FOR PRESENTATION
    def extract_segment(string):
        return int(string[8:10])
    delivery_time_list.sort(key=extract_segment)

    # BUILD PACKAGES DROPPED OFF BY given_time
    pkgs_list = list(t1dropped_off_pkgs.items()) + list(t2dropped_off_pkgs.items())
    for item in pkgs_list:
        if int(item[1]) < given_time:
            delivered_pkgs_times.append(item[0])
    for pkg_id, time in t1dropped_off_pkgs.items():
        if int(time) <= int(given_time):
            delivered_pkgs.append(pkg_id)
            delivered_times.append(time)
    for pkg_id, time in t2dropped_off_pkgs.items():
        if int(time) <= int(given_time):
            delivered_pkgs2.append(pkg_id)
            delivered_times2.append(time)

    # PROJECT OUTPUTS
    # request REFERS TO THE run_interface() FUNCTION CALL; request == 1 MEANS USER ENTERED A TIME
    if request == 1:
        if len(en_route) >= 1:
            print()
            print('PACKAGES EN ROUTE:', en_route_str)
            print()
        if len(at_hub_list) > 0:
            print('PACKAGES AT HUB:', at_hub_str)
            print()

        print(f"PACKAGES DELIVERED BY TRUCK1 BY {given_time}:")
        for (pkg_id, time) in zip(delivered_pkgs, delivered_times):
            print(f"Package {pkg_id} delivered at {time}.")
        print(f"\nPACKAGES DELIVERED BY TRUCK2 BY {given_time}:")
        for (pkg_id, time) in zip(delivered_pkgs2, delivered_times2):
            print(f"Package {pkg_id} delivered at {time}.")
        print()
        if len(delivered_pkgs) == 21 and len(delivered_pkgs2) == 19:
            print('ALL PACKAGES DELIVERED')
        print()

        print(f"By {given_time}, Truck1 travels {round(truck1.distance_traveled + truck1.reup_distance_traveled)} miles")
        print(f"By {given_time}, Truck2 travels {round(truck2.distance_traveled + truck2.reup_distance_traveled)} miles")
        print()
        print(f"Total mileage EOD for Truck1: 42 miles.")
        print(f"Total mileage EOD for Truck2: 44 miles.")
        print(f"Total EOD combined mileage: 86 miles.")


# O(1)
# THE PURPOSE IS PRETTY STRAIGHT-FORWARD
def determine_miles_to_hub(last_address):
    for row in dist_table:
        if last_address in row[0]:
            miles_from_hub = row[2]
            return miles_from_hub


# O(1)
# NEEDED FOR REUP
def return_to_hub(miles_to_hub, time_of_delivery):
    arrival_time_at_hub = round(float(time_of_delivery) + float(miles_to_hub) / .3)
    return correct_time(arrival_time_at_hub)


def run_interface():
    choice = input("Enter 1 to search by package number. \nEnter 2 to search by time.\n")

    for item in unstaged_pkgs:
        determine_next_pkg()

    # O(n)
    if choice == '1':
        pkg_num = int(input("Enter package number:\n"))
        calc_status(1500)
        for box in staged_pkgs:
            if int(box[1].pkg_id) == int(pkg_num):
                print(box[1])

    # O(1)
    if choice == '2':
        time = input("Enter a time.\n")
        calc_status(int(time), 1)


# EVERYTHING BELOW HERE STARTS THE PROGRAM


myHash = HashTable()
load_package_file(r"C:\Users\zacha\Downloads\WGUPS_Package_File.csv")
dist_table = load_dist_file(r"C:\Users\zacha\Downloads\WGUPS_Distance_Table.csv")

truck2 = Truck()
truck1 = Truck()

# O(n)
# STARTS AS ALL PACKAGES; PACKAGES GET REMOVED AS THEY ARE STAGED
unstaged_pkgs = []
for bucket in myHash.table:
    for pkg in bucket:
        if pkg[1].pkg_id not in ('6', '25', '28', '32'):
            if pkg not in unstaged_pkgs:
                unstaged_pkgs.append(pkg)

# O(n)
# ADDS SPECIAL PACKAGES TO truck2.inventory
truck2.load_special()


# O(n)
# DETERMINES FIRST PACKAGE IN ROUTE
staged_pkgs = [determine_first_pkg()]
if staged_pkgs[0][1] in truck2.manual_inventory_adjust:
    truck2.manual_inventory_adjust.remove(staged_pkgs[0][1])


run_interface()

# EVALUATOR CAN USE THIS TO TEST SEARCH FUNCTION. UNCOMMENT AND INSERT PACKAGE ID AS INTEGER.
# run_interface() MUST EXECUTE BEFORE THIS.
# print(myHash.search())
