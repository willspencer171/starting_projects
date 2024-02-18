import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QGridLayout,
)
from functools import partial

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"

# View
class PyCalcWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {} # blank dictionary to be filled with button objects
        buttonsLayout = QGridLayout()
        keyboard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """Set display text"""
        self.display.setText(text)
        self.display.setFocus

    @property
    def displayText(self):
        """Get display text"""
        return self.display.text()

    def clearDisplayText(self):
        """Clear display text"""
        self.display.setText("")

# Model
def evaluateCalculatorExpression(expression):
    try:
        # passing two empty dicts restricts access to any global
        # or local variables
        return f"{eval(expression, {}, {})}"
    except (SyntaxError, NameError, ZeroDivisionError, TypeError):
        return ERROR_MSG

# Controller
class PyCalc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    # Calculate the result and display it
    def _calculateResult(self):
        result = self._evaluate(self._view.displayText)
        self._view.setDisplayText(result)
    
    def _buildExpression(self, subExpression):
        if self._view.displayText == ERROR_MSG:
            self._view.clearDisplayText()
        expression = self._view.displayText + subExpression
        self._view.setDisplayText(expression)
    
    def _connectSignalsAndSlots(self):
        # Connect the character-adding buttons
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        
        # Connect the remaining characters AND check if the
        # return key was pressed with the QLineEdit in focus
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplayText)

def main():
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()

    PyCalc(evaluateCalculatorExpression, pycalcWindow)

    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
