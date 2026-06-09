import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget,
    QPushButton, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QElapsedTimer
from PyQt5.QtGui import QPalette, QColor, QFontDatabase, QFont


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.is_24h = True
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Clock + Stopwatch')
        self.setGeometry(600, 300, 400, 300)

        # Black background
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#000000"))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        neon = "#39FF14"
        # Load custom “Technology” font
        font_id = QFontDatabase.addApplicationFont("Technology.ttf")
        fam = QFontDatabase.applicationFontFamilies(font_id)
        tech_font = fam[0] if fam else "Arial"

        # --- Clock Labels ---
        time_lbl = QLabel(self)
        time_lbl.setFont(QFont(tech_font, 48, QFont.Bold))
        time_lbl.setStyleSheet(f"color:{neon}; text-shadow:0 0 20px {neon};")
        self.clock_label = time_lbl

        date_lbl = QLabel(self)
        date_lbl.setFont(QFont(tech_font, 22))
        date_lbl.setStyleSheet(f"color:{neon}; text-shadow:0 0 10px {neon};")
        self.date_label = date_lbl

        # --- Stopwatch Labels & Buttons ---
        self.stopwatch_display = QLabel("00:00:00.000", self)
        self.stopwatch_display.setFont(QFont(tech_font, 24))
        self.stopwatch_display.setStyleSheet(f"color:{neon}; text-shadow:0 0 10px {neon};")
        self.stopwatch_display.setAlignment(Qt.AlignCenter)

        # Stopwatch control buttons
        sw_start = QPushButton("Start", self)
        sw_stop  = QPushButton("Stop", self)
        sw_reset = QPushButton("Reset", self)
        for btn in (sw_start, sw_stop, sw_reset):
            btn.setStyleSheet(
                f"background-color:#111; color:{neon}; border:2px solid {neon};"
                "font-size:14px; font-weight:bold;"
            )
        sw_start.clicked.connect(self.sw_start)
        sw_stop.clicked.connect(self.sw_stop)
        sw_reset.clicked.connect(self.sw_reset)

        sw_btn_layout = QHBoxLayout()
        sw_btn_layout.addWidget(sw_start)
        sw_btn_layout.addWidget(sw_stop)
        sw_btn_layout.addWidget(sw_reset)

        # --- Time Format Button ---
        self.format_btn = QPushButton("Switch to 12H", self)
        self.format_btn.clicked.connect(self.toggle_time_format)
        self.format_btn.setStyleSheet(
            f"background-color:#111; color:{neon}; border:2px solid {neon};"
            "font-size:16px; font-weight:bold;"
        )

        # Layout assembly
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.clock_label)
        top_layout.addWidget(self.date_label)

        sw_layout = QVBoxLayout()
        sw_layout.addWidget(self.stopwatch_display)
        sw_layout.addLayout(sw_btn_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.format_btn)
        main_layout.addSpacing(10)
        main_layout.addLayout(sw_layout)
        self.setLayout(main_layout)

        # Timers
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        # Stopwatch backend
        self.elapsed = QElapsedTimer()
        self.sw_timer = QTimer(self)
        self.sw_timer.setInterval(50)  # refresh every 50 ms
        self.sw_timer.timeout.connect(self.update_stopwatch)
        self.running = False

    def update_clock(self):
        t = QTime.currentTime()
        d = QDate.currentDate()
        fmt = 'HH:mm:ss' if self.is_24h else 'hh:mm:ss A'
        self.clock_label.setText(t.toString(fmt))
        self.date_label.setText(d.toString('dddd, MMMM d, yyyy'))

    def toggle_time_format(self):
        self.is_24h = not self.is_24h
        self.format_btn.setText("Switch to 12H" if self.is_24h else "Switch to 24H")
        self.update_clock()

    # --- Stopwatch slots ---
    def sw_start(self):
        if not self.running:
            if not self.elapsed.isValid():
                # First start
                self.elapsed.start()
            else:
                # Resuming: account for paused duration by restarting elapsed from now minus already run
                paused_ms = int(self.elapsed.elapsed_display_ms)
                self.elapsed = QElapsedTimer()
                self.elapsed.start()
                self.elapsed.elapsed_display_ms = paused_ms
            self.running = True
            self.sw_timer.start()

    def sw_stop(self):
        if self.running:
            # Save elapsed
            self.elapsed.elapsed_display_ms = self.elapsed.elapsed()
            self.running = False
            self.sw_timer.stop()

    def sw_reset(self):
        self.running = False
        self.sw_timer.stop()
        self.elapsed = QElapsedTimer()
        self.stopwatch_display.setText("00:00:00.000")

    def update_stopwatch(self):
        ms_total = (self.elapsed.elapsed_display_ms
                    if hasattr(self.elapsed, 'elapsed_display_ms')
                    else 0) + self.elapsed.elapsed()
        hrs = ms_total // 3_600_000
        mins = (ms_total % 3_600_000) // 60_000
        secs = (ms_total % 60_000) // 1_000
        ms   = ms_total % 1_000
        self.stopwatch_display.setText(f"{hrs:02}:{mins:02}:{secs:02}.{ms:03}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
