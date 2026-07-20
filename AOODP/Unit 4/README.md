# Unit 4: Design Patterns II - Structural Patterns

## Unit Topic

This unit covers seven structural design patterns, Adapter, Bridge,
Composite, Decorator, Facade, Proxy, and Flyweight, which organize
classes and objects into larger, more flexible structures. The formative
activity for this unit was a collaborative discussion applying Adapter,
Bridge, and Composite; Decorator was not built hands-on here, it became a
practical exercise later, in Unit 10.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the purpose and use of key structural design
  patterns, including Adapter, Bridge, Composite, Decorator, Facade,
  Proxy, and Flyweight.
- Recognize how structural patterns enable modular, flexible, and
  maintainable code.
- Apply the Decorator pattern in a practical coding exercise to
  dynamically enhance code functionality.
- Analyze real-world examples of structural patterns in action, such as
  in network security systems.

## Formative Assignment

*(Formative, collaborative discussion format)*

Apply three structural patterns to real-world scenarios, with a Python
code example for each:

1. **Adapter** — integrating a legacy SOAP-based payment system with a
   modern RESTful e-commerce platform.
2. **Bridge** — managing different devices (TV, Radio) and their remote
   controls (Basic, Advanced), decoupling abstraction from implementation.
3. **Composite** — managing a file system where files and folders are
   treated uniformly through a shared interface.

Full post: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%204

## Reading List

Di Francesco, H. (2024) *JavaScript Design Patterns: Deliver Fast and
Efficient Production-Grade JavaScript Applications at Scale*. 1st edn.
Birmingham: Packt Publishing. Chapters 2 and 3.

## Reflection

I deliberately chose a domain outside typical textbook examples for my
original post, an AI-driven Security Operations Centre, to test whether
structural patterns actually generalized rather than taking that
generality on faith.

**Understanding the purpose of structural patterns.** Modelling the
Adapter pattern around telemetry normalization made the pattern's real
purpose click: it's not just about making two interfaces compatible, it's
about ensuring the *integrity* of what flows downstream. This became
sharper through peer discussion, replying to Joseph's SIEM-focused post, I
recognized we had independently arrived at the same underlying
requirement, a normalized data layer, at different points in the maturity
curve of security operations: correlation engine, human analyst, or
autonomous agent, the same problem needs solving before anything above it
can function reliably.

**Recognizing how structural patterns enable modular, flexible code.** My
Composite implementation (a MITRE ATT&CK threat hierarchy, traversed
identically by an AI reasoning agent) and a classmate's file-system
Composite arrived at the same structural approach from genuinely different
problem domains, evidence that the pattern generalizes as an
architectural principle rather than being tied to any one kind of
hierarchy.

**Applying Decorator in a practical exercise.** This did not happen in
Unit 4 itself; the formative activity here was the collaborative
discussion on Adapter, Bridge, and Composite. Decorator became genuinely
hands-on in Unit 10, wrapping actions with audit logging.

**Analyzing real-world examples in security systems.** Reviewing a peer's
`PaymentAdapter`, I identified that hardcoding a currency inside the
adapter class quietly mixed two responsibilities, interface translation
and currency policy, a Single Responsibility Principle violation (Martin,
2003) hiding inside a structural pattern that looked correct on the
surface. Catching that in someone else's code was, in hindsight, good
preparation for the same kind of self-check I later had to apply to my
own work, catching an inconsistency in my own Strategy implementations
across Units 5 and 8.

## References

Martin, R.C. (2003) *Agile Software Development: Principles, Patterns,
and Practices*. Upper Saddle River, NJ: Prentice Hall.
