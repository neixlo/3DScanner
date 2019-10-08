# SemiSynthDataset_ObjScan
Automated process of shooting photos and rotate a turntable/lazysusan to get images in a 360°/steps view. A 3D object can then be generated with a photogrammetry tool such as Agisoft PhotoScan/Metashape. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

#### Hardware

- Stepper Motor (Longruner NEMA 17, Bipolar Stepper Motor Driver, 1.7 A/24 V 42x40 mm Body, 4 Lead Stepper Motor & 32 Segments 4A 40V 57/86 Stepper Motor Driver LD09) \
https://www.amazon.de/gp/product/B07FKJK1H9/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&language=en_GB&psc=1
- Power supply (e.g. 90W Universal Laptop Notebook power supply 90w -240v AC 50/60hz output voltage 15v,Output 5amps Max)\
https://www.amazon.de/gp/product/B00LATEQ7I/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
- USB-A to USB-B Kable for PC connection
- Camera with serial interface and cabel (e.g. NikonD3200)

#### Hardware setup

Setup as described in:
https://www.hackster.io/ashleyblack/tb6600-stepper-motor-driver-tester-85a29e

Except of 
1. That I used an Arduino UNO and therfore the code **_TB6600_Step_Driver.ino_** changed.
2. The wiring of the driver stage is changing accordingly: \
**_ENA-_** --- to ---	ArduinoUNO  **_GND_** \
**_ENA+_** --- to ---	ArduinoUNO  **_Pin2** \
**_DIR-_** --- to ---	ArduinoUNO  **_GND** \
**_DIR+_** --- to ---	ArduinoUNO  **_Pin3** \
**_PUL-_** --- to ---	ArduinoUNO  **_GND** \
**_PUL+_** --- to ---	ArduinoUNO  **_Pin4** \
**_B-_** --- to ---	StepperMotor  **_black** \
**_B+_** --- to ---	StepperMotor  **_green** \
**_A-_** --- to ---	StepperMotor  **_red** \
**_A+_** --- to ---	StepperMotor  **_blue** \
**_GND_** --- to ---	PowerSupply  **_GND** \
**_VCC_** --- to ---	PowerSupply  **_+15V** 

3. The switches all are OFF but **_switch 4 is ON_**

#### Software 

**_TBD_**

