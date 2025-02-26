import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette


class PomodoroThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, x, x2, t):
        super().__init__()
        self.x = x
        self.x2 = x2
        self.t = t

    def run(self):
        for i in range(self.t):
            if i < self.t - 1:
                for y in range(self.x - 1, -1, -1):
                    for z in range(59, -1, -1):
                        self.update_signal.emit(f"Time for the break: {y}:{str(z).zfill(2)}")
                        time.sleep(1)
            else:
                for y in range(self.x - 1, -1, -1):
                    for z in range(59, -1, -1):
                        self.update_signal.emit(f"Time for ending studying: {y}:{str(z).zfill(2)}")
                        time.sleep(1)

            if i < self.t - 1:
                for y2 in range(self.x2 - 1, -1, -1):
                    for z2 in range(59, -1, -1):
                        self.update_signal.emit(f"time for the pomodoro: {y2}:{str(z2).zfill(2)}")
                        time.sleep(1)


# Ana pencere sınıfı
class PomodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(100, 100, 400, 300)

        # Karanlık tema uygula
        self.set_dark_theme()

        # Ana widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Başlık etiketi
        self.title_label = QLabel("Pomodoro Timer")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.layout.addWidget(self.title_label)

        # Giriş alanları
        self.pomodoro_label = QLabel("time for the pomodoro (as_minute):")
        self.pomodoro_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.layout.addWidget(self.pomodoro_label)

        self.pomodoro_input = QLineEdit()
        self.pomodoro_input.setStyleSheet("""
            QLineEdit {
                background-color: #2E3440;
                color: #FFFFFF;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.pomodoro_input)

        self.break_label = QLabel("time for the break (as_minute):")
        self.break_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.layout.addWidget(self.break_label)

        self.break_input = QLineEdit()
        self.break_input.setStyleSheet("""
            QLineEdit {
                background-color: #2E3440;
                color: #FFFFFF;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.break_input)

        self.count_label = QLabel("count of pomodoro (as_minute):")
        self.count_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.layout.addWidget(self.count_label)

        self.count_input = QLineEdit()
        self.count_input.setStyleSheet("""
            QLineEdit {
                background-color: #2E3440;
                color: #FFFFFF;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.count_input)

        
        self.start_button = QPushButton("start")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        self.start_button.clicked.connect(self.start_pomodoro)
        self.layout.addWidget(self.start_button)

        
        self.timer_label = QLabel("Timer: 00:00")
        self.timer_label.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

    
    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(46, 52, 64))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(46, 52, 64))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(94, 129, 172))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        QApplication.setPalette(dark_palette)

    
    def start_pomodoro(self):
        try:
            x = int(self.pomodoro_input.text())
            x2 = int(self.break_input.text())
            t = int(self.count_input.text())

            self.thread = PomodoroThread(x, x2, t)
            self.thread.update_signal.connect(self.update_timer)
            self.thread.start()

        except ValueError:
            QMessageBox.warning(self, "please enter new numbers")

    # Zamanlayıcıyı güncelleme fonksiyonu
    def update_timer(self, text):
        self.timer_label.setText(text)


# Uygulamayı çalıştır
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())
