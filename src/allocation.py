import pandas as pd
import random
import numpy as np

# Load the datasets
hotels = pd.read_excel('..\\data\\hotels.xlsx')
guests = pd.read_excel('..\\data\\guests.xlsx')
preferences = pd.read_excel('..\\data\\preferences.xlsx')

# Set pandas options to display all rows
pd.set_option('display.max_rows', None)  # Show all rows

# Display the datasets
print("Hotels Data:")
print(len(hotels))

print("\nGuests Data:")
print(len(guests))

print("\nPreferences Data:")
print(len(preferences))

def random_allocation(hotels, guests):
    # Shuffle the guests randomly
    guests = guests.sample(frac=1).reset_index(drop=True)
    
    # List to store allocation details
    allocation_records = []
    
    # Track the availability of rooms in each hotel
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
        
        # Calculate satisfaction score (for random strategy, we'll set it arbitrarily)
        satisfaction_score = np.random.uniform(0.5, 1)  # Random satisfaction score
        
        # Record the allocation
        allocation_records.append({
            'guest_id': guest['guest'],
            'hotel_id': room['hotel'],
            'room_id': room['rooms'],
            'price_paid': price_paid,
            'discount_applied': discount,
            'satisfaction_score': satisfaction_score
        })
        
        # Remove the assigned room from available rooms
        available_rooms = available_rooms.drop(room.name)

    # Convert allocation records to a DataFrame
    allocation_df = pd.DataFrame(allocation_records, columns=['guest_id', 'hotel_id', 'room_id', 'price_paid', 'discount_applied', 'satisfaction_score'])
    return allocation_df
allocation_result = random_allocation(hotels, guests)
print(allocation_result)
