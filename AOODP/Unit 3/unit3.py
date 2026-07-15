# AOODP25_PCOM7E April 2026 Unit 3 
# Implementing the Factory Method Pattern

from abc import ABC, abstractmethod

# Abstract base class for all car types.
# Guarantees that any subclass will implement a drive() method,
# ensuring consistent behaviour across all car types.
class Car(ABC):
    @abstractmethod
    def drive(self):
        pass

# Concrete implementation of Car for a Sedan.
# Inherits from Car and implements drive() with Sedan-specific behaviour.
class CorollaCross(Car):
    def drive(self):
        return "Driving the Toyota Corolla Cross – smooth and comfortable ride."

# Concrete implementation of Car for an SUV.
# Inherits from Car and implements drive() with SUV-specific behaviour.
# New car types like this can be added at any time without modifying existing code.
class RAV4(Car):
    def drive(self):
        return "Driving the Toyota RAV4 – powerful and spacious, perfect for hauling gear."

# Concrete implementation of Car for a Hatchback.
# Inherits from Car and implements drive() with Hatchback-specific behaviour.
class PriusC(Car):
    def drive(self):
        return "Driving the Toyota Prius c – compact and fuel-efficient."

# Abstract base class for all car factories.
# Guarantees that any subclass will implement a create_car() method,
# ensuring a consistent interface for car creation across all factory types.
class CarFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass

# Concrete factory for creating Corolla Cross instances.
# Inherits from CarFactory and implements create_car() to return a Corolla Cross.
class CorollaCrossFactory(CarFactory):
    def create_car(self):
        return CorollaCross()

# Concrete factory for creating RAV4 instances.
# Inherits from CarFactory and implements create_car() to return a RAV4.
class RAV4Factory(CarFactory):
    def create_car(self):
        return RAV4()

# Concrete factory for creating Prius c instances.
# Inherits from CarFactory and implements create_car() to return a Prius c.
class PriusCFactory(CarFactory):
    def create_car(self):
        return PriusC()

# Client code that operates solely against the abstract CarFactory and Car interfaces.
# Accepts any CarFactory subclass, creates a car, and drives it —
# without any knowledge of the specific car type being produced.
def client_code(factory: CarFactory):
    car = factory.create_car()
    print(car.drive())

# To best understand these design patterns, I modeled what's available in my own garage
# as factories. 
garage = {
    "corolla_cross": CorollaCrossFactory(),
    "rav4": RAV4Factory(),
    "prius_c": PriusCFactory()
}

# Example 1: Eldest son needs a car to get to work — any available vehicle will do.
# The factory resolves which car is available at runtime without the caller needing to specify.
# Our modularity in this design pattern supports this. 

available_car = next(iter(garage.values()))  # grab the first available vehicle
print("Eldest son heading to work:")
client_code(available_car)

# Example 2: Youngest son needs the RAV4 specifically to haul two mountain bikes to the trail.
# The specific factory is requested by name because the use case demands it.
print("\nYoungest son heading to the trail with the bikes:")
client_code(RAV4Factory())

# Of course, we hope that the eldest hasn't taken the RAV4 to work, 
# but managing vehicle fleet inventory counts, and checking for concurrence 
# is definiately beyond the scope of this demonstration. :)
