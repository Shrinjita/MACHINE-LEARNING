import grovepi
import time

# Connect an LED to the GrovePi board on D3 port
led_port = 3

while True:
    try:
        # Turn the LED on
        grovepi.digitalWrite(led_port, 1)
        time.sleep(1)

        # Turn the LED off
        grovepi.digitalWrite(led_port, 0)
        time.sleep(1)

    except KeyboardInterrupt:
        break
    except IOError:
        print("Error: Unable to control the LED")
