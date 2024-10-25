import pandas as pd

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

# Optionally reset the option to its default (to avoid displaying too many rows in the future)
pd.reset_option('display.max_rows')

