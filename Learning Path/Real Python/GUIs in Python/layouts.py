import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    
)

app = QApplication([])

window = QWidget()
window.resize(1080, 680)
window.setWindowTitle("Layout App")

windowLayoutGrid = QGridLayout()
gridLayoutVBox = QVBoxLayout()
gridLayoutHBox = QHBoxLayout()
gridLayoutForm = QFormLayout()

# 3 rows down
windowLayoutGrid.addLayout(gridLayoutVBox, 0, 0, 3, 1)
# 3 columns across
windowLayoutGrid.addLayout(gridLayoutHBox, 0, 1, 1, 3)
# 2 by 2 button
windowLayoutGrid.addWidget(QPushButton("Nothing here"), 1, 1, 3, 3)
# Form on bottom row
windowLayoutGrid.addLayout(gridLayoutForm, 3, 2, 1, 2)

gridLayoutVBox.addWidget(QPushButton("Top!"))
gridLayoutVBox.addWidget(QPushButton("Middle!"))
gridLayoutVBox.addWidget(QPushButton("Bottom!"))

gridLayoutHBox.addWidget(QPushButton("Left!"))
gridLayoutHBox.addWidget(QPushButton("Center!"))
gridLayoutHBox.addWidget(QPushButton("Right!"))

gridLayoutForm.addRow("Name: ", QLabel("Annyeong"))
gridLayoutForm.addRow("Age: ", QLabel("Hello"))
gridLayoutForm.addRow("Address: ", QLabel("Hi"))

window.setLayout(windowLayoutGrid)
window.show()

sys.exit(app.exec())
