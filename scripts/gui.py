import sys
#import pyperclip
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt6.QtCore import QTimer
import json
import os
from datetime import datetime

CLIPBOARD_CLEAR_INTERVAL_MS = 10000
#TODO add a button to clear clipboard manually
#TODO show data in gui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My PyQt6 App")  # Set the window title
        self.setGeometry(100, 100, 400, 300)  # Set window size & position

        layout = QVBoxLayout()

        self.label = QLabel("Paste a URL and enter some text, then click 'Save'")
        layout.addWidget(self.label)

        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)

        """self.button = QPushButton("Save", self)
        self.button.clicked.connect(self.on_save)  # Connect button click to a method
        layout.addWidget(self.button)"""

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.clipboard_changed)

        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.clear_clipboard)
        #self.clipboard_timer.start(CLIPBOARD_CLEAR_INTERVAL_MS)  # Clear the clipboard every 5 seconds

        self.current_url = ""
    
    def clear_clipboard(self):
        self.clipboard.clear()
        self.current_url = ""
        self.label.setText("Clipboard cleared!")


    def clipboard_changed(self):
        clipboard_content = self.clipboard.text()
        if clipboard_content.startswith("http://") or clipboard_content.startswith("https://"):
            self.current_url = clipboard_content
            self.clipboard_timer.start(CLIPBOARD_CLEAR_INTERVAL_MS)
            self.label.setText(f"URL Copied: {self.current_url}\nWaiting for additional text to be copied...")
        elif self.current_url and len(clipboard_content) > 100:
            self.save_data(clipboard_content)


    def save_data(self, text):
        data_file = "read_knowledge.json"
        data = {}

        # If the file already exists, load the existing data
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)

        # Get the current time as a string
        current_time = datetime.now().isoformat()

        # If the current URL is in the data, add the new text to its dictionary
        if self.current_url in data:
            data[self.current_url][current_time] = text
        else:  # If the current URL is not in the data, add a new dictionary for it
            data[self.current_url] = {current_time: text}

        # Save the data back to the file
        with open(data_file, "w") as file:
            json.dump(data, file, indent=4)

        #self.label.setText("Data saved automatically! Copy another URL to continue.")
        #self.current_url = ""  # Reset the current URL

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())

