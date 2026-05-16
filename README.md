# ⚡ LiteFPS

An ultra-lightweight, zero-lag performance overlay for Windows. Built with Python and PyQt5, designed to stay out of your way while giving you the most critical system stats in real-time.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-green.svg)
![Performance](https://img.shields.io/badge/Performance-Ultra--Lite-orange.svg)

## 🚀 Key Features

-   **⚡ Zero-Lag Dragging**: Optimized window handling allows you to move the overlay anywhere on your screen with zero stutter.
-   **🧵 Multithreaded Monitoring**: Hardware polling (GPU) runs in a background thread, ensuring the UI remains perfectly responsive even when the system is under heavy load.
-   **📊 Intelligent Performance Model**: Provides a numerical "Estimated FPS" value based on real-time CPU and GPU utilization.
-   **🖱️ Full-Area Drag**: Click anywhere on the widget to reposition it instantly.
-   **💾 Auto-Save**: Automatically remembers its last position on your desktop.
-   **🎨 Minimalist Aesthetic**:
    *   Pure numeric display with dynamic coloring (Green 🟢 / Yellow 🟡 / Red 🔴).
    *   Ultra-low resource footprint (CPU/RAM).
    *   Borderless, distraction-free design.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lubadpap-cmyk/Litefps.git
    cd Litefps
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python fps_monitor.py
    ```

## 🎮 Controls

-   **Move**: Left-click and drag **anywhere** on the overlay.
-   **Exit**: Right-click the system tray icon (next to the clock) and select **"Exit"**.

## 📦 Requirements

-   Windows 10/11
-   Python 3.7+
-   PyQt5
-   psutil

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
