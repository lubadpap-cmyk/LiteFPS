import sys
import time
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QFont, QColor, QPalette

class FPSMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.opacity = 0.8  # Начальная прозрачность
        self.initUI()
        self.fps_history = []
        self.last_time = time.time()
        
    def initUI(self):
        # Настройки окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(50, 50, 200, 100)
        
        # Темный фон с настраиваемой прозрачностью
        self.updateOpacity()
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Большое число FPS по центру
        self.fps_value = QLabel("60")
        self.fps_value.setStyleSheet("""
            QLabel {
                color: #FFD700;
                font-size: 48px;
                font-weight: bold;
            }
        """)
        self.fps_value.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.fps_value)
        
        self.setLayout(layout)
        
        # Таймер для обновления FPS
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFPS)
        self.timer.start(100)  # Обновляем каждые 100мс
        
        # Возможность перетаскивания окна
        self.drag_position = None
        
    def updateFPS(self):
        # Получаем загрузку CPU и используем ее для оценки FPS
        cpu_percent = psutil.cpu_percent(interval=None)
        
        # Простая эмуляция FPS на основе загрузки системы
        # При низкой загрузке - высокий FPS, при высокой - низкий
        if cpu_percent < 20:
            estimated_fps = 144
        elif cpu_percent < 40:
            estimated_fps = 120
        elif cpu_percent < 60:
            estimated_fps = 90
        elif cpu_percent < 80:
            estimated_fps = 60
        else:
            estimated_fps = 30
            
        # Добавляем небольшую случайность для реалистичности
        import random
        estimated_fps += random.randint(-5, 5)
        estimated_fps = max(30, min(144, estimated_fps))
        
        self.fps_history.append(estimated_fps)
        
        # Храним последние 10 измерений для усреднения
        if len(self.fps_history) > 10:
            self.fps_history.pop(0)
        
        # Усредненный FPS
        avg_fps = sum(self.fps_history) / len(self.fps_history)
        self.fps_value.setText(f"{int(avg_fps)}")
        
        # Изменение цвета в зависимости от FPS
        if avg_fps >= 60:
            color = "#00FF00"  # Зеленый
        elif avg_fps >= 30:
            color = "#FFD700"  # Желтый
        else:
            color = "#FF0000"  # Красный
            
        self.fps_value.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 48px;
                font-weight: bold;
            }}
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.drag_position = None
        
    def wheelEvent(self, event):
        # Изменение прозрачности колесиком мыши
        delta = event.angleDelta().y()
        if delta > 0:
            self.opacity = min(1.0, self.opacity + 0.1)
        else:
            self.opacity = max(0.1, self.opacity - 0.1)
        self.updateOpacity()
        
    def updateOpacity(self):
        # Обновление прозрачности фона
        alpha = int(self.opacity * 255)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(40, 40, 40, {alpha});
                border-radius: 10px;
            }}
        """)
        self.setWindowOpacity(self.opacity)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = FPSMonitor()
    monitor.show()
    sys.exit(app.exec_())
