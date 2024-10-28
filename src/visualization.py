import allocation
import pandas as pd
import os

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

# Ensure the results directory exists
results_dir = '..\\results'
os.makedirs(results_dir, exist_ok=True)

# Run and save each allocation strategy
strategies = {
    'random_allocation': allocation.random_allocation,
    'preference_allocation': allocation.preference_allocation,
    'price_allocation': allocation.price_allocation,
    'availability_allocation': allocation.availability_allocation
}

for strategy_name, strategy_func in strategies.items():
    # Run the allocation strategy
    allocation_result = strategy_func(hotels, guests, preferences)
    
    # Save the result to an Excel file in the 'results' directory
    output_file = f"{results_dir}/{strategy_name}.xlsx"
    allocation_result.to_excel(output_file, index=False)
    print(f"{strategy_name} result saved to {output_file}")

print("All allocation strategies have been executed and saved.")
