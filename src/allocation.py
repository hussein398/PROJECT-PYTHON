import pandas as pd
import random

# Define the absolute path to the directory where the files are located
path_to_files = r'C:\Users\Hussein\Desktop\kalb\\'

# Load the datasets
hotels = pd.read_excel(path_to_files + 'hotels.xlsx')
guests = pd.read_excel(path_to_files + 'guests.xlsx')
preferences = pd.read_excel(path_to_files + 'preferences.xlsx')

# Set pandas options to display all rows
pd.set_option('display.max_rows', None)  # Show all rows

# Display the datasets
print("Hotels Data:")
print(hotels)

print("\nGuests Data:")
print(guests)

print("\nPreferences Data:")
print(preferences)

# Allocation functions

def random_allocation(hotels, guests):
    allocation = {}
    available_rooms = hotels.set_index('hotel')['rooms'].to_dict()

    for guest in guests['guest']:
        available_hotels = [hotel for hotel, rooms in available_rooms.items() if rooms > 0]
        if available_hotels:
            selected_hotel = random.choice(available_hotels)
            allocation[guest] = selected_hotel
            
            # Decrement the room count
            available_rooms[selected_hotel] -= 1
            
            if available_rooms[selected_hotel] == 0:
                del available_rooms[selected_hotel]
    return allocation


def customer_preference_allocation(hotels, guests, preferences):
    allocation = {}
    available_rooms = hotels.set_index('hotel')['rooms'].to_dict()

    for guest in guests['guest']:
        guest_preferences = preferences[preferences['guest'] == guest].sort_values('priority')['hotel'].tolist()
        
        for preferred_hotel in guest_preferences:
            if preferred_hotel in available_rooms and available_rooms[preferred_hotel] > 0:
                allocation[guest] = preferred_hotel
                available_rooms[preferred_hotel] -= 1
                
                if available_rooms[preferred_hotel] == 0:
                    del available_rooms[preferred_hotel]
                break
    return allocation


def price_based_allocation(hotels, guests):
    allocation = {}
    available_rooms = hotels.set_index('hotel')['rooms'].to_dict()
    
    # Debugging: Print available hotels at the start
    print("Available Hotels at the start:", available_rooms.keys())
    
    # Sort hotels by price (ascending)
    sorted_hotels = hotels.sort_values('price')
    
    for guest in guests['guest']:
        for _, hotel in sorted_hotels.iterrows():
            hotel_name = hotel['hotel']
            print(f"Checking availability for hotel: {hotel_name}")  # Debugging line
            
            if hotel_name in available_rooms and available_rooms[hotel_name] > 0:
                allocation[guest] = hotel_name
                available_rooms[hotel_name] -= 1
                
                if available_rooms[hotel_name] == 0:
                    print(f"No more rooms available in {hotel_name}. Removing from available hotels.")  # Debugging line
                    del available_rooms[hotel_name]
                break
    return allocation


def availability_based_allocation(hotels, guests):
    allocation = {}
    available_rooms = hotels.set_index('hotel')['rooms'].to_dict()

    # Sort hotels by availability (descending)
    sorted_hotels = hotels.sort_values('rooms', ascending=False)
    
    for guest in guests['guest']:
        for _, hotel in sorted_hotels.iterrows():
            hotel_name = hotel['hotel']
            if hotel_name in available_rooms and available_rooms[hotel_name] > 0:
                allocation[guest] = hotel_name
                available_rooms[hotel_name] -= 1
                
                if available_rooms[hotel_name] == 0:
                    del available_rooms[hotel_name]
                break
    return allocation

# Example usage of allocation functions
allocation_random = random_allocation(hotels, guests)
allocation_preference = customer_preference_allocation(hotels, guests, preferences)
allocation_price = price_based_allocation(hotels, guests)
allocation_availability = availability_based_allocation(hotels, guests)

# Display the allocation results
print("\nRandom Allocation Result:")
print(allocation_random)

print("\nCustomer Preference Allocation Result:")
print(allocation_preference)

print("\nPrice-Based Allocation Result:")
print(allocation_price)

print("\nAvailability-Based Allocation Result:")
print(allocation_availability)

# Reset pandas option to avoid displaying too many rows in the future
pd.reset_option('display.max_rows')

