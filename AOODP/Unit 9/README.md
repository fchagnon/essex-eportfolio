# Unit 9: Object-Oriented Software Architecture

## Unit Topic

This unit covers software architecture styles (layered, microservices,
monolithic) and how object-oriented design principles support scalable,
maintainable, and secure systems, applied hands-on by designing ShopEase,
a layered e-commerce architecture.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain key software architecture styles, including
  layered architecture, microservices, and monolithic applications.
- Recognize the role of object-oriented design in creating scalable,
  maintainable, and secure architectures.
- Analyze a case study on designing a secure architecture for a
  large-scale system.
- Apply architectural principles to build a simple object-oriented-based
  software architecture.

## Formative Assignment

Design an online shopping system (ShopEase) for a growing number of users
and products, addressing:

1. **Scalability** — handling growth in users and products.
2. **Modularity** — independent modules (user management, product
   catalogue, order processing).
3. **Security** — protecting user data and transactions.
4. **Extensibility** — easy addition of new features (payment methods,
   recommendation engines).
5. **Layered architecture** — Presentation, Business Logic, and Data
   Access layers, each internally modular and built on encapsulation,
   inheritance, and polymorphism.

Full code and design rationale: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%209

## Reading List

Chow, J. (2024) *Software Architecture with Kotlin: Combine Various
Architectural Styles to Create Sustainable and Scalable Software
Solutions*. 1st edn. Birmingham: Packt Publishing. Chapters 6, 7, and 13.

Garcia, M.M. and Telang, T. (2023) *Learn Microservices with Spring Boot
3: A Practical Approach Using Event-Driven Architecture, Cloud-Native
Patterns, and Containerization*. 3rd edn. Berkeley, CA: Apress. Chapters
6, 7, and 8.

## Reflection

I relied on UML diagrams to map out classes and their dependencies before
writing a single line of code, a habit that prevented me from falling
back into monolithic procedures that violated SOLID principles.

**Understanding architecture styles.** The brief specifies layered
architecture directly, so the real learning here wasn't choosing between
styles, it was understanding *why* layering solves the stated
requirements at all, rather than treating it as an arbitrary structural
choice.

**Recognizing the role of OOP in scalable, secure architecture.** Working
through this gave me a concrete answer to a question I hadn't had to
think about explicitly before: what actually makes an architecture
"large-scale ready." The answer isn't size, it's decoupling, the same
principle behind splitting an application into layers connected only
through abstractions, so any one can be swapped without breaking the
others. Every mechanism in ShopEase, Repository for storage, a
composition root for wiring, Abstract Factory for payment providers,
Observer for notifications, is a separate instance of that same rule.

**Analyzing the case study.** Security split into two genuinely different
problems that needed different solutions: credentials, handled through
hashed passwords, and payment data, handled by never letting it touch the
application's own code at all, `PaymentGateway.charge(amount)` accepts
only a monetary amount, keeping card capture entirely inside the
provider's systems by design.

**Applying architectural principles.** Two patterns beyond the brief's
own requirements, Abstract Factory and Visitor, were deliberately added
during this unit, not because ShopEase's own brief called for them, but
because no other unit's work provided an artefact for either pattern.
Abstract Factory turned out to be a legitimate answer to the brief's own
extensibility requirement regardless; Visitor was added purely for
portfolio completeness, justified on its own design merits (keeping
`Product` and `Order` free of reporting logic) rather than anything the
brief itself asked for.
