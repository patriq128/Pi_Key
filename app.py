import serial
import serial.tools.list_ports
import platform
import time
import requests
import json
import os

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
                
            time.sleep(1)

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
    print("\033c", end="")
    global ser
    name = input("Name of API: ")
    type_ai = input("Type of AI: ")
    api_key = input("Your API key: ")
    ser.write(b"make_api\n")
    time.sleep(0.1)
    ser.write(f"{name}\n{type_ai}\n{api_key}\n".encode())

def chat_ai():
    print("\033c", end="")
    global ser
    ser.write(b"chat_ai\n")
    names = []

    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            if line != "---":
                names.append(line)
            else:
                break

    for i, name in enumerate(names):
        print(f"{i}: {name}")

    picked = None

    choice = input("Pick AI: ").strip()

    if choice.isdigit():
        idx = int(choice)

        if 0 <= idx < len(names):
            picked = names[idx]
            print("Picked:", picked)
        else:
            print("wrong number")
    else:
        print("This is not number")
        
    if picked:
        ser.write((picked + "\n").encode())

    while True:
        line1 = ser.readline().decode(errors="ignore").strip()
        line2 = ser.readline().decode(errors="ignore").strip()

        if line1:
            api = line1
            type_nice = line2
            break

    
    names = ["New chat"]
    ser.write(b"history\n")
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            if line != "---":
                names.append(line)
            else:
                break

    for i, name in enumerate(names):
        print(f"{i}: {name}")

    picked = None

    choice = input("Pick History: ").strip()

    if choice.isdigit():
        idx = int(choice)

        if 0 <= idx < len(names):
            picked = names[idx]
            print("Picked:", picked)
        else:
            print("wrong number")
    else:
        print("This is not number")
        
    if picked == "New chat":
        ser.write(b"next\n")
    else:
        ser.write((picked + "\n").encode())
    

    while True:
        line1 = ser.readline().decode(errors="ignore").strip()
        if line1:
            if line1 == "new":
                messages = [] 
                chat_name = None
                first_message = True
            else:
                chat_name = picked
                first_message = False
                messages = json.loads(line1)
                ser.write((chat_name + "\n").encode())
            break

    print(messages)

    while True:
        input_user = input("You => ")

        if input_user == "exit":
            break

        messages.append({
            "role": "user",
            "content": input_user
        })

        if first_message:
            title_response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + api,
                    "Content-Type": "application/json"
                },
                json={
                    "model": type_nice,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Generate a short title (maximum 3 words) for this chat: " + input_user
                        }
                    ]
                }
            )

            chat_name = title_response.json()["choices"][0]["message"]["content"].strip()
            first_message = False

        ser.write((chat_name + "\n").encode())

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + api,
                "Content-Type": "application/json"
            },
            json={
                "model": type_nice,
                "messages": messages
            }
        )

        bot_reply = response.json()["choices"][0]["message"]["content"]
        print("AI => ", bot_reply, "\n")

        messages.append({
            "role": "assistant",
            "content": bot_reply
        })
        ser.write((json.dumps(messages) + "\n").encode())

def edit_api():
    ser.write(b"edit_api\n")

def read_history():
    global ser
    ser.write(b"read_history\n")
    while True:
        line1 = ser.readline().decode().strip()
        line2 = ser.readline().decode().strip()
        line3 = ser.readline().decode().strip()
        if line1:
            print(line1)
            print(line2)
            print("\n")
        if line3 == "---":
            break

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

def pi_key():
    print("Connect the device to your computer!")
    print("Searching the device...")
    connect_device()

