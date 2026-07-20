# Unit 11: Dependency Injection and Inversion of Control (IoC)

## Unit Topic

This unit covers Dependency Injection and Inversion of Control, decoupling
components so dependencies are supplied from outside a class rather than
created internally, improving flexibility, modularity, and testability.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the principles of Dependency Injection (DI) and
  Inversion of Control (IoC).
- Recognize how DI frameworks like Spring and Google Guice make code
  more flexible, modular, and testable.
- Apply DI principles to implement dependency injection in a Python
  application.
- Reflect on how DI and IoC can improve the maintainability and
  scalability of software systems.

## Formative Assignment

*(Not completed)*

Refactor a tightly coupled `UserManager`/`EmailService` example to use DI
and IoC: introduce a `NotificationService` interface, inject it into
`UserManager` rather than instantiating `EmailService` directly, and test
`UserManager` in isolation using a mock notification service.

## Reading List

Taelman, R. et al. (2023) 'Components.js: Semantic dependency injection',
*Semantic Web*, 14(1), pp. 135-153. Sections 1, 2, and 4.

Laigner, R. et al. (2022) 'Cataloging dependency injection anti-patterns
in software systems', *The Journal of Systems and Software*, 184, 111125.

Tuğan, S., Arslan, E. and Tiryaki, A.M. (2024) 'Developing a Web
Framework Based on Inversion of Control', *The European Journal of
Research and Development*, 4(2), pp. 96-109.

## Reflection

I completed the reading for this unit but, running behind schedule at
this point in the module, skipped the formative assignment itself and
moved directly into Unit 12's summative work, the EMA itself, instead.
That is a genuine gap, not a design choice, and worth stating plainly
rather than working around it.

The underlying concept did not go unpracticed, though, it appeared
independently in two later units, without me deliberately setting out to
apply it. Unit 9's `ProductRepository` and Unit 10's `Protocol`-based
`SubmissionRepository` both depend on an injected abstraction rather than
a concrete class, the same principle this unit's `UserManager` exercise
would have demonstrated directly. Taelman et al. (2023) frame DI as
objects asking for the interfaces they require rather than instantiating
them, an inversion of the usual direction of control so the dependency,
not the dependent class, waits to be called, which matches exactly how
both of those later classes are actually constructed.

If I were to complete this unit's formative properly, the most honest
next step would be finishing it on its own terms rather than only relying
on where the concept resurfaced elsewhere, since a `NotificationService`
mock test is a different, more direct demonstration of testability than
either later example provides on its own.
