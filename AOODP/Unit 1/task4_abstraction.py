# =============================================================================
# Task 4: Abstraction with Base Class
# =============================================================================
# Objective:
#   - Define an abstract class 'Animal' with an abstract method make_sound()
#   - Create 'Dog' and 'Cat' subclasses that each override make_sound()
#   - Dog returns "Woof!" and Cat returns "Meow!"
#
# Key Concepts:
#   - Abstraction: hiding complex or irrelevant implementation details and
#     exposing only what's necessary. The WHAT is defined here (every Animal
#     makes a sound), but the HOW is left to each concrete subclass.
#   - This builds on Task 2's ABC pattern, but focuses on abstraction as a
#     design principle rather than polymorphism as the primary goal —
#     the abstract class acts as a blueprint that enforces a shared interface.
#   - Contrast with Task 2: Shape.area() had math in each subclass.
#     Here make_sound() simply returns a string — the point is the contract,
#     not the computation.
# =============================================================================

from abc import ABC, abstractmethod


# --- Abstract Base Class ---
# Animal inherits from ABC, making it an abstract class.
# It defines WHAT all animals must be able to do (make a sound),
# without specifying HOW any particular animal does it.
class Animal(ABC):

    def __init__(self, name):
        """
        Even abstract classes can have an __init__ and concrete attributes.
        'name' is shared by all animals, so it belongs here in the base class.
        Subclasses will call super().__init__(name) to set this up.
        """
        self.name = name  # e.g. "Rex", "Whiskers"

    @abstractmethod
    def make_sound(self):
        """
        Abstract method — declares the CONTRACT that every Animal subclass
        must implement make_sound(). No body is provided here because
        there is no single correct answer at the Animal level.

        If a subclass does NOT implement this method, Python will refuse
        to instantiate it and raise a TypeError — the contract is enforced
        at object creation time, not at call time.
        """
        pass

    def describe(self):
        """
        A CONCRETE method on the abstract class — this IS fully implemented
        and inherited as-is by all subclasses. Subclasses don't need to
        override it, but they benefit from it automatically.

        This illustrates an important nuance: abstract classes can mix
        abstract methods (must be overridden) with concrete methods (ready
        to use as-is). Only the abstract ones enforce the contract.
        """
        # make_sound() is called here — even though Animal doesn't define it,
        # this works because by the time describe() runs on any real object,
        # that object is guaranteed to be a concrete subclass with make_sound()
        # implemented (the ABC contract ensures this).
        print(f"I am {self.name} and I say: {self.make_sound()}")


# --- Subclass 1: Dog ---
# Dog inherits from Animal and fulfills the contract by implementing make_sound().
class Dog(Animal):

    def __init__(self, name):
        """
        Calls super().__init__(name) to let Animal's __init__ handle
        setting self.name — no need to repeat that logic here.
        """
        super().__init__(name)  # Delegates name assignment to Animal.__init__

    def make_sound(self):
        """
        Concrete implementation of the abstract method for Dog.
        Simply returns the string "Woof!" — Dog's specific sound.
        The return value (rather than print) keeps this method flexible;
        callers decide what to do with the sound (print, log, compare, etc.).
        """
        return "Woof!"


# --- Subclass 2: Cat ---
# Cat also inherits from Animal and provides its own make_sound() implementation.
class Cat(Animal):

    def __init__(self, name):
        """Same pattern as Dog — super() handles the shared name attribute."""
        super().__init__(name)

    def make_sound(self):
        """
        Concrete implementation of the abstract method for Cat.
        Returns "Meow!" — entirely independent of Dog's implementation,
        yet both satisfy the same abstract contract defined in Animal.
        """
        return "Meow!"


# =============================================================================
# --- Demo / Test ---
# =============================================================================

print("=== Individual Animals ===")
dog = Dog(name="Rex")
cat = Cat(name="Whiskers")

# Calling make_sound() directly — each returns its own sound
print(f"{dog.name} says: {dog.make_sound()}")
print(f"{cat.name} says: {cat.make_sound()}")

print()
print("=== Using the Inherited describe() Method ===")
# describe() is defined once in Animal but works on both Dog and Cat,
# because it internally calls make_sound() — which each subclass has implemented.
dog.describe()
cat.describe()

print()
print("=== Abstraction via Mixed-Type List ===")
# A list of Animal objects — the calling code doesn't need to know
# whether each is a Dog or Cat; it just calls make_sound() on each.
# The correct sound is returned automatically based on the actual type.
animals = [Dog("Buddy"), Cat("Luna"), Dog("Max"), Cat("Shadow")]

for animal in animals:
    # type(animal).__name__ gives the class name as a string for display
    print(f"  {type(animal).__name__:>4} ({animal.name:<8}) → {animal.make_sound()}")

print()
print("=== Proving Abstract Class Cannot Be Instantiated ===")
# Animal is abstract — instantiating it directly violates the contract
# because make_sound() has no implementation at the Animal level.
try:
    generic_animal = Animal("Unknown")
except TypeError as e:
    print(f"  TypeError caught: {e}")

print()
print("=== Confirming Inheritance Chain ===")
# Both Dog and Cat are Animals — isinstance() confirms the hierarchy
print(f"  dog is a Dog:    {isinstance(dog, Dog)}")
print(f"  dog is an Animal: {isinstance(dog, Animal)}")
print(f"  cat is a Cat:    {isinstance(cat, Cat)}")
print(f"  cat is an Animal: {isinstance(cat, Animal)}")
