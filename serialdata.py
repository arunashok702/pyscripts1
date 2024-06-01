#!/usr/bin/env python3

import socket
import serial
import time

# Configure your URL and UART settings
host = '127.0.0.1'   #ip of local host
port = 7878    
uart_device = "/dev/ttyS3" #this tty3 is the UART3 RX and TX
baudrate = 115200  #This same baud rate need to be set for both devices ESP32
interval = 1  # in seconds

def fetch_data():
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            while True:
                data = sock.recv(4096).decode('utf-8')  # Receive data
                if not data:
                    break
                lines = data.split('\n')  # Split data by newline
                for line in lines:
                    yield line.strip()  # Yield each line
    except socket.error as e:
        print(f"Error fetching data: {e}")

def send_via_uart(data):
    try:
        with serial.Serial(
            uart_device,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1,
        ) as uart3:
            uart3.write((data + '\n').encode('utf-8'))  # Ensure each message is newline-terminated
            print(f"Sent data: {data}")
    except Exception as e:
        print(f"Error sending data via UART: {e}")

def main():
    for line in fetch_data():
        if line:
            send_via_uart(line)
        else:
            send_via_uart("no connection established")
        time.sleep(interval)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
