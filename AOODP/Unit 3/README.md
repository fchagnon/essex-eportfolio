# Unit 3: Design Patterns I - Creational Patterns

## Unit Topic

This unit introduces design patterns as proven, reusable solutions to
common design problems, focusing on five creational patterns: Singleton,
Factory Method, Builder, Prototype, and Abstract Factory. The formative
exercise focuses specifically on Factory Method, implemented hands-on;
the other four are covered conceptually through the reading and case
study rather than built directly in this unit.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain what design patterns are and why they are
  important in software development.
- Identify and apply key creational design patterns, including Singleton,
  Factory Method, Builder, Prototype, and Abstract Factory.
- Recognize how creational patterns are used in real-world software
  systems to improve flexibility and maintainability.
- Implement the Factory Method pattern in a practical coding exercise.

## Formative Assignment

*(Formative, not assessed; informal tutor feedback only)*

Design a system for a car manufacturer producing different car types
using the Factory Method pattern, so the main program can create cars
without specifying their exact class:

- A `Car` abstract class with a `drive()` method.
- Concrete car classes (implemented here as real Toyota models rather
  than the generic Sedan/SUV/Hatchback naming suggested in the brief).
- A `CarFactory` abstract class with a factory method `create_car()`.
- Concrete factory classes overriding `create_car()` for each car type.
- A demonstration where client code depends only on the abstract `Car`
  and `CarFactory`, never a concrete class.

Full code: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%203

## Reading List

Sarcar, V. (2022) *Java Design Patterns: A Hands-On Experience with
Real-World Examples*. 3rd edn. Berkeley, CA: Apress. Parts 1, 2, and 4.

Reddy, M. (2024) *API Design for C++*. 2nd edn. San Diego: Elsevier
Science and Technology. Chapters 3, 9, 10, and 12.

## Reflection

While SOLID principles from Unit 2 were familiar to me, design patterns
like Factory Method were new. Either these patterns weren't yet refined
in the mid-2000s, or my study in application programming didn't go deep
enough to reach them.

**Understanding what design patterns are.** This unit was the first place
the difference between a principle and a pattern actually landed: SOLID
gives you rules for how classes should relate to each other, a pattern is
a specific, named structure for solving a recurring problem within those
rules. That distinction wasn't obvious walking in.

**Identifying and applying creational patterns.** Only Factory Method was
built hands-on here; Singleton, Builder, Prototype, and Abstract Factory
stayed conceptual through the reading and case study. Abstract Factory
specifically became hands-on much later, in Unit 9's payment provider
system, where the family-of-related-objects idea from this unit's reading
finally had a real problem to solve.

**Recognizing creational patterns in real-world systems.** This required
real, ground-up learning rather than translation from prior experience.
This really forced me to start thinking much more abstractly about
design. That is not natural for me, it goes very against the grain.

**Implementing Factory Method.** New car types are added as new classes;
the client code that requests a car never changes, since it only ever
depends on the abstract `Car` interface. Simple in hindsight, but the
exercise of building it, rather than just reading about it, is what made
the abstraction genuinely click rather than remain a definition.
