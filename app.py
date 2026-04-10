import customtkinter as ctk
import tkinter as tk

# --- Theme Settings ---
ctk.set_appearance_mode("dark")  # Dark Theme for Professional Look
ctk.set_default_color_theme("blue")

class AuraSyncStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("AuraSync AI Studio - Professional Music Remaker")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Grid Layout (3 Columns: Left, Center, Right)
        self.grid_columnconfigure(0, weight=1) # Left Panel
        self.grid_columnconfigure(1, weight=2) # Center Panel (Bigger)
        self.grid_columnconfigure(2, weight=1) # Right Panel
        self.grid_rowconfigure(0, weight=1)    # Main Content
        self.grid_rowconfigure(1, weight=0)    # Bottom Bar

        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
        self.build_bottom_bar()

    def build_left_panel(self):
        # Left Panel - Input & AI Director
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.left_frame, text="🎙️ INPUT & AI DIRECTOR", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        # Audio Dropzone
        self.btn_upload = ctk.CTkButton(self.left_frame, text="Drop Original Song Here\n(or Click to Browse)", height=80, fg_color="#2b2b2b", hover_color="#3b3b3b", border_width=2, border_color="#1f538d")
        self.btn_upload.pack(padx=20, pady=10, fill="x")

        # AI Prompt Box
        ctk.CTkLabel(self.left_frame, text="AI Music Prompt:").pack(anchor="w", padx=20, pady=(10, 0))
        self.txt_prompt = ctk.CTkTextbox(self.left_frame, height=100)
        self.txt_prompt.pack(padx=20, pady=5, fill="x")
        self.txt_prompt.insert("0.0", "E.g., Sri Lankan Baila, upbeat, acoustic guitar...")

        # Style Dropdowns
        ctk.CTkLabel(self.left_frame, text="Genre:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_genre = ctk.CTkComboBox(self.left_frame, values=["Baila", "Pop", "Classical", "EDM", "Rock", "Acoustic"])
        self.combo_genre.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self.left_frame, text="Mood:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_mood = ctk.CTkComboBox(self.left_frame, values=["Energetic", "Sad", "Romantic", "Cinematic", "Dark"])
        self.combo_mood.pack(padx=20, pady=5, fill="x")

    def build_center_panel(self):
        # Center Panel - The Arranger & Timeline
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.center_frame, text="🎛️ MULTI-TRACK ARRANGER", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        # Placeholder for Waveform
        self.wave_frame = ctk.CTkFrame(self.center_frame, height=150, fg_color="#141414")
        self.wave_frame.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(self.wave_frame, text="[ Audio Waveform Visualizer ]", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")

        # Stems (Tracks)
        tracks =["🎤 AI Cleaned Vocals", "🥁 Drums & Percussion", "🎸 Bass", "🎹 Melody & Chords"]
        for track in tracks:
            track_frame = ctk.CTkFrame(self.center_frame, height=60, fg_color="#242424")
            track_frame.pack(padx=20, pady=5, fill="x")
            ctk.CTkLabel(track_frame, text=track, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkSlider(track_frame, width=150).pack(side="right", padx=15, pady=15) # Volume Slider

    def build_right_panel(self):
        # Right Panel - Pro Mastering & Effects
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.right_frame, text="🎚️ PRO MASTERING", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        # Vocal Processing
        ctk.CTkLabel(self.right_frame, text="Vocal Processing", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.switch_cleaner = ctk.CTkSwitch(self.right_frame, text="AI Noise Cleaner")
        self.switch_cleaner.pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(self.right_frame, text="Auto-Tune Level:").pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        # Mastering FX
        ctk.CTkLabel(self.right_frame, text="Mastering FX", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(self.right_frame, text="Reverb (Space):").pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self.right_frame, text="Stereo Widener:").pack(anchor="w", padx=20, pady=(5, 0))
        ctk.CTkSlider(self.right_frame).pack(padx=20, pady=5, fill="x")

        # API Settings Button
        self.btn_api = ctk.CTkButton(self.right_frame, text="⚙️ API Settings", fg_color="transparent", border_width=1, text_color="white")
        self.btn_api.pack(side="bottom", padx=20, pady=20, fill="x")

    def build_bottom_bar(self):
        # Bottom Bar - Action & Playback
        self.bottom_frame = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color="#141414")
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        # Playback Controls
        self.btn_play = ctk.CTkButton(self.bottom_frame, text="▶ PLAY", width=80, fg_color="#28a745", hover_color="#218838")
        self.btn_play.pack(side="left", padx=20, pady=20)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.bottom_frame, width=400)
        self.progress.pack(side="left", padx=20, pady=20)
        self.progress.set(0)

        # Generate Button (The Big One)
        self.btn_generate = ctk.CTkButton(self.bottom_frame, text="🔥 GENERATE MASTERPIECE", font=ctk.CTkFont(size=16, weight="bold"), height=45, fg_color="#d9534f", hover_color="#c9302c")
        self.btn_generate.pack(side="right", padx=20, pady=15)

if __name__ == "__main__":
    app = AuraSyncStudio()
    app.mainloop()
