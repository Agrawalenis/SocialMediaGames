import tkinter as tk
import random

# Options
OPTIONS = ['rock', 'paper', 'scissor']

# Game logic
def get_winner(user_choice):
    comp_choice = random.choice(OPTIONS)

    if user_choice == comp_choice:
        result_text.set(f"It's a draw! You both chose {user_choice.upper()}")
    elif (user_choice == 'rock' and comp_choice == 'paper') or \
         (user_choice == 'paper' and comp_choice == 'scissor') or \
         (user_choice == 'scissor' and comp_choice == 'rock'):
        result_text.set(f"Computer wins! It chose {comp_choice.upper()}")
    else:
        result_text.set(f"You win! Computer chose {comp_choice.upper()}")

# GUI Setup
root = tk.Tk()
root.title("Stone Paper Scissor")
root.geometry("400x300")
root.config(bg="#f5cfe5")

title = tk.Label(root, text="Choose Your Move:", font=('Arial', 16, 'bold'), bg="#f5cfe5")
title.pack(pady=20)

btn_frame = tk.Frame(root, bg="#f5cfe5")
btn_frame.pack()

def create_button(text):
    return tk.Button(btn_frame, text=text.upper(), font=('Arial', 12, 'bold'),
                     bg="#33bdef", fg="white", width=10, height=2,
                     activebackground="#019ad2", command=lambda: get_winner(text))

for option in OPTIONS:
    btn = create_button(option)
    btn.pack(side='left', padx=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=('Arial', 14), fg="#db2b92", bg="#f5cfe5")
result_label.pack(pady=30)

root.mainloop()
