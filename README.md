# Robotics Workshop 🤖

Welcome to the Robotics Workshop repository! This project contains a collection of scripts and examples demonstrating computer vision, hand gesture recognition, object detection, and hardware control using Python, OpenCV, MediaPipe, YOLOv8, and MQTT for ESP8266.

## 📁 Repository Structure

Here is a breakdown of what each file and folder does:

### Python Scripts
- **`1-basic-opencv.py`**: A simple script to get started with OpenCV, demonstrating how to open the webcam and read frames.
- **`2-haarcascade_frontalface-opencv.py`**: Uses OpenCV's built-in Haar Cascades for basic facial detection.
- **`3-media-pipe.py`**: An introduction to Google's MediaPipe for pose or face detection.
- **`4-mediapipe-hand.py`**: Focuses specifically on MediaPipe's Hand tracking module to identify hand landmarks in real-time.
- **`5-LED-media-pipe.py`**: Integrates MediaPipe hand tracking with MQTT. Detects "Open" or "Closed" hand gestures to send MQTT commands to an ESP8266 to toggle an LED.
- **`6-yolov8.py`**: A real-time object detection script using the Ultralytics YOLOv8 model.
- **`7-robot-arm-media-pipe.py`**: Advanced script using hand gestures to control a robotic arm via MQTT.

### Folders
- **`4-dof-arm/`**: Contains resources related to a 4-Degree of Freedom (DOF) robotic arm.
  - `esp8266_mqtt_arm.txt`: Arduino C++ code for an ESP8266 to receive MQTT commands and control servo motors.
  - `robot-simulation.txt`: Simulation or structural information for the robot arm.
- **`mediapipe/`**: Contains ESP8266 code specifically for MediaPipe integrations.
  - `esp8266_mqtt_led.txt`: Arduino C++ code for an ESP8266 to turn an LED on and off based on MQTT messages.
- **`mqtt/`**: Contains testing materials and documentation for the MQTT broker setup.

---

## 🛠️ Setup Instructions

This project uses `uv` for lightning-fast Python dependency management. Follow these steps to set up your environment:

### 1. Create a Virtual Environment
First, create an isolated Python virtual environment named `.venv` in the root of this project:
```bash
uv venv .venv
```

### 2. Activate the Virtual Environment
Before installing packages or running scripts, you must "source" or activate the environment:

- **On Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **On Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **On Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies
With the environment activated, install all required libraries from the `requirements.txt` file (or `pyproject.toml`) using `uv pip`:

```bash
uv pip install -r requirements.txt
```
*(Note: If you are using uv's newer project management, you can also simply run `uv sync` if a `pyproject.toml` is configured).*

---

## 🚀 Clone the Repository

If you are downloading or cloning this repository from GitHub:
```bash
git clone https://github.com/punithkrishnakeepudi/robotics-workshop.git
cd robotics-workshop
```
