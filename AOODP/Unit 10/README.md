# Unit 10: Test-Driven Development (TDD) and Behaviour Driven Development (BDD)

## Unit Topic

This unit covers Test-Driven Development, writing tests before
implementation, and unit testing more broadly, applied hands-on by
designing, implementing, and testing a secure e-learning platform module
using Python's `Protocol` for structural typing and the Decorator pattern
for cross-cutting concerns.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the principles of Test-Driven Development (TDD)
  and its benefits.
- Recognize the importance of unit testing in ensuring code quality and
  reducing bugs.
- Apply TDD principles to write test cases and develop a software
  component.
- Reflect on how TDD and unit testing can improve the quality and
  maintainability of code.

## Formative Assignment

Design, implement, and test a secure e-learning platform module using
object-oriented architecture and TDD:

1. **Architecture** — choose and justify a style (layered, microservices,
   or monolithic) against scalability, maintainability, and security.
2. **Implementation** — build at least one module (implemented here as
   assignment submission handling) using TDD, tests written before the
   functionality they verify.
3. **Testing** — unit tests for all public methods, refactored based on
   results.

Full code: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%2010

## Reading List

Tibi, A. (2022) *Pragmatic Test-Driven Development in C# and .NET: Write
Loosely Coupled, Documented, and High-Quality Code with DDD Using
Familiar Tools and Libraries*. 1st edn. Birmingham: Packt Publishing.
Chapters 1-5.

Agbla, E.A. (2024) *Mastering Angular Test-Driven Development: Build
High-Quality Angular Apps with Step-by-Step Instructions and Practical
Examples*. 1st edn. Birmingham: Packt Publishing. Chapter 1 Part 1 and
Chapter 3 Part 2.

Lu, Q. et al. (2024) *Responsible AI Pattern Catalogue: A Collection of
Best Practices for AI Governance and Engineering*. ACM Computing Surveys,
56(7).

Lu, Q. et al. (2022) *Responsible-AI-by-Design: A Pattern Collection for
Designing Responsible AI Systems*. arXiv preprint.

## Reflection

**Understanding TDD principles.** A test double, specifically a mock, is
an object that stands in for a real dependency and records how it was
used so a test can later assert against that (Tibi, 2022, ch.4). Writing
`SubmitAssignmentAction`'s tests before its implementation meant the
interface had to be decided first: what would the action need injected,
and what would count as success or failure, before any of the actual
logic existed to answer those questions.

**Recognizing the importance of unit testing.** Running the full suite
with `unittest discover` surfaced a genuine issue rather than a clean
pass: an earlier test file called `SubmitAssignmentAction()` without the
`repository` argument its constructor had since come to require, a
leftover from before dependency injection was introduced into the class.
The fix was injecting `Mock()` in its place, since the test's own
validation logic raises before the repository is ever touched. That is
precisely what a test suite is supposed to catch, an interface changing
without every dependent test being updated to match, and it would have
gone unnoticed without actually running the whole suite rather than just
the newest file.

**Applying TDD to develop a component.** `SubmissionRepository` is
defined as a `typing.Protocol` rather than an `ABC`: a class can satisfy
it without ever importing or inheriting from it, satisfying a contract by
accident of shape rather than by agreement. That decoupling is what makes
conjuring up a fake repository for a test require no boilerplate at all,
directly enabling the mock-based tests built around it. `LoggingDecorator`
was developed the same way, wrapping `Action` with audit logging and
tested using a mocked inner action, verifying both the success path and
that a failure is logged and still re-raised, rather than silently
swallowed.

**Reflecting on TDD's effect on quality and maintainability.** The
discipline of writing the test first didn't just catch the constructor
bug after the fact, it's the reason the bug was even discoverable: a
codebase without tests covering `SubmitAssignmentAction` would have
carried that broken constructor call indefinitely, since nothing would
ever have exercised it.
