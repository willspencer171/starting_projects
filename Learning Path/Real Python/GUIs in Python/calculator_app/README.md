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
