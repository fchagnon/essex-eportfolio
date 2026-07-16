# Unit 10: TDD-Driven Secure E-Learning Module

## Overview

This unit implements a small slice of a secure e-learning platform using
Test-Driven Development. The brief asked for at least one module built
test-first, with unit tests covering all public methods, refactored based
on results. The module built here is assignment submission, using the
Decorator pattern to add security and audit logging without modifying the
core business logic.

## Architecture Style

The system uses a **layered architecture** rather than microservices.

At this scale, a coursework-sized system with no independent scaling needs
and no separate teams, the operational overhead of network boundaries
between services would introduce coupling risk (implicit contracts between
services, harder-to-trace failures) without a corresponding benefit.
Splitting a system into independently deployed services only pays off once
release cadence, team ownership, or scaling needs actually diverge; absent
those pressures, it adds surface area for silent breakage rather than
reducing it.

Within that layered structure, identity and access management (IDAM) is
treated as an external, already-solved concern. The system consumes a
verified identity (a user ID and associated claims or token) and is
responsible only for authorization: mapping an authenticated identity to
entitlements within this system's own domain (is this user a student or
instructor, what actions can they perform, are they enrolled in the
relevant course). Authentication and authorization are kept as distinct
responsibilities, which avoids a single User class that conflates a
security boundary with a domain entity.

## Core Design: Actions, Context, and Decorators

### The problem being solved

Actions in this system (submitting an assignment, updating a grade, and
others not yet built) share a repeating shape: checks that need to happen
before the core logic runs (is the user authenticated, are they entitled to
do this, is the input valid), the core logic itself, and side effects that
need to happen after (logging, notification).

Writing these checks directly inside each action method creates two
problems as the system grows. First, every new cross-cutting rule (a new
security check, a new notification requirement) means editing every
existing action method individually, which does not scale cleanly as the
number of actions and concerns grows. Second, and more importantly for a
TDD-focused unit, it makes it impossible to test an action's core logic in
isolation without dragging in unrelated concerns like logging.

### The solution

**`Action`** (`actions.py`) is an abstract base class with a single method,
`execute(context)`. Every action in the system, and every decorator, shares
this interface, which is what makes the design composable.

**`ActionContext`** (`actions.py`) is the object passed through every
action and decorator call. It is split into two parts:

- **Header fields** (`correlation_id`, `user_id`): common metadata that any
  decorator can read regardless of which action is running, without
  needing to understand what that action actually does. This mirrors a
  network packet header: consistent structure regardless of payload,
  readable by any layer without unpacking the contents.
- **Payload**: action-specific data (for `SubmitAssignmentAction`, this is
  the assignment ID, student ID, file content, and comments). The payload
  is deliberately typed loosely (`Any`) at the `ActionContext` level and
  treated as opaque by every decorator. Only the concrete action that owns
  a given payload type narrows it back to something concrete, using a type
  hint assignment at the start of `execute()`. This preserves a single,
  reusable interface for every decorator while still giving the action
  itself full static-typing support inside its own method body.

A generic wrapper (for example, `ActionContext[TPayload]`) was considered
and rejected. Making the context generic would force `Action.execute()` to
become generic as well, which in turn forces any general-purpose decorator
(one meant to wrap *any* action) to fall back to `Action[Any]` to remain
reusable. At that point the same lack of compile-time safety as the plain
`Any` approach is reached anyway, with more syntax and no actual benefit.

**`SubmitAssignmentAction`** (`actions.py`) is the first concrete action.
It depends on a `SubmissionRepository` (a `Protocol`, not a concrete class)
for persistence, injected through its constructor. This keeps the action
decoupled from any specific storage mechanism and testable without a real
database.

