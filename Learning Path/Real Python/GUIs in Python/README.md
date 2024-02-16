# Graphical User Interfaces in Python

When it comes to making a program, sometimes, it's easier to give the user the option to see everything they do, and to make it interactive. In this way you can directly manage what the user sees and doesn't see. For my case that I'm trying to build, I'd like for my finance analysis to be interactive so I can pick and choose what data is shown to me in my reports, and what graphs are built. I want to be able to see the changes I make in real-time as well. But I also don't want to have to think about the choices I make too much (is this column's data categorical, continuous or count? What graphs can I actually produce from this?) but still be able to create a report that works.

So, I thought I'd look into GUIs in Python. I used to try Tk Inter every now and then when I first ever did anything in Python, but it got really annoying to work with in script form rather than class form and I never learned how to do it properly back then. Now I'm in my era of learning things properly, I'm going to give it a shot again. But this time, with PyQt.

## PyQt

> PyQt is a Python wrapper for the C++ set of libraries and development tools, Qt, which provides platform-independent abstractions for GUIs.

PyQt, being a wrapper for Qt, is an API, and is very similar to PySide - Nokia's more official answer that has been adopted by the Qt project. There are so few differences between the two (and none of them really tangible) that it makes no difference which you learn, just know that it can be easy enough to port between the two.

Qt has undergone a recent update to Qt6, and as such PyQt and PySide have stable releases for it (PyQt6 and PySide6).

Install `PyQt6` using the pip command as normal (without caps) and awayyyyy we go!

### Let's Start with a Small Example

There are a few simple stages to creating your first application:

- Import `QApplication` and all the required widgets from `PyQt6.QtWidgets`.
- Create an instance of `QApplication`.
- Create your application’s GUI.
- Show your application’s GUI.
- Run your application’s event loop, or main loop.

First, we need to import `sys`. This allows us to use the `exit()` command to handle termination of the event loop.

Then, we create an instance of `QApplication`, passing either an empty list in the constructor, or `sys.argv`. You'd use `sys.argv` if you want your application to handle any command-line arguments

Next, we need to create our window in our application:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

app = QApplication([])

# Create the top-level window
window = QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)

# Next, a label
message = QLabel("<h1>Hello World!</h1>", parent=window) 
# PyQt6 will parse HTML by default!
```

First, we create our Application object, taking no arguments. Then, we have a `QWidget` which is the parent class for all Qt Widgets. This represents our top-level window.

> PyQt (and most other GUI engines) use a parent-child relationship hierarchy system whereby a parent has children, and a child is attached to a parent
>
> A Widget without a parent is a top-level window, and any Widget with a parent is a child, contained within the parent.
>
> The nature of the parent-child relationship is such that if a parent is deleted, all of its children go with it - no orphanages in the RAM!

We then attach a child `QLabel` object to the top-level window whose message can be parsed as HTML. We then set the position of this label within the parent.

Now, we want to be able to run it! We can do this in two lines:

```python
window.show()

sys.exit(app.exec())
```

We show the window. Then we run `sys.exit()` with a call to `app.exec()` inside it. the `exec()` method runs our application's event loop and begins execution by adding a Paint event to the event queue. When the application is exited, the exit code is passed to `sys.exit()` for better clean-up.

And this is what this looks like!

<p align="center">
    <img width="60%" src="Images/Hello World.png">
</p>

#### An Aside on Code Style

PyQt is built around a C++ library. Because of this, its naming conventions adhere to those of C++. This isn't really in line with PEP 8, but this PEP does state that you should keep in line with the style of whatever third-party packages you use. So we'll be using the C++ naming convention of camelCase rather than the Python snake_case (which I prefer but don't tell anyone).

## Let's move on a bit

The basics of PyQt are important, and most applications can be made from these basic building blocks. The main things to learn about are:

- Widgets
- Layout managers
- Dialogs
- Main windows
- Applications
- Event loops
- Signals and slots

### Widgets [→](https://realpython.com/python-pyqt-gui-calculator/#widgets)

Widgets are the things that people see on their screens and are rectangular components you can place on your window. You have several options for how these widgets will look, and your widgets can also detect and release signals and events

Some of the most common widgets are:

- Buttons
- Labels
- Line Edits
- Combo Boxes
- Radio Buttons

There are over [40 different widgets](https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/qwidget.html) that you can use and it's amazing.

### Layout Managers [→](https://realpython.com/python-pyqt-gui-calculator/#layout-managers)

When we have a lot of widgets all in one place, the last thing we want is to get them all messed up and with weird positions. We can control the position and size of a widget using the `.move()` and `.resize()` methods, but this only works in absolute space. We want to be able to manage things in relation to each other so that we don't end up with issues down the line.

Enter Layout Managers

These are the mos useful things you'll have when sorting your layouts. They come in four types:

- `QHBoxLayout` - Horizontal box
- `QVBoxLayout` - Vertical box
- `QGridLayout` - A grid layout
- `QFormLayout` - Two-column layout that looks like a form

In all of these, they're similar to flex boxes in that they'll grow dynamically depending on how much stuff is in them, and the content will be resized accordingly. For example, if you have a `QHBoxLayout` and you add 3 widgets to it, each one will have the same size. Then if you add a fourth one, they'll still all have equal size to each other, but will be smaller.

Let's make a grid that contains all the examples above:

<details><summary>Code Here!</summary>

```python
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
```

</details>

<p align="center">
    <img width="80%" src="Images/Grid Layouts.png">
    <p align="center">So yeah, was hoping that would look nicer but oh well</p>
</p>

Loads more about Layouts can be found [here](https://realpython.com/python-pyqt-layout/), which is kinda sexy.

### Dialogs [→](https://realpython.com/python-pyqt-gui-calculator/#dialogs)

There are two main types of GUI that we'll be looking at. Firstly is dialog-based GUIs (main window style will come later, but is what we were doing earlier tbf). Dialogs are windows that typically warrant communication from the user, and only appear a few times, rather than being an entire application.

In a main-window style application that uses dialog windows, you can show them in two ways: *modal* and *modeless*. Modal dialogs prevent the user interacting with other visible windows while the dialog is open, while modeless ones do not. They can be activated by using the window's `.exec()` command or `.show()` command, respectively.
