import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")

        # Central Widget 
        central_widget = QWidget()
        self.setCentralWidget(central_widget
    
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # UI Elements
        label = QLabel("Hello, CVSS Tool!")
        layout.addWidget(label) 

        attack_vector = QComboBox()
        attack_vector.addItem("Network")
        attack_vector.addItem("Adjacent")
        attack_vector.addItem("Local")
        attack_vector.addItem("Physical")
        layout.addWidget(attack_vector) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
