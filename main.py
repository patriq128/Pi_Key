# πKey

# from tools.storage import main as storage_main

storage_tool = False

from machine import Pin, SPI # type: ignore
import libarys.sdcard as sdcard
import os
import time
import urandom # type: ignore
import sys

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
            if sdcard_if and not "password.txt" in os.listdir("/sd"):
                make_password = True
            else:
                make_password = False
                
            if sdcard_if and "password.txt" in os.listdir("/sd"):
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
            print(f"{make_password}\n{new_password}\n{make_apis}\n{edit_apis}\n{read_history}\n{edit_files}")
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