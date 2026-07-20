# Unit 8: Refactoring and Code Smells

## Unit Topic

This unit covers code smells and refactoring techniques for maintaining
clean, readable, sustainable code, applied hands-on to a
`calculate_total_price` function containing two classic smells.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain what code smells are and how to detect them in a
  codebase.
- Apply refactoring techniques to improve code maintainability and
  readability.
- Refactor an existing codebase to eliminate code smells, using
  object-oriented principles.
- Recognize the importance of refactoring in maintaining high-quality,
  sustainable software systems.

## Formative Assignment

*(Formative, collaborative discussion format)*

Identify at least two code smells in a `calculate_total_price` function
and refactor it:

```python
def calculate_total_price(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * 0.9 # 10% discount for books
        elif item['type'] == 'electronics':
            total += item['price'] * 0.8 # 20% discount for electronics
        else:
            total += item['price']
    return total
```

Full post: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%208

## Reading List

Clausen, C. (2021) *Five Lines of Code*. Manning Publications. Chapters
1 and 2.

Eland, M. and Smith, S. (2023) *Refactoring with C#: Safely Improve .NET
Applications and Pay Down Technical Debt with Visual Studio, .NET 8, and
C# 12*. 1st edn. Birmingham: Packt Publishing. Chapters 1-5, 6, 7, and 9.

Alls, J. (2023) *Clean Code with C#: Refactor Your Legacy C# Code Base
and Improve Application Performance Using Best Practices*. 2nd edn.
Birmingham: Packt Publishing. Chapters 1, 6, 11, and 14.

## Reflection

I hadn't thought to actually code the solutions until I saw other posts,
so my own follow-up produced two versions: a simpler constants-only fix,
and a Strategy pattern refactor.

**Understanding and detecting code smells.** Two smells stood out: magic
numbers (`0.9` and `0.8` hardcoded directly into the calculation, Eland
and Smith, 2023) and a long method with conditional logic, where every
new discount rule means another branch bolted onto the same function
(Clausen, 2021).

**Applying refactoring techniques.** The constants-only version fixes the
magic-numbers smell directly but leaves the conditional chain untouched.
The Strategy version resolves both: the conditional disappears entirely,
and a new item type is added by writing a new class and a new dictionary
entry, with zero changes to `calculate_total_price` itself.

**Refactoring using object-oriented principles.** Peer discussion
surfaced a genuine design question I hadn't fully settled on my own.
Replying to Amnon's version, I asked directly whether a two-category
system actually warrants a full Strategy abstraction at all, whether the
pattern was earning its keep or solving a problem the code didn't yet
have, since Eland and Smith (2023) caution that more abstraction doesn't
always mean more maintainable for a small, stable domain. Replying to
Elvira's version, a different design question emerged: her approach
attached the discount object to each `Item` at construction time, rather
than looking it up by a type string inside `calculate_total_price`. Both
eliminate the conditional, but they disagree on *who owns* the
type-to-discount mapping, the item itself, or a central lookup. Neither
is simply correct; it depends on where in the system that information is
naturally already known.

**Recognizing the importance of refactoring.** The real lesson from this
unit wasn't any single refactor, it was that the same pattern can be
applied several genuinely different ways, and the right one depends on
projected growth and where responsibility naturally belongs, not on which
version looks the most "designed."
