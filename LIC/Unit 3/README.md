# Unit 3: Principles of Computer Science

## Unit Topic

This unit covers algorithms, data structures, and computational
complexity, the step-by-step logic behind problem-solving in computing,
and how Big-O notation is used to evaluate algorithmic efficiency at
scale.

## Learning Outcomes

On completion of this unit, I should be able to:

- Identify and analyze key principles of algorithms and data structures.
- Gather and synthesize information to apply computational principles to
  business challenges.
- Evaluate the efficiency and suitability of algorithms and data
  structures for specific computing problems.

## Formative Assignment

Implement a sorting algorithm, analyze its time complexity in Big-O
notation, and compare it against another algorithm solving the same
problem, submitted as code, a performance graph, and a 300-word report.

Full submission: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%203

## Reading List

Walton, D.J. (2024) *Culturally Responsive Computing: An Introduction
into Computer Science, Security, and Technology*. Boston, MA: ROTEL.
Chapters 3 and 5.

## Reflection

**Identifying key principles of algorithms.** Bubble Sort's *O(n²)*
comparisons happen regardless of the data's initial state unless
optimised with a swap flag for early termination, which our benchmarks
deliberately did not employ, so the worst case was allowed to actually
manifest rather than being masked by an optimization. Quick Sort's *O(n
log n)* complexity, by contrast, comes from partitioning data around a
pivot rather than exhaustive pairwise comparison, a structurally
different approach to the same problem, not just a faster version of the
same idea.

**Gathering and synthesising information to apply computational
principles.** The most interesting finding came from testing an
assumption rather than confirming one: sorting a reverse-sorted list,
Bubble Sort's theoretical worst case, was empirically *faster* than
sorting random data. This is best explained by branch prediction
(Hennessy and Patterson, 2017): a reverse-sorted list keeps the swap
condition consistently true, letting the CPU maintain a steady
instruction prediction pipeline, while random data causes frequent
pipeline flushes from incorrectly predicted branches. That's a real
hardware effect Big-O notation alone doesn't capture, since Big-O
describes the algorithm in the abstract, not its behavior on actual
silicon.

**Evaluating efficiency and suitability.** At 100,000 integers, Quick
Sort outperformed Bubble Sort by several orders of magnitude, and
Python's native Timsort outperformed our own Quick Sort implementation
by a similar margin again, not because Timsort is asymptotically
superior (it shares Quick Sort's *O(n log n)* complexity), but because it
runs as compiled C rather than interpreted Python. That's the same
lesson as the branch-prediction finding from a different angle:
theoretical complexity tells you how an algorithm scales, not how fast it
actually runs, real-world performance depends heavily on implementation
and hardware, not algorithm choice alone.

## Tutor Feedback and Response

**Feedback.** The submission was well received, particularly the
discussion of architectural effects on sort performance, the graphics,
and the reference use. The one specific note: while both sort algorithms
are long-established, it remains appropriate to cite the original
authors or designers, flagged as a pointer for the properly assessed
version of this exercise (Assessment 2), for which this submission is
described as an excellent starting point.

**My response.** This is a fair and easy correction to carry forward:
citing Bubble Sort and Quick Sort's original designers (the latter
generally attributed to Tony Hoare) is a small addition that costs
nothing and directly addresses academic completeness, distinct from
citing supporting literature like Hennessy and Patterson for the
hardware explanation, which the submission already did well.
