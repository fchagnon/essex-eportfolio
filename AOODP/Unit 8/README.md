# Unit 8 Collaborative Discussion: Code Smells and Refactoring

This formative Collaborative Discussion starts and ends in this unit week.

Analyse the provided code snippet and identify areas where refactoring can improve code maintainability and readability.

## Discussion Tasks

### Identify at least two code smells in the provided code

1. **Magic Numbers**
   - Hardcoded discounts (`0.9`, `0.8`) reduce readability and maintainability.
   - Problem: Changing discounts requires modifying the function directly.

2. **Long Method with Conditional Logic**
   - The if-elif-else chain handles multiple discount rules in one place.
   - Problem: Adding new item types or discount rules bloats the function.

### Suggested Refactoring Techniques

- **Replace Magic Numbers with Constants**
  - Define discount factors as named constants (e.g., `BOOK_DISCOUNT = 0.9`).

- **Replace Conditional with Polymorphism (Strategy Pattern)**
  - Encapsulate discount rules in separate classes (e.g., `BookDiscount`, `ElectronicsDiscount`).

### Refactored Code Structure

- **Option 1:** Using Constants (Simpler Approach).
- **Option 2:** Strategy Pattern (More Scalable).

## Code Snippet

```
def calculate_total_price(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * 0.9  # 10% discount for books
        elif item['type'] == 'electronics':
            total += item['price'] * 0.8  # 20% discount for electronics
        else:
            total += item['price']
    return total
```
