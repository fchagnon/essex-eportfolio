# =============================================================================
# Task 2: Polymorphism with Methods
# =============================================================================
# Objective:
#   - Define an abstract base class 'Shape' with an abstract method area()
#   - Create 'Circle' and 'Rectangle' subclasses that inherit from Shape
#   - Each subclass implements area() using its own formula
#
# Key Concepts:
#   - ABC (Abstract Base Class): a class that cannot be instantiated directly;
#     it exists only to be subclassed. It enforces a "contract" — any subclass
#     MUST implement all abstract methods, or Python will raise a TypeError.
#   - abstractmethod: a decorator that marks a method as abstract (no body).
#   - Polymorphism: different classes respond to the SAME method call (area())
#     in their own way — same interface, different behavior.
# =============================================================================

import math  # Provides math.pi for the Circle area formula

# ABC and abstractmethod are imported from Python's built-in 'abc' module
from abc import ABC, abstractmethod


# --- Abstract Base Class ---
# Inheriting from ABC marks this as an abstract class.
# Shape cannot be instantiated on its own — it only defines the interface
# that all concrete subclasses must follow.
class Shape(ABC):

    @abstractmethod
    def area(self):
        """
        The @abstractmethod decorator declares area() as a contract:
        every subclass of Shape is REQUIRED to provide its own implementation.

        There is intentionally no body here (just a docstring/pass) —
        Shape itself has no meaningful way to calculate an area.
        Attempting to instantiate Shape directly will raise:
            TypeError: Can't instantiate abstract class Shape with abstract method area
        """
        pass


# --- Subclass 1: Circle ---
# Circle inherits from Shape and fulfills the contract by implementing area().
class Circle(Shape):

    def __init__(self, radius):
        """
        Circle only needs one attribute — its radius.
        No super().__init__() call is needed here because Shape's __init__
        (inherited from ABC) takes no arguments beyond self.
        """
        self.radius = radius  # e.g. 5.0

    def area(self):
        """
        Implements the abstract method with the circle area formula:
            A = π * r²
        math.pi provides a precise value of π (3.141592653589793).
        ** is Python's exponentiation operator, so radius**2 = radius squared.
        """
        return math.pi * self.radius ** 2


# --- Subclass 2: Rectangle ---
# Rectangle also inherits from Shape and provides its own area() implementation.
class Rectangle(Shape):

    def __init__(self, length, width):
        """Rectangle is defined by two dimensions: length and width."""
        self.length = length  # e.g. 8.0
        self.width = width    # e.g. 3.0

    def area(self):
        """
        Implements the abstract method with the rectangle area formula:
            A = length * width
        Simple multiplication — but critically, it's the SAME method name
        as Circle.area(), which is what makes this polymorphism.
        """
        return self.length * self.width


# =============================================================================
# --- Demo / Test ---
# =============================================================================

# Instantiate one of each concrete shape
circle = Circle(radius=5)
rectangle = Rectangle(length=8, width=3)

# Polymorphism in action: the same method name area() is called on both objects.
# Python automatically dispatches to the correct implementation based on the
# actual type of each object — no if/else needed.
print("=== Circle ===")
print(f"Radius: {circle.radius}")
print(f"Area (π * r²): {circle.area():.4f}")  # :.4f formats to 4 decimal places

print()

print("=== Rectangle ===")
print(f"Length: {rectangle.length} | Width: {rectangle.width}")
print(f"Area (length * width): {rectangle.area():.4f}")

print()

# Demonstrate polymorphism explicitly: iterate over a list of mixed Shape objects
# and call area() on each — same call, different results based on type.
shapes = [Circle(7), Rectangle(10, 4), Circle(2.5), Rectangle(6, 6)]

print("=== Polymorphic Loop Over Mixed Shapes ===")
for shape in shapes:
    # type(shape).__name__ gives us the class name as a string (e.g. "Circle")
    print(f"{type(shape).__name__:>12} → area = {shape.area():.4f}")

print()

# Demonstrate that Shape itself cannot be instantiated (the abstract contract)
print("=== Attempting to Instantiate Abstract Class ===")
try:
    s = Shape()  # This will raise a TypeError
except TypeError as e:
    print(f"TypeError caught: {e}")
