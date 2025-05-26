import sys, os, time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel,
    QHeaderView, QComboBox, QTabWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from uds_core import UDSFlashSession
from j2534_can import J2534IsoTPChannel

CONFIG_FILE = "device_config.json"
DEFAULT_PATHS = {
    "Mongoose-Plus Ford2": r"C:\Program Files (x86)\Drew Technologies, Inc\J2534\Mongoose-Plus Ford2\mongooseplus_ford2_0404_32.dll"
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

        self.load_btn = QPushButton("📂 Load BIN File")
        self.flash_btn = QPushButton("🚀 Start Flash")
        self.test_btn = QPushButton("🧪 Test Connection")

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Dir", "Raw Data", "Decoded Info"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        self.info_table = QTableWidget(4, 2)
        self.info_table.setHorizontalHeaderLabels(["Label", "Value"])
        self.info_table.verticalHeader().setVisible(False)
        self.info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        for i, label in enumerate(["VIN", "Calibration ID", "CVN", "ECU Name"]):
            self.info_table.setItem(i, 0, QTableWidgetItem(label))

        tabs = QTabWidget()
        tabs.addTab(self.table, "UDS Log")
        tabs.addTab(self.info_table, "ECU Info")

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)

        hl = QHBoxLayout()
        hl.addWidget(QLabel("Select Device:"))
        hl.addWidget(self.device_select)
        layout.addLayout(hl)

        layout.addWidget(self.load_btn)
        layout.addWidget(self.flash_btn)
        layout.addWidget(self.test_btn)
        layout.addWidget(tabs)

        self.setLayout(layout)

        self.session = None
        self.bin_data = None

        self.load_btn.clicked.connect(self.load_bin)
        self.flash_btn.clicked.connect(self.flash_pcm)
        self.test_btn.clicked.connect(self.test_connection)

        self.load_devices()

    def load_devices(self):
        self.device_select.clear()
        for name, path in DEFAULT_PATHS.items():
            if os.path.exists(path):
                self.device_map[name] = path
                self.device_select.addItem(name)

    def test_connection(self):
        name = self.device_select.currentText()
        dll = self.device_map.get(name)
        if not dll:
            self.status_label.setText("❌ No valid DLL selected")
            return

        self.session = UDSFlashSession(dll_path=dll, debug_func=self.log_msg)
        try:
            self.session.connect()
            self.status_label.setText("✅ Connection OK.")
            self.query_ecu_info()
        except Exception as e:
            self.status_label.setText(f"❌ Test failed: {e}")
        finally:
            self.session.close()

    def query_ecu_info(self):
        mapping = {
            "VIN": 0xF190,
            "Calibration ID": 0xF187,
            "CVN": 0xF188,
            "ECU Name": 0xF194
        }
        for row, (label, did) in enumerate(mapping.items()):
            try:
                value = self.session.read_data_by_identifier(did)
                self.info_table.setItem(row, 1, QTableWidgetItem(value))
            except Exception as e:
                self.info_table.setItem(row, 1, QTableWidgetItem(f"ERR: {e}"))

    def load_bin(self):
        pass

    def flash_pcm(self):
        pass

    def log_msg(self, msg, direction="TX", decoded=None):
        row = self.table.rowCount()
        self.table.insertRow(row)
        timestamp = time.strftime("%H:%M:%S")

        color = QColor("#D0F0FF") if direction == "TX" else QColor("#FFDADA")
        for i, val in enumerate([timestamp, direction, msg, decoded or ""]):
            item = QTableWidgetItem(val)
            item.setBackground(color)
            self.table.setItem(row, i, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UDSFlasherGUI()
    gui.show()
    sys.exit(app.exec_())
