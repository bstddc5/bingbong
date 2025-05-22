import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Ford UDS Flash Tool'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel('Ford UDS Flash Tool GUI', self)
        label.move(50, 50)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
