import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import json
import os
import requests
import threading
import time
import pygame

# --- Theme Settings ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "api_config.json"
APP_VERSION = "v1.7" # Added Test Button & Fixed Replicate 422 Error

class AuraSyncStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"AuraSync AI Studio ({APP_VERSION}) - Professional Music Remaker")
        self.geometry("1200x850")
        self.minsize(1000, 750)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        pygame.mixer.init()
        self.uploaded_file_path = None
        self.generated_audio_url = None
        self.is_playing = False

        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
        self.build_bottom_bar()

    def build_left_panel(self):
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.left_frame, text="🎙️ INPUT & AI DIRECTOR", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        self.btn_upload = ctk.CTkButton(self.left_frame, text="Drop Original Song Here\n(or Click to Browse)", height=80, fg_color="#2b2b2b", hover_color="#3b3b3b", border_width=2, border_color="#1f538d", command=self.upload_audio)
        self.btn_upload.pack(padx=20, pady=10, fill="x")
        
        self.lbl_file_name = ctk.CTkLabel(self.left_frame, text="No file selected", text_color="gray")
        self.lbl_file_name.pack(pady=(0, 10))

        ctk.CTkLabel(self.left_frame, text="AI Music Prompt:").pack(anchor="w", padx=20, pady=(10, 0))
        self.txt_prompt = ctk.CTkTextbox(self.left_frame, height=120)
        self.txt_prompt.pack(padx=20, pady=5, fill="x")
        self.txt_prompt.insert("0.0", "EDM, heavy bass, club dance vibe")

        self.btn_magic = ctk.CTkButton(self.left_frame, text="✨ Create Magic Prompt", fg_color="#f0ad4e", hover_color="#ec971f", text_color="black", command=self.generate_magic_prompt_only)
        self.btn_magic.pack(padx=20, pady=10, fill="x")

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

        self.btn_play = ctk.CTkButton(self.bottom_frame, text="▶ PLAY", width=80, fg_color="#28a745", hover_color="#218838", command=self.toggle_playback)
        self.btn_play.pack(side="left", padx=20, pady=20)

        self.progress = ctk.CTkProgressBar(self.bottom_frame, width=400)
        self.progress.pack(side="left", padx=20, pady=20)
        self.progress.set(0)

        self.btn_generate = ctk.CTkButton(self.bottom_frame, text="🔥 GENERATE MASTERPIECE", font=ctk.CTkFont(size=16, weight="bold"), height=45, fg_color="#d9534f", hover_color="#c9302c", command=self.start_generation)
        self.btn_generate.pack(side="right", padx=20, pady=15)

    def upload_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.uploaded_file_path = file_path
            file_name = os.path.basename(file_path)
            self.lbl_file_name.configure(text=f"Selected: {file_name}", text_color="#5cb85c")
            self.update_status(f"[ Ready to process: {file_name} ]", "white")

    def toggle_playback(self):
        if not self.generated_audio_url:
            self.update_status("No generated audio to play!", "red")
            return

        if self.is_playing:
            pygame.mixer.music.pause()
            self.btn_play.configure(text="▶ PLAY", fg_color="#28a745")
            self.is_playing = False
        else:
            if self.generated_audio_url.startswith("http"):
                self.update_status("Downloading audio for playback...", "yellow")
                threading.Thread(target=self._download_and_play).start()
            else:
                pygame.mixer.music.unpause()
                self.btn_play.configure(text="⏸ PAUSE", fg_color="#d9534f")
                self.is_playing = True

    def _download_and_play(self):
        try:
            temp_file = "temp_output.wav"
            response = requests.get(self.generated_audio_url)
            with open(temp_file, "wb") as f:
                f.write(response.content)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            self.btn_play.configure(text="⏸ PAUSE", fg_color="#d9534f")
            self.is_playing = True
            self.update_status("[ Playing Generated Masterpiece ]", "#5cb85c")
            self.generated_audio_url = temp_file
        except Exception as e:
            self.update_status("Playback Error!", "red")

    # --- PRO API SETTINGS ---
    def open_api_settings(self):
        api_window = ctk.CTkToplevel(self)
        api_window.title(f"Pro API Configuration ({APP_VERSION})")
        api_window.geometry("700x750")
        api_window.attributes("-topmost", True)

        tabview = ctk.CTkTabview(api_window, width=650, height=650)
        tabview.pack(padx=20, pady=10, fill="both", expand=True)

        tab_llm = tabview.add("🧠 LLM (Magic Prompt)")
        tab_audio = tabview.add("🎸 Audio (Dynamic Engine)")

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
        self.entry_base_url = ctk.CTkEntry(self.frame_custom, width=450)
        self.entry_base_url.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.frame_custom, text="Model Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_model = ctk.CTkEntry(self.frame_custom, width=450)
        self.entry_model.grid(row=1, column=1, padx=10, pady=5)

        btn_test_llm = ctk.CTkButton(tab_llm, text="🔌 Test Connection", fg_color="#1f538d", command=self.test_llm_connection)
        btn_test_llm.pack(pady=10)

        # --- AUDIO TAB ---
        ctk.CTkLabel(tab_audio, text="Audio API Key (Replicate or HuggingFace):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.txt_audio_keys = ctk.CTkTextbox(tab_audio, height=60)
        self.txt_audio_keys.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(tab_audio, text="API Type (How it works):").pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_audio_type = ctk.CTkComboBox(tab_audio, values=["Replicate (Polling)", "Direct (HuggingFace/Local)"], command=self.on_audio_type_change)
        self.combo_audio_type.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(tab_audio, text="Base URL:").pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_audio_url = ctk.CTkEntry(tab_audio)
        self.entry_audio_url.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(tab_audio, text="Headers (JSON format - use <API_KEY> placeholder):").pack(anchor="w", padx=10, pady=(5, 0))
        self.txt_audio_headers = ctk.CTkTextbox(tab_audio, height=60)
        self.txt_audio_headers.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(tab_audio, text="Payload (JSON format - use <PROMPT> placeholder):").pack(anchor="w", padx=10, pady=(5, 0))
        self.txt_audio_payload = ctk.CTkTextbox(tab_audio, height=100)
        self.txt_audio_payload.pack(padx=10, pady=5, fill="x")

        # NEW: Added Test Audio Connection Button back!
        self.lbl_audio_status = ctk.CTkLabel(tab_audio, text="Waiting for Token...", text_color="orange", font=ctk.CTkFont(weight="bold"))
        self.lbl_audio_status.pack(pady=5)

        btn_test_audio = ctk.CTkButton(tab_audio, text="🔌 Test Audio Connection", fg_color="#1f538d", command=self.test_audio_connection)
        btn_test_audio.pack(pady=5)

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

    def on_audio_type_change(self, choice):
        self.entry_audio_url.delete(0, "end")
        self.txt_audio_headers.delete("0.0", "end")
        self.txt_audio_payload.delete("0.0", "end")

        if choice == "Replicate (Polling)":
            # FIX FOR 422 ERROR: Using the direct model endpoint instead of version hash
            self.entry_audio_url.insert(0, "https://api.replicate.com/v1/models/meta/musicgen/predictions")
            self.txt_audio_headers.insert("0.0", '{\n  "Authorization": "Token <API_KEY>",\n  "Content-Type": "application/json"\n}')
            self.txt_audio_payload.insert("0.0", '{\n  "input": {\n    "prompt": "<PROMPT>",\n    "model_version": "melody",\n    "duration": 8\n  }\n}')
        elif choice == "Direct (HuggingFace/Local)":
            self.entry_audio_url.insert(0, "https://api-inference.huggingface.co/models/facebook/musicgen-small")
            self.txt_audio_headers.insert("0.0", '{\n  "Authorization": "Bearer <API_KEY>",\n  "Content-Type": "application/json"\n}')
            self.txt_audio_payload.insert("0.0", '{\n  "inputs": "<PROMPT>"\n}')

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
                self.lbl_llm_status.configure(text=f"❌ API Error: {response.status_code}", text_color="red")
        except Exception as e:
            self.lbl_llm_status.configure(text="❌ Network Error", text_color="red")

    def test_audio_connection(self):
        self.lbl_audio_status.configure(text="Testing Connection... Please wait.", text_color="yellow")
        threading.Thread(target=self._run_audio_test).start()

    def _run_audio_test(self):
        keys = self.txt_audio_keys.get("0.0", "end").strip().split('\n')
        api_key = keys[0].strip() if keys else ""
        if not api_key:
            self.lbl_audio_status.configure(text="❌ Error: No Token Found", text_color="red")
            return
            
        api_type = self.combo_audio_type.get()
        
        try:
            if api_type == "Replicate (Polling)":
                headers = {"Authorization": f"Token {api_key}"}
                res = requests.get("https://api.replicate.com/v1/models/meta/musicgen", headers=headers, timeout=10)
                if res.status_code == 200:
                    self.lbl_audio_status.configure(text="✅ Replicate Token Valid!", text_color="#28a745")
                else:
                    self.lbl_audio_status.configure(text=f"❌ API Error: {res.status_code}", text_color="red")
            else:
                url = self.entry_audio_url.get()
                headers = {"Authorization": f"Bearer {api_key}"}
                res = requests.post(url, headers=headers, json={"inputs": "test"}, timeout=10)
                if res.status_code in [200, 503, 400, 422]:
                    self.lbl_audio_status.configure(text="✅ HF Token Valid!", text_color="#28a745")
                else:
                    self.lbl_audio_status.configure(text=f"❌ API Error: {res.status_code}", text_color="red")
        except Exception as e:
            self.lbl_audio_status.configure(text="❌ Network Error", text_color="red")

    def save_api_settings(self, window):
        data = {
            "llm_keys": self.txt_llm_keys.get("0.0", "end").strip(),
            "provider": self.combo_provider.get(),
            "base_url": self.entry_base_url.get(),
            "model_name": self.entry_model.get(),
            "audio_keys": self.txt_audio_keys.get("0.0", "end").strip(),
            "audio_type": self.combo_audio_type.get(),
            "audio_url": self.entry_audio_url.get(),
            "audio_headers": self.txt_audio_headers.get("0.0", "end").strip(),
            "audio_payload": self.txt_audio_payload.get("0.0", "end").strip()
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
                self.entry_base_url.insert(0, data.get("base_url", ""))
                self.entry_model.insert(0, data.get("model_name", ""))
                
                self.txt_audio_keys.insert("0.0", data.get("audio_keys", ""))
                self.combo_audio_type.set(data.get("audio_type", "Replicate (Polling)"))
                self.entry_audio_url.insert(0, data.get("audio_url", ""))
                self.txt_audio_headers.insert("0.0", data.get("audio_headers", ""))
                self.txt_audio_payload.insert("0.0", data.get("audio_payload", ""))
        else:
            self.on_provider_change("Groq")
            self.on_audio_type_change("Replicate (Polling)")

    def generate_magic_prompt_only(self):
        self.btn_magic.configure(state="disabled", text="⏳ Creating...")
        self.update_status("[ Creating Magic Prompt... ]", "#f0ad4e")
        threading.Thread(target=self._run_magic_prompt).start()

    def _run_magic_prompt(self):
        try:
            if not os.path.exists(CONFIG_FILE):
                self.update_status("Error: Please save API Keys first!", "red")
                return

            with open(CONFIG_FILE, "r") as f:
                keys_data = json.load(f)

            llm_key = keys_data.get("llm_keys", "").split('\n')[0].strip()
            if not llm_key:
                self.update_status("Error: LLM API Key is missing!", "red")
                return

            url = keys_data.get("base_url", "")
            model = keys_data.get("model_name", "")
            user_prompt = self.txt_prompt.get("0.0", "end").strip()
            
            if "✨ MAGIC PROMPT:\n" in user_prompt:
                user_prompt = user_prompt.replace("✨ MAGIC PROMPT:\n", "")

            genre = self.combo_genre.get()
            mood = self.combo_mood.get()

            system_instruction = "You are an expert AI Music Prompt Engineer. Convert the user's short idea into a highly detailed, professional music generation prompt (max 40 words). Focus on instruments, tempo, and atmosphere."
            user_message = f"Idea: {user_prompt}, Genre: {genre}, Mood: {mood}"

            headers = {"Authorization": f"Bearer {llm_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages":[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_message}], "max_tokens": 100}

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                magic_prompt = response.json()['choices'][0]['message']['content'].strip()
                self.txt_prompt.delete("0.0", "end")
                self.txt_prompt.insert("0.0", f"✨ MAGIC PROMPT:\n{magic_prompt}")
                self.update_status("[ Magic Prompt Ready! ]", "#5cb85c")
            else:
                self.update_status(f"LLM API Error: {response.status_code}", "red")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
        finally:
            self.btn_magic.configure(state="normal", text="✨ Create Magic Prompt")

    def start_generation(self):
        if not self.uploaded_file_path:
            self.update_status("Error: Please upload an original song first!", "red")
            return

        self.btn_generate.configure(state="disabled", text="⏳ GENERATING...")
        self.progress.set(0.1)
        self.update_status("[ Starting Generation Process... ]", "#f0ad4e")
        threading.Thread(target=self.process_audio_generation).start()

    def process_audio_generation(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                keys_data = json.load(f)

            audio_key = keys_data.get("audio_keys", "").split('\n')[0].strip()
            if not audio_key:
                self.update_status("Error: Audio API Key is missing!", "red")
                return

            final_prompt = self.txt_prompt.get("0.0", "end").strip()
            if "✨ MAGIC PROMPT:\n" in final_prompt:
                final_prompt = final_prompt.replace("✨ MAGIC PROMPT:\n", "")

            api_type = keys_data.get("audio_type", "")
            url = keys_data.get("audio_url", "")
            headers_str = keys_data.get("audio_headers", "")
            payload_str = keys_data.get("audio_payload", "")

            headers_str = headers_str.replace("<API_KEY>", audio_key)
            safe_prompt = final_prompt.replace('"', '\\"').replace('\n', ' ')
            payload_str = payload_str.replace("<PROMPT>", safe_prompt)

            try:
                headers = json.loads(headers_str)
                payload = json.loads(payload_str)
            except json.JSONDecodeError:
                self.update_status("Error: Invalid JSON in Audio Settings!", "red")
                return

            self.progress.set(0.4)
            self.update_status("[ Sending Request to Audio AI... ]", "#5cb85c")

            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code not in[200, 201]:
                self.update_status(f"Audio API Error: {response.status_code} - {response.text[:50]}", "red")
                return

            if api_type == "Replicate (Polling)":
                pred_url = response.json().get("urls", {}).get("get")
                if not pred_url:
                    self.update_status("Error: Replicate didn't return a polling URL", "red")
                    return
                
                while True:
                    time.sleep(3)
                    status_res = requests.get(pred_url, headers=headers)
                    status_data = status_res.json()
                    
                    if status_data["status"] == "succeeded":
                        self.generated_audio_url = status_data["output"]
                        break
                    elif status_data["status"] == "failed":
                        self.update_status("Music Generation Failed!", "red")
                        return
                    
                    self.update_status(f"[ Generating Music... Status: {status_data['status']} ]", "yellow")

            elif api_type == "Direct (HuggingFace/Local)":
                temp_file = "temp_output.wav"
                with open(temp_file, "wb") as f:
                    f.write(response.content)
                self.generated_audio_url = temp_file

            self.progress.set(1.0)
            self.update_status("[ Masterpiece Ready! Click PLAY ]", "#28a745")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
        finally:
            self.btn_generate.configure(state="normal", text="🔥 GENERATE MASTERPIECE")

    def update_status(self, text, color):
        self.lbl_status.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = AuraSyncStudio()
    app.mainloop()
