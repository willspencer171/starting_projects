# Building a Calculator App with PyQt6

Now that I've gone over the [fundamentals](../README.md) of PyQt6 (and simultaneously, PySide6), let's have a look into building an actual app!

To that end, I'm going to be creating a simple calculator and it's going to be amazing and you're going to love it.

## MVC (Model-View-Controller) Design Pattern

The Model-View-Controller design pattern is ubiquitous and everyone needs to have some sort of understanding about how it works. The MVC pattern comprises three layers - Model, View and Controller. I'm going to be using the MVC pattern in this application, so let me break down the components for you:

### Model

The model is essentially the functionality of your application. It takes care of the [business logic](https://en.wikipedia.org/wiki/Business_logic) of your system. Business logic is the code that represents the real-world rules that your system must follow to develop a solution.

In a calculator app, the model will handle calculations and input values.

### View

The view is exactly what it says on the tin, your view is what your user will see on their screen (not to be confused with [Django views](https://github.com/willspencer171/python_roadmap/tree/master/Frameworks/Synchronous/Django#lets-talk-about-views)).

In my case, this is the calculator window that will appear on screen

### Controller

The controller is the interface between the model and view. It takes care of events and gets the model to work, which in turn will update the view. The three layers create a sort of cycle - the user does something with the view, the controller manipulates the model, which updates the view:

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a0/MVC-Process.svg" width=30%>
</p>

## Let's get into it

First, we'll build a really simple skeleton that will run the app: Just a `QMainWindow` that is 235x235 pixels with a `QWidget` central widget. Nothing more.

### The View

<details><summary>Code Here!</summary>

```python
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget
)

# Window Dimensions
WINDOW_SIZE = 235

# Main Window class
class PyCalcWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

# Main method run when script runs
def main():
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()

    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
```

</details>

Problem is, this doesn't really make anything that looks like a calculator, but this is the skeleton that we'll be working with and building everything into.

We should add in a few bits and pieces to make this an actual calculator:

```python
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,    # For the user to interact with
    QVBoxLayout,    # For the general layout of the app
    QGridLayout,    # For the keyboard layout of buttons
    QLineEdit,      # To display our calculations
)
```

We're going to need to implement these objects in our code now. Since we're implementing with a class-based approach, we can add a few methods to our class to build our view layer. Let's look at the calculator display first since it's quite simple:

```python
DISPLAY_HEIGHT = 35

class PyCalcWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.mainLayout = QVBoxLayout()

        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        # Construction methods
        self._createDisplay()
        self._createButtons()
    
    # Text Display creation method
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Means a user can't edit the display
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
```

This method creates our display, gives it a fixed height (of 35px), sets its alignment and sets it to read-only. Nice and simple for now.

Now, we need to create our grid of buttons in the `_createButtons()` method:

```python
BUTTON_SIZE = 40

class PyCalcWindow(QMainWindow):
    ...

    def _createButtons(self):
        self.buttonMap = {} # blank dictionary to be filled with buttons
        buttonsLayout = QGridLayout()
        keyboard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        # I hate that this is actually the fastest way to populate
        # the dictionary - a solid O(n^2)
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, 
                                                 BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        
        self.generalLayout.addLayout(buttonsLayout)
```

Aside from actually putting the components on our user's screen, we need to create methods to actually get information to and from the screen's displays. To this end, we create getter and setter functions for the display `QLineEdit` as well as a clear function:

```python
def setDisplayText(self, text):
    self.display.setText(text)
    self.display.setFocus

def displayText(self):
    return self.display.text()

def clearDisplayText(self):
    self.display.setText("")
```

So this is what it looks like so far which is nice!

<p align="center">
    <img width=50% src="./Images/Partial Calculator.png">
</p>

Not that it does anything! Let's change that

### The Model

Okay so I lied. Here, I'm only talking about the model, rather than the controller that connects the model and view. It's relatively simple actually, I'm going to be using the built-in Python method `eval` to evaluate any expressions given to the calculator via the buttons.

> People always say that `eval` is an unsafe or insecure method to use for anything that takes a user's input. However, since our QLineEdit is read-only, and the only way of inputting data will be through a set of predefined buttons, this method will be safe to use.

We can implement our calculator's functionality (model) as follows:

```python
# Error message to display on calculator
ERROR_MSG = "ERROR"

def evaluateCalculatorExpression(expression):
    try:
        # passing two empty dicts restricts access to any global
        # or local variables
        return str(eval(expression, {}, {}))
    except Exception:
        return ERROR_MSG
```

Since this function is not part of the view, it is not included as part of the `PyCalcWindow` class definition.

We use this function to return a string - either the correctly evaluated expression OR the error message.

And that's it! The whole model done!

### The Controller

This is a separate class that we now need to create. This class will control the `PyCalcWindow` that we created earlier via the model and its own functions. This one will just be called `PyCalc`.

The `PyCalc` class will take in the model and view as arguments in its constructor method, and use these to carry out everything it needs to, including calculating the result, building the expression in the display, and connecting signals and slots together. Let's create methods for each of those:

```python
class PyCalc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    # Calculate the result and display it
    def _calculateResult(self):
        result = self._evaluate(self._view.displayText())
        self._view.setDisplayText(result)
    
    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplayText()
        expression = self._view.displayText() + subExpression
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
        self._view.buttonMap["C"].clicked
            .connect(self._view.clearDisplayText)
```

SO, we have our View, Model and Controller for our calculator which is awesome! Now we just need to create an instance of our controller in the `main()` function like `PyCalc(model=evaluateCalculatorExpression, view=pycalcWindow)`. No need to save it to a variable or anything, just create it and it'll work (somehow)

At the end of the day, PyQt lends itself to the Model-View architecture which is essentially the same, but doesn't really distinguish the View layer from the Controller layer. An example of this can be found [here](https://www.pythonguis.com/tutorials/pyqt6-modelview-architecture/), which makes a basic to-do list app (maybe worth trying to implement yourself, look into other types of widget)

Anyway, thanks for checking this out, have a look at the [source code](./src/pycalc.py) if you'd like and as always,

Have a beautiful day
