import serial
import time

port = 'COM5'
baud = 9600

try:
    print(f"Connecting to Arduino at port {port} with baud {baud}.")
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino at port {port} with baud {baud}.")

    while True:
        comm = input(f"Enter '0' to turn off the LED, '1' to turn off the LED, and 'q' to quit.").strip().lower()

        if comm == 'q':
            break
        elif comm in ['0', '1']:
            if comm == '0':
                print("Setting LED to OFF.")
            else:
                print("Setting LED to ON.")
            ser.write(comm.encode())
            time.sleep(0.1)
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(f"Set LED to {response}.")
        else:
            print("Invalid command.")
except serial.SerialException as error:
    print(f"The connection to port {port} has failed. Ensure the Arduino is plugged in and the Serial Monitor in the Arduino IDE is closed, then try again.\n{error}")
except Exception as error:
    print(f"An unknown exception occured.\n{error}")
finally:
    print(f"Closing connection to Arduino at port {port} with baud {baud}.")
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Closed connection to port {port} with baud {baud}.")
    else:
        print(f"The connection to port {port} was not found.")
    print("Program complete.")
