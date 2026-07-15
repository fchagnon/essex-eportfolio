# ShopEase — Design Rationale
### Unit 9 Artefact — Design Decisions Derived from the Brief's Five Requirements

This document traces each of the brief's five stated requirements to the specific
design decision it forced, and the specific class(es) in the accompanying UML
diagram (`shopease_uml.png` / `.pdf`) that decision produced. Two additional
patterns — Abstract Factory and Visitor — were layered on top of the brief's own
requirements, for reasons explained in their own section at the end.

The diagram is colour-coded to match the groupings this document arrives at:

| Colour | Group |
|---|---|
| Yellow | Domain Model (`User`, `Product`, `Order`) |
| Blue | Data Access Layer |
| Green | Business Logic Layer |
| Orange | Observer (Notifications) |
| Purple | Abstract Factory (Payment) |
| Pink | Visitor (Reporting) |

---

## 1. Scalability

**Brief requirement:** *"The system should handle a growing number of users and products."*

**What the requirement forces.** A growing number of users and products will
eventually hit a capacity or performance ceiling on whatever underlying storage
is used. Resolving that, in infrastructure terms, means being able to swap or
scale the storage mechanism (e.g. moving to a distributed database) without
that change rippling into the rest of the system.

**Design choice made.** Business logic classes (`ProductCatalog`,
`OrderProcessor`) never talk to a specific storage technology directly.
Instead, they depend only on an interface — a contract specifying operations
like `get`, `save`, `all` — without knowing or caring how those operations are
actually carried out underneath. The storage implementation is handed in from
outside at construction time (Dependency Injection), rather than created
internally, so swapping it later touches zero lines inside the classes that
use it.

**Resulting diagram element(s).** `ProductRepository` and `OrderRepository`,
drawn as `<<interface>>` classes, with `InMemoryProductRepository` /
`InMemoryOrderRepository` as concrete implementations connected via an
"implements" (dashed hollow-triangle) relationship. This is the **Repository
pattern**.

---

## 2. Modularity

**Brief requirement:** *"The system should be divided into independent modules
(e.g., user management, product catalogue, order processing)."*

**What the requirement forces.** "Independent modules" means classes should
hold no direct knowledge of each other. Removing or replacing one class
shouldn't ripple into others. But something, somewhere, has to connect them —
otherwise the system never actually does anything.

**Design choice made.** `UserManager`, `ProductCatalog`, and `OrderProcessor`
never reference each other directly, and never appear in one another's
constructors. `Order` is the deliberate exception and connecting point — its
entire purpose is to hold a `User` and a set of `Product`s together, so that
`UserManager` and `ProductCatalog` never need to know about each other. All
wiring — looking up a user, looking up products, assembling them into an
`Order`, handing that `Order` to `OrderProcessor` — happens in a single
separate place: the **composition root** (`main.py`), the one part of the
system deliberately allowed to know about everything.

**Resulting diagram element(s).** No direct arrows exist between
`UserManager`, `ProductCatalog`, and `OrderProcessor` — that absence of a
connection *is* the design decision. `main.py` isn't drawn in the class
diagram at all, since it isn't a class; it's the runtime wiring that sits
outside the diagram entirely.

---

## 3. Security

**Brief requirement:** *"The system must protect user data and transactions."*

**What the requirement forces.** This splits into two genuinely different
problems: protecting login credentials, and protecting payment/card data. Each
has a different correct solution.

**Design choice made — credentials.** Following the Unit 7 authentication
work, `User` holds a hashed password (via bcrypt), never plaintext.
`UserManager.register()` is responsible for taking a raw password in, hashing
it, and storing only the hash — mirroring the NIST-aligned policy and
rate-limiting logic already built in that artefact.

**Design choice made — payment data.** ShopEase's own code never receives or
stores raw card details at all. `PaymentGateway.charge(amount)` and
`RefundHandler.refund(amount)` only ever take a monetary amount as a
parameter — card capture and validation happen entirely inside Stripe/PayPal's
own systems, outside anything this project has written. This keeps ShopEase
outside PCI-DSS's stricter obligations by design, rather than by later
hardening.

**Resulting diagram element(s).** Security isn't drawn as its own box or
arrow — it shows up as an absence: no method signature anywhere accepts card
details, and `User`'s password field is implied to be a hash, not raw text.

---

## 4. Extensibility

**Brief requirement:** *"The system should allow for easy addition of new
features (e.g., payment methods, recommendation engines)."*

