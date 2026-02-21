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
        self.port = self.auto_detect_arduino()
        self.connection = self.connect_to_arduino(self.port, self.baud_rate)

    def auto_detect_arduino(self):
        """
        Automatically detects the COM port of a connected Arduino device.
        """    
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == ARDUINO_VID:
                print(f"Detected Arduino at {port.device}")
                return port.device

        print("No Arduino found. Please check connections.")
        return None

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

    def close(self):
        """
        Closes the serial connection.
        """
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    arduino = ArduinoReader()

    if arduino.connection:
        print("Serial connection established.")
        try:
            while True:
                data = arduino.read_line()
                if data:
                    # Echoing the received data
                    print(data)
        except KeyboardInterrupt:
            print("Program terminated by user.")
        finally:
            arduino.close()
            print("Serial connection closed.")