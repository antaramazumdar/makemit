
import requests
import threading
import subprocess
import random
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QGraphicsDropShadowEffect, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QColor

# --- 🔑 CONFIGURATION ---
VOICES_URL = "https://api.elevenlabs.io/v1/voices"
ELEVEN_KEY = "d4dc9c60fec5a25472fa8ba900653932f75fe1a2f9f86a1d038455fcb80f9540" # Add API key here

class WorkerSignals(QObject):
    result = pyqtSignal(str)
    finished = pyqtSignal()

class MonitorThread(QThread):
    slouch_found = pyqtSignal()
    status_update = pyqtSignal(str)

    def __init__(self, duration_mins):
        super().__init__()
        self.duration_secs = duration_mins * 60
        self.active = True

    def run(self):
        try:
            reader = ArduinoReader()
            start_time = time.time()
            self.status_update.emit("👀 Monitoring Active...")

            while self.active and (time.time() - start_time < self.duration_secs):
                # Poll the Arduino via your detect_slouch method
                # Note: Adjust your ArduinoReader to return True/False or similar
                if reader.detect_slouch(): 
                    self.slouch_found.emit()
                    time.sleep(8) # Cool-down to prevent audio/slap overlapping
                
                self.msleep(100) # CPU-friendly polling
            
            reader.close()
        except Exception as e:
            self.status_update.emit(f"Serial Error: {e}")


class WhackWorker(threading.Thread):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.roasts = [
            "Your posture violates at least three constraints in any reasonable optimization problem.",
            "Stop imitating a shrimp and sit up like a citizen!",
            "You're bent like a resistor in a breadboard that nobody bothered to straighten. Fix it!",
            "The moment arm on that hunch is impressive. Reduce the load and move it back over your center of mass.",
            "Your spine has worse load distribution than a bridge designed by a freshman.",
            "You're one vertebra away from being classified as a non-load-bearing wall.",
            "Your posture looks like code that works but nobody knows why, how bought you git pull your head back",
            "Your spine looks like a capacitor charging curve"
        ]

    def run(self):
        try:
            # 1. Voice Roulette
            headers = {"xi-api-key": ELEVEN_KEY}
            v_res = requests.get(VOICES_URL, headers=headers)
            
            if v_res.status_code != 200:
                voice = {"name": "Broken API Newsie", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
            else:
                voices_list = v_res.json().get("voices", [])
                
                if not voices_list:
                    voice = {"name": "Lonely Newsie", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
                else:
                    # Logic to make sure we don't pick a Newsie if we have other options
                    voice = random.choice(voices_list)
            
            roast = random.choice(self.roasts)

            # 2. TTS
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['voice_id']}"
            tts_res = requests.post(tts_url, headers=headers, json={
                "text": roast, "model_id": "eleven_turbo_v2_5"
            })

            if tts_res.status_code == 200:
                with open("whack.mp3", "wb") as f:
                    f.write(tts_res.content)
                subprocess.run(["mpg123", "-q", "whack.mp3"])
            else:
                print(f"TTS ERROR: {tts_res.text}")
        except Exception as e:
            self.signals.result.emit(f"Error: {e}")
        finally:
            self.signals.finished.emit()

class WhimsicalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WHACKATHON")
        self.setFixedSize(500, 550)
        
        # --- UI DESIGN (QSS) ---
        self.setStyleSheet("""
            QMainWindow { background-color: #2B2622; }
            QLabel#Header {
                color: #D4AF37;
                font-family: 'Comic Sans MS';
                font-size: 32px;
                font-weight: bold;
            }
            QLabel {
                color: #F5DEB3;
                font-family: 'Comic Sans MS';
                font-size: 14px;
            }
            QSpinBox {
                background-color: #1A1714;
                color: #F5DEB3;
                border: 2px solid #D4AF37;
                border-radius: 10px;
                font-family: 'Comic Sans MS';
                font-size: 24px;
                padding: 10px;
                selection-background-color: #D4AF37;
            }
            /* Styling the buttons */
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 40px;
                background-color: #3E3832;
                border-left: 1px solid #D4AF37;
                border-bottom: 1px solid #D4AF37;
                border-top-right-radius: 8px;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 40px;
                background-color: #3E3832;
                border-left: 1px solid #D4AF37;
                border-bottom-right-radius: 8px;
            }
            /* Use built-in primitive arrows that Qt understands */
            QSpinBox::up-arrow {
                width: 14px;
                height: 14px;
                /* This is the key: simple color and primitive arrow */
                border-left: 7px solid #2B2622; 
                border-right: 7px solid #2B2622;
                border-bottom: 9px solid #D4AF37;
            }
            QSpinBox::down-arrow {
                width: 14px;
                height: 14px;
                border-left: 7px solid #2B2622;
                border-right: 7px solid #2B2622;
                border-top: 9px solid #D4AF37;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4E463D;
            }
            QPushButton {
                background-color: #D4AF37;
                color: #1A1714;
                font-family: 'Comic Sans MS';
                font-size: 22px;
                font-weight: bold;
                border-radius: 30px;
                min-height: 70px;
            }
            QPushButton:hover {
                background-color: #F5DEB3;
            }
            QPushButton:pressed {
                background-color: #B8860B;
            }
            QPushButton:disabled {
                background-color: #444;
                color: #888;
            }
        """)

        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        self.header = QLabel("WHACKATHON")
        self.header.setObjectName("Header")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header)

        # --- THE NEW NUMERICAL DROPDOWN (SPINBOX) ---
        self.time_input = QSpinBox()
        self.time_input.setRange(1, 120)
        self.time_input.setSuffix(" min")
        self.time_input.setValue(15)
        layout.addWidget(self.time_input)

        # Status Label
        self.status_label = QLabel("Ready to watch your back...")
        self.status_label.setStyleSheet("color: #F5DEB3; font-size: 12px; font-weight: normal; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Execute Button
        self.btn = QPushButton("Start Monitoring")
        self.btn.clicked.connect(self.start_monitoring)
        
        # Add a subtle shadow to the button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.btn.setGraphicsEffect(shadow)
        
        layout.addWidget(self.btn)

        # Central Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_monitoring(self):
        self.btn.setEnabled(False)
        self.btn.setText("WATCHING...")
        
        self.monitor = MonitorThread(self.time_input.value())
        self.monitor.status_update.connect(self.status_label.setText)
        self.monitor.slouch_found.connect(self.trigger_voice_roast)
        self.monitor.finished.connect(self.on_finished)
        self.monitor.start()

    def trigger_voice_roast(self):
        self.status_label.setText("🚨 SLOUCH! WHACKING...")
        self.signals = WorkerSignals()
        self.signals.finished.connect(lambda: self.status_label.setText("👀 Monitoring..."))
        self.voice_worker = WhackWorker(self.signals)
        self.voice_worker.start()

    def on_finished(self):
        self.btn.setEnabled(True)
        self.btn.setText("Start Monitoring")
        self.status_label.setText("Session Finished.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhimsicalApp()
    window.show()
    sys.exit(app.exec())
