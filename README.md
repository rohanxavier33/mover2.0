# Mouse Mover - Keep Computer Active

![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-green.svg)

A simple Windows application that prevents your computer from going to sleep by simulating user activity through periodic keyboard and mouse movements.

## Features

- Simulates keyboard activity (Volume mute/unmute, Caps Lock toggle)
- Random mouse cursor movement
- Simple GUI with start/stop controls
- Runs in background without interrupting work
- Prevents screen lock and sleep mode

## Installation

### Direct Download (For End Users)
1. Download the latest `MouseMover.exe` from [Releases](#)
2. Right-click the executable -> Properties -> Check "Unblock"
3. Double-click to run

### Requirements
- Windows 8.1 or newer
- .NET Framework 4.6.1+
- Visual C++ Redistributable

## Usage

1. Launch `MouseMover.exe`
2. Click "Start Script" to begin activity simulation
3. Click "Stop Script" to end the simulation
4. Close the window to exit the application

**Note:** The script will:
- Toggle Caps Lock every 10 seconds
- Move mouse cursor randomly
- Simulate volume key presses

## Building from Source (For Developers)

### Prerequisites
- Python 3.12+
- pip package manager

### Setup
```powershell
# Clone repository
git clone https://github.com/yourusername/mouse-mover.git
cd mouse-mover

# Install dependencies
pip install toga pyautogui pyinstaller
