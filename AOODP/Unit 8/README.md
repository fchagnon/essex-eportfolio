# Unit 8: Refactoring and Code Smells
### Collaborative Discussion
*(Formative, collaborative discussion format)*

## Task

Analyze the code smells present in a given calculate_total_price function
and refactor it.

**Original code:**

```python
def calculate_total_price(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * 0.9
        elif item['type'] == 'electronics':
            total += item['price'] * 0.8
        else:
            total += item['price']
    return total
```

## My Original Post

**Code smells identified:**

1. **Magic Numbers.** The discount multipliers 0.9 and 0.8 are hardcoded
   directly into the calculation. Eland and Smith (2023) describe this exact
   problem in their baggage-pricing example, where fee amounts appear as
   unexplained literals scattered through a method. A magic number is a
   value with no indication of what it represents or why it was chosen, so
   anyone maintaining the code later has to guess at its meaning, and every
   future change to a discount rate means hunting down and editing the raw
   number everywhere it appears.

2. **Long Method with Conditional Logic.** The if-elif-else chain packs
   every discount rule into a single function. Clausen (2021) frames this
   kind of problem as a simple, checkable rule rather than a fuzzy smell: a
   method should stay short and focused on one responsibility. As item types
   grow, this function grows right along with them, since every new discount
   rule means another branch bolted onto the same method.

**Suggested fixes:**

- **Replace Magic Numbers with Constants**: pull 0.9 and 0.8 out into
  named constants like BOOK_DISCOUNT and ELECTRONICS_DISCOUNT. This
  mirrors the "Introduce constant" refactoring Eland and Smith (2023) walk
  through, and it centralizes the pricing rules in one discoverable place.
- **Replace Conditional with Polymorphism**: give each item type its own
  discount class (e.g. BookDiscount, ElectronicsDiscount) implementing a
  shared interface. New item types can then be added without touching the
  original function at all.

## Follow-Up Post: Refactored Code

*"I hadn't thought to actually code the solutions until I saw other posts.
So here are my refactored versions."*

**Option 1: Using Constants (Simpler Approach)**

```python
BOOK_DISCOUNT = 0.9
ELECTRONICS_DISCOUNT = 0.8

def calculate_total_price(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * BOOK_DISCOUNT
        elif item['type'] == 'electronics':
            total += item['price'] * ELECTRONICS_DISCOUNT
        else:
            total += item['price']
    return total
```

This fixes the magic numbers smell directly: the discount rates are named,
defined once, and easy to find and update. It doesn't address the
long-method smell though, since the if-elif-else chain is still there,
and every new item type still means editing this function.

**Option 2: Strategy Pattern (More Scalable)**

```python
class NoDiscount:
    def apply(self, price):
        return price

class BookDiscount:
    def apply(self, price):
        return price * BOOK_DISCOUNT

class ElectronicsDiscount:
    def apply(self, price):
        return price * ELECTRONICS_DISCOUNT

DISCOUNTS = {
    'book': BookDiscount(),
    'electronics': ElectronicsDiscount()
}

def calculate_total_price(items):
    total = 0
    for item in items:
        strategy = DISCOUNTS.get(item['type'], NoDiscount())
        total += strategy.apply(item['price'])
    return total
```

This resolves both smells: the constants are named, and the conditional
chain is gone entirely. New item types are added by writing a new class and
a new dictionary entry, with zero changes to calculate_total_price itself.

For a small, stable set of item types, Option 1 is arguably easier to read
at a glance. Option 2 only pays off once pricing rules are expected to grow.

## Note on Consistency with Unit 5

It is worth flagging directly that Option 2's DISCOUNTS dictionary is
structurally the same design I raised as a concern in my Unit 5 peer reply
to Reena, a lookup map that must be manually updated whenever a new type is
added, which I argued at the time still requires modification even though
the strategy classes themselves are extension-only. Unit 8 does not resolve
that tension; it uses the pattern anyway, since for a small, stable set of
item types the practical convenience of Option 2 over Option 1 outweighs the
theoretical OCP concern. Whether that is a reasonable trade-off or a quiet
inconsistency in my own reasoning is something worth sitting with rather
than glossing over.

## References

Clausen, C. (2021) *Five Lines of Code*. Manning Publications.

Eland, M. and Smith, S. (2023) *Refactoring with C#: Safely Improve .NET
Applications and Pay down Technical Debt with Visual Studio, .NET 8, and
C# 12*. 1st edn. Birmingham: Packt Publishing.

## Reflection

*To be added.*
