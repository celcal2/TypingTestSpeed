import tkinter as tk
import random
import time
from bs4 import BeautifulSoup
import requests

LIGHT = "#FFF0F5"
PEACH = '#FFEADD'
PURPULE = "#916DB3"
FONT_NAME = "times"

class TypingSpeedTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title('Check your Typing Speed')
        self.root.config(padx=5, pady=5, bg=LIGHT)
        self.root.iconbitmap('flower.ico')

        # Variables
        self.start_time = 0

        # UI Elements
        self.label_sentence = tk.Label(root, text='', font=(FONT_NAME, 20), bg=LIGHT, fg=PURPULE)
        self.label_sentence.pack(pady=20)
        self.entry_typing = tk.Entry(root, font=(FONT_NAME, 20), bg=LIGHT, fg=PURPULE)
        self.entry_typing.pack(pady=10)

        self.btn_start = tk.Button(root, text="Start the test", width=20, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, "bold"), activebackground=PURPULE, command=self.start_typing_test)
        self.btn_start.pack(pady=10)

    def start_typing_test(self):
        self.response = requests.get('https://wolnelektury.pl/katalog/lektura/borowski-alicja-w-krainie-czarow.html')
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.words = self.soup.text.split(",")
        self.word = random.randint(0, (len(self.words) - 1))
        self.sentences = self.words[self.word]

        # Display the sentence
        self.label_sentence.config(text=self.sentences, font=(FONT_NAME, 20), bg=LIGHT, fg=PURPULE)

        # Enable the entry widget for typing
        self.entry_typing.config(state=tk.NORMAL, font=(FONT_NAME, 20), bg=LIGHT, fg='black')
        self.entry_typing.focus()
        self.entry_typing.delete(0, tk.END)

        # Record the start time
        self.start_time = time.time()

        # Bind the Enter key to the check_typing_speed method
        self.root.bind('<Return>', self.check_typing_speed)


    def check_typing_speed(self, event=None):

        # Calculate typing speed
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        typed_text = self.entry_typing.get()
        typed_words = len(typed_text.split())
        words_per_minute = int(typed_words / (elapsed_time / 60))

        # Display the typing speed
        result_message = f"Your typing speed: {words_per_minute} words per minute"
        self.label_sentence.config(text=result_message)

        # Disable the entry widget and re-enable the "Start Typing Test" button
        self.entry_typing.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.NORMAL)

        # Unbind the Enter key
        self.root.unbind('<Return>')

if __name__ == "__main__":
    root = tk.Tk()
    TypingSpeedTestApp(root)
    root.mainloop()

