# MQTT Sensor and Actuator System

This folder contains two scripts for an ESP8266-based IoT system using the MQTT protocol.

## 1. Transmitter (`tx.txt`)

This code configures an ESP8266 board as an **MQTT Publisher**. It reads data from an Infrared (IR) sensor and sends it to an MQTT broker.

**Hardware Setup:**
*   **IR Sensor** connected to pin **D1**.

**Behavior:**
*   Connects to the Wi-Fi network `IICLUB`.
*   Connects to the public MQTT broker at `test.mosquitto.org` (port 1883).
*   Reads the IR sensor state every 2 seconds.
*   Publishes the sensor state (0 or 1) as a String to the topic: `sensor/ir1`.

## 2. Receiver (`rx.txt`)

This code configures an ESP8266 board as an **MQTT Subscriber**. It listens for messages on the specified topic and controls actuators (an LED and a Servo motor) based on the received data.

**Hardware Setup:**
*   **LED** connected to pin **D2**.
*   **Servo Motor** connected to pin **D4**.

**Behavior:**
*   Connects to the Wi-Fi network `IICLUB`.
*   Connects to the public MQTT broker at `test.mosquitto.org` (port 1883).
*   Subscribes to the topic: `sensor/ir1`.
*   If the received message is `"1"`: Turns the LED ON and moves the servo to 0 degrees.
*   If the received message is `"0"`: Turns the LED OFF and moves the servo to 180 degrees.
