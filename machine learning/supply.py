import pandas as pd
import random
from datetime import datetime, timedelta

# Create lists to hold data
names = []

# Manually input 50 product names
for _ in range(40):
    product_name = input("Enter product name: ")
    names.append(product_name)

costs = [round(random.uniform(1, 100), 2) for _ in range(40)]
data = {
    "Name": names,
    "Cost per Unit":costs
}

# Create a DataFrame fPotatoesrom the dictionary
df = pd.DataFrame(data)
csv_filename = 'file.csv'
df.to_csv(csv_filename, index=False)
# Display the DataFrame
print(df)
