# 👁️ The Third Eye: Hybrid AI Glasses for Predictive Navigation

## 📌 Overview

**The Third Eye** is an AI-powered assistive system designed to help visually impaired individuals navigate safely.
It combines **ESP32-CAM**, **computer vision**, and **cloud-based AI models** to detect surroundings and provide real-time audio feedback.

---

## 🚀 Key Features

* 📷 Real-time image capture using ESP32-CAM
* 🤖 Object detection using YOLOv8
* 🧠 AI-based scene understanding (LLM integration)
* 🔊 Audio feedback using Text-to-Speech (TTS)
* ☁️ Cloud-based processing via Flask server
* 📡 Wireless communication using Wi-Fi

---

## 🛠️ Tech Stack

### 🔹 Hardware

* ESP32-CAM
* (Optional) VL53L0X Distance Sensor

### 🔹 Software

* Python
* Flask
* YOLOv8 (Ultralytics)
* OpenCV
* gTTS (Google Text-to-Speech)

### 🔹 Tools

* Arduino IDE
* Git & GitHub
* Google Cloud Platform

---

## 🏗️ System Architecture

1. ESP32-CAM captures an image
2. Image is sent to Flask server
3. YOLOv8 performs object detection
4. AI model generates scene description
5. Text is converted into audio (TTS)
6. Audio feedback is delivered to the user

---

## 📂 Project Structure

```
THIRD_EYE_PROJECT/
│
├── backend/
│   ├── app.py
│   ├── utils/
│   │   └── tts.py
│   ├── uploads/
│   ├── static/
│   └── yolov8n.pt
│
├── esp32/
│   └── esp32_camera_code/
│       ├── esp32_camera_code.ino
│       └── camera_pins.h
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sai0045/The-Third-Eye.git
cd The-Third-Eye
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Backend Server

```bash
python app.py
```

### 4️⃣ Upload Code to ESP32-CAM

* Open Arduino IDE
* Select **ESP32-CAM board**
* Upload `esp32_camera_code.ino`

---

## 📊 Applications

* Assistive technology for visually impaired
* Smart wearable AI systems
* Real-time object detection devices

---

## 🔮 Future Scope

* 📏 Distance estimation using sensors
* 📱 Mobile app integration
* 🌐 Offline AI processing
* 📍 GPS-based navigation

---

## 👨‍💻 Author

**Saurabh Lahare**

---


