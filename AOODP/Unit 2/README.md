# Unit 2: SOLID Principles of Object-Oriented Design

## Unit Topic

This unit covers the five SOLID principles, Single Responsibility,
Open/Closed, Liskov Substitution, Interface Segregation, and Dependency
Inversion, and how they combine to make object-oriented code more
maintainable, extensible, and testable. It builds directly on Unit 1's
foundational OOP concepts, moving from individual classes to how classes
should relate to one another.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain each of the five SOLID principles and their
  importance in object-oriented design.
- Apply the SOLID principles to refactor code, making it more maintainable
  and scalable.
- Recognize how SOLID principles are used in real-world systems to improve
  software design.

## Formative Assignment

Refactor a poorly designed online shopping system (cart management, total
calculation, and payment processing all handled by a single `Order`
class) to adhere to all five SOLID principles:

1. **SRP** — split `Order` into `Order` (items and totals) and
   `PaymentProcessor` (payments), so `Order` no longer handles payments.
2. **OCP** — replace the payment `if`/`elif` chain with an abstraction, so
   a new payment method no longer requires modifying existing code.
3. **LSP** — ensure every `PaymentMethod` subclass implements `pay()`
   correctly, so a new subclass like `CryptoPayment` can substitute for
   the parent without breaking anything.
4. **ISP** — keep the `PaymentMethod` interface small and focused, so no
   subclass is forced to implement a method it doesn't need.
5. **DIP** — have `Order` depend on the `PaymentMethod` abstraction
   rather than any concrete payment class.

Full code: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%202

## Reading List

Sridhar, S., Indumathi, V. and Hariharan, M. (2023) *Python Programming*.
Pearson India. Chapters 3 and 12-19.

Marcotte, C.H. and Zebdi, A. (2022) *An Atypical ASP.NET Core 6 Design
Patterns Guide: A SOLID Adventure into Architectural Principles and Design
Patterns Using .NET 6 and C# 10*. 2nd edn. Birmingham: Packt Publishing.
Sections 2-4.

## Reflection

**Understanding each principle and its importance.** Working through this
refactor made the five principles concrete rather than five separate
definitions to memorize, each one turned out to solve a specific,
nameable problem already visible in the original code: one class doing
three jobs, an `if`/`elif` chain that would need editing for every new
payment type, and the risk of a subclass being forced to fake-implement a
method that didn't apply to it. Mapping the refactoring steps to the
principles myself, before checking which was which, made the ordering
click: SRP has to come first, since separating payment logic out of
`Order` is what creates the space for an abstraction to exist at all, and
DIP has to come last, since it only makes sense once that abstraction
exists to depend on (Marcotte and Zebdi, 2022, ch.3).

**Applying SOLID to refactor code.** `CryptoPayment` was written last,
after everything else was "done," and required zero changes to any
existing class, direct proof that the refactor actually achieved OCP
rather than just describing it.

**Recognizing SOLID in real-world systems.** This principle resurfaced
throughout the rest of the module in different forms: Unit 9's
`ProductRepository` is the same Dependency Inversion reasoning applied to
storage instead of payments, and Unit 6's private lock inside
`BankAccount` is the same Single Responsibility instinct applied to
concurrency. SOLID here wasn't a one-off exercise, it became a lens
carried into every later design decision.
