import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QMessageBox,
    QFontComboBox, QColorDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QColor, QPalette, QPixmap


class CustomWeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "3a5fa7e31221eaea70a433aee0758f03"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Weather App – Customizable")
        self.setGeometry(400, 200, 350, 320)

        # --- Base neon-on-black theme ---
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#000000"))
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        neon = "#39FF14"

        # --- Load fallback “Technology” font if present ---
        fid = QFontDatabase.addApplicationFont("Technology.ttf")
        fallback = (
            QFontDatabase.applicationFontFamilies(fid)[0]
            if fid != -1 else "Arial"
        )

        # --- Layouts ---
        main = QVBoxLayout()
        inp_row = QHBoxLayout()
        display = QVBoxLayout()
        display.setAlignment(Qt.AlignCenter)
        ctrl_row = QHBoxLayout()

        # City input + Get Weather button
        self.city_in = QLineEdit()
        self.city_in.setPlaceholderText("Enter city name")
        self.city_in.setFont(QFont(fallback, 12))
        self.city_in.setStyleSheet(
            f"color:{neon}; background:#111; border:2px solid {neon};"
        )
        inp_row.addWidget(self.city_in)

        get_btn = QPushButton("Get Weather")
        get_btn.setFont(QFont(fallback, 12, QFont.Bold))
        get_btn.setStyleSheet(
            f"background:#111; color:{neon}; border:2px solid {neon};"
        )
        get_btn.clicked.connect(self.check_weather)
        inp_row.addWidget(get_btn)

        # Large temperature label
        self.temp_lbl = QLabel("--°C")
        self.temp_lbl.setFont(QFont(fallback, 48, QFont.Bold))
        self.temp_lbl.setStyleSheet(f"color:{neon};")
        self.temp_lbl.setAlignment(Qt.AlignCenter)

        # Weather icon
        self.icon_lbl = QLabel()
        self.icon_lbl.setAlignment(Qt.AlignCenter)

        # Description (supports emoji via rich text)
        self.desc_lbl = QLabel("--")
        self.desc_lbl.setFont(QFont(fallback, 18))
        self.desc_lbl.setStyleSheet(f"color:{neon};")
        self.desc_lbl.setAlignment(Qt.AlignCenter)
        self.desc_lbl.setTextFormat(Qt.RichText)

        display.addWidget(self.temp_lbl)
        display.addWidget(self.icon_lbl)
        display.addWidget(self.desc_lbl)

        # Font picker
        font_combo = QFontComboBox()
        font_combo.setCurrentFont(QFont(fallback))
        font_combo.currentFontChanged.connect(self.apply_font)
        ctrl_row.addWidget(font_combo)

        # Color picker
        color_btn = QPushButton("Text Color")
        color_btn.setFont(QFont(fallback, 10))
        color_btn.setStyleSheet(f"background:#111; color:{neon}; border:2px solid {neon};")
        color_btn.clicked.connect(self.choose_color)
        ctrl_row.addWidget(color_btn)

        main.addLayout(inp_row)
        main.addSpacing(10)
        main.addLayout(display)
        main.addSpacing(20)
        main.addLayout(ctrl_row)
        self.setLayout(main)

    def check_weather(self):
        city = self.city_in.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={self.api_key}&units=metric"
        )
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()

            # Temperature
            temp = round(data["main"]["temp"])
            self.temp_lbl.setText(f"{temp}°C")

            # Icon
            icon = data["weather"][0]["icon"]
            pic = QPixmap()
            pic.loadFromData(
                requests.get(f"https://openweathermap.org/img/wn/{icon}@2x.png").content
            )
            self.icon_lbl.setPixmap(pic)

            # Description with emoji (e.g., “☀️ Sunny”)
            desc = data["weather"][0]["description"].capitalize()
            emoji_map = {
                "clear sky": "☀️",
                "few clouds": "⛅",
                "rain": "🌧️",
                "snow": "❄️",
                # add more mappings as desired
            }
            emj = emoji_map.get(desc.lower(), "")
            # Use rich text so emojis render correctly alongside custom font
            self.desc_lbl.setText(f"<span>{emj} {desc}</span>")

        except Exception:
            QMessageBox.warning(self, "API Error", "Could not retrieve weather data.")

    def apply_font(self, font: QFont):
        """Apply selected font to all labels."""
        for lbl in (self.temp_lbl, self.desc_lbl, self.city_in):
            lbl.setFont(font)

    def choose_color(self):
        """Open QColorDialog and apply chosen color to text."""
        col = QColorDialog.getColor(parent=self, title="Select Text Color")
        if col.isValid():
            style = f"color:{col.name()};"
            # update stylesheet for labels and input
            self.temp_lbl.setStyleSheet(style)
            self.desc_lbl.setStyleSheet(style)
            self.city_in.setStyleSheet(
                f"color:{col.name()}; background:#111; border:2px solid {col.name()};"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = CustomWeatherApp()
    win.show()
    sys.exit(app.exec_())

# Note: Replace YOUR_OPENWEATHER_API_KEY with your actual API key from OpenWeatherMap.  
# Ensure you have the Technology.ttf font file in the same directory as this script.
# You can download the font from various online sources or use any other font you prefer.