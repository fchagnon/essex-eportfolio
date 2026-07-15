# Unit 3: Design Patterns I: Creational Patterns
### Implementing the Factory Method Pattern
*(Formative, not assessed; submitted, no tutor feedback received)*

## Task

Design a system for a car manufacturer producing different car types, using
the Factory Method Pattern so the main program can create cars without
specifying their exact class.

Required:
- A `Car` interface/abstract class with `drive()`
- Concrete car classes implementing `Car`
- A `CarFactory` abstract class with factory method `create_car()`
- Concrete factories overriding `create_car()`
- A demonstration of the pattern in use

## Artefact

`unit3.py`: implemented with real Toyota models instead of the generic
Sedan/SUV/Hatchback naming suggested by the brief: `CorollaCross`, `RAV4`,
`PriusC`, each a concrete `Car` subclass implementing `drive()`, paired with
matching `CorollaCrossFactory`, `RAV4Factory`, `PriusCFactory` classes
implementing `create_car()`.

The demonstration is framed around a personal scenario: modeling an actual
garage of vehicles as factories, with two use cases:
1. **Any available car will do**: the factory is resolved generically
   (`next(iter(garage.values()))`), with the caller never specifying which
   concrete car type it receives.
2. **A specific car is required for the task**: `RAV4Factory()` is requested
   by name, since hauling mountain bikes specifically needs the RAV4's cargo
   capacity, illustrating that the pattern doesn't prevent requesting a
   specific type when the use case genuinely demands it, it just removes
   the *need* to hardcode that choice everywhere else.

## Factory Method vs. Abstract Factory: the distinction this artefact shows

This is worth stating explicitly, since both patterns appear in this
portfolio (Abstract Factory in the Unit 9 ShopEase payment system) and
they're easy to conflate:

- **Factory Method** (this artefact): each factory produces **one kind of
  product**: `CorollaCrossFactory` only ever makes a `CorollaCross`. The
  pattern's value is letting client code (`client_code(factory)`) depend on
  the abstract `CarFactory`/`Car` interfaces only, never a concrete car class.
- **Abstract Factory** (Unit 9): each factory produces a **matched family of
  related products**: `StripeProviderFactory` produces both a gateway *and*
  a refund handler that must always come from the same provider. The
  extra structure exists specifically to prevent mismatched combinations,
  a concern that doesn't arise when a factory only ever makes one thing.

## Reflection

*Awaiting, Fred to provide.*
