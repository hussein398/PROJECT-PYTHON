import pandas as pd
import os

# Function to generate the report
def generate_report(file_path):
    # Extract the allocation name from the file name
    allocation_name = os.path.splitext(os.path.basename(file_path))[0]

    # Read the data from the Excel file
    df = pd.read_excel(file_path)

    # Calculate metrics
    total_customers = df['guest_id'].nunique()
    total_rooms_occupied = df[['hotel_id', 'room_id']].drop_duplicates().shape[0]  # Unique hotel_id + room_id combinations
    total_hotels_occupied = df['hotel_id'].nunique()
    total_volume_of_business = df['price_paid'].sum()
    average_satisfaction_score = df['satisfaction_score'].mean()

    # Group by hotel to calculate individual hotel statistics
    df['hotel_room_combination'] = df['hotel_id'].astype(str) + '_' + df['room_id'].astype(str)
    hotel_stats = df.groupby('hotel_id').agg({
        'guest_id': 'nunique',  # Number of unique customers
        'hotel_room_combination': 'nunique',  # Number of unique hotel + room combinations
        'price_paid': 'sum',    # Total earnings
        'satisfaction_score': 'mean'  # Average satisfaction score
    }).rename(columns={
        'guest_id': 'customers_accommodated',
        'hotel_room_combination': 'rooms_occupied',
        'price_paid': 'total_earnings',
        'satisfaction_score': 'avg_satisfaction_score'
    }).reset_index()

    # Print the overall report
    print(f"Overall Report for Allocation: {allocation_name}")
    print("-----------------")
    print(f"Total Customers Accommodated: {total_customers}")
    print(f"Total Rooms Occupied: {total_rooms_occupied}")
    print(f"Total Hotels Occupied: {total_hotels_occupied}")
    print(f"Total Volume of Business: ${total_volume_of_business:.2f}")
    print(f"Overall Average Satisfaction Score: {average_satisfaction_score:.2f}\n")
    print("----------------------------------------------------------")

allocation_files=["..\\results\\availability_allocation.xlsx", "..\\results\\preference_allocation.xlsx", "..\\results\\price_allocation.xlsx","..\\results\\random_allocation.xlsx"]

for file in allocation_files:
    generate_report(file)
