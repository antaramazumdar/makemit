"""
This script reads data from the Arduino serial port and stores it for later use. 
"""

import serial.tools.list_ports
import serial
import time

# Set Constants
BAUD_RATE = 115200

# Slouch distance thresholds (in cm)
MAX_DISTANCE = 40.0   # The distance considered to be a "full slouch"
MIN_DISTANCE = 10.0   # The distance considered to be "perfect posture"


class ArduinoReader:
    def __init__(self, baud_rate=BAUD_RATE):
        self.baud_rate = baud_rate
        self.port = self.get_arduino_port()
        self.connection = self.connect_to_arduino(self.port, self.baud_rate)
        
        # Track how long the user has been leaning
        self.slouch_start_time = None

    def get_arduino_port(self):
        """
        Returns the hardcoded COM port for the Arduino.
        Change this if your Arduino connects to a different port!
        """
        # Hardcoded to COM16 based on the system check
        port = "COM16"
        print(f"Connecting to explicitly defined port: {port}")
        return port

    def connect_to_arduino(self, port_address, baud_rate):
        """
        Connects to the detected serial port.
        """
        if port_address is None:
            return None
            
        try:
            ser = serial.Serial(port_address, baud_rate, timeout=1)
            time.sleep(2) 
            print(f"Successfully connected to {port_address}")
            return ser
        except serial.SerialException as e:
            print(f"Error opening serial port {port_address}: {e}")
            return None

    def read_line(self):
        """
        Reads a single line of data from the Arduino if available.
        """
        if self.connection and self.connection.in_waiting > 0:
            return self.connection.readline().decode('utf-8').strip()
        return None

    def read_and_parse_data(self):
        """
        Reads a line from the Arduino, expecting the format '<val1,val2,val3>'
        and returns a list of parsed numeric values.
        """
        line = self.read_line()
        if line:
            if line.startswith('<') and line.endswith('>'):
                content = line[1:-1]
                values_str = content.split(',')
                try:
                    values = [float(val.strip()) for val in values_str if val.strip()]
                    return values
                except ValueError as e:
                    print(f"Error parsing data: {line} -> {e}")
            else:
                print(f"Malformed data received: {line}")
        return None
    
    def calculate_slouch_intensity(self, data):
        """
        Maps the lowest distance (worst slouch) to a value between 0 and 220.
        (We stop at 220 so it runs the UI, but avoids triggering the physical 900 slap limit 
        until the 2-second timer completes)
        """
        min_dist = min(data)
        if min_dist <= MIN_DISTANCE:
            return 0
        elif min_dist >= MAX_DISTANCE:
            return 220
        else:
            # Scale the distance to a 1-220 byte value.
            ratio = (MAX_DISTANCE - min_dist) / (MAX_DISTANCE - MIN_DISTANCE)
            return int(ratio * 220)

    def send_intensity(self, intensity):
        """
        Sends the byte value to the Arduino to drive the Shrimp Meter.
        """
        if self.connection:
            try:
                self.connection.write(bytes([intensity]))
            except serial.SerialException as e:
                print(f"Failed to send intensity: {e}")

    def detect_slouch(self):
        """
        Detects the degree of slouching and acts on it.
        """
        data = self.read_and_parse_data()
        if data is not None and len(data) >= 6:
            intensity = self.calculate_slouch_intensity(data)
            
            # Continuously send the degree of slouching to the Shrimp Meter
            self.send_intensity(intensity)
            print(f"Distances: {data} | Shrimp Level: {intensity}/220")
            
            if intensity > 128:  # threshold representing 50% slouch
                if self.slouch_start_time is None:
                    # Start the timer!
                    self.slouch_start_time = time.time()
                    print("Slouch detected! Starting 2-second timer...")
                else:
                    elapsed_time = time.time() - self.slouch_start_time
                    
                    if elapsed_time >= 2.0:
                        print(f"---> Slouch Detected for {elapsed_time:.1f}s! SLAPPING!!! <---")
                        self.send_intensity(255)
                        self.slouch_start_time = None
                    else:
                        print(f"Slouching... (Warning: {elapsed_time:.1f}s / 2.0s)")
            else:
                self.slouch_start_time = None
                print("Posture is good.")
                
    def close(self):
        """
        Closes the serial connection.
        """
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    arduino = ArduinoReader()

    if arduino.connection:
        print("Listening for slouching...")
        try:
            while True:
                arduino.detect_slouch()
                # A small delay to prevent maxing out the CPU
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Stopping script...")
        finally:
            arduino.close()
    else:
        print("Could not connect to Arduino. Exiting.")