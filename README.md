# 🗞️ Wackathon: Web Control & Slouch Detector

**Created for MakeMIT 2026 Hackathon**

## Project Overview
This project combines real-time physical sensor data from an Arduino with a web-controlled interface to create an interactive, multi-persona experience. It features two main components:
1. **Arduino Sensor Integration:** Reads physical sensor data (like posture/slouching) via a serial connection and parses it in real-time.
2. **Streamlit Web Dashboard:** A control panel that allows users to trigger a physical catapult and assign different AI personas and voices to the interaction.

---

## Features

- **Hardware-to-Software Bridge:** Custom `ArduinoReader` Python class automatically detects connected Arduino devices and parses incoming comma-separated sensor data.
- **Real-time Slouch Detection:** Interprets live sensor streams to detect poor posture based on configured thresholds.
- **Interactive Web UI:** Built with **Streamlit**, providing a clean interface for users to control hardware remotely.
- **Cloud Database Integration:** Uses **Supabase** to manage state and send commands (like "FIRE") from the web app to the local hardware.
- **Dynamic AI Personas:** Integrates with **ElevenLabs** to give the system unique voices (e.g., 1950s Newsie, Angry Drill Sergeant).

---

## Hardware Requirements
- Arduino Microcontroller (Vendor ID: `0x2341`)
- Sensors for slouch detection hooked up to the Arduino
- Catapult mechanism capable of receiving network triggers

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [your-repo-link]
   cd makemit
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   You will need to set up your Supabase credentials. If running locally, you can create a `.streamlit/secrets.toml` file with:
   ```toml
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_anon_key"
   ```

---

## Usage

### Running the Web Dashboard
To start the Streamlit control panel:
```bash
streamlit run app.py
```

### Running the Arduino Listener
Ensure your Arduino is plugged in and flashed with the `arduino_to_laptop.ino` code, then run:
```bash
python arduino_to_laptop.py
```

---

## File Structure
- `app.py`: The Streamlit web application for controlling the catapult and selecting personas.
- `arduino_to_laptop.py`: The Python script responsible for reading, parsing, and interpreting data from the Arduino.
- `arduino_to_laptop/arduino_to_laptop.ino`: The C++ code running on the Arduino that packages sensor data and sends it over Serial.
- `requirements.txt`: Python package dependencies.