**What the requirement forces.** Adding or removing a payment provider
shouldn't require editing `OrderProcessor`'s own code (the same ripple-effect
problem as Modularity and Scalability). Additionally, a payment provider isn't
one capability but two — charging and refunding — and those two must never be
mismatched (e.g. a Stripe charge paired with a PayPal refund).

**Design choice made.** Rather than injecting a gateway and refund handler as
two independent objects (which relies on whoever wires the system remembering
they must match), a single factory object is injected instead. Each concrete
factory (`StripeProviderFactory`, `PayPalProviderFactory`) is responsible for
producing a matched gateway/refund-handler pair from the same provider, by
construction — mismatching becomes structurally impossible rather than merely
a discipline the wiring code has to maintain.

**Resulting diagram element(s).** `PaymentProviderFactory` as an
`<<interface>>`, with `StripeProviderFactory` / `PayPalProviderFactory`
implementing it, and dashed "creates" arrows from each factory to its own
matching `Gateway`/`RefundHandler` pair. `OrderProcessor` depends only on the
abstract `PaymentProviderFactory`, never on Stripe or PayPal by name. This is
the **Abstract Factory pattern**.

---

## 5. Layered Architecture (and the Decoupling Principle Underlying It)

**Brief requirement:** *"Object-Oriented Architecture Design... layered
architecture with Presentation, Business Logic, and Data Access layers."*
Guidance also specifically calls out Dependency Injection and the Observer
Pattern for notifications.

**Observer (notifications), derived alongside this requirement.** `OrderProcessor`
shouldn't need to know the specific list of notification channels, or edit
itself every time that list changes. It holds a generic list of observers,
each satisfying the same `OrderObserver` interface (`update(order, event)`).
It announces events without knowing who's listening or how many.
`EmailNotifier` and `SMSNotifier` are two current implementations; adding a
third requires only writing a new class and appending it to the list, with
zero changes to `OrderProcessor`.

**What "layering" actually means.** Not three rigid physical boxes, but a name
for a specific, deliberate application of a single underlying principle:
**decoupling** — keeping two classes structurally apart so that changing one
(swapping storage, swapping a payment provider, adding a notification channel)
never forces a change in the other. Every mechanism derived above — Repository,
the composition root, Abstract Factory, Observer — is a separate instance of
the same rule. "Layers" is simply the name for grouping these decoupled
relationships into broad categories: Data Access, Business Logic, and the
boundary with the outside world (payments, notifications).

**Resulting diagram element(s).** The diagram's colour groups are the visual
expression of this grouping. Every dashed "implements" arrow and every solid
"uses/depends on" arrow is a point of deliberate decoupling — the arrows exist
precisely so two classes never need direct knowledge of each other's concrete
type.

---

## Patterns Added Beyond the Brief

The brief's own five requirements, worked through above, produce four
mechanisms: Repository, the composition root, Abstract Factory, and Observer.
Two further patterns were deliberately layered on top, for portfolio reasons
rather than because Unit 9 asked for them:

**Abstract Factory** — as it happens, this one is also a legitimate answer to
the brief's own Extensibility requirement (see Section 4), so its inclusion is
justified by the brief itself, not only by portfolio need.

**Visitor** (`ReportVisitor`, `SalesReportVisitor`, `InventoryReportVisitor`) —
this one is **not** requested anywhere in the brief. It was added purely
because the EMA's Task 2 explicitly requires a Visitor artefact, and no other
unit's work provides one. The justification used is that a real store would
plausibly want sales and inventory reports without cluttering `Product`/`Order`
themselves with reporting logic unrelated to what a product or order *is* —
a reasonable design choice on its own merits, but one motivated by portfolio
completeness rather than the Unit 9 brief.

---

## Summary Table

| Requirement | Mechanism | Pattern Name | Diagram Colour |
|---|---|---|---|
| Scalability | Swappable storage behind an interface | Repository | Blue |
| Modularity | No cross-knowledge between business logic classes; wiring isolated in `main.py` | Composition Root | (unshown — outside diagram) |
| Security | Hashed credentials; card data never touched by our code | — | (shown as absence) |
| Extensibility | Matched provider pairs from one factory | Abstract Factory | Purple |
| Layering / DI / Notifications | Generic observer list; decoupling as the unifying principle | Observer | Orange |
| *(portfolio addition)* | Reporting logic separated from domain objects | Visitor | Pink |
