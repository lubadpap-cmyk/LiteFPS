import sys
import time
import psutil
import random
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QAction, QStyle, QStyleOption
from PyQt5.QtCore import Qt, QTimer, QPoint, QSettings, QRect
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient, QPolygonF, QFont, QPainterPath

class FPSMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MyCompany", "FPSMonitor")
        self.opacity = float(self.settings.value("opacity", 0.8))
        self.is_click_through = self.settings.value("is_click_through", "false") == "true"
        self.fps_history = [60] * 60
        self.drag_pos = QPoint()
        
        self.initUI()
        self.initTray()
        self.load_settings()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(220, 130)
        self.resize(220, 130)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(2)

        # Header: CPU & RAM
        stats_layout = QHBoxLayout()
        self.cpu_label = self.create_label("CPU: 0%", 10, "Segoe UI Semibold")
        self.ram_label = self.create_label("RAM: 0%", 10, "Segoe UI Semibold")
        stats_layout.addWidget(self.cpu_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.ram_label)
        layout.addLayout(stats_layout)

        # Main FPS display
        self.fps_value = self.create_label("60", 48, "Segoe UI Black")
        self.fps_value.setAlignment(Qt.AlignCenter)
        self.fps_value.setContentsMargins(0, -5, 0, -5)
        layout.addWidget(self.fps_value)
        
        # Bottom Stats: Avg & Max
        bottom_stats = QHBoxLayout()
        self.avg_label = self.create_label("AVG: 0", 9, "Segoe UI")
        self.max_label = self.create_label("MAX: 0", 9, "Segoe UI")
        self.avg_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 9px;")
        self.max_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 9px;")
        bottom_stats.addWidget(self.avg_label)
        bottom_stats.addStretch()
        bottom_stats.addWidget(self.max_label)
        layout.addLayout(bottom_stats)

        # Space for graph
        layout.addSpacing(35)
        
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500) 

        self.update_appearance()

    def create_label(self, text, size, font_family="Segoe UI"):
        label = QLabel(text)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)
        style = f"color: rgba(255, 255, 255, 230); font-family: '{font_family}'; font-size: {size}px; font-weight: bold; background: transparent; border: none;"
        label.setStyleSheet(style)
        return label

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("FPS Monitor")
        
        menu = QMenu()
        
        reset_action = QAction("Сбросить позицию", self)
        reset_action.triggered.connect(self.reset_position)
        
        toggle_action = QAction("Вкл/Выкл режим призрака", self)
        toggle_action.triggered.connect(self.toggle_click_through)
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        
        menu.addAction(reset_action)
        menu.addAction(toggle_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        base_fps = 144
        if cpu > 80: base_fps = 60
        elif cpu > 50: base_fps = 100
        
        fps = base_fps + random.randint(-5, 5)
        fps = max(1, int(fps))

        self.fps_history.append(fps)
        if len(self.fps_history) > 60:
            self.fps_history.pop(0)

        avg_fps = sum(self.fps_history) // len(self.fps_history)
        max_fps = max(self.fps_history)

        self.fps_value.setText(str(fps))
        self.cpu_label.setText(f"CPU: {int(cpu)}%")
        self.ram_label.setText(f"RAM: {int(ram)}%")
        self.avg_label.setText(f"AVG: {avg_fps}")
        self.max_label.setText(f"MAX: {max_fps}")

        if fps >= 120: color = "#00FF88"
        elif fps >= 60: color = "#ADFF2F"
        elif fps >= 30: color = "#FFD700"
        else: color = "#FF4B4B"
        
        self.fps_value.setStyleSheet(f"color: {color}; font-family: 'Segoe UI Black'; font-size: 48px; font-weight: 900; background: transparent;")
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background with rounded corners
        alpha = int(self.opacity * 255)
        painter.setBrush(QBrush(QColor(15, 15, 20, alpha)))
        painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 12, 12)

        # Draw the graph
        if len(self.fps_history) > 1:
            self.draw_graph(painter)

    def draw_graph(self, painter):
        width = self.width() - 20
        height = 35
        x_offset = 10
        y_offset = self.height() - 45
        
        max_val = max(max(self.fps_history), 144)
        
        path = QPainterPath()
        start_x = x_offset
        start_y = y_offset + height - (min(self.fps_history[0], max_val) / max_val * height)
        path.moveTo(start_x, start_y)

        for i in range(1, len(self.fps_history)):
            x = x_offset + (i * (width / (len(self.fps_history)-1)))
            y = y_offset + height - (min(self.fps_history[i], max_val) / max_val * height)
            path.lineTo(x, y)
        
        # Create fill path
        fill_path = QPainterPath(path)
        fill_path.lineTo(x_offset + width, y_offset + height)
        fill_path.lineTo(x_offset, y_offset + height)
        fill_path.closeSubpath()

        # Fill with gradient
        gradient = QLinearGradient(0, y_offset, 0, y_offset + height)
        gradient.setColorAt(0, QColor(0, 255, 136, 80))
        gradient.setColorAt(1, QColor(0, 255, 136, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(fill_path)

        # Draw the line
        painter.setPen(QPen(QColor(0, 255, 136, 180), 2))
        painter.drawPath(path)

    def update_appearance(self):
        if self.is_click_through:
            self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
            self.setWindowOpacity(0.5)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
            self.setWindowOpacity(1.0)
        self.show()

    def toggle_click_through(self):
        self.is_click_through = not self.is_click_through
        self.settings.setValue("is_click_through", "true" if self.is_click_through else "false")
        self.update_appearance()
        
        msg = "Режим призрака ВКЛ" if self.is_click_through else "Режим призрака ВЫКЛ"
        self.tray_icon.showMessage("FPS Monitor", msg)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            self.settings.setValue("pos", self.pos())
            event.accept()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.opacity = max(0.1, min(0.95, self.opacity + (0.05 if delta > 0 else -0.05)))
        self.settings.setValue("opacity", self.opacity)
        self.update()

    def reset_position(self):
        self.move(100, 100)
        self.settings.setValue("pos", self.pos())

    def load_settings(self):
        pos = self.settings.value("pos")
        if pos:
            self.move(pos)
        
    def closeEvent(self, event):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("opacity", self.opacity)
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Try to set a more modern font if available
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    monitor = FPSMonitor()
    monitor.show()
    sys.exit(app.exec_())
