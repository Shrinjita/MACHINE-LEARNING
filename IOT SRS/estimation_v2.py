# Here we will be using the triangulation algorithm instead 

import RPi.GPIO as GPIO
import time
import math

# Define the GPIO pins for the ultrasonic sensors
sensor_pins = [4, 17, 18]  # Example GPIO pins, adjust as needed
num_sensors = len(sensor_pins)

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins for ultrasonic sensors
for pin in sensor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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

# Function to estimate position based on triangulation
def estimate_position(d1, d2, d3):
    # Coordinates of the three ultrasonic sensors (adjust as needed)
    x1, y1 = 0, 0
    x2, y2 = 100, 0
    x3, y3 = 0, 100

    # Calculate intermediate values
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = 2 * (x3 - x1)
    D = 2 * (y3 - y1)

    E = d2**2 - d1**2 - x2**2 + x1**2 - y2**2 + y1**2
    F = d3**2 - d1**2 - x3**2 + x1**2 - y3**2 + y1**2

    # Calculate estimated position (x, y)
    x = (E * D - B * F) / (A * D - B * C)
    y = (E * C - A * F) / (B * C - A * D)

    return x, y

try:
    while True:
        # Measure distances from three ultrasonic sensors
        d1 = measure_distance(sensor_pins[0], sensor_pins[0])
        d2 = measure_distance(sensor_pins[1], sensor_pins[1])
        d3 = measure_distance(sensor_pins[2], sensor_pins[2])

        # Estimate position based on triangulation
        x, y = estimate_position(d1, d2, d3)

        print(f"Estimated Position: ({x:.2f} cm, {y:.2f} cm)")

        time.sleep(2)  # Adjust the sleep time as needed

except KeyboardInterrupt:
    GPIO.cleanup()
