import serial
import serial.tools.list_ports
import platform
import time
import keyboard
import requests

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

def make_password():
    ser.write(b"make_password\n")

def new_password():
    ser.write(b"new_password\n")

def make_api():
    global ser
    name = input("Name of API: ")
    type_ai = input("Type of AI: ")
    api_key = input("Your API key: ")
    ser.write(b"make_api\n")
    time.sleep(0.1)
    ser.write(f"{name}\n{type_ai}\n{api_key}\n".encode())

def chat_ai():
    global ser
    ser.write(b"chat_ai\n")
    while True:
        line1 = ser.readline().decode().strip()
        line2 = ser.readline().decode().strip()
        line3 = ser.readline().decode().strip()

        if line1:
            name = line1
            type_nice = line2
            api = line3
            break
        
    input_user = input("write something: ")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": api,
            "Content-Type": "application/json"
        },
        json={
            "model": type_nice,
            "messages": [
                {
                    "role": "user",
                    "content": input_user
                }
            ]
        }
    )

    print(response.json()["choices"][0]["message"]["content"])

def edit_api():
    ser.write(b"edit_api\n")

def read_history():
    ser.write(b"read_history\n")

def edit_files():
    ser.write(b"edit_files\n")

def ask_device_what_can_do():
    global ser

    ser.write(b"what_can_do\n")
    can_do = []
    while True:
        line1 = ser.readline().decode().strip()
        line2 = ser.readline().decode().strip()
        line3 = ser.readline().decode().strip()
        line4 = ser.readline().decode().strip()
        line5 = ser.readline().decode().strip()
        line6 = ser.readline().decode().strip()
        line7 = ser.readline().decode().strip()
        if line1 == "True":
            can_do.append(("Make password", make_password))
        if line2 == "True":
            can_do.append(("New password", new_password))
        if line3 == "True":
            can_do.append(("Make API's list", make_api))
        if line4 == "True":
            can_do.append(("Chat with AI's", chat_ai))
            can_do.append(("Make API's list", make_api))
            can_do.append(("Edit API's list", edit_api))
        if line5 == "True":
            can_do.append(("Read history", read_history))
        if line6 == "True":
            can_do.append(("Edit files", edit_files))
        if line7 == "okay":
            break
    for i, (name, _) in enumerate(can_do, 1):
        print(f"{i}. {name}")

    choice = int(input("Select: ")) - 1

    if 0 <= choice < len(can_do):
        can_do[choice][1]()

def hello():
    print("Welcome in πKey")
    print("What you want to do ?")
    print("---------------------")
    ask_device_what_can_do()

def welcome():
    global sd_card
    print("Welcome in πKey")
    print(f"OS type: {os_type}")
    print("Connect the device to your computer!")
    print("Searching the device...")
    connect_device()

welcome()