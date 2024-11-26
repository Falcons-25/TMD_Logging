import serial, serial.serialutil, serial.tools.list_ports
import sys
import time

def set_comport(port: str):
    ser = serial.Serial(port=port, baudrate=57600)
    print("serial initialised.")
    try:
        with open("serial_log.csv", "a") as file:
            while True:
                data = [str(x) for x in ser.readline().decode().strip().split(",")]
                try:
                    # thrust = 0.82 - float(data[0])
                    thrust = 0
                    throttle = int(float(data[1]))
                except ValueError:
                    print(data)
                    continue
                except IndexError:
                    print(data)
                    continue
                # thrust = 0.82 - float(data[0])
                thrust = 0
                throttle = int(float(data[1]))
                print(f"{time.strftime('%H:%M:%S')},{thrust:.5f},{throttle}")
                # print(f"{time.strftime('%H:%M:%S')},{thrust:.5f},{throttle}", file=file)
                # print(f"{time.strftime('%H:%M:%S')},{thrust:.5f}", file=file)
    except serial.serialutil.SerialException:
        print("Arduino disconnected.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("User terminated ops.")
        sys.exit(0)

comports = sorted([str(x) for x in serial.tools.list_ports.comports()])
if comports:
    if len(comports)!=1:
        print("Select a COM port for data input:")
        for i, port in enumerate(comports):
            print(f"{i+1}. {port}")
        selected_port = comports[int(input("Enter option: "))-1].split()[0]
    else: selected_port = comports[0].split()[0]
    try:
        set_comport(selected_port)
    except KeyboardInterrupt:
        error_code = 2
        sys.exit(0)
else:
    sys.exit(0)
