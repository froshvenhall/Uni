#!/usr/bin/python3

import reservationapi
import configparser
import sys
import time

# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Create an API object to communicate with the band API
band  = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

def parallel_slots(hotel_list, band_list):
    list_parallels = []
    for i in range(0, len(hotel_list)):
        for j in range(0, len(band_list)):
            if (hotel_list[i] == band_list[j]):
                list_parallels.append(hotel_list[i]["id"])
                
    return list_parallels
                
def book_common_slot():
    for i in range(0, 3): 
        slots_held = hotel.get_slots_held()
        # if there are less than 2 reservations
        if (len(slots_held) < 2):

            common_slots = parallel_slots(hotel.get_slots_available(), band.get_slots_available())

            hotel.reserve_slot(common_slots[0])
            band.reserve_slot(common_slots[0]) 
        
        # If there are already 2 reservations
        else:
            common_slots = parallel_slots(hotel.get_slots_available(), band.get_slots_available())
            for k in range(0, len(common_slots)):
                if ((int(common_slots[k]) > int(slots_held[0]["id"])) and (int(common_slots[k]) > int(slots_held[1]["id"]))):
                    break
                elif ((int(common_slots[k]) < int(slots_held[0]["id"])) or int(common_slots[k]) < int(slots_held[1]["id"])):
                    if (int(slots_held[0]["id"]) < int(slots_held[1]["id"])):
                        hotel.release_slot(slots_held[1]["id"])
                        hotel.reserve_slot(common_slots[k])

                        band.release_slot(slots_held[1]["id"])
                        band.reserve_slot(common_slots[k])
                    else:
                        hotel.release_slot(slots_held[0]["id"])
                        hotel.reserve_slot(common_slots[k])

                        band.release_slot(slots_held[0]["id"])
                        band.reserve_slot(common_slots[k])
                else:
                    break

    # clean up, keep soonest booked slot and check slots match
    slots_held = hotel.get_slots_held()
    if (int(len(slots_held)) > 1):
        if (int(slots_held[0]["id"]) > int(slots_held[1]["id"])):
            hotel.release_slot(slots_held[0]["id"])
            band.release_slot(slots_held[0]["id"])
        else:
            hotel.release_slot(slots_held[1]["id"])
            band.release_slot(slots_held[1]["id"])

    # make sure bookings match
    slots_held = hotel.get_slots_held()
    if (slots_held[0] != band.get_slots_held()[0]):
        hotel.release_slot(slots_held[0]["id"])
        band.release_slot(slots_held[0]["id"])

def main():
    while (True):
        print("\nWelcome to the hotel and band booking system")
        print("ENTER A NUMBER TO RUN A COMMAND:")
        print("1 - view current bookings")
        print("2 - to release slots")
        print("3 - book earliest common slot for band and hotel")
        print("4 - to exit application")

        response = input("> ")
        if (response == "1"):
            print("Hotel slots held: ")
            hotel.get_slots_held()
            print("Band slots held: ")
            band.get_slots_held()

        elif (response == "2"):
            slots = hotel.get_slots_held()
            for i in range(0, len(slots)):
                hotel.release_slot(slots[i]["id"])
            slots = band.get_slots_held()
            for i in range(0, len(slots)):
                band.release_slot(slots[i]["id"])

        elif (response == "3"):
            book_common_slot()

        elif (response == "4"):
            sys.exit()
        
        else:
            print("\nPlease enter a valid input\n")

main()