**`LoggingDecorator`** (`decorators.py`) wraps any `Action`. It logs before
and after the wrapped action's `execute()` call, and specifically logs a
failure case (catching the exception, logging it, then re-raising) so that
the wrapped action's exception contract is completely unchanged for
callers, while still producing an audit trail even when the wrapped action
fails. Because `LoggingDecorator` itself implements `Action`, decorators
can wrap other decorators, which is what allows multiple concerns (logging,
and in future work, authorization) to be composed around the same core
action without either one being aware of the other.

## Why Decorator

The brief's security requirement and the general need for audit logging
share the same shape described above: behavior that must run around a core
action without the core action knowing about it. Decorator was chosen over
handling this with hardcoded calls inside each action method specifically
because it keeps every concern testable in isolation and reusable across
every current and future action, without editing existing code each time a
new concern is added.

## Test-Driven Development Process

Development followed red-green-refactor throughout. `SubmitAssignmentAction`
was tested before `LoggingDecorator`, since it has no dependency on
anything else in the system, while a decorator by definition needs
something to wrap.

Tests were added in order of increasing complexity:

1. `test_execute_missing_file_content_raises_value_error`: the cheapest
   possible failure to check, rejecting invalid input before any
   persistence logic is reached.
2. `test_execute_empty_assignment_id_raises_value_error`: a parametrized
   test (using `subTest`) covering `None`, empty string, and
   whitespace-only input in a single test method, since all three
   represent the same underlying validation failure.
3. `test_execute_valid_payload_saves_submission_to_repository`: the happy
   path, verifying the action actually persists a correctly constructed
   `Submission` object, using a `Mock` in place of a real repository.
4. Two tests for `LoggingDecorator`: one confirming the wrapped action is
   actually called (delegation), and one confirming that an exception
   raised by the wrapped action still propagates out to the caller
   unchanged (transparency on failure).

Adding the `SubmissionRepository` dependency to `SubmitAssignmentAction`'s
constructor partway through development broke the two existing validation
tests, since they had been constructing the action with no arguments. This
was caught immediately by running the test suite after the change, before
any further work was done, and fixed by introducing a `DummySubmissionRepository`
test double (a double that does nothing, since those two tests never reach
the persistence step). This is included here deliberately, since it is a
real example of TDD catching the consequence of a design change
immediately rather than silently.

## Known Gaps and Deliberate Scope Decisions

- **`student_id` is not independently validated.** `ActionContext` already
  carries `user_id` in its header, which is typically the same person
  submitting an assignment. `student_id` in the payload exists to support
  administrative overrides (for example, an instructor submitting on
  behalf of a student who had technical issues), which makes it partially
  redundant with `user_id` on the direct-submission path. This redundancy,
  and the question of what happens if the two disagree, is a data
  integrity question not resolved in this iteration.
- **Only one decorator (`LoggingDecorator`) is implemented.** An
  authorization/entitlement decorator was designed conceptually (checking
  role and course enrollment before allowing an action to proceed) but not
  built, given time constraints. The `Action` interface and `ActionContext`
  header were deliberately shaped to support adding it later without
  restructuring existing code.
- **Persistence is not implemented.** `SubmissionRepository` is defined as
  a `Protocol` with a single `save()` method; no concrete implementation
  (database, file system) exists. This keeps the module testable without
  external dependencies, consistent with the Repository pattern used in
  Unit 9.

## Reflection

This module has seriously challenged me and stretched my understanding and
appreciation for software architecture and engineering. I understood
classes, but this formative exercise had me making classes that would be
used to wrap, and call, other classes. I'm increasingly appreciative of the
fact that object-oriented programming is all about building blocks and
puzzle pieces, and that UML diagrams, which I thought were a learning aid,
are blueprints for good design work.

## Files

- `actions.py`: `Action`, `ActionContext`, `Submission`,
  `SubmissionRepository`, `SubmitAssignmentAction`
- `decorators.py`: `LoggingDecorator`
- `test_submit_assignment.py`: tests for `SubmitAssignmentAction`
- `test_decorators.py`: tests for `LoggingDecorator`
