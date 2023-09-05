import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load your food supply data
data = pd.read_csv('file.csv')

# Assuming your data has features like 'temperature', 'rainfall', 'population', etc.
features = ['temperature', 'rainfall', 'population']
target = 'food_production'

# Split data into features (X) and target (y)
X = data[features]
y = data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Now, you can use the trained model to make predictions for new data
new_data = pd.DataFrame({
        'temperature': [25],
            'rainfall': [100],
                'population': [500000]
                })

predicted_production = model.predict(new_data)
print(f"Predicted Food Production: {predicted_production[0]}")