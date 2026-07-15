# Unit 1: Introduction and Recap of Object-Oriented Programming (OOP)

Programming exercises covering Classes, Objects, Access Control, Inheritance,
Polymorphism, Abstraction, and Encapsulation.

## Tasks

### Task 1: Basic Class Hierarchy (Inheritance)
- Define a base class `Vehicle` with `brand` and `fuel_type` as instance attributes (`__init__`).
- Create a subclass `Car` that inherits from `Vehicle` and adds `num_doors`.
- `Car` calls the parent class's `__init__` via `super()`.

### Task 2: Polymorphism with Methods
- Define an abstract `Shape` class with an abstract method `area()` (`ABC`, `abstractmethod`).
- Create `Circle` and `Rectangle` subclasses inheriting from `Shape`.
- Implement `area()` in each (`Circle`: πr²; `Rectangle`: length × width).

### Task 3: Encapsulation with Access Control
- Define `BankAccount` with a private attribute `__balance` (double underscore).
- Public methods:
  - `deposit(amount)` — adds to `__balance`.
  - `withdraw(amount)` — deducts from `__balance`, checking for sufficient funds.
- Getter method `get_balance()` for read access.

### Task 4: Abstraction with Base Class
- Create an abstract `Animal` class with an abstract method `make_sound()`.
- Implement `Dog` and `Cat` subclasses, overriding `make_sound()` to return
  `"Woof!"` and `"Meow!"` respectively.
- Use `ABC` and `abstractmethod`.

### Task 5: Constructor and Destructor
- Define a `Person` class with `__init__(self, name)`.
- Add a destructor `__del__(self)` printing a farewell message
  (e.g. `"Goodbye, {name}!"`).
- Test by creating and deleting an instance (`del` explicitly, or letting it
  go out of scope).

## Artefacts

All five tasks implemented and tested with inline demos.

- **`task1_inheritance.py`** — `Vehicle` base class with `brand`/`fuel_type`;
  `Car` subclass adds `num_doors` and calls `super().__init__()`. Demo confirms
  inheritance via `isinstance()`.
- **`task2_polymorphism.py`** — Abstract `Shape` class (`ABC`, `@abstractmethod`
  `area()`); `Circle` and `Rectangle` subclasses implement `area()` independently.
  Demo iterates a mixed list of shapes calling `area()` polymorphically, and
  confirms `Shape` itself cannot be instantiated directly.
- **`task3_encapsulation.py`** — `BankAccount` with private `__balance`
  (name-mangled to `_BankAccount__balance`); `deposit()`/`withdraw()` enforce
  validation (positive amounts, sufficient funds) as the only access path.
  Demo explicitly shows direct external access failing, and the mangled name
  as the (not-recommended) underlying mechanism.
- **`task4_abstraction.py`** — Abstract `Animal` class with abstract
  `make_sound()` and a concrete inherited `describe()` method; `Dog`/`Cat`
  subclasses implement `make_sound()`. Demonstrates mixing abstract and
  concrete methods on the same base class.
- **`task5_constructor_destructor.py`** — `Person` class with `__init__`
  and `__del__`. Demo covers four scenarios: explicit `del`, scope exit,
  multiple references (deletion only firing on the last reference), and
  interpreter shutdown cleanup.

## How Each Concept Was Applied

- **Inheritance** (Task 1) — `Car(Vehicle)` demonstrates that a subclass gains
  everything the parent defines, provided `super().__init__()` is called;
  without it, `self.brand`/`self.fuel_type` would never be set on a `Car`
  instance, and accessing them would raise an `AttributeError`.
- **Polymorphism** (Task 2) — `Circle` and `Rectangle` both implement `area()`
  with completely different formulas, but calling code (the loop over
  `shapes`) never branches on type — it calls `.area()` uniformly and Python
  dispatches to the correct implementation automatically.
- **Encapsulation** (Task 3) — `__balance`'s name-mangling
  (`_BankAccount__balance`) is Python's mechanism for signalling "don't touch
  this directly," enforced by convention rather than a hard language lock.
  All reads/writes are forced through `deposit()`/`withdraw()`/`get_balance()`,
  so validation rules (no negative deposits, no overdrafts) live in exactly
  one place.
- **Abstraction** (Task 4) — `Animal` mixes an abstract method
  (`make_sound()`, no implementation, contract only) with a concrete method
  (`describe()`, fully implemented and inherited as-is). This distinguishes
  abstraction (defining *what* must exist) from polymorphism (Task 2's focus
  on *how* the same call produces different results).
- **Constructors/Destructors** (Task 5) — `Person.__del__` demonstrates
  Python's reference-counting model directly: Test 3 shows that `del` on one
  of two variables pointing to the same object does *not* trigger `__del__`,
  since a reference still exists; only removing the last reference does.

## Reflection

This unit was a refresher on OO concepts I hadn't had to actively think about
since the early 2000s. Back then, I was studying OOP as part of a Computer
Science undergraduate degree, and using object-oriented Perl professionally
to build the back-end of a virtual hosting platform for an internet service
provider. By the mid-2000s, my career shifted away from development and into
networks, security, and infrastructure, and my software engineering skills
went largely unused for close to two decades. This unit was the first thing
to genuinely shake the rust off — concepts like inheritance, encapsulation,
and abstraction were familiar in outline, but writing them again from
scratch, in a language I hadn't used for this purpose before, made clear how
much had gone dormant rather than been forgotten outright.
