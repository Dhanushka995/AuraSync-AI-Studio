import customtkinter as ctk
import tkinter as tk
import json
import os
import requests
import threading

# --- Theme Settings ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "api_config.json"
APP_VERSION = "v1.4" # Updated Version

class AuraSyncStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"AuraSync AI Studio ({APP_VERSION}) - Professional Music Remaker")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
        self.build_bottom_bar()

    def build_left_panel(self):
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.left_frame, text="🎙️ INPUT & AI DIRECTOR", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        self.btn_upload = ctk.CTkButton(self.left_frame, text="Drop Original Song Here\n(or Click to Browse)", height=80, fg_color="#2b2b2b", hover_color="#3b3b3b", border_width=2, border_color="#1f538d")
        self.btn_upload.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(self.left_frame, text="AI Music Prompt:").pack(anchor="w", padx=20, pady=(10, 0))
        self.txt_prompt = ctk.CTkTextbox(self.left_frame, height=100)
        self.txt_prompt.pack(padx=20, pady=5, fill="x")
        self.txt_prompt.insert("0.0", "EDM, heavy bass, club dance vibe")

        ctk.CTkLabel(self.left_frame, text="Genre:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_genre = ctk.CTkComboBox(self.left_frame, values=["EDM", "Baila", "Pop", "Classical", "Rock", "Acoustic"])
        self.combo_genre.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self.left_frame, text="Mood:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_mood = ctk.CTkComboBox(self.left_frame, values=["Energetic", "Sad", "Romantic", "Cinematic", "Dark"])
        self.combo_mood.pack(padx=20, pady=5, fill="x")

    def build_center_panel(self):
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.center_frame, text="🎛️ MULTI-TRACK ARRANGER", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        self.wave_frame = ctk.CTkFrame(self.center_frame, height=150, fg_color="#141414")
        self.wave_frame.pack(padx=20, pady=10, fill="x")
        self.lbl_status = ctk.CTkLabel(self.wave_frame, text="[ Ready to Generate ]", text_color="gray")
        self.lbl_status.place(relx=0.5, rely=0.5, anchor="center")

        tracks =["🎤 AI Cleaned Vocals", "🥁 Drums & Percussion", "🎸 Bass", "🎹 Melody & Chords"]
        for track in tracks:
            track_frame = ctk.CTkFrame(self.center_frame, height=60, fg_color="#242424")
            track_frame.pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(track_frame, text=track, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkSlider(track_frame, width=150).pack(side="right", padx=15, pady=15)

    def build_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.right_frame, text="🎚️ PRO MASTERING", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        ctk.CTkLabel(self.right_frame, text="Vocal Processing", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.switch_cleaner = ctk.CTkSwitch(self.right_frame, text="AI Noise Cleaner")
        self.switch_cleaner.pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(self.right_frame, text="Auto-Tune Level:").pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self.right_frame, text="Mastering FX", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(self.right_frame, text="Reverb (Space):").pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self.right_frame, text="Stereo Widener:").pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        self.btn_api = ctk.CTkButton(self.right_frame, text="⚙️ API Settings", fg_color="transparent", border_width=1, text_color="white", command=self.open_api_settings)
        self.btn_api.pack(side="bottom", padx=20, pady=20, fill="x")

    def build_bottom_bar(self):
        self.bottom_frame = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color="#141414")
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.btn_play = ctk.CTkButton(self.bottom_frame, text="▶ PLAY", width=80, fg_color="#28a745", hover_color="#218838")
        self.btn_play.pack(side="left", padx=20, pady=20)

        self.progress = ctk.CTkProgressBar(self.bottom_frame, width=400)
        self.progress.pack(side="left", padx=20, pady=20)
        self.progress.set(0)

        self.btn_generate = ctk.CTkButton(self.bottom_frame, text="🔥 GENERATE MASTERPIECE", font=ctk.CTkFont(size=16, weight="bold"), height=45, fg_color="#d9534f", hover_color="#c9302c", command=self.start_generation)
        self.btn_generate.pack(side="right", padx=20, pady=15)

    # --- PRO API SETTINGS ---
    def open_api_settings(self):
        api_window = ctk.CTkToplevel(self)
        api_window.title(f"Pro API Configuration ({APP_VERSION})")
        api_window.geometry("650x550")
        api_window.attributes("-topmost", True)

        tabview = ctk.CTkTabview(api_window, width=600, height=450)
        tabview.pack(padx=20, pady=10, fill="both", expand=True)

        tab_llm = tabview.add("🧠 LLM (Magic Prompt)")
        tab_audio = tabview.add("🎸 Audio (Replicate API)")

        # --- LLM TAB ---
        ctk.CTkLabel(tab_llm, text="API Key Pool (Paste multiple keys, one per line):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.txt_llm_keys = ctk.CTkTextbox(tab_llm, height=80)
        self.txt_llm_keys.pack(padx=10, pady=5, fill="x")

        self.lbl_llm_status = ctk.CTkLabel(tab_llm, text="Waiting for API Keys...", text_color="orange", font=ctk.CTkFont(weight="bold"))
        self.lbl_llm_status.pack(pady=5)

        ctk.CTkLabel(tab_llm, text="Provider Preset:").pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_provider = ctk.CTkComboBox(tab_llm, values=["Groq", "NVIDIA Build", "OpenRouter", "Custom (OpenAI Compatible)"], command=self.on_provider_change)
        self.combo_provider.pack(padx=10, pady=5, fill="x")

        self.frame_custom = ctk.CTkFrame(tab_llm, fg_color="transparent")
        self.frame_custom.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(self.frame_custom, text="Base URL:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_base_url = ctk.CTkEntry(self.frame_custom, width=400)
        self.entry_base_url.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.frame_custom, text="Model Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_model = ctk.CTkEntry(self.frame_custom, width=400)
        self.entry_model.grid(row=1, column=1, padx=10, pady=5)

        btn_test_llm = ctk.CTkButton(tab_llm, text="🔌 Test Connection", fg_color="#1f538d", command=self.test_llm_connection)
        btn_test_llm.pack(pady=10)

        # --- AUDIO TAB (REPLICATE - NO LIBRARY NEEDED) ---
        ctk.CTkLabel(tab_audio, text="Replicate API Token (For MusicGen):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.txt_audio_keys = ctk.CTkTextbox(tab_audio, height=80)
        self.txt_audio_keys.pack(padx=10, pady=5, fill="x")

        self.lbl_audio_status = ctk.CTkLabel(tab_audio, text="Waiting for Token...", text_color="orange", font=ctk.CTkFont(weight="bold"))
        self.lbl_audio_status.pack(pady=5)

        ctk.CTkLabel(tab_audio, text="MusicGen Model Version:").pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_audio_model = ctk.CTkEntry(tab_audio, width=400)
        self.entry_audio_model.pack(padx=10, pady=5, fill="x")

        btn_test_audio = ctk.CTkButton(tab_audio, text="🔌 Test Replicate Connection", fg_color="#1f538d", command=self.test_audio_connection)
        btn_test_audio.pack(pady=10)

        # Save Button
        ctk.CTkButton(api_window, text="💾 Save All Settings", fg_color="#28a745", hover_color="#218838", height=40, command=lambda: self.save_api_settings(api_window)).pack(pady=10)

        self.load_api_settings()

    def on_provider_change(self, choice):
        self.entry_base_url.delete(0, "end")
        self.entry_model.delete(0, "end")
        
        if choice == "Groq":
            self.entry_base_url.insert(0, "https://api.groq.com/openai/v1/chat/completions")
            self.entry_model.insert(0, "llama3-8b-8192")
        elif choice == "NVIDIA Build":
            self.entry_base_url.insert(0, "https://integrate.api.nvidia.com/v1/chat/completions")
            self.entry_model.insert(0, "meta/llama-3.1-8b-instruct")
        elif choice == "OpenRouter":
            self.entry_base_url.insert(0, "https://openrouter.ai/api/v1/chat/completions")
            self.entry_model.insert(0, "meta-llama/llama-3-8b-instruct:free")

    # --- REAL API TESTING LOGIC ---
    def test_llm_connection(self):
        self.lbl_llm_status.configure(text="Testing Connection... Please wait.", text_color="yellow")
        threading.Thread(target=self._run_llm_test).start()

    def _run_llm_test(self):
        keys = self.txt_llm_keys.get("0.0", "end").strip().split('\n')
        api_key = keys[0].strip() if keys else ""
        if not api_key:
            self.lbl_llm_status.configure(text="❌ Error: No API Key Found", text_color="red")
            return
        
        url = self.entry_base_url.get()
        model = self.entry_model.get()
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages":[{"role": "user", "content": "Hi"}], "max_tokens": 5}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                self.lbl_llm_status.configure(text="✅ Connection Successful! Key is working.", text_color="#28a745")
            else:
                self.lbl_llm_status.configure(text=f"❌ API Error: {response.status_code} - Check Key or Model", text_color="red")
        except Exception as e:
            self.lbl_llm_status.configure(text="❌ Network Error: Check Base URL", text_color="red")

    def test_audio_connection(self):
        self.lbl_audio_status.configure(text="Testing Connection... Please wait.", text_color="yellow")
        threading.Thread(target=self._run_audio_test).start()

    def _run_audio_test(self):
        keys = self.txt_audio_keys.get("0.0", "end").strip().split('\n')
        api_key = keys[0].strip() if keys else ""
        
        if not api_key:
            self.lbl_audio_status.configure(text="❌ Error: No Token Found", text_color="red")
            return
            
        try:
            # Using raw requests instead of replicate library
            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json"
            }
            # We check the models endpoint to see if the token is valid
            response = requests.get("https://api.replicate.com/v1/models/meta/musicgen", headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.lbl_audio_status.configure(text="✅ Replicate Token Valid & Ready!", text_color="#28a745")
            elif response.status_code == 401:
                self.lbl_audio_status.configure(text="❌ API Error: 401 - Invalid Token", text_color="red")
            else:
                self.lbl_audio_status.configure(text=f"❌ API Error: {response.status_code}", text_color="red")
        except Exception as e:
            self.lbl_audio_status.configure(text="❌ Network Error", text_color="red")

    def save_api_settings(self, window):
        data = {
            "llm_keys": self.txt_llm_keys.get("0.0", "end").strip(),
            "provider": self.combo_provider.get(),
            "base_url": self.entry_base_url.get(),
            "model_name": self.entry_model.get(),
            "audio_keys": self.txt_audio_keys.get("0.0", "end").strip(),
            "audio_model_id": self.entry_audio_model.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        window.destroy()

    def load_api_settings(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.txt_llm_keys.insert("0.0", data.get("llm_keys", ""))
                self.combo_provider.set(data.get("provider", "Groq"))
                
                self.entry_base_url.delete(0, "end")
                self.entry_base_url.insert(0, data.get("base_url", ""))
                
                self.entry_model.delete(0, "end")
                self.entry_model.insert(0, data.get("model_name", ""))
                
                self.txt_audio_keys.insert("0.0", data.get("audio_keys", ""))
                
                self.entry_audio_model.delete(0, "end")
                self.entry_audio_model.insert(0, data.get("audio_model_id", "meta/musicgen:7a76a8258b23fae65c5a22debb88e5d2d7e81618e4d4cb711878d1d327142b96"))
        else:
            self.on_provider_change("Groq")
            self.entry_audio_model.insert(0, "meta/musicgen:7a76a8258b23fae65c5a22debb88e5d2d7e81618e4d4cb711878d1d327142b96")

    # --- GENERATION LOGIC ---
    def start_generation(self):
        self.btn_generate.configure(state="disabled", text="⏳ GENERATING...")
        self.progress.set(0.1)
        self.lbl_status.configure(text="[ Step 1: Creating Magic Prompt... ]", text_color="#f0ad4e")
        threading.Thread(target=self.process_magic_prompt).start()

    def process_magic_prompt(self):
        try:
            if not os.path.exists(CONFIG_FILE):
                self.update_status("Error: Please save API Keys first!", "red")
                return

            with open(CONFIG_FILE, "r") as f:
                keys_data = json.load(f)

            llm_keys = keys_data.get("llm_keys", "").split('\n')
            api_key = llm_keys[0].strip() if llm_keys else ""
            
            if not api_key:
                self.update_status("Error: LLM API Key is missing!", "red")
                return

            url = keys_data.get("base_url", "")
            model = keys_data.get("model_name", "")
            user_prompt = self.txt_prompt.get("0.0", "end").strip()
            genre = self.combo_genre.get()
            mood = self.combo_mood.get()

            system_instruction = "You are an expert AI Music Prompt Engineer. Convert the user's short idea into a highly detailed, professional music generation prompt (max 40 words). Focus on instruments, tempo, and atmosphere."
            user_message = f"Idea: {user_prompt}, Genre: {genre}, Mood: {mood}"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages":[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 100
            }

            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                magic_prompt = response.json()['choices'][0]['message']['content'].strip()
                
                self.txt_prompt.delete("0.0", "end")
                self.txt_prompt.insert("0.0", f"✨ MAGIC PROMPT:\n{magic_prompt}")
                
                self.progress.set(0.4)
                self.update_status("[ Step 2: Magic Prompt Ready! Waiting for MusicGen... ]", "#5cb85c")
            else:
                self.update_status(f"API Error: {response.status_code}", "red")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
        finally:
            self.btn_generate.configure(state="normal", text="🔥 GENERATE MASTERPIECE")

    def update_status(self, text, color):
        self.lbl_status.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = AuraSyncStudio()
    app.mainloop()
