import grovepi
import time

# Connect the light sensor to the GrovePi board on A0 port
light_sensor_port = 0

while True:
    try:
        light_intensity = grovepi.analogRead(light_sensor_port)
        print(f"Light Intensity: {light_intensity}")
        time.sleep(2)

    except KeyboardInterrupt:
        break
    except IOError:
        print("Error: Unable to communicate with the sensor")
