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

    def close(self):
        """
        Closes the serial connection.
        """
        if self.connection:
            self.connection.close()