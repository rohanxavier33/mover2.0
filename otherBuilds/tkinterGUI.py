import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
from random import randint


class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Mover")

        # Control flag to indicate if we're running or not
        self.running = False

        # Variables for the GUI
        self.hours_var = tk.StringVar(value="")
        self.minutes_var = tk.StringVar(value="")
        self.infinite_var = tk.BooleanVar(value=False)

        # Set up the GUI elements
        self.create_widgets()

        # We'll keep references to the worker threads
        self.script_thread = None
        self.countdown_thread = None

    def create_widgets(self):
        # Frame for hour/minute inputs
        time_frame = ttk.Frame(self.root)
        time_frame.pack(pady=10)

        ttk.Label(time_frame, text="Hours:").grid(row=0, column=0, padx=5)
        self.hours_entry = ttk.Entry(time_frame, textvariable=self.hours_var, width=5)
        self.hours_entry.grid(row=0, column=1, padx=5)

        ttk.Label(time_frame, text="Minutes:").grid(row=0, column=2, padx=5)
        self.minutes_entry = ttk.Entry(time_frame, textvariable=self.minutes_var, width=5)
        self.minutes_entry.grid(row=0, column=3, padx=5)

        # Infinite checkbox
        self.infinite_check = ttk.Checkbutton(
            self.root,
            text="Infinite",
            variable=self.infinite_var,
            command=self.on_infinite_toggle
        )
        self.infinite_check.pack()

        # Label to display time left
        self.time_left_label = ttk.Label(self.root, text="Time Left: --:--:--", font=("TkDefaultFont", 10, "bold"))
        self.time_left_label.pack(pady=5)

        # Start/Stop buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        start_button = ttk.Button(button_frame, text="Start Script", command=self.start_script)
        start_button.grid(row=0, column=0, padx=10)

        stop_button = ttk.Button(button_frame, text="Stop Script", command=self.stop_script)
        stop_button.grid(row=0, column=1, padx=10)

    def on_infinite_toggle(self):
        """Enable/disable hour & minute entries depending on the infinite checkbox."""
        if self.infinite_var.get():
            self.hours_entry.config(state='disabled')
            self.minutes_entry.config(state='disabled')
            self.hours_var.set("")
            self.minutes_var.set("")
            self.time_left_label.config(text="Time Left: Infinite")
        else:
            self.hours_entry.config(state='normal')
            self.minutes_entry.config(state='normal')
            self.time_left_label.config(text="Time Left: --:--:--")

    def start_script(self):
        """Starts the mouse mover and optional countdown threads."""
        if not self.running:
            self.running = True

            # Parse hours and minutes
            hours = self.safe_int(self.hours_var.get())
            minutes = self.safe_int(self.minutes_var.get())

            # Start the main worker thread
            self.script_thread = threading.Thread(target=self.run_script, daemon=True)
            self.script_thread.start()

            # If not infinite, and we have some time set
            if not self.infinite_var.get():
                if hours > 0 or minutes > 0:
                    total_seconds = hours * 3600 + minutes * 60
                    self.countdown_thread = threading.Thread(
                        target=self.countdown,
                        args=(total_seconds,),
                        daemon=True
                    )
                    self.countdown_thread.start()
                else:
                    # If 0 time is entered, treat it effectively as infinite
                    self.time_left_label.config(text="Time Left: Infinite (0 entered)")

    def run_script(self):
        """
        The "mouse mover" loop:
        Press volume mute/up, move mouse, press capslock, etc.
        Continues while `self.running` is True.
        """
        while self.running:
            pyautogui.press('volumemute')
            x = randint(1, 1000)
            y = randint(1, 1000)
            pyautogui.press('volumeup')
            pyautogui.moveTo(x, y, 5)
            pyautogui.press('capslock')
            time.sleep(10)
            pyautogui.press('capslock')

    def countdown(self, total_seconds):
        """
        Decrements total_seconds every second, updating the label.
        When total_seconds hits 0, stop the script automatically.
        """
        while self.running and total_seconds > 0:
            # Convert total_seconds to H:M:S
            hrs_left = total_seconds // 3600
            mins_left = (total_seconds % 3600) // 60
            secs_left = total_seconds % 60

            # Update label. In a perfect world, we'd do this with .after().
            # For simplicity, we'll do it directly here.
            self.time_left_label.config(
                text=f"Time Left: {hrs_left:02d}:{mins_left:02d}:{secs_left:02d}"
            )

            time.sleep(1)
            total_seconds -= 1

        # If we run out of time while still running => time is up
        if total_seconds == 0 and self.running:
            self.stop_script()

    def stop_script(self):
        """Stops both the mouse mover and countdown."""
        if self.running:
            self.running = False
            self.time_left_label.config(text="Time Left: --:--:--")

    @staticmethod
    def safe_int(val):
        """Converts string to int, returns 0 on invalid."""
        try:
            return int(val)
        except ValueError:
            return 0


def main():
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
