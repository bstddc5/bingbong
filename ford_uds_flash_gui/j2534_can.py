import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
from uds_core import UDSFlashSession


class UDSFlasherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ford UDS Flash Tool")
        self.setGeometry(200, 200, 850, 500)

        self.layout = QVBoxLayout()
        self.status = QLabel("Status: Idle")
        self.status.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Dir", "Raw Data", "Decoded Info"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.load_btn = QPushButton("Load BIN File")
        self.flash_btn = QPushButton("Start Flash")

        self.layout.addWidget(self.status)
        self.layout.addWidget(self.load_btn)
        self.layout.addWidget(self.flash_btn)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.session = None
        self.bin_data = None

        self.load_btn.clicked.connect(self.load_bin)
        self.flash_btn.clicked.connect(self.flash_pcm)

    def log(self, direction, data, info=""):
        row = self.table.rowCount()
        self.table.insertRow(row)

        time_str = time.strftime("%H:%M:%S")
        self.table.setItem(row, 0, QTableWidgetItem(time_str))
        self.table.setItem(row, 1, QTableWidgetItem(direction))
        self.table.setItem(row, 2, QTableWidgetItem(" ".join(f"{b:02X}" for b in data)))
        self.table.setItem(row, 3, QTableWidgetItem(info))
        self.table.scrollToBottom()

    def load_bin(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open BIN file", "", "BIN Files (*.bin)")
        if fname:
            with open(fname, "rb") as f:
                self.bin_data = f.read()
            self.status.setText(f"Loaded: {fname} ({len(self.bin_data)} bytes)")

    def flash_pcm(self):
        if not self.bin_data:
            self.status.setText("Please load a BIN file first.")
            return

        self.status.setText("Flashing in progress...")
        self.session = UDSFlashSession(logger=self.log)

        try:
            self.session.run(self.bin_data)
            self.status.setText("Flash completed successfully.")
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UDSFlasherGUI()
    gui.show()
    sys.exit(app.exec_())
