# Unit 5: Design Patterns III - Behavioural Patterns

## Unit Topic

This unit covers six behavioural design patterns, Strategy, Observer,
Chain of Responsibility, Template Method, Command, and State, which
govern how objects interact and communicate. The formative exercise
focuses specifically on Strategy, implemented hands-on; the other five
are covered conceptually through the reading and case study.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the purpose and use of key behavioural design
  patterns, including Strategy, Observer, Chain of Responsibility,
  Template Method, Command, and State.
- Recognize how behavioural patterns enable efficient interaction and
  communication between objects.
- Apply the Strategy pattern in a practical coding exercise to make code
  more flexible and reusable.
- Analyze real-world examples of behavioural patterns in action, such as
  the Observer pattern in cybersecurity systems.

## Formative Assignment

*(Formative, collaborative discussion format)*

Refactor a payment processor's `if`/`elif` chain using the Strategy
pattern: identify the problems in the original implementation, explain
how Strategy solves them, provide a refactored version, and discuss the
benefits.

Full post: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%205

## Reading List

Nesteruk, D. (2022) *Design Patterns in Modern C++20: Reusable
Approaches for Object-Oriented Software Design*. 2nd edn. California:
Apress. Parts I, II, and III.

## Reflection

**Understanding the purpose of behavioural patterns.** Strategy was the
one pattern this unit made genuinely hands-on, and comparing my own
implementation against two classmates' versions of the identical problem
showed how differently the same pattern can be applied while staying
correct. Joseph's version required a strategy to be set explicitly via
`set_strategy()` before use, guarded by a `ValueError` if called too
early; mine required a strategy at construction, so a `PaymentProcessor`
could never exist in an invalid state at all. Neither is simply right,
Joseph's own answer to that exact question was that requiring a strategy
at construction is generally more robust, but the optional approach earns
its place in scenarios like dynamic UI workflows, where the processor
needs to exist before a user has chosen a payment method. The other five
patterns in this unit, Observer, Chain of Responsibility, Template
Method, Command, and State, stayed conceptual here; Observer and Template
Method became genuinely hands-on later, in Units 9 and 6 respectively.

**Recognizing how behavioural patterns enable communication between
objects.** Reena's refactor used a `strategy_map` dictionary in place of
the `if`/`elif` chain. I flagged a real limitation in that approach: the
map itself still needs a new entry for every new payment type, meaning
extension still requires modification, just moved one level up rather
than eliminated. I could not find a home for the map that avoided this;
placing it in the abstract base class violates SRP, placing it in
`PaymentProcessor` violates OCP. That inconsistency mattered more later
than it did in the moment, I used the identical dictionary structure
myself in Unit 8's refactor without initially noticing the contradiction.

**Applying Strategy in a practical exercise.** The core fix was the same
across every version submitted in this discussion: extracting each
payment method into its own class behind a shared interface, so
`PaymentProcessor` never needs to change when a new payment type is
added, only a new class does.

**Analyzing real-world examples.** Joseph's version, framed around
African mobile money providers (M-Pesa, MTN MoMo), made the practical
case for Strategy concrete in a way a generic credit-card example does
not: a genuinely fragmented payment landscape is exactly the scenario
where the Open/Closed Principle earns its keep, since a new provider is
common, not exceptional, in that context.

## References

Nesteruk, D. (2022) *Design Patterns in Modern C++20: Reusable
Approaches for Object-Oriented Software Design*. 2nd edn. California:
Apress.
