import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import csv
import datetime
import os
import getpass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline CVSS 3.1 Scoring Tool")

        # Central Widget 
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout (Vertical)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Define dropdown options (use dictionaries for readability)
        attack_vector_options = {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"}
        privileges_options = {"N": "None", "L": "Low", "H": "High"}
        complexity_options = {"L": "Low", "H": "High"}
        user_interaction_options = {"N": "None", "R": "Required"}
        scope_options = {"U": "Unchanged", "C": "Changed"}
        impact_options = {"H": "High", "L": "Low", "N": "None"}
        maturity_options = {"U": "Unproven", "P": "Proof-of-Concept", "F": "Functional",  "H": "High", "X": "Not Defined"}
        remediation_options = {"O": "Official Fix", "TF": "Temporary Fix", "W": "Workaround", "U": "Unavailable", "X": "Not Defined"}
        confidence_options = {"C": "Confirmed", "R": "Reasonable", "U": "Unknown", "X": "Not Defined"}

        
        # Base Score Metrics Section
        base_score_groupbox = QGroupBox("Base Score Metrics")
        base_score_layout = QVBoxLayout()  # Change to QVBoxLayout
        base_score_groupbox.setLayout(base_score_layout)
        main_layout.addWidget(base_score_groupbox)  # Add to main layout
        
        # Create subsections and dropdowns (Exploitability)
        exploitability_specs = [
            ("Attack Vector", attack_vector_options),
            ("Attack Complexity", complexity_options),
            ("Privileges Required", privileges_options),
            ("User Interaction", user_interaction_options),
            ("Scope", scope_options) 
        ] 
        exploitability_widget = self.create_section(base_score_layout, "Exploitability Metrics", exploitability_specs)
        base_score_layout.addWidget(exploitability_widget)

        # Create subsections and dropdowns (Impact)
        impact_specs = [
            ("Confidentiality", impact_options),
            ("Integrity", impact_options),
            ("Availability", impact_options)
        ]
        impact_widget = self.create_section(base_score_layout, "Impact Metrics", impact_specs)
        base_score_layout.addWidget(impact_widget) 

        self.exploitability_widget = exploitability_widget
        self.impact_widget = impact_widget        

        # Temporal Score Metrics
        temporal_specs = [
            ("Exploit Code Maturity", maturity_options), 
            ("Remediation Level", remediation_options),
            ("Report Confidence", confidence_options)
        ] 
        self.create_section(main_layout, "Temporal Score Metrics", temporal_specs)

        # Environmental Score Metrics (Copy of Base Score Metrics)
        environmental_specs = [
            ("Attack Vector", attack_vector_options),  
            ("Attack Complexity", complexity_options),
            ("Privileges Required", privileges_options),
            ("User Interaction", user_interaction_options),
            ("Scope", scope_options)
        ]  
        self.create_section(main_layout, "Environmental Score Metrics", environmental_specs)

    def create_section(self, layout, title, dropdown_specs):
        groupbox = QGroupBox(title)
        section_layout = QVBoxLayout()  # Vertical layout for each section
        groupbox.setLayout(section_layout)
        layout.addWidget(groupbox) 

        for label_text, options in dropdown_specs:
            self.create_dropdown(section_layout, label_text, options)
            
        return groupbox

    def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    def save_cvss_config(self, filename=None):
        ensure_directory_exists("cvss_records")
        cvss_vector_string = ""
        for groupbox in [self.exploitability_widget, self.impact_widget]:
            for dropdown in groupbox.findChildren(QComboBox):
                cvss_vector_string += dropdown.currentData()
                cvss_vector_string += "/"  # Add the slash separator
    
        cvss_vector_string = cvss_vector_string[:-1]
        if filename is None:
            user = getpass.getuser()  # Get current username
            initials = user[0] + user[-1]  # Extract first and last initials
            now = datetime.datetime.now(datetime.timezone.utc).astimezone()
            formatted_time = now.strftime("%H:%M:%S")
            filename = f"cvss_records/VulnerabilityName_{now.strftime('%m-%d-%Y_%H-%M-%S')}_{initials}.csv"
    
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(cvss_vector_string.split("/"))
    
    def load_cvss_config(self):
        ensure_directory_exists("cvss_records")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("CSV Files (*.csv)")
        dialog.setDirectory("cvss_records/")
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            if filename:
                try:
                    with open(filename, "r") as csvfile:
                        reader = csv.reader(csvfile)
                        cvss_values = next(reader)
    
                    dropdowns = []
                    for groupbox in [self.exploitability_widget, self.impact_widget]:
                        dropdowns.extend(groupbox.findChildren(QComboBox))
    
                    if len(cvss_values) == len(dropdowns):
                        for value, dropdown in zip(cvss_values, dropdowns):
                            index = dropdown.findData(value)
                            if index >= 0:
                                dropdown.setCurrentIndex(index)
                    else:
                        QMessageBox.warning(self, "Error", "Invalid CVSS configuration file.")
                except FileNotFoundError:
                    QMessageBox.warning(self, "Error", "File not found.")
    
    def save(self):
        if hasattr(self, "current_filename") and self.current_filename:
            self.save_cvss_config(self.current_filename)
        else:
            self.save_as()
    
    def save_as(self):
        ensure_directory_exists("cvss_records")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter("CSV Files (*.csv)")
        dialog.setDirectory("cvss_records/")
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            if filename:
                if not filename.endswith(".csv"):
                    filename += ".csv"
                self.save_cvss_config(filename)
                self.current_filename = filename

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Create the menubar
    menubar = window.menuBar()

    # Add the File menu
    file_menu = menubar.addMenu("File")
    open_action = file_menu.addAction("Open")
    open_action.triggered.connect(window.load_cvss_config)
    save_action = file_menu.addAction("Save")
    save_action.triggered.connect(window.save)
    save_as_action = file_menu.addAction("Save As")
    save_as_action.triggered.connect(window.save_as)

    window.show()
    sys.exit(app.exec_())
