import time
import winsdk.windows.devices.sensors as sensors

# Get the default accelerometer
accel = sensors.Accelerometer.get_default()

def reading_changed_handler(accel, args):
  """
  Callback function to process accelerometer readings
  """
  reading = args.reading
  print(f"X: {reading.acceleration_x:.2f} g")
  print(f"Y: {reading.acceleration_y:.2f} g")
  print(f"Z: {reading.acceleration_z:.2f} g\n")

# Register the callback function
accel.add_reading_changed(reading_changed_handler)

# Continuously read data (loop can be modified for specific use cases)
while True:
  time.sleep(0.1)