# =============================================================================
# Task 1: Basic Class Hierarchy (Inheritance)
# =============================================================================
# Objective:
#   - Define a base class 'Vehicle' with instance attributes: brand, fuel_type
#   - Create a subclass 'Car' that inherits from Vehicle and adds: num_doors
#   - Use super() in Car.__init__ to call the parent class initializer
# =============================================================================


# --- Base Class ---
# 'Vehicle' serves as the parent/base class.
# It defines attributes shared by ALL vehicles, regardless of type.
class Vehicle:

    def __init__(self, brand, fuel_type):
        """
        __init__ is the constructor — it runs automatically when an object
        is created from this class.

        Instance attributes (self.x) belong to each individual object,
        meaning each Vehicle instance stores its own brand and fuel_type.
        """
        self.brand = brand          # e.g. "Toyota", "Ford"
        self.fuel_type = fuel_type  # e.g. "Gasoline", "Electric"

    def describe(self):
        """A simple method to display the vehicle's core attributes."""
        print(f"Brand: {self.brand} | Fuel Type: {self.fuel_type}")


# --- Subclass ---
# 'Car' inherits from Vehicle by passing it in parentheses: class Car(Vehicle)
# This means Car automatically gains everything defined in Vehicle.
class Car(Vehicle):

    def __init__(self, brand, fuel_type, num_doors):
        """
        Car's __init__ accepts all Vehicle attributes PLUS its own (num_doors).

        super().__init__(...) calls the PARENT class's __init__ method.
        This ensures self.brand and self.fuel_type are properly set on the Car
        object, without duplicating that initialization logic here.

        Without super(), the inherited attributes would never be assigned,
        and accessing self.brand on a Car instance would raise an AttributeError.
        """
        super().__init__(brand, fuel_type)  # Delegates to Vehicle.__init__
        self.num_doors = num_doors          # Car-specific attribute, e.g. 2 or 4

    def describe(self):
        """
        Overrides Vehicle.describe() to include the Car-specific num_doors.
        Calls the parent's describe() first, then adds additional detail.
        """
        super().describe()  # Reuse the parent's output
        print(f"Number of Doors: {self.num_doors}")


# =============================================================================
# --- Demo / Test ---
# =============================================================================

# Instantiate a base Vehicle object
generic_vehicle = Vehicle(brand="Yamaha", fuel_type="Gasoline")
print("=== Vehicle ===")
generic_vehicle.describe()

print()

# Instantiate a Car object — it uses BOTH Vehicle's and Car's __init__ logic
my_car = Car(brand="Toyota", fuel_type="Hybrid", num_doors=4)
print("=== Car ===")
my_car.describe()

print()

# Confirm inheritance: isinstance() checks if my_car is a Car AND a Vehicle
print(f"my_car is a Car:     {isinstance(my_car, Car)}")      # True
print(f"my_car is a Vehicle: {isinstance(my_car, Vehicle)}")  # True — inheritance confirmed
