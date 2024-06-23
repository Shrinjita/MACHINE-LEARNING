import grovepi
import time

# Connect the PIR motion sensor to the GrovePi board on D2 port
pir_sensor_port = 2

while True:
    try:
        motion_detected = grovepi.digitalRead(pir_sensor_port)
        if motion_detected:
            print("Motion detected!")
        else:
            print("No motion detected")
        time.sleep(1)

    except KeyboardInterrupt:
        break
    except IOError:
        print("Error: Unable to communicate with the sensor")
