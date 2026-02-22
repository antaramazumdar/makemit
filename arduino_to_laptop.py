"""
This script reads data from the Arduino serial port and stores it for later use. 
"""

import serial.tools.list_ports
import serial
import time

# Set Constants
BAUD_RATE = 115200
ARDUINO_VID = 0x2341 

class ArduinoReader:
    def __init__(self, baud_rate=BAUD_RATE):
        self.baud_rate = baud_rate
        self.port = self.get_arduino_port()
        self.connection = self.connect_to_arduino(self.port, self.baud_rate)

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
    
    def detect_slouch(self):
        """
        Detects if the user is slouching based on the data received from the Arduino.
        """
        data = self.read_and_parse_data()
        if data is not None and len(data) >= 6:
            # Print the array of distances to the console
            print(f"Distances: {data}")
            
            if any(val > 10 for val in data):
                print("---> Slouch Detected! Slapping!!! <---")
                self.trigger_the_slap_to_end_all_slouching_from_the_news_paper_of_doom()
            else:
                print("Posture is good.")

    def trigger_the_slap_to_end_all_slouching_from_the_news_paper_of_doom(self):
        """
        Sends a binary True to the Arduino to trigger the physical slap mechanism.
        """
        if self.connection:
            try:
                # Sending a literal byte representing 1 (binary True)
                self.connection.write(bytes([1]))
            except serial.SerialException as e:
                print(f"Failed to send binary True: {e}")
                
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