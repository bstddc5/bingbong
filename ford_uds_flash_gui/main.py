import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt
from uds_core import UDSFlashSession


class UDSFlasherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ford UDS Flash Tool")
        self.setGeometry(300, 200, 900, 500)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.load_btn = QPushButton("📂 Load BIN File")
        self.flash_btn = QPushButton("🚀 Start Flash")

        # Connect button events
        self.load_btn.clicked.connect(self.load_bin)
        self.flash_btn.clicked.connect(self.flash_pcm)

        # Table for log output
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Dir", "Raw Data", "Decoded Info"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.flash_btn)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Flash session
        self.session = None
        self.bin_data = None

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

        self.status_label.setText("⚙️ Flashing in progress...")
        self.session = UDSFlashSession(logger=self.log_to_table)

        try:
            self.session.run(self.bin_data)
            self.status_label.setText("✅ Flash completed successfully.")
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")

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
