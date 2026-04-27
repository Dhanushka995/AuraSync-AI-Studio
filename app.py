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

class AuraSyncStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AuraSync AI Studio - Professional Music Remaker")
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
        self.txt_prompt.insert("0.0", "Sri Lankan Baila, upbeat, acoustic guitar")

        ctk.CTkLabel(self.left_frame, text="Genre:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_genre = ctk.CTkComboBox(self.left_frame, values=["Baila", "Pop", "Classical", "EDM", "Rock", "Acoustic"])
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

        # Generate Button is now connected to the function!
        self.btn_generate = ctk.CTkButton(self.bottom_frame, text="🔥 GENERATE MASTERPIECE", font=ctk.CTkFont(size=16, weight="bold"), height=45, fg_color="#d9534f", hover_color="#c9302c", command=self.start_generation)
        self.btn_generate.pack(side="right", padx=20, pady=15)

    def open_api_settings(self):
        api_window = ctk.CTkToplevel(self)
        api_window.title("API Configuration")
        api_window.geometry("550x400")
        api_window.attributes("-topmost", True)

        ctk.CTkLabel(api_window, text="Connect AI Models", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        ctk.CTkLabel(api_window, text="Hugging Face API Key (For Music Generation):").pack(anchor="w", padx=20)
        hf_entry = ctk.CTkEntry(api_window, width=500, show="*")
        hf_entry.pack(padx=20, pady=5)

        ctk.CTkLabel(api_window, text="Select AI Brain (For Magic Prompt):").pack(anchor="w", padx=20, pady=(15,0))
        provider_combo = ctk.CTkComboBox(api_window, width=500, values=["Groq (Fastest)", "NVIDIA Build (High Quality)", "OpenRouter (Multi-Model)"])
        provider_combo.pack(padx=20, pady=5)

        ctk.CTkLabel(api_window, text="Provider API Key:").pack(anchor="w", padx=20, pady=(10,0))
        llm_entry = ctk.CTkEntry(api_window, width=500, show="*")
        llm_entry.pack(padx=20, pady=5)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                hf_entry.insert(0, data.get("huggingface", ""))
                provider_combo.set(data.get("llm_provider", "Groq (Fastest)"))
                llm_entry.insert(0, data.get("llm_key", ""))

        def save_keys():
            keys = {
                "huggingface": hf_entry.get(),
                "llm_provider": provider_combo.get(),
                "llm_key": llm_entry.get()
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(keys, f)
            api_window.destroy()

        ctk.CTkButton(api_window, text="Save Keys", fg_color="#28a745", hover_color="#218838", command=save_keys).pack(pady=20)

    # --- NEW: Generation Logic ---
    def start_generation(self):
        # Start in a new thread so the UI doesn't freeze
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
                keys = json.load(f)

            provider = keys.get("llm_provider", "")
            api_key = keys.get("llm_key", "")
            
            if not api_key:
                self.update_status("Error: LLM API Key is missing!", "red")
                return

            user_prompt = self.txt_prompt.get("0.0", "end").strip()
            genre = self.combo_genre.get()
            mood = self.combo_mood.get()

            system_instruction = "You are an expert AI Music Prompt Engineer. Convert the user's short idea into a highly detailed, professional music generation prompt (max 40 words). Focus on instruments, tempo, and atmosphere."
            user_message = f"Idea: {user_prompt}, Genre: {genre}, Mood: {mood}"

            # Setup API URL based on provider
            if "Groq" in provider:
                url = "https://api.groq.com/openai/v1/chat/completions"
                model = "llama3-8b-8192"
            elif "NVIDIA" in provider:
                url = "https://integrate.api.nvidia.com/v1/chat/completions"
                model = "meta/llama3-8b-instruct"
            elif "OpenRouter" in provider:
                url = "https://openrouter.ai/api/v1/chat/completions"
                model = "meta-llama/llama-3-8b-instruct:free"
            else:
                self.update_status("Error: Unsupported Provider", "red")
                return

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
                
                # Update UI with the new Magic Prompt
                self.txt_prompt.delete("0.0", "end")
                self.txt_prompt.insert("0.0", f"✨ MAGIC PROMPT:\n{magic_prompt}")
                
                self.progress.set(0.4)
                self.update_status("[ Step 2: Magic Prompt Ready! Waiting for MusicGen... ]", "#5cb85c")
                
                # Next step will be calling MusicGen here...
                
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
