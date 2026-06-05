# πKey

# from tools.storage import main as storage_main

storage_tool = False

from machine import Pin, SPI # type: ignore
import sdcard
import os
import time
import urandom # type: ignore
import sys
import json

# inicializing LEDs
led_1 = Pin(0, Pin.OUT)
led_2 = Pin(1, Pin.OUT)
led_3 = Pin(6, Pin.OUT)

# inicializing button
button = Pin(15, Pin.IN, Pin.PULL_UP)

# inicializing SD card
try:
    spi = SPI(
        0,
        baudrate=1000000,
        polarity=0,
        phase=0,
        sck=Pin(2),
        mosi=Pin(3),
        miso=Pin(4)
    )

    cs = Pin(5, Pin.OUT)

    sd = sdcard.SDCard(spi, cs)

    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")

    sdcard_if = True

except Exception as e:
    sdcard_if = False

# if you hold button on start it will open the test menu
def button_hold_start():
    msg = sys.stdin.readline().strip()
    while True:
        if msg == "connected":
            led_1.value(1)
            led_2.value(1)
            led_3.value(1)
            time.sleep(1)
            led_1.value(0)
            led_2.value(0)
            led_3.value(0)
            print("button_down")
            break

    if sdcard_if:
        print("SD card detected.")
    else:
        print("No SD card detected.")

    with open("id_key.txt", "r") as f:
        id = f.read()
    print(f"ID of this device: {id}")

# id generator
def generate_id():
    id_key = ''.join(str(urandom.getrandbits(4) % 10) for _ in range(8))
    with open("id_key.txt", "w") as f:
        f.write(id_key)

    with open("/sd/id_key.txt", "w") as f:
        f.write(id_key)  
    print("This is your ID key please write it somewhere")
    print(f"Generated ID key: {id_key}")

# if the device is booting with SD that have no hello.txt file in it it would make it 
def first_time():
    led_1.value(1)
    led_2.value(1)
    led_3.value(1)
    with open("/sd/hello.txt", "w") as f:
        f.write("Hello from πKey team... We are wery happy to see you here! :3")
    print("First time...")
    generate_id()
    time.sleep(1)
    led_1.value(0)
    led_2.value(0)
    led_3.value(0)

def what_can_do():
    global sdcard_if 
    while True:
        msg = sys.stdin.readline().strip()
        if msg == "what_can_do":
            led_3.value(1)
            if sdcard_if and not "password.txt" in os.listdir("/"):
                make_password = True
            else:
                make_password = False
                
            if sdcard_if and "password.txt" in os.listdir("/"):
                new_password = True
            else:
                new_password = False

            if sdcard_if and not "apis.json" in os.listdir("/sd"):
                make_apis = True
            else:
                make_apis = False

            if sdcard_if and "apis.json" in os.listdir("/sd"):
                edit_apis = True
            else:
                edit_apis = False

            if sdcard_if and "history.json" in os.listdir("/sd"):
                read_history = True
            else:
                read_history = False

            if sdcard_if:
                edit_files = True
            else:
                edit_files = False
            print(f"{make_password}\n{new_password}\n{make_apis}\n{edit_apis}\n{read_history}\n{edit_files}\nokay")
            break

def make_password():
    print("nice")

def new_password():
    print("nice")

def make_api():
    while True:
        msg = sys.stdin.readline().strip()
        line1 = sys.stdin.readline().strip()
        line2 = sys.stdin.readline().strip()

        if msg:
            if not "apis.json" in os.listdir("/sd"):
                payload = {"Name": msg, "Type": line1, "API": line2}
                with open("/sd/apis.json", "w") as f:
                    json.dump(payload, f)

            else:
                with open("/sd/apis.json", "r") as f:
                    payload = json.load(f)
                payload.append({"Name": msg, "Type": line1, "API": line2})
                with open("/sd/apis.json", "w") as f:
                    json.dump(payload, f)
            break

def chat_ai():
    with open("/sd/apis.json", "r") as f:
        data = json.load(f)
    print(f"{data["Name"]}\n")
    print(f"{data["Type"]}\n")
    print(f"{data["API"]}")

def edit_api():
    print("nice")

def read_history():
    print("nice")

def edit_files():
    print("nice")

def wait_next():
    while True:
        msg = sys.stdin.readline().strip()
        if msg == "make_password":
            make_password()
        if msg == "new_password":
            new_password()
        if msg == "make_api":
            make_api()
        if msg == "chat_ai":
            chat_ai()
        if msg == "edit_api":
            edit_api()
        if msg == "read_histroy":
            read_history()
        if msg == "edit_files":
            edit_files()
        if msg:
            break

# this just read file idk
def main():
    while True:
        msg = sys.stdin.readline().strip()
        if msg == "connected":
            led_1.value(1)
            led_2.value(1)
            led_3.value(1)
            time.sleep(1)
            led_1.value(0)
            led_2.value(0)
            led_3.value(0)
            print(f"okay\n{sdcard_if}")
            break
    what_can_do()
    wait_next()

# this is something like main
def boot_start():
    if button.value():

        for i in range(3):
            led_1.value(1)
            time.sleep(0.5)
            led_1.value(0)
            led_2.value(1)
            time.sleep(0.5)
            led_2.value(0)
            led_3.value(1)
            time.sleep(0.5)
            led_3.value(0)

        for i in range(2):
            led_1.value(1)
            led_2.value(1)
            led_3.value(1)
            time.sleep(0.5)
            led_1.value(0)
            led_2.value(0)
            led_3.value(0)

        if sdcard_if:
            if "hello.txt" in os.listdir("/sd"):
                main()
            else:
                first_time()
        else:
            main()
        
    else:
        led_1.value(1)
        led_2.value(1)
        led_3.value(1)
        button_hold_start()
        led_1.value(0)
        led_2.value(0)
        led_3.value(0)


if __name__ == "__main__":
    boot_start()