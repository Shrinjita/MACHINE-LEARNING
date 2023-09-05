import pandas as pd
import random
from datetime import datetime, timedelta

# Create lists to hold data
names = []

# Manually input 50 product names
for _ in range(3):
    product_name = input("Enter product name: ")
    names.append(product_name)

costs = [round(random.uniform(1, 100), 2) for _ in range(3)]
units = ["pcs", "kg", "liters", "meters", "boxes"]
#suppliers = [input("Enter supplier name: ") for _ in range(3)]
#dates = [input("Enter date of price (YYYY-MM-DD): ") for _ in range(30)]
data = {
    "Name": names,
    "Cost per Unit":costs,
    "Unit of Measurement": [random.choice(units) for _ in range(3)]
    #"Supplier": suppliers,
    #"Date of Price": dates
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)
df.to_csv('file1.csv')
# Display the DataFrame
print(df)
