# Pi_Key
![Pi\_Main](images/pi-key.png)

Pi_Key is a compact RP2040-powered device designed to look like a USB flash drive while providing the flexibility of a programmable embedded platform.

The device features three status LEDs and a microSD card interface, making it suitable for data logging, portable applications, diagnostics, and custom embedded projects.

## Features

* RP2040 microcontroller
* USB-powered operation
* 3 status LEDs
* microSD card support
* Compact USB flash drive form factor
* Compatible with C/C++, MicroPython, and Rust

## Hardware Overview

### Main Components

* RP2040 Microcontroller
* 3 × Status LEDs
* microSD Card Interface
* USB Connector

## Pinout

### microSD Card Connections

| SD Card Pin | RP2040 GPIO |
| ----------- | ----------- |
| MOSI        | 3           |
| MISO        | 4           |
| SCK         | 2           |
| CS          | 5           |

### Button Connection

| BUTTON | GPIO 15 |
| ------ | ------- |


### LED Connections

| LED   | RP2040 GPIO |
| ----- | ----------- |
| LED 1 | 0           |
| LED 2 | 1           |
| LED 3 | 6           |

## Schematic

The complete hardware schematic can be found below.

![Pi\_Key Schematic](images/schematic-1.png)

## Photos

### Front Side

![Pi\_Key Front](images/front1.png)
![Pi\_Key Front](images/front2.png)
### Back Side

![Pi\_Key Back](images/back1.png)
![Pi\_Key Back](images/back2.png)

## Applications

* Data logging
* Portable embedded development
* Hardware experimentation
* Educational projects
* Custom USB devices
* ! Working On AI API's Saving !
