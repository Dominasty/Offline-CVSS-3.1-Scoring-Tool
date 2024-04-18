from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline CVSS 3.1 Scoring Tool")

        # Optional for clarity:
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
