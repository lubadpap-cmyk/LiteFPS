import sys
import time
import psutil
import subprocess
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QTimer, QPoint, QSettings, QThread, pyqtSignal

# Фоновый поток для сбора данных GPU, чтобы не фризить окно
class GPUThread(QThread):
    gpu_signal = pyqtSignal(int)
    
    def run(self):
        while True:
            try:
                # Медленный запрос к PowerShell теперь в отдельном потоке
                cmd = r'Get-Counter "\GPU Engine(*)\Utilization Percentage" | Select-Object -ExpandProperty CounterSamples | Select-Object -Property CookedValue'
                res = subprocess.check_output(['powershell', '-Command', cmd], creationflags=subprocess.CREATE_NO_WINDOW).decode()
                values = [float(v.strip().replace(',', '.')) for v in res.split('\n') if v.strip() and v.strip()[0].isdigit()]
                load = int(max(values)) if values else 0
                self.gpu_signal.emit(load)
            except:
                self.gpu_signal.emit(0)
            time.sleep(2) # Опрос раз в 2 секунды

class LiteFPS(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("lubadpap-cmyk", "LiteFPS")
        self.gpu_load = 0
        self._last_tier = -1
        self.drag_pos = QPoint()
        
        # Настройка окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        # CPU/RAM Row
        self.res_label = QLabel("CPU: 0%  |  RAM: 0%")
        self.res_label.setStyleSheet("color: #AAAAAA; font-family: 'Segoe UI Bold'; font-size: 10px;")
        self.res_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.res_label)

        # MAIN FPS (Estimated)
        self.fps_label = QLabel("---")
        self.fps_label.setStyleSheet("color: #00FF88; font-family: 'Segoe UI Black'; font-size: 54px; font-weight: 900; margin: -5px 0;")
        self.fps_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.fps_label)

        # GPU Label
        self.gpu_label = QLabel("GPU LOAD: 0%")
        self.gpu_label.setStyleSheet("color: #888888; font-family: 'Segoe UI Bold'; font-size: 9px; letter-spacing: 1px;")
        self.gpu_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.gpu_label)
        
        self.setLayout(layout)
        
        # UI Таймер (только для отрисовки цифр)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(200) 

        # Запуск фонового потока для GPU
        self.gpu_worker = GPUThread()
        self.gpu_worker.gpu_signal.connect(self.on_gpu_updated)
        self.gpu_worker.start()
        
        self.initTray()
        
        pos = self.settings.value("pos")
        if pos: self.move(pos)

    def on_gpu_updated(self, value):
        self.gpu_load = value

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("LiteFPS")
        menu = QMenu()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def update_ui(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        # Расчет FPS
        headroom = 100 - (self.gpu_load * 0.7 + cpu * 0.3)
        fps = int(headroom * 1.44)
        fps = max(1, fps + random.randint(-1, 1))

        self.res_label.setText(f"CPU: {int(cpu)}%  |  RAM: {int(ram)}%")
        self.gpu_label.setText(f"GPU LOAD: {self.gpu_load}%")
        self.fps_label.setText(str(fps))

        tier = 3 if fps >= 100 else (2 if fps >= 50 else 1)
        if tier != self._last_tier:
            color = "#00FF88" if tier == 3 else ("#FFD700" if tier == 2 else "#FF4B4B")
            self.fps_label.setStyleSheet(f"color: {color}; font-family: 'Segoe UI Black'; font-size: 54px; font-weight: 900; margin: -5px 0;")
            self._last_tier = tier

    # --- ПЛАВНОЕ ПЕРЕМЕЩЕНИЕ БЕЗ ЛАГОВ ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Двигаем окно мгновенно
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Сохраняем позицию только после того, как отпустили мышь (чтобы не тормозить при движении)
        self.settings.setValue("pos", self.pos())
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = LiteFPS()
    monitor.show()
    sys.exit(app.exec_())
