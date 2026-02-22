import customtkinter as ctk
import requests
import threading
import subprocess
import random


VOICES_URL = "https://api.elevenlabs.io/v1/voices"
GEMINI_KEY = "AIzaSyD-G2rMovW2m3rrtoa3NLfpe6jIxJ5sdfE"
ELEVEN_KEY = "d4dc9c60fec5a25472fa8ba900653932f75fe1a2f9f86a1d038455fcb80f9540"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_KEY}"

# Set UI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WhimsicalWhack(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WHACKATHON")
        self.geometry("500x550")
        self.configure(fg_color="#2B2622") # Deep chocolate background

        # Header
        self.header = ctk.CTkLabel(self, text="WHACKATHON",
                                   font=("Helvetica", 28, "bold"), text_color="#D4AF37")
        self.header.pack(pady=(30, 10))

        # Minimalist Display (Only shows the roast)
        self.display = ctk.CTkTextbox(self, width=400, height=200, 
                                     fg_color="#1A1714", border_color="#D4AF37",
                                     border_width=2, font=("Helvetica", 16, "italic"),
                                     text_color="#F5DEB3", corner_radius=15)
        self.display.pack(pady=20)
        #self.display.insert("0.0", "Sit up straight and press the button to begin...")

        # Burn Slider Label
        self.slider_label = ctk.CTkLabel(self, text="ROAST INTENSITY", font=("Helvetica", 12, "bold"))
        self.slider_label.pack()

        # Whimsical Slider
        self.burn_slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=10, 
                                        button_color="#D4AF37", progress_color="#D4AF37")
        self.burn_slider.set(5)
        self.burn_slider.pack(pady=(0, 20))

        # The Big Button
        self.btn = ctk.CTkButton(self, text="💥 EXECUTE WHACK 💥", 
                                 font=("Helvetica", 18, "bold"),
                                 height=60, width=300, corner_radius=30,
                                 fg_color="#D4AF37", text_color="#1A1714",
                                 hover_color="#F5DEB3", command=self.start_whack)
        self.btn.pack(pady=20)

    def update_display(self, text):
        self.display.delete("0.0", "end")
        self.display.insert("0.0", text)

    def start_whack(self):
        self.btn.configure(state="disabled", text="🔥 ROASTING...")
        threading.Thread(target=self.process_whack, daemon=True).start()

    def process_whack(self):
        try:
            # 1. Voice Roulette
            headers = {"xi-api-key": ELEVEN_KEY}
            v_res = requests.get(VOICES_URL, headers=headers)
            voice = random.choice(v_res.json()["voices"]) if v_res.status_code == 200 else {"name": "Newsie", "voice_id": "JBFqnCBsd6RMkjVDRZzb"}
            
            # 2. Roast Logic
            burn = int(self.burn_slider.get())
            tone = "brutal" if burn > 7 else "sarcastic" if burn > 4 else "mild"
            prompt = f"Roleplay as '{voice['name']}'. Give a 1-sentence {tone} roast to someone slouching."
            
            g_res = requests.post(GEMINI_URL, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            roast = g_res.json()['candidates'][0]['content']['parts'][0]['text'].strip() if g_res.status_code == 200 else "Sit up, you noodle!"

            self.update_display(f"Persona: {voice['name']}\n\n\"{roast}\"")

            # 3. ElevenLabs TTS
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['voice_id']}"
            tts_res = requests.post(tts_url, headers=headers, json={"text": roast, "model_id": "eleven_turbo_v2_5"})

            if tts_res.status_code == 200:
                with open("whack.mp3", "wb") as f:
                    f.write(tts_res.content)
                subprocess.run(["mpg123", "-q", "whack.mp3"])

        except Exception as e:
            self.update_display(f"Error: {str(e)}")
        
        finally:
            self.btn.configure(state="normal", text="💥 EXECUTE WHACK 💥")

if __name__ == "__main__":
    app = WhimsicalWhack()
    app.mainloop()
