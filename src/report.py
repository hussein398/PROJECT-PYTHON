import pandas as pd
import os
import matplotlib.pyplot as plt

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

    return {
        "allocation_name": allocation_name,
        "total_customers": total_customers,
        "total_rooms_occupied": total_rooms_occupied,
        "total_hotels_occupied": total_hotels_occupied,
        "total_volume_of_business": total_volume_of_business,
        "average_satisfaction_score": average_satisfaction_score
    }

# Plotting function
def visualize_data(reports):
    # Create a directory for figures if it doesn't exist
    figures_dir = "figures"
    os.makedirs(figures_dir, exist_ok=True)

    allocation_names = [r['allocation_name'] for r in reports]
    total_customers = [r['total_customers'] for r in reports]
    total_rooms_occupied = [r['total_rooms_occupied'] for r in reports]
    total_hotels_occupied = [r['total_hotels_occupied'] for r in reports]
    total_volume_of_business = [r['total_volume_of_business'] for r in reports]
    average_satisfaction_scores = [r['average_satisfaction_score'] for r in reports]

    # Bar chart for Total Hotels Occupied
    plt.figure(figsize=(10, 6))
    plt.bar(allocation_names, total_hotels_occupied, color='skyblue')
    plt.title('Total Hotels Occupied per Allocation Strategy')
    plt.xlabel('Allocation Strategy')
    plt.ylabel('Total Hotels Occupied')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'total_hotels_occupied.png'))
    plt.close()

    # Bar chart for Total Volume of Business
    plt.figure(figsize=(10, 6))
    plt.bar(allocation_names, total_volume_of_business, color='green')
    plt.title('Total Volume of Business per Allocation Strategy')
    plt.xlabel('Allocation Strategy')
    plt.ylabel('Total Volume of Business ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'total_volume_of_business.png'))
    plt.close()

    # Bar chart for Average Satisfaction Scores
    plt.figure(figsize=(10, 6))
    plt.bar(allocation_names, average_satisfaction_scores, color='orange')
    plt.title('Average Satisfaction Score per Allocation Strategy')
    plt.xlabel('Allocation Strategy')
    plt.ylabel('Average Satisfaction Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'average_satisfaction_score.png'))
    plt.close()

    # Line chart for Comparison of Metrics
    plt.figure(figsize=(10, 6))
    plt.plot(allocation_names, total_customers, marker='o', label='Total Customers')
    plt.plot(allocation_names, total_rooms_occupied, marker='o', label='Total Rooms Occupied')
    plt.title('Comparison of Customers and Rooms per Allocation Strategy')
    plt.xlabel('Allocation Strategy')
    plt.ylabel('Count')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'comparison_customers_rooms.png'))
    plt.close()

allocation_files = ["..\\results\\availability_allocation.xlsx", "..\\results\\preference_allocation.xlsx", "..\\results\\price_allocation.xlsx", "..\\results\\random_allocation.xlsx"]

reports = []
for file in allocation_files:
    reports.append(generate_report(file))

visualize_data(reports)

