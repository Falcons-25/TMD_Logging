from pymavlink import mavutil
import sys
import serial, serial.serialutil, serial.tools.list_ports
import time

def connect_arduino(port, baud) -> bool:
    global ser
    try:
        ser = serial.Serial(port=port, baudrate=baud)
        return True
    except serial.serialutil.SerialException:
        print("Error with arduino serial port.")
        return False

def connect_mavlink(device, baud) -> bool:
    global connection
    connection = mavutil.mavlink_connection(device=device, baud=baud)
    try:
        msg = connection.wait_heartbeat(timeout=5)
        print(msg)
        print(f"Heartbeat received from system {connection.target_system}, component {connection.target_component}")
        return True
    except mavutil.mavlink.MAVError:
        print("No heartbeat received.")
        return False

def setup():
    """
    0  - Accepted
    1  - Temporarily Rejected
    2  - Denied
    3  - Unsupported
    4  - Failed
    5  - In Progress
    6  - Cancelled
    7  - long-only
    8  - int-only
    9  - Unsupported Frame
    10 - Permission Denied
    """
    # get com
    with open("config.txt", 'r') as file:
        data = file.readlines()
        if len(data):
            serial_com = data[0].strip().split(',')[0].strip()
            serial_baud = data[0].strip().split(',')[1].strip()
            mavlink_com = data[1].strip().split(',')[0].strip()
            mavlink_baud = data[1].strip().split(',')[1].strip()
        else:
            serial_com = ""
            mavlink_com = ""
    if serial_com and mavlink_com:
        print(f"Serial COM : {serial_com}, {serial_baud}\nMAVLink COM: {mavlink_com}, {mavlink_baud}")
        s = input("Use last configuration? y/n: ")
        if s in 'Yy':
            pass
        else:
            comports = sorted([str(x) for x in serial.tools.list_ports.comports()])
            for (i, port) in enumerate(comports):
                print(f"{i+1}. {port}")
            serial_com = comports[int(input("Choose serial COM Port: "))-1]
            serial_baud = int(input("Enter serial port baud: "))
            mavlink_com = comports[int(input("Choose MAVLink COM Port: "))-1]
            mavlink_baud = int(input("Enter MAVLink baud: "))
            with open("coms.txt", 'w') as file:
                print(f"{serial_com}, {serial_baud}", file=file)
                print(f"{mavlink_com}, {mavlink_baud}", file=file)
    a = connect_arduino(serial_com, serial_baud)
    b = connect_mavlink(mavlink_com, mavlink_baud)
    if a and b:
        print("COM Ports set up correctly.")
    else:
        print("Data inputs not initialised correctly.")
        print(f"Serial ({serial_com}): {a}\nMAV ({mavlink_com}): {b}")
        sys.exit(0)

    # testing component selection
    with open("config.txt", 'r') as file:
        data = [x.strip() for x in file.readlines()]
        motor = data[2]
        kv = data[3]
        esc = data[4]
        batt = data[5]
        prop = data[6]
        print(f"{prop}\n{motor} ({kv}KV)\n{esc}\n{batt}")
        s = input("Testing same configuration? ")
        if s in 'yY':
            pass
        else:
            n = 1
            while n:
                print("1> Prop\n2> Motor\n3> ESC\n4> Battery")
                n = int(input("Update: "))
                if n==1:
                    # print available, pick number
                    pass
                elif n==2:
                    pass
                elif n==3:
                    pass
                elif n==4:
                    pass
            print(f"{prop}\n{motor} ({kv}KV)\n{esc}\n{batt}")
            print("Configuration confirmed.")
    with open("TM_log.csv", 'a') as file:
        print(f"{time.strftime("%Y-%m-%d %H:%M:%S")},{prop},{motor} ({kv}),{esc},{batt}")

    print("Setting up MAVLink data...")
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 34, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "RC_CHANNELS_SCALED set to 5Hz", sep='\n')
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 35, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "RC_CHANNELS_RAW set to 5Hz", sep='\n')
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 65, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "RC_CHANNELS set to 5Hz", sep='\n')
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 147, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "BATTERY_STATUS set to 5Hz", sep='\n')
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 290, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "ESC_INFO set to 5Hz", sep='\n')
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 291, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "ESC_STATUS set to 5Hz", sep='\n')
    # ?
    connection.mav.command_long_send(
        connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 235, 200000, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(blocking=True, type="COMMAND_ACK")
    print(msg, "HIGH_LATENCY2 set to 5Hz", sep='\n')
    print("MAVLink data rate set up.")

def loop():
    voltage = 0
    voltage2 = 0
    current = 0
    current2 = 0
    charge = 0
    throttle = 0
    thrust = 0
    rpm = 0
    all = 0b00000000
    try:
        with open("TM_Log.csv", 'a') as file:
            print("Starting data logging.")
            while True:
                msg = connection.recv_match(blocking=True, type=["BATTERY_STATUS", "RC_CHANNELS_SCALED", "RC_CHANNELS", "RC_CHANNELS_RAW", "ESC_INFO", "ESC_STATUS", "HIGH_LATENCY2"])
                print(msg)
                if msg.get_type() == "BATTERY_STATUS":
                    voltage = msg.voltages[0]
                    all = all | 0b00001000
                    current = msg.current_battery/100
                    all = all | 0b00100000
                    charge = msg.current_consumed
                    all = all | 0b00000001
                elif msg.get_type() == "RC_CHANNELS":
                    throttle = msg.chan1_raw                        # adjust
                    throttle = int(throttle)
                    print(f"RC_CHANNELS:        {throttle}")
                    all = all | 0b10000000
                elif msg.get_type() == "RC_CHANNELS_RAW":
                    throttle = msg.chan1_raw                        # adjust
                    print(f"RC_CHANNELS_RAW:    {throttle}")
                    all = all | 0b10000000
                elif msg.get_type() == "RC_CHANNELS_SCALED":
                    throttle = msg.chan1_scaled                     # adjust
                    print(f"RC_CHANNELS_SCALED: {throttle}")
                    all = all | 0b10000000
                elif msg.get_type()=="ESC_INFO":
                    print(msg.connection_type, msg.failure_flags)   # adjust
                elif msg.get_type()=="ESC_STATUS":
                    voltage2 = msg.voltage[0]
                    all = all | 0b00000100
                    current2 = msg.current[0]
                    all = all | 0b00010000
                    rpm = msg.rpm
                    all = all | 0b00000010
                elif msg.get_type()=="HIGH_LATENCY2":
                    throttle = msg.throttle
                    print(f"HIGH_LATENCY2: {throttle}")
                    all = all | 0b10000000
                thrust = ser.readline().strip()
                data = f"{time.strftime("%Y-%m-%d %H:%M:%S")},{throttle},{thrust},{(current*voltage):.2f},{current:.2f},{current2},{voltage:.3f},{voltage2},{rpm},{charge}"
                print(data)
                if (all|0b00010110)==0b11111111:
                    print(data, file=file)
                    all = 0
    except KeyboardInterrupt:
        with open("TM_log.csv", 'a') as file:
            print(file=file)
        print("User terminated execution.")
        sys.exit(0)

if __name__ == "__main__":
    print("Setting up...")
    setup()
    print("Setup complete.")
    print("Starting logging...")
    loop()
