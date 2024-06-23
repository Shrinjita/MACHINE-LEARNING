import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the ultrasonic sensors
sensor_pins = [4, 17, 18, 27]  # Example GPIO pins, adjust as needed
num_sensors = len(sensor_pins)

# Define the GPIO pins for controlling lights and fans in each zone
zone_pins = {
    "Zone1": {"light_pin": 5, "fan_pin": 6},
    "Zone2": {"light_pin": 13, "fan_pin": 19},
    "Zone3": {"light_pin": 26, "fan_pin": 21},
    "Zone4": {"light_pin": 22, "fan_pin": 23},
}

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins for ultrasonic sensors
for pin in sensor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Set up GPIO pins for lights and fans
for zone, pins in zone_pins.items():
    GPIO.setup(pins["light_pin"], GPIO.OUT)
    GPIO.setup(pins["fan_pin"], GPIO.OUT)
    GPIO.output(pins["light_pin"], GPIO.LOW)
    GPIO.output(pins["fan_pin"], GPIO.LOW)

# Function to measure distance using ultrasonic sensor
def measure_distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound = 343 m/s

    return distance

try:
    while True:
        for zone, pins in zone_pins.items():
            detected = False

            for i in range(num_sensors):
                # Trigger and echo pins for each sensor (adjust as needed)
                trigger_pin = sensor_pins[i]
                echo_pin = sensor_pins[i]

                distance = measure_distance(trigger_pin, echo_pin)

                if distance < 100:  # Adjust this threshold as needed
                    detected = True
                    break

            if detected:
                print(f"Person detected in {zone}")
                GPIO.output(pins["light_pin"], GPIO.HIGH)
                GPIO.output(pins["fan_pin"], GPIO.HIGH)
            else:
                print(f"No person detected in {zone}")
                GPIO.output(pins["light_pin"], GPIO.LOW)
                GPIO.output(pins["fan_pin"], GPIO.LOW)

        time.sleep(2)  # Adjust the sleep time as needed

except KeyboardInterrupt:
    GPIO.cleanup()
