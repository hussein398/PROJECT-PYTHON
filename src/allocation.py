import pandas as pd
import random
import numpy as np

def random_allocation(hotels, guests, preferences):
    # Shuffle the guests randomly
    guests = guests.sample(frac=1).reset_index(drop=True)
    
    # List to store allocation details
    allocation_records = []
    
    # Track the availability of rooms in each hotel (deep copy to modify counts)
    available_rooms = hotels.copy()

    for _, guest in guests.iterrows():
        # Check if any rooms are still available
        if available_rooms.empty:
            break  # Stop if no rooms are left
        
        # Randomly select a room from the available rooms
        room = available_rooms.sample(n=1).iloc[0]
        
        # Calculate the price paid with discount
        discount = guest['discount']  # Assuming discount is a fraction (e.g., 0.1 for 10%)
        price_paid = room['price'] * (1 - discount)
        
        # Retrieve the preference priority for the current guest and assigned hotel
        guest_preferences = preferences[(preferences['guest'] == guest['guest']) & (preferences['hotel'] == room['hotel'])]
        
        if not guest_preferences.empty:
            # Get the priority; lower priority value means higher satisfaction score
            priority = guest_preferences['priority'].iloc[0]
            satisfaction_score = 1 / priority  # Higher priority (1) results in a higher score (1.0)
        else:
            # If no preference is found, assign a default low satisfaction score
            satisfaction_score = 0.1  # Default score if no preference is listed
        
        # Record the allocation
        allocation_records.append({
            'guest_id': guest['guest'],
            'hotel_id': room['hotel'],
            'room_id': room['rooms'],
            'price_paid': price_paid,
            'discount_applied': discount,
            'satisfaction_score': satisfaction_score
        })
        
        # Decrement the room count for the assigned hotel
        available_rooms.loc[room.name, 'rooms'] -= 1
        if available_rooms.loc[room.name, 'rooms'] == 0:
            # If no rooms are left in the hotel, remove it from the available list
            available_rooms = available_rooms.drop(room.name)

    # Convert allocation records to a DataFrame and sort by satisfaction score
    allocation_df = pd.DataFrame(allocation_records, columns=['guest_id', 'hotel_id', 'room_id', 'price_paid', 'discount_applied', 'satisfaction_score'])
    allocation_df = allocation_df.sort_values('satisfaction_score', ascending=False)
    
    return allocation_df


def preference_allocation(hotels, guests, preferences):
    # Initialize an empty list to store allocation records
    allocation_records = []
    
    # Track available rooms in each hotel (deep copy to modify room counts)
    available_rooms = hotels.copy()

    for _, guest in guests.iterrows():
        # Retrieve the guest's preferences in priority order
        guest_preferences = preferences[preferences['guest'] == guest['guest']].sort_values('priority')
        
        allocated = False  # Flag to check if guest has been allocated a room

        # Try to allocate a room based on preferences
        for _, pref in guest_preferences.iterrows():
            if allocated:
                break  # Stop if room has already been allocated

            # Check if there are available rooms in the preferred hotel
            preferred_hotel_rooms = available_rooms[available_rooms['hotel'] == pref['hotel']]
            if not preferred_hotel_rooms.empty:
                # Allocate the first available room in the preferred hotel
                room = preferred_hotel_rooms.iloc[0]
                
                # Calculate the price paid with discount
                discount = guest['discount']  # Assuming discount is a fraction (e.g., 0.1 for 10% discount)
                price_paid = room['price'] * (1 - discount)
                
                # Calculate satisfaction score based on preference priority
                satisfaction_score = 1 / pref['priority']  # Higher priority gives a higher score (e.g., priority 1 gives 1.0)
                
                # Record the allocation
                allocation_records.append({
                    'guest_id': guest['guest'],
                    'hotel_id': room['hotel'],
                    'room_id': room['rooms'],
                    'price_paid': price_paid,
                    'discount_applied': discount,
                    'satisfaction_score': satisfaction_score
                })
                
                # Decrement room availability for the allocated hotel
                available_rooms.loc[room.name, 'rooms'] -= 1
                if available_rooms.loc[room.name, 'rooms'] == 0:
                    # If no rooms are left in the hotel, remove it from available rooms
                    available_rooms = available_rooms.drop(room.name)
                
                allocated = True  # Set flag indicating allocation is complete

        # If no preferred room is available, assign a random room
        if not allocated and not available_rooms.empty:
            room = available_rooms.sample(n=1).iloc[0]
            
            # Calculate the price paid with discount
            discount = guest['discount']
            price_paid = room['price'] * (1 - discount)
            
            # Set a default low satisfaction score for a non-preferred room
            satisfaction_score = 0.0  # Adjust as needed
            
            # Record the allocation
            allocation_records.append({
                'guest_id': guest['guest'],
                'hotel_id': room['hotel'],
                'room_id': room['rooms'],
                'price_paid': price_paid,
                'discount_applied': discount,
                'satisfaction_score': satisfaction_score
            })
            
            # Decrement room availability for the randomly assigned hotel
            available_rooms.loc[room.name, 'rooms'] -= 1
            if available_rooms.loc[room.name, 'rooms'] == 0:
                # If no rooms are left in the hotel, remove it from available rooms
                available_rooms = available_rooms.drop(room.name)

    # Convert allocation records to DataFrame and sort by satisfaction score in descending order
    allocation_df = pd.DataFrame(allocation_records, columns=['guest_id', 'hotel_id', 'room_id', 'price_paid', 'discount_applied', 'satisfaction_score'])
    allocation_df = allocation_df.sort_values('satisfaction_score', ascending=False).reset_index(drop=True)
    
    return allocation_df

