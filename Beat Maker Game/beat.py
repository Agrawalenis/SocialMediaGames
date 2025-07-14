import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import os
import io
import time
from pydub import AudioSegment
from PIL import Image, ImageTk

# Initialize mixer
pygame.mixer.init()

# Key-to-file mappings
SOUNDS = {
    'w': 'sounds/sound1.mp3',
    'a': 'sounds/sound2.mp3',
    's': 'sounds/sound3.mp3',
    'd': 'sounds/sound4.mp3',
    'j': 'sounds/sound5.mp3',
    'k': 'sounds/sound6.mp3',
    'l': 'sounds/sound7.mp3'
}

LABELS = {
    'w': 'Tom 1',
    'a': 'Tom 2',
    's': 'Tom 3',
    'd': 'Tom 4',
    'j': 'Snare',
    'k': 'Crash',
    'l': 'Kick'
}

# Recording
recording = False
recorded_sequence = []
record_start_time = 0

# Load button images
image_refs = {}
def load_images():
    for key in SOUNDS.keys():
        try:
            img_path = f"images/{key}.png"
            img = Image.open(img_path).resize((80, 80))
            image_refs[key] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Image for '{key}' missing or invalid: {e}")
            image_refs[key] = None

# Play sound and record if active
def play_sound(key):
    current_key.set(key.upper())
    try:
        audio = AudioSegment.from_file(SOUNDS[key])
        buf = io.BytesIO()
        audio.export(buf, format='wav')
        buf.seek(0)
        pygame.mixer.Sound(file=buf).play()
        if recording:
            timestamp = time.perf_counter()
            recorded_sequence.append((timestamp, key))
    except Exception as e:
        print(f"Error playing {key}: {e}")

def animate_button(btn):
    btn.config(style="Pressed.TButton")
    btn.after(100, lambda: btn.config(style="TButton"))

def on_keypress(event):
    key = event.char.lower()
    if key in SOUNDS:
        play_sound(key)
        animate_button(button_refs[key])

def start_recording():
    global recording, recorded_sequence, record_start_time
    recording = True
    recorded_sequence = []
    record_start_time = time.perf_counter()
    record_label.set("🎙️ Recording...")

def stop_recording():
    global recording
    recording = False
    record_label.set("⏹️ Recording Stopped")
    if not recorded_sequence:
        messagebox.showinfo("Info", "No sounds recorded.")
        return
    save_recorded_beat()

def save_recorded_beat():
    try:
        if not recorded_sequence:
            return

        base_time = recorded_sequence[0][0]
        duration = int((recorded_sequence[-1][0] - base_time) * 1000) + 1000
        beat = AudioSegment.silent(duration=duration)

        for timestamp, key in recorded_sequence:
            offset = int((timestamp - base_time) * 1000)
            segment = AudioSegment.from_file(SOUNDS[key])
            beat = beat.overlay(segment, position=offset)

        file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")],
                                                 title="Save your beat as MP3")
        if file_path:
            beat.export(file_path, format="mp3")
            messagebox.showinfo("Success", f"MP3 beat saved:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not save MP3:\n{e}")


# GUI setup
root = tk.Tk()
root.title("🎵 Drum Kit Recorder")
root.geometry("700x650")
root.configure(bg="#1f2937")
root.bind("<KeyPress>", on_keypress)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12), padding=8, background="#3b82f6", foreground="white")
style.map("TButton", background=[('active', '#2563eb')])
style.configure("Pressed.TButton", background="#f59e0b")

tk.Label(root, text="🥁 Custom Drum Kit with Recording", font=("Helvetica", 22, "bold"), bg="#1f2937", fg="#fbbf24").pack(pady=10)
tk.Label(root, text="Press W, A, S, D, J, K, L or click buttons", bg="#1f2937", fg="#e5e7eb", font=("Arial", 12)).pack()

current_key = tk.StringVar(value="-")
tk.Label(root, textvariable=current_key, font=("Courier", 20, "bold"), bg="#1f2937", fg="#fbbf24").pack(pady=10)

frame = tk.Frame(root, bg="#1f2937")
frame.pack(pady=10)

button_refs = {}
row, col = 0, 0
load_images()

for key in ['w', 'a', 's', 'd', 'j', 'k', 'l']:
    img = image_refs.get(key)
    if img:
        btn = ttk.Button(frame, image=img, text=f"\n{key.upper()}", compound="top",
                         command=lambda k=key: [play_sound(k), animate_button(button_refs[k])])
    else:
        btn = ttk.Button(frame, text=f"{key.upper()}\n{LABELS[key]}",
                         command=lambda k=key: [play_sound(k), animate_button(button_refs[k])])

    btn.grid(row=row, column=col, padx=12, pady=12, ipadx=5, ipady=5)
    button_refs[key] = btn
    col += 1
    if col == 4:
        row += 1
        col = 0

# Controls
ttk.Button(root, text="🎙️ Start Recording", command=start_recording).pack(pady=5)
ttk.Button(root, text="⏹️ Stop & Save Recording", command=stop_recording).pack(pady=5)

record_label = tk.StringVar(value="Not Recording")
tk.Label(root, textvariable=record_label, bg="#1f2937", fg="white", font=("Arial", 12)).pack(pady=5)

tk.Label(root, text="Made by Akshay 🎧 using Python, Pygame, Tkinter, Pydub",
         bg="#1f2937", fg="#9ca3af", font=("Arial", 10)).pack(pady=20)

root.mainloop()
