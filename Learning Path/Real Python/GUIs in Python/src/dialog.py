import sys
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

# We use a class-based design here, which allows us to create
# a blueprint and also customise things a little.
# We can even include our own methods which is nice
class Window(QDialog):
    def __init__(self) -> None:
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        dialogLayout = QVBoxLayout()

        # Form layout
        formLayout = QFormLayout()
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Age:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Hobbies:", QLineEdit())
        dialogLayout.addLayout(formLayout)

        # Group of buttons
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            # These buttons don't do anything yet
            # They're unbound
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons)

        self.setLayout(dialogLayout)

# IMPORTANT
# __name__ == "__main__" is used to make sure that nothing
# gets run unless the script is run as a program, rather
# than when it gets imported OBVS
if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()

    sys.exit(app.exec())
