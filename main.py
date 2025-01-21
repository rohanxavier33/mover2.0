"""
Keeps computer alert and alive
"""


import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pyautogui import moveTo, press
from time import sleep
from random import randint
import threading

def run_script():
    while True:
        press('volumemute')
        x = randint(1, 1000)
        y = randint(1, 1000)
        press('volumeup')
        moveTo(x, y, 5)
        press('capslock')
        sleep(10)
        press('capslock')

class MouseMoverApp(toga.App):
    def startup(self):
        # Create the main window
        self.main_window = toga.MainWindow(title=self.name, size=(300, 150))

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

        # Create a box to hold the buttons
        box = toga.Box(
            children=[start_button, stop_button],
            style=Pack(direction=COLUMN, padding=10)
        )

        # Add the box to the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

        # Variable to control the script's execution
        self.running = False

    def start_script(self, widget):
        if not self.running:
            self.running = True
            # Run the script in a separate thread
            self.script_thread = threading.Thread(target=run_script, daemon=True)
            self.script_thread.start()

    def stop_script(self, widget):
        self.running = False

def main():
    # Create and run the app
    return MouseMoverApp('Mouse Mover', 'org.beeware.mousemover')

if __name__ == '__main__':
    app = main()
    app.main_loop()