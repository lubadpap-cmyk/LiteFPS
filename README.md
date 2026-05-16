# 🚀 Modern FPS & System Monitor

A sleek, lightweight, and highly customizable FPS and system resource monitor built with Python and PyQt5. Designed for gamers and power users who want a beautiful overlay without the bloat.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

-   **📊 Dynamic Smooth Graph**: Real-time FPS history visualized with a beautiful anti-aliased area chart and gradient fills.
-   **🖥️ System Stats**: Live monitoring of CPU and RAM utilization.
-   **📈 Performance Metrics**: Track your **Average** and **Maximum** FPS at a glance.
-   **👻 Ghost Mode**: Toggle "click-through" functionality so the overlay never interferes with your gaming sessions.
-   **💾 Persistence**: Automatically saves your preferred window position and transparency level between restarts.
-   **🎨 Premium Aesthetics**:
    *   Frameless, semi-transparent window with rounded corners.
    *   Adaptive coloring (Green 🟢 / Yellow 🟡 / Red 🔴) based on FPS performance.
    *   Modern typography using Segoe UI Black.
-   **⚙️ Quick Controls**:
    *   **Drag**: Left-click and move to reposition.
    *   **Transparency**: Scroll your mouse wheel to adjust opacity (10% - 95%).
    *   **Tray Menu**: Full control via the system tray icon, including "Reset Position" and "Exit".

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

## 🎮 Usage

-   **Move it**: Click and drag anywhere on the widget.
-   **Adjust Opacity**: Hover over the widget and use your **Mouse Wheel**.
-   **Ghost Mode**: Right-click the system tray icon and select **"Вкл/Выкл режим призрака"**. In this mode, the window becomes semi-transparent and ignores all mouse inputs, allowing you to click through it into your game.
-   **Reset**: If the window goes off-screen, use **"Сбросить позицию"** from the tray menu.

## 📦 Requirements

-   Python 3.7+
-   PyQt5
-   psutil

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
