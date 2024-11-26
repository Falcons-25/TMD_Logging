# TMD_Logging
Automate logging throttle% and thrust for propulsion configuration performance testing

## Overview
This project consists of two components:  
1. **AutoLogger.py**: A Python script that initializes a serial connection with an Arduino and logs the data to a CSV file.
2. **TMD_Logging.ino**: An Arduino sketch that reads data from a load cell using an HX711 module, converts the readings to kilograms, and sends the data via serial.

## Files

### 1. AutoLogger.py
This Python script communicates with the Arduino via a serial connection and logs the output to a CSV file for later analysis. It automatically detects and initializes the serial port, ensuring data is stored in an organized manner.

#### Features:
- Initializes serial communication with Arduino.
- Logs sensor data to a CSV file.
- Can be easily extended for additional data processing or visualization.

### 2. TMD_Logging.ino
This Arduino sketch uses the HX711 library to interface with a load cell through the HX711 module. The program reads analog data from the load cell, converts the values to kilograms, and sends the result through the serial port. Also reads PWM signal for throttle input to receiver and sends through serial port.

#### Features:
- Reads from a load cell using the HX711 module.
- Converts raw sensor data to kilograms.
- Outputs data to the serial monitor for logging.

## Resources
This project relies on external libraries and tutorials to interface with the load cell and HX711 module.

- **HX711 Library**: A library that simplifies reading data from the HX711 module.
  - [HX711 GitHub Repository](https://github.com/bogde/HX711)

- **Tutorial for Load Cell and HX711**: A step-by-step guide on using the HX711 module with a load cell.
  - [Arduino Load Cell Tutorial](https://randomnerdtutorials.com/arduino-load-cell-hx711/)

## Setup Instructions

### Hardware
- **Load Cell** connected to the **HX711** module.
- **Arduino** microcontroller.
- Connect the HX711 module to the Arduino according to the tutorial linked above.

### Software
1. **TMD_Logging.ino**:
   - Install the **HX711** library via Arduino Library Manager or from the GitHub repository.
   - Upload the `TMD_Logging.ino` sketch to your Arduino.

2. **AutoLogger.py**:
   - Ensure you have Python installed along with the necessary libraries (`pySerial`, `csv`).
   - Run `AutoLogger.py` to start logging the data from the Arduino.

```bash
pip install pyserial
python AutoLogger.py
