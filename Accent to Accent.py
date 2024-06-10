import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import speech_recognition as sr
import threading
import os

class AccentTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Accent Translator")

        self.label = ttk.Label(master, text="Accent Translator")
        self.label.pack(pady=10)

        self.accent_var = tk.StringVar(value="1")
        self.accent_label = ttk.Label(master, text="Choose an accent type:")
        self.accent_label.pack()

        self.accent_combobox = ttk.Combobox(
            master,
            textvariable=self.accent_var,
            values=[
                "US English (en-US)",
                "UK English (en-GB)",
                "Spanish (es)",
                "French (fr)",
                "Indian English (en-IN)",
                "Canadian English (en-CA)",
                "Chinese (zh)",
                "Japanese (ja)",
            ],
        )
        self.accent_combobox.pack(pady=5)

        self.start_button = ttk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.recording_thread = None

    def get_accent(self):
        return {
            "1": "en-US",
            "2": "en-GB",
            "3": "es",
            "4": "fr",
            "5": "en-IN",
            "6": "en-CA",
            "7": "zh",
            "8": "ja",
        }.get(self.accent_var.get(), "en-US")

    def start_recording(self):
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join()
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED

    def record_audio(self):
        try:
            # Get the accent type from the combobox
            accent_type = self.get_accent()

            # Initialize the recognizer
            recognizer = sr.Recognizer()

            # Use the default microphone as the audio source
            with sr.Microphone() as source:
                print("Please start speaking...")

                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source)

                while True:
                    # Listen to the audio until there's silence or the stop button is pressed
                    audio_data = recognizer.listen(source, phrase_time_limit=5)

                    try:
                        # Recognize the speech using Google Speech Recognition
                        text = recognizer.recognize_google(audio_data)
                        print("You said:", text)

                        # Convert the recognized text to speech in the chosen accent
                        language = accent_type
                        speech = gTTS(text=text, lang=language, slow=False)
                        speech.save("texttospeech2.mp3")

                        # Play the generated audio on the command prompt
                        os.system("start texttospeech2.mp3")

                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")

        except Exception as e:
            print(f"Error in recording thread: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AccentTranslatorApp(root)
    root.mainloop()
