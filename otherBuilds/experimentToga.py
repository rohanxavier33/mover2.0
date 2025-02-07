"""
Keeps computer alert and alive with a user-configurable runtime.
"""

import threading
import time
from random import randint

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

# We'll modify the run_script so that it checks 'app.running' on each loop iteration.
def run_script(app):
    import pyautogui
    while app.running:
        pyautogui.press('volumemute')
        x = randint(1, 1000)
        y = randint(1, 1000)
        pyautogui.press('volumeup')
        pyautogui.moveTo(x, y, 5)
        pyautogui.press('capslock')
        time.sleep(10)
        pyautogui.press('capslock')

def countdown(app, hours, minutes):
    total_seconds = hours * 3600 + minutes * 60

    while app.running and total_seconds > 0:
        hrs_left = total_seconds // 3600
        mins_left = (total_seconds % 3600) // 60
        secs_left = total_seconds % 60

        # Update the label with remaining time
        app.time_left_label.text = f"Time Left: {hrs_left:02d}:{mins_left:02d}:{secs_left:02d}"

        time.sleep(1)
        total_seconds -= 1

    # Time is up if total_seconds==0 while still running
    if total_seconds == 0 and app.running:
        app.stop_script(None)

class MouseMoverApp(toga.App):
    def startup(self):
        # Use 'formal_name' to avoid deprecation warnings
        self.main_window = toga.MainWindow(title=self.formal_name, size=(350, 250))
        self.running = False

        # Hours input
        self.hours_input = toga.TextInput(
            placeholder='Hours',
            style=Pack(width=70)
        )

        # Minutes input
        self.minutes_input = toga.TextInput(
            placeholder='Minutes',
            style=Pack(width=70)
        )

        # Infinite switch (no on_toggle param; set callback below)
        self.infinite_switch = toga.Switch(
            "Infinite",
            style=Pack(padding=(0, 10))
        )
        # Attach a callback for when the switch is pressed/toggled:
        self.infinite_switch.on_press = self.on_infinite_toggle

        # Label to display time left
        self.time_left_label = toga.Label("Time Left: --:--:--", style=Pack(padding=(10, 0)))

        # Create a button to start the script
        start_button = toga.Button(
            'Start Script',
            on_press=self.start_script,
            style=Pack(padding=10)
        )

        # Create a button to stop the script
        stop_button = toga.Button(
            'Stop Script',
            on_press=self.stop_script,
            style=Pack(padding=10)
        )

        # Layout for the hour/minute inputs
        time_input_box = toga.Box(
            children=[self.hours_input, self.minutes_input],
            style=Pack(direction=ROW, alignment="center", spacing=10)
        )

        # Layout for start/stop buttons
        button_box = toga.Box(
            children=[start_button, stop_button],
            style=Pack(direction=ROW, alignment="center", spacing=10)
        )

        # Main layout
        main_box = toga.Box(
            children=[
                time_input_box,
                self.infinite_switch,
                self.time_left_label,
                button_box
            ],
            style=Pack(direction=COLUMN, padding=10, alignment="center", spacing=10)
        )

        self.main_window.content = main_box
        self.main_window.show()

        self.script_thread = None
        self.countdown_thread = None

    def on_infinite_toggle(self, widget):
        """
        Called when the infinite switch is toggled.
        Check widget.value to see if it's True or False.
        """
        if widget.value:
            # If infinite is selected, disable hour/min inputs
            self.hours_input.enabled = False
            self.minutes_input.enabled = False
            self.hours_input.value = ""
            self.minutes_input.value = ""
            self.time_left_label.text = "Time Left: Infinite"
        else:
            self.hours_input.enabled = True
            self.minutes_input.enabled = True
            self.time_left_label.text = "Time Left: --:--:--"

    def start_script(self, widget):
        if not self.running:
            self.running = True
            self.script_thread = threading.Thread(target=run_script, args=(self,), daemon=True)
            self.script_thread.start()

            # If not infinite, start countdown if hours/minutes > 0
            if not self.infinite_switch.value:
                try:
                    hours = int(self.hours_input.value) if self.hours_input.value else 0
                    minutes = int(self.minutes_input.value) if self.minutes_input.value else 0
                except ValueError:
                    hours, minutes = 0, 0

                if hours > 0 or minutes > 0:
                    self.countdown_thread = threading.Thread(
                        target=countdown,
                        args=(self, hours, minutes),
                        daemon=True
                    )
                    self.countdown_thread.start()
                else:
                    self.time_left_label.text = "Time Left: Infinite (0 entered)"

    def stop_script(self, widget):
        if self.running:
            self.running = False
            self.time_left_label.text = "Time Left: --:--:--"
            # Threads will stop automatically because they're daemon threads.

def main():
    # Provide 'formal_name' to avoid the name deprecation warning
    return MouseMoverApp(formal_name='Mouse Mover', app_id='org.beeware.mousemover')

if __name__ == '__main__':
    app = main()
    app.main_loop()
