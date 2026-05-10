# FPS Monitor

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

A lightweight, unobtrusive FPS overlay that provides real-time performance monitoring without disrupting your workflow. Designed for gamers, developers, and performance enthusiasts who need instant visibility into their system's frame rate while maintaining a clean desktop environment.

## Features

- **Always on top** - stays visible when switching between applications
- **Dynamic color indication**:
  - **Green**: 60+ FPS (excellent performance)
  - **Yellow**: 30-60 FPS (moderate performance)
  - **Red**: below 30 FPS (poor performance)
- **Mouse controls**:
  - Left click + drag to move window
  - Mouse wheel to adjust transparency (10% - 100%)
- **Minimalist design** - only FPS digits without unnecessary elements
- **Adjustable transparency** - adapts to any desktop environment

## Screenshot

```
┌─────────────────┐
│                 │
│        60       │  ← Color changes based on FPS
│                 │
└─────────────────┘
```

## Quick Start

### Requirements
- Windows 10/11
- Python 3.7 or higher

### Installation and Running

1. **Clone the repository**:
```bash
git clone https://github.com/lubadpap-cmyk/LiteFPS.git
cd LiteFPS
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python fps_monitor.py
```

## Dependencies

```
PyQt5==5.15.10
psutil==5.9.5
```

## Controls

| Action | Result |
|----------|-----------|
| **Left mouse button + drag** | Move window |
| **Mouse wheel up** | Increase transparency |
| **Mouse wheel down** | Decrease transparency |
| **Alt + F4** | Close application |

## How it works

The application uses:
- **psutil** for CPU load monitoring
- **PyQt5** for transparent GUI creation
- FPS emulation algorithm based on system load

## Build to .exe (optional)

To create a portable executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed fps_monitor.py
```

## TODO

- [ ] Add position memory feature
- [ ] Hotkey support
- [ ] macOS and Linux support
- [ ] Customizable colors and sizes

## Contributing

Pull requests are welcome! Please open an issue to discuss changes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Stars

If this project was helpful to you, give it a star on GitHub!

---

Made for gamers and performance enthusiasts
