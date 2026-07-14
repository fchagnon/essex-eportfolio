"""
Unit 8: Code Smells and Refactoring — 'After' version.

Refactors the original if/elif discount logic using the Strategy
pattern. Each discount rule is now its own class implementing a
common `apply(price)` interface, and item types are mapped to their
strategy via the DISCOUNTS dictionary.

This addresses the code smell in the original version:
- Adding a new item type/discount no longer requires modifying
  calculate_total_price(); a new strategy class is added and
  registered in DISCOUNTS instead (Open/Closed Principle).
- Each discount rule is self-contained and independently testable.
- The lookup replaces a growing if/elif chain with a single
  dictionary access.
"""

class NoDiscount:
    # Fallback strategy: applies no discount, returns price unchanged.
    def apply(self, price):
        return price

class BookDiscount:
    # Discount strategy for books, applying BOOK_DISCOUNT.
    def apply(self, price):
        return price * BOOK_DISCOUNT

class ElectronicsDiscount:
    # Discount strategy for electronics, applying ELECTRONICS_DISCOUNT.
    def apply(self, price):
        return price * ELECTRONICS_DISCOUNT

# Maps item type strings to their corresponding discount strategy
# instance. New item types can be supported by adding an entry here
# and a matching strategy class, without touching
# calculate_total_price().
DISCOUNTS = {
    'book': BookDiscount(),
    'electronics': ElectronicsDiscount()
}

def calculate_total_price(items):
    """ Calculate the total price of a list of items using the Strategy
    pattern to apply type-based discounts.

    Args:
        items (list[dict]): Each item is expected to have a 'type'
            key (e.g. 'book', 'electronics') and a 'price' key.

    Returns:
        float: The total price after strategy-based discounts are
            applied to each item.  """

    total = 0
    for item in items:
        # Look up the appropriate strategy for this item's type,
        # defaulting to NoDiscount if the type isn't registered.
        strategy = DISCOUNTS.get(item['type'], NoDiscount())
        total += strategy.apply(item['price'])
    return total
