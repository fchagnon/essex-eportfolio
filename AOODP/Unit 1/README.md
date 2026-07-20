# Unit 1: Introduction and Recap of Object-Oriented Programming (OOP)

## Unit Topic

This unit revisits the four pillars of OOP, inheritance, polymorphism,
abstraction, and encapsulation, alongside classes, objects, constructors,
destructors, and access control. It also introduces how these principles
scale into large-scale and secure software design, the theme the rest of
the module builds on.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the four key OOP concepts: inheritance,
  polymorphism, abstraction, and encapsulation.
- Describe the role of classes, objects, constructors, destructors, and
  access control in OOP.
- Apply OOP principles to design basic class hierarchies in Python or Java.
- Recognize the importance of OOP in large-scale and secure software design.

## Formative Assignment

Five programming exercises covering classes, objects, access control,
inheritance, polymorphism, abstraction, and encapsulation:

1. **Inheritance** — a `Vehicle` base class with `brand` and `fuel_type`,
   and a `Car` subclass adding `num_doors`, calling the parent constructor
   via `super()`.
2. **Polymorphism** — an abstract `Shape` class with an abstract `area()`
   method, implemented differently by `Circle` and `Rectangle`.
3. **Encapsulation** — a `BankAccount` class with a private `__balance`,
   accessed only through `deposit()`, `withdraw()`, and `get_balance()`.
4. **Abstraction** — an abstract `Animal` class with an abstract
   `make_sound()`, implemented by `Dog` and `Cat`.
5. **Constructors and destructors** — a `Person` class with `__init__` and
   `__del__`, tested across explicit deletion, scope exit, and multiple
   references.

Full code: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%201

## Reading List

Lott, S.F. (2024) *Modern Python Cookbook: 130+ Updated Recipes for Modern
Python 3.12 with New Techniques and Tools*. 3rd edn. Birmingham: Packt
Publishing. Chapters 7, 8, and 15.

Sarcar, V. (2023) *Java Design Patterns: A Hands-On Experience with
Real-World Examples*. 3rd edn. Berkeley, CA: Apress. Chapters 1 and 12-18.

## Reflection

Each of the four learning outcomes for this unit maps onto something real
from working through it, and onto where it resurfaced later in the module.

**Understanding the four pillars.** These were familiar in outline before
this unit, from an undergraduate degree in the early 2000s and years of
object-oriented Perl, but writing them again from scratch, in a language I
hadn't used this way before, made clear how much had gone dormant rather
than been forgotten outright.

**Classes, objects, constructors, destructors, and access control.**
`Person.__del__` was the most instructive exercise here, testing it across
explicit deletion, scope exit, and multiple references showed directly
that Python's reference-counting model doesn't behave like the destructors
I remembered from C++, deletion only fires once the last reference is
gone, not the first `del` call. `BankAccount`'s `__balance` and Python's
name mangling were a similar case: privacy here is a convention, not a
hard enforcement mechanism, unlike the access modifiers I was used to
from Java.

**Applying OOP principles to basic class hierarchies.** This came back
directly and repeatedly across the module: constructor injection first
appeared conceptually here and became the actual mechanism behind Unit 6's
`TransactionSimulator` and Unit 9's `ProductRepository`.

**Recognizing OOP's role in large-scale and secure software design.** This
outcome only became concrete much later. It's one thing to be told OOP
matters for large-scale, secure systems in a first-week overview; it's
another to have actually built one, Unit 9's ShopEase architecture and
Unit 7's authentication system are what this outcome actually looks like
in practice, not something this unit could demonstrate on its own.
