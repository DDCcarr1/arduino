import serial
import time
import json

#port = 'COM5'
#port = '/dev/cu.usbserial-1420'
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

        if comm == "q":
            break

        elif len(comm) > maxChar:
            print(f"Too many characters were entered. The maximum limit is {maxChar}.")
            continue

        elif len(comm) == 0:
            continue

        else:
            payload = {"text": comm}
            json_string = json.dumps(payload) + "\n"

            print(f"Sending JSON payload of {json_string.strip()}")
            ser.write(json_string.encode('utf-8'))
            timeout_start = time.time()
            while ser.in_waiting > 0:
                if time.time() - timeout_start > 5:
                    print("Error: The Arduino failed to respond within 5 seconds.")
                    break

            response = ser.readline().decode('utf-8').strip()
            print(f"{response}")
            print()
            continue

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
