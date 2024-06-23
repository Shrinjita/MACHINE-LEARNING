import grovepi
import time

# Connect the DHT sensor to the GrovePi board on D4 port
dht_sensor_port = 4  # Adjust this port based on your actual connection

while True:
    try:
        # Read data from the DHT sensor
        [temperature, humidity] = grovepi.dht(dht_sensor_port, 0)  # 0 represents the DHT22 sensor

        # Check if data is valid
        if not isnan(temperature) and not isnan(humidity):
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        else:
            print("Failed to read data from the sensor")

        time.sleep(2)  # Read data every 2 seconds (adjust as needed)

    except KeyboardInterrupt:
        break
    except IOError:
        print("Error: Unable to communicate with the sensor")