def USB_storage_type():
    global path
    global os_type

    with open("configure.json", "r") as f:
        data = json.load(f)

    usbID = data["Serial"]
    usbM = data["Model"]

    input("Is the USB device pluged in ? if Yes press Enter...")
    if os_type == "Linux":
        import pyudev
        import os
        import getpass

        TARGET_SERIAL = usbID
        TARGET_MODEL = usbM

        context = pyudev.Context()

        user = getpass.getuser()

        for device in context.list_devices(subsystem="block", DEVTYPE="partition"):

            serial = device.get("ID_SERIAL_SHORT")
            model = device.get("ID_MODEL")

            if serial == TARGET_SERIAL and model == TARGET_MODEL:

                mount_path = device.get("ID_FS_LABEL_ENC")

                if not mount_path:
                    mount_path = device.get("ID_FS_LABEL")

                base = f"/media/{user}/{mount_path}/"

                print("USB PATH:", base)

                if not os.path.exists(base):
                    base = f"/media/{user}/{mount_path}/"

        path = base

    elif os_type == "Windows":
        import wmi # type: ignore

        TARGET_SERIAL = usbID
        TARGET_MODEL = usbM

        def find_usb_path():
            c = wmi.WMI()

            for disk in c.Win32_DiskDrive():
                if "USB" in str(disk.InterfaceType):

                    serial = str(disk.SerialNumber).strip()
                    model = str(disk.Model).strip()

                    if TARGET_SERIAL in serial and TARGET_MODEL in model:
                        for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                            for logical in partition.associators("Win32_LogicalDiskToPartition"):
                                return logical.DeviceID + "\\"

            return None


        path = find_usb_path()

        print("USB PATH:", path)

    elif os_type == "Darwin":
        import subprocess
        import os

        TARGET_SERIAL = usbID
        TARGET_MODEL = usbM

        def get_usb_name():
            out = subprocess.check_output(["system_profiler", "SPUSBDataType"]).decode()

            model = None
            serial = None

            for line in out.split("\n"):
                if "Product ID" in line:
                    model = line.split(":")[-1].strip()

                if "Serial Number" in line:
                    serial = line.split(":")[-1].strip()

            return model, serial


        def find_path():
            volumes = os.listdir("/Volumes")

            model, serial = get_usb_name()

            if model == TARGET_MODEL and serial == TARGET_SERIAL:
                return "/Volumes/" + volumes[-1] + "/"

            return None


        path = find_path()

        print("USB PATH:", path)

    with open(path + "pi_key.txt", "w") as f:
        f.write("Welcome in πKey")

def new_api_usb():
    global path
    name = input("Name: ")
    type_api = input("Type of AI: ")
    api = input("API key: ")
    new = {"Name": name, "Type": type_api, "API": api}
    if not os.path.exists(path + "apis.json"):
        data = []
    else:
        with open(path + "apis.json", "r") as f:
            try:
                data = json.load(f)
            except:
                    data = []
                
    data.append(new)
    with open(path + "apis.json", "w") as f:
        json.dump(data, f)

def read_api_usb():
    with open(path + "apis.json", "r") as f:
        data = json.load(f)

    for item in data:
        print("-----------")
        print(item["Name"])
        print(item["Type"])
        print(item["API"])

def chat_ai_usb():
    names = []
    with open(path + "apis.json", "r") as f:
        data = json.load(f)

    for item in data:
        names.append(item["Name"])
    print("chat ai")

    for i, name in enumerate(names):
        print(f"{i}: {name}")

    picked = None
    while True:
        choice = input("Pick AI: ").strip()

        if choice.isdigit():
            idx = int(choice)

            if 0 <= idx < len(names):
                picked = names[idx]
                print("Picked:", picked)
                break
            else:
                print("wrong number")
                continue
        else:
            print("This is not number")
            continue

    for item in data:
        if item["Name"] == picked:
            AI_api = item["API"]
            AI_type = item["Type"]

    print(AI_api)
    print(AI_type)

    names = ["New chat"]
    if os.path.exists(path + "history.json"):
        with open(path + "history.json", "r") as f:
            data = json.load(f)
        names = ["New chat"]
        for item in data:
            names.append(item["Name"])
    else:
        names = ["New chat"]

    for i, name in enumerate(names):
        print(f"{i}: {name}")

    picked = None

    choice = input("Pick History: ").strip()

    while True:
        if choice.isdigit():
            idx = int(choice)

            if 0 <= idx < len(names):
                picked = names[idx]
                print("Picked:", picked)
                break
            else:
                print("wrong number")
                continue
        else:
            print("This is not number")  
            continue      

    if picked == "New chat":
        messages = [] 
        chat_name = None
        first_message = True
    else:
        for item in data:
            if item["Name"] == picked:
                message = item["Conversation"]
        chat_name = picked
        first_message = False
        messages = message
                

    while True:
        input_user = input("You => ")

        if input_user == "exit":
            break

        messages.append({
            "role": "user",
            "content": input_user
        })

        if first_message:
            title_response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + AI_api,
                    "Content-Type": "application/json"
                },
                json={
                    "model": AI_type,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Generate a short title (maximum 3 words) for this chat: " + input_user
                        }
                    ]
                }
            )

            chat_name = title_response.json()["choices"][0]["message"]["content"].strip()
            first_message = False


        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + AI_api,
                "Content-Type": "application/json"
            },
            json={
                "model": AI_type,
                "messages": messages
            }
        )

        try:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("API Error:", e)
        print("AI => ", bot_reply, "\n")

        messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        file = path + "history.json"

        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        else:
            data = []

        new = {
            "Name": chat_name,
            "Conversation": messages
        }

        found = False
        for i, item in enumerate(data):
            if item["Name"] == chat_name:
                data[i] = new
                found = True
                break

        if not found:
            data.append(new)

        with open(file, "w") as f:
            json.dump(data, f, indent=2)