def price_allocation(hotels, guests, preferences):
    # Sort rooms by price in ascending order (cheapest first)
    available_rooms = hotels.sort_values('price').reset_index(drop=True)
    
    # DataFrame to store allocation records
    allocation_records = []

    for _, guest in guests.iterrows():
        # Check if any rooms are still available
        if available_rooms.empty:
            break  # Stop if no rooms are left

        # Allocate the cheapest room available
        room = available_rooms.iloc[0]
        
        # Calculate the price paid with discount
        discount = guest['discount']  # Assuming discount is a fraction (e.g., 0.1 for 10% discount)
        price_paid = room['price'] * (1 - discount)
        
        # Retrieve the preference priority for the current guest and assigned hotel
        guest_preferences = preferences[(preferences['guest'] == guest['guest']) & (preferences['hotel'] == room['hotel'])]
        
        if not guest_preferences.empty:
            # Get the priority; lower priority value means higher satisfaction score
            priority = guest_preferences['priority'].iloc[0]
            satisfaction_score = 1 / priority  # Higher priority (1) results in a higher score (1.0)
        else:
            # If no preference is found, assign a default low satisfaction score
            satisfaction_score = 0.1  # Default score if no preference is listed

        # Record the allocation
        allocation_records.append({
            'guest_id': guest['guest'],
            'hotel_id': room['hotel'],
            'room_id': room['rooms'],
            'price_paid': price_paid,
            'discount_applied': discount,
            'satisfaction_score': satisfaction_score
        })
        
        # Decrement the room count for the assigned hotel
        available_rooms.loc[room.name, 'rooms'] -= 1
        if available_rooms.loc[room.name, 'rooms'] == 0:
            # If no rooms are left, remove the hotel from the available list
            available_rooms = available_rooms.drop(room.name).reset_index(drop=True)

    # Convert allocation records to DataFrame and sort by satisfaction score in descending order
    allocation_df = pd.DataFrame(allocation_records, columns=['guest_id', 'hotel_id', 'room_id', 'price_paid', 'discount_applied', 'satisfaction_score'])
    allocation_df = allocation_df.sort_values('satisfaction_score', ascending=False).reset_index(drop=True)
    
    return allocation_df


def availability_allocation(hotels, guests, preferences):
    # Sort hotels by room availability in descending order (most rooms first)
    available_rooms = hotels.sort_values('rooms', ascending=False).reset_index(drop=True)
    
    # DataFrame to store allocation records
    allocation_records = []

    for _, guest in guests.iterrows():
        # Check if any rooms are still available
        if available_rooms.empty:
            break  # Stop if no rooms are left

        # Allocate a room from the hotel with the highest room availability
        room = available_rooms.iloc[0]
        
        # Calculate the price paid with discount
        discount = guest['discount']  # Assuming discount is a fraction (e.g., 0.1 for 10% discount)
        price_paid = room['price'] * (1 - discount)
        
        # Retrieve the preference priority for the current guest and assigned hotel
        guest_preferences = preferences[(preferences['guest'] == guest['guest']) & (preferences['hotel'] == room['hotel'])]
        
        if not guest_preferences.empty:
            # Get the priority; lower priority value means higher satisfaction score
            priority = guest_preferences['priority'].iloc[0]
            satisfaction_score = 1 / priority  # Higher priority (1) results in a higher score (1.0)
        else:
            # If no preference is found, assign a default low satisfaction score
            satisfaction_score = 0.1  # Default score if no preference is listed

        # Record the allocation
        allocation_records.append({
            'guest_id': guest['guest'],
            'hotel_id': room['hotel'],
            'room_id': room['rooms'],
            'price_paid': price_paid,
            'discount_applied': discount,
            'satisfaction_score': satisfaction_score
        })
        
        # Decrement room availability for the allocated hotel
        available_rooms.at[0, 'rooms'] -= 1
        if available_rooms.at[0, 'rooms'] == 0:
            # If no rooms are left, remove the hotel from the list
            available_rooms = available_rooms.drop(available_rooms.index[0]).reset_index(drop=True)

    # Convert allocation records to DataFrame and sort by satisfaction score in descending order
    allocation_df = pd.DataFrame(allocation_records, columns=['guest_id', 'hotel_id', 'room_id', 'price_paid', 'discount_applied', 'satisfaction_score'])
    allocation_df = allocation_df.sort_values('satisfaction_score', ascending=False).reset_index(drop=True)
    
    return allocation_df
