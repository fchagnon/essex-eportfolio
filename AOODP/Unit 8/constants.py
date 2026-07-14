"""
Unit 8: Code Smells and Refactoring — 'Before' version.

This function calculates the total price of a shopping cart, applying
different discounts based on item type. It demonstrates a classic
conditional/switch-statement code smell: as new item categories are
added, this function must be modified directly, violating the
Open/Closed Principle (OCP)-- code should be open for extension but
closed for modification.

Other "smells" present (still getting used to that term)
- "Magic numbers" ( a.k.a hardcoded constants) BOOK_DISCOUNT, 
  ELECTRONICS_DISCOUNT are hardcoded at module level rather than 
  being associated with their relevant discount behaviour.

- Adding a new item type means editing this function's if/elif chain,
  rather than adding a new self-contained class
"""

BOOK_DISCOUNT = 0.9
ELECTRONICS_DISCOUNT = 0.8

def calculate_total_price(items):
    """
    Calculate the total price of a list of items, applying a discount
    based on item type.

    Args:
        items (list[dict]): Each item is expected to have a 'type'
            key (e.g. 'book', 'electronics') and a 'price' key.

    Returns:
        float: The total price after type-based discounts are applied.

    Smell:
        This if/elif chain grows every time a new item type or
        discount rule is introduced, coupling pricing logic to type
        checks instead of encapsulating each pricing rule behind its
        own strategy/class.
    """
    total = 0
    for item in items:
        if item['type'] == 'book':
            # Books get a 10% discount
            total += item['price'] * BOOK_DISCOUNT
        elif item['type'] == 'electronics':
            # Electronics get a 20% discount
            total += item['price'] * ELECTRONICS_DISCOUNT
        else:
            # No discount for unrecognised item types
            total += item['price']
    return total
