import serial
import time

port = 'COM5'
baud = 9600
maxChar = 16

try:
    print(f"Searching for Arduino at port {port} with baud {baud}.")
    ser = serial.Serial(port, baud, timeout=1)
    print(f"Found Arduino at port {port} with baud {baud}.\nConnecting to Arduino at port {port} with baud {baud}.")
    time.sleep(2)
    print(f"Connected to Arduino at port {port} with baud {baud}.")

    while True:
        comm = str(input(f"Enter a string with a character limit of {maxChar} or 'q' to quit.\n\t").strip())

        if len(comm) > maxChar:
            print(f"Too many characters were entered. The maximum limit is {maxChar}.")
            continue

        elif len(comm) == 0:
            print(f"No characters were entered. The maximum limit is {maxChar}.")

        elif comm == "q":
            break

        else:
            print(f"Sending {comm} to the Arduino to print.")
            ser.write((comm + "\n").encode())
            time.sleep(0.1)
            timeout_start = time.time()
            while ser.in_waiting == 0:
                if time.time() - timeout_start > 2:  # 2-second timeout
                    print(f"Failed to send {comm} to the Arduino to print.")
                    break

            response = ser.readline().decode('utf-8').strip()
            print(f"Sent {response} to the Arduino to print.")

except serial.SerialException as error:
    print(f"The connection to port {port} has failed. Ensure the Arduino is plugged in and the Serial Monitor in the Arduino IDE is closed, then try again.\n{error}")
except Exception as error:
    print(f"An unknown exception occurred.\n{error}")
finally:
    print(f"Closing connection to Arduino at port {port} with baud {baud}.")
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Closed connection to port {port} with baud {baud}.")
    else:
        print(f"The connection to port {port} was not found.")
    print("Program complete.")
