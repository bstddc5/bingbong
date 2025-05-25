import sys
import os

print(f"[DEBUG] Running Python from: {sys.executable}")

import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QComboBox
)
from PyQt5.QtCore import Qt
from uds_core import UDSFlashSession

CONFIG_FILE = "device_config.json"

DEFAULT_PATHS = {
    "Tactrix OpenPort 2.0": r"C:\Program Files (x86)\OpenECU\J2534\op20pt32.dll",
    "Mongoose-Plus Ford2": r"C:\Program Files (x86)\Drew Technologies, Inc\J2534\Mongoose-Plus Ford2\0500\mongooseplus_ford2_0500_32.dll"
}

class UDSFlasherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ford UDS Flash Tool")
        self.setGeometry(300, 200, 900, 600)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.device_select = QComboBox()
        self.device_map = {}
        self.load_devices()

        self.load_btn = QPushButton("📂 Load BIN File")
        self.flash_btn = QPushButton("🚀 Start Flash")
        self.test_btn = QPushButton("🔌 Test Connection")

        self.load_btn.clicked.connect(self.load_bin)
        self.flash_btn.clicked.connect(self.flash_pcm)
        self.test_btn.clicked.connect(self.test_connection)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Dir", "Raw Data", "Decoded Info"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Select Device:"))
        layout.addWidget(self.device_select)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.flash_btn)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.session = None
        self.bin_data = None

    def load_devices(self):
        self.device_map = {}
        self.device_select.clear()
        for name, path in DEFAULT_PATHS.items():
            if os.path.exists(path):
                self.device_map[name] = path
                self.device_select.addItem(name)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    import json
                    config = json.load(f)
                    if config.get("last_device") in self.device_map:
                        self.device_select.setCurrentText(config["last_device"])
            except:
                pass

    def save_selection(self):
        selected = self.device_select.currentText()
        with open(CONFIG_FILE, "w") as f:
            import json
            json.dump({"last_device": selected}, f)

    def load_bin(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select BIN File", "", "BIN Files (*.bin)")
        if file_path:
            with open(file_path, "rb") as f:
                self.bin_data = f.read()
            self.status_label.setText(f"Loaded: {file_path} ({len(self.bin_data)} bytes)")

    def flash_pcm(self):
        if not self.bin_data:
            self.status_label.setText("❌ Please load a BIN file before flashing.")
            return
        dll_path = self.device_map[self.device_select.currentText()]
        self.status_label.setText(f"⚙️ Flashing using {self.device_select.currentText()}...")
        self.save_selection()
        self.session = UDSFlashSession(logger=self.log_to_table, dll_path=dll_path)
        try:
            self.session.run(self.bin_data)
            self.status_label.setText("✅ Flash completed successfully.")
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")

    def test_connection(self):
        dll_path = self.device_map[self.device_select.currentText()]
        self.status_label.setText(f"🔌 Testing {self.device_select.currentText()}...")
        try:
            self.session = UDSFlashSession(logger=self.log_to_table, dll_path=dll_path)
            self.session.test_session()
            self.status_label.setText("✅ Connection OK.")
        except Exception as e:
            self.status_label.setText(f"❌ Test failed: {str(e)}")

    def log_to_table(self, direction, data, info=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(time.strftime("%H:%M:%S")))
        self.table.setItem(row, 1, QTableWidgetItem(direction))
        self.table.setItem(row, 2, QTableWidgetItem(" ".join(f"{b:02X}" for b in data)))
        self.table.setItem(row, 3, QTableWidgetItem(info))
        self.table.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UDSFlasherGUI()
    gui.show()
    sys.exit(app.exec_())
