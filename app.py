import serial
import serial.tools.list_ports
import platform
import time
import keyboard

os_type = platform.system()

def test_menu():
    global ser
    ser.write(b"okay\n")    
    print("Opening test menu...")
    line_1 = ser.readline().decode().strip()
    print(f"{line_1}")

def connect_device():
    global sd_card
    global port
    global ser
    PICO_VID = "2E8A"

    def find_pico():
        for p in serial.tools.list_ports.comports():
            if p.vid is not None and hex(p.vid).upper().replace("0X", "") == PICO_VID:
                return p.device
        return None

    port = find_pico()

    if not port:
        print("Device not found")
        exit()

    ser = serial.Serial(port, 115200)
    print("Connected:", port)
    ser.write(b"connected\n")
    while True:
        line1 = ser.readline().decode().strip()
        line2 = ser.readline().decode().strip()

        output = f"{line1}\n{line2}"
        if line1 == "button_down":
            test_menu()
            break
        else:
            if line1 == "okay" and line2 == "True":
                    print("Connection confirmed by device.")
                    sd_card = True
                    print(f"SD Card detected: {sd_card}")
                    

            elif line1 == "okay" and line2 == "False":
                print("Connection confirmed by device.")
                sd_card = False
                print(f"SD Card detected: {sd_card}")
                
            time.sleep(3)
            
            for i in range(3):
                for i in range(4):
                    print("\033c", end="")
                    print("Loading" + "." * (i % 4))
                    time.sleep(0.4)
            print("\033c", end="")
            hello()
            break

def ask_device_what_can_do():
    global ser
    ser.write(b"what_can_do\n")
    while True:
        line1 = ser.readline().decode().strip()
        line2 = ser.readline().decode().strip()
        line3 = ser.readline().decode().strip()
        line4 = ser.readline().decode().strip()
        line5 = ser.readline().decode().strip()
        line6 = ser.readline().decode().strip()
        if line1 == "True":
            print("Make password")
        if line2 == "True":
            print("New password")
        if line3 == "True":
            print("Make API's list")
        if line4 == "True":
            print("Edit API's list")
        if line5 == "True":
            print("Read history")
        if line6 == "True":
            print("Edit files")

def hello():
    print("Welcome in πKey")
    print("What you want to do ?")
    ask_device_what_can_do()

def welcome():
    global sd_card
    print(f"OS type: {os_type}")
    print("Connect the device to your computer!")
    print("Searching the device...")
    connect_device()

welcome()