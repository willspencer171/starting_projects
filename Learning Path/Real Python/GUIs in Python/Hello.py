import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication([]) # Can pass sys.argv if you have command line arguments

# Now for the application window (top-level window)

window = QWidget()
window.setWindowTitle("PyQT App")
window.setGeometry(100, 100, 280, 80)

message = QLabel("<h1>Hello World!</h1>", parent=window)
message.move(60, 15)

# Now, we run

window.show()

sys.exit(app.exec())