def read_history_usb():
    global path
    with open(path + "history.json") as f:
        data = json.load(f)
    names = []
    for item in data:
        print("---------")
        print(item["Name"])
        names.append(item["Name"])

    for i, name in enumerate(names):
        print(f"{i}: {name}")

    picked = None

    choice = input("Pick History: ").strip()

    while True:
        if choice.isdigit():
            idx = int(choice)

            if 0 <= idx < len(names):
                picked = names[idx]
                print("Picked:", picked)
                break
            else:
                print("wrong number")
                continue
        else:
            print("This is not number")  
            continue      

    for item in data:
        if item["Name"] == picked:
            print(item["Conversation"])


def settings():
    with open("configure.json", "r") as f:
        data = json.load(f)
    print("Type:", data["Type"])
    print("Serial:", data["Serial"])
    print("Model:", data["Model"])

    def new_usb():
        global serial
        global model
        what_usbid()
        data = {"Type": "2", "Serial": serial, "Model": model}
        with open("configure.json", "w") as f:
            json.dump(data, f, indent=4)

    to_do = []
    to_do.append(("Find new USB device" , new_usb))
    to_do.append(("Exit", usb_do))
    for i, (name, _) in enumerate(to_do, 1):
        print(f"{i}. {name}")

    choice = int(input("Select: ")) - 1

    if 0 <= choice < len(to_do):
        to_do[choice][1]()

def usb_do():
    can_do = []
    global path
    if not os.path.exists(path + "apis.json"):
        api = False
    else:
        api = True


    if os.path.exists(path + "history.json"):
        read_history = True
    else:
        read_history = False
    
    if api:
        can_do.append(("New API", new_api_usb))
        can_do.append(("Read API's", read_api_usb))
        can_do.append(("Chat AI", chat_ai_usb))

    else:
        can_do.append(("New API", new_api_usb))
    
    if read_history:
        can_do.append(("Read history", read_history_usb))
    can_do.append(("Settings", settings))

    for i, (name, _) in enumerate(can_do, 1):
        print(f"{i}. {name}")

    choice = int(input("Select: ")) - 1

    if 0 <= choice < len(can_do):
        can_do[choice][1]()

def main():
    print("Welcome in πKey")
    print(f"OS type: {os_type}")
    with open("configure.json", "r") as f:
        data = json.load(f)

    if data["Type"] == "1":
        print("Opening Pi-Key...")
        pi_key()
    else:
        print("Opening USB device...")
        USB_storage_type()
        usb_do()


def what_usbid():
    global model
    global serial
    global os_type
    print("Connect your USB device")
    if os_type == "Linux":
        import pyudev

        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='block')

        print("Waiting for USB...")

        for device in iter(monitor.poll, None):
            if device.action == "add":
                serial = device.get("ID_SERIAL_SHORT")
                model = device.get("ID_MODEL")
                vendor = device.get("ID_VENDOR")

                print("USB connected!")
                print("Serial:", serial)
                print("Model:", model)

                break

    elif os_type == "Windows":
        import wmi # type: ignore

        c = wmi.WMI()
        watcher = c.Win32_VolumeChangeEvent.watch_for()

        print("Waiting for USB...")

        while True:
            event = watcher()

            if event.EventType == 2:  
                print("USB connected!")

                for disk in c.Win32_DiskDrive():
                    if "USB" in str(disk.InterfaceType):
                        
                        serial = disk.SerialNumber
                        model = disk.Model

                        print("Serial:", serial)
                        print("Model:", model)
                        break

    elif os_type == "Darwin":
        import subprocess
        import time

        def get_usb_snapshot():
            return subprocess.check_output(["system_profiler", "SPUSBDataType"]).decode()

        print("Waiting for USB...")

        before = get_usb_snapshot()

        while True:
            time.sleep(1)
            after = get_usb_snapshot()

            if after != before:
                print("USB connected!")

                model = None
                serial = None
                vendor = None

                for line in after.split("\n"):

                    if "Product ID" in line:
                        model = line.split(":")[-1].strip()

                    if "Serial Number" in line:
                        serial = line.split(":")[-1].strip()


                print("MODEL:", model)
                print("SERIAL:", serial)
                break

            before = after
    return serial, model

def first_time():
    print("Welcome in πKey for the first time.")
    print("You can choose what type of using the PI-key you want")
    print("""1.] PI-Key
2.] USB device""")
    ask = input("> ")

    if ask == "2":
        serial, model = what_usbid()
    else:
        serial = None
        model = None
    print("Saving...")
    data = {"Type": ask, "Serial": serial, "Model": model}
    with open("configure.json", "w") as f:
        json.dump(data, f, indent=4)
    

def welcome():
    if os.path.exists("configure.json"):
        main()
    else:
        first_time()

if __name__ == "__main__":
    welcome()