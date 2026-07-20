# Unit 4: Software Engineering

## Unit Topic

This unit covers the Software Development Life Cycle (SDLC), software
design methodologies (Waterfall, Agile, DevOps), and sustainable software
engineering practices, including energy-efficient coding and minimising
technical debt.

## Learning Outcomes

On completion of this unit, I should be able to:

- Identify and analyze challenges in software design and development.
- Gather and synthesize information to apply software engineering
  principles systematically.
- Evaluate software development methodologies and their suitability for
  different projects.

## Formative Assignment

There was no separate formative task this week; this unit concluded the
four-week summative discussion begun in Unit 1, with a summary post
synthesising the discussion thread on the NotPetya/Maersk cyberattack.

Full post: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%204

## Reading List

Greenaway, J. (2023) *Fundamentals for Self-Taught Programmers: Embark on
Your Software Engineering Journey without Exhaustive Courses and Bulky
Tutorials*. Birmingham: Packt Publishing. Chapters 1-3.

## Reflection

**Identifying and analysing challenges in software design.** The
NotPetya/Maersk case gave a concrete, real-world example of what
happens when a core software engineering tenet, encapsulation, is
absent at a global-network scale: a flat architecture with no logical
isolation between segments let malware treat the entire network as a
single, unpartitioned graph. Framing this as an encapsulation failure,
not just a security failure, connected this unit's own subject matter
directly to a real, catastrophic engineering outcome.

**Gathering and synthesising information across the module.** Writing
this summary meant drawing threads from three classmates' contributions,
Bonanomi's data-science framing of EDR/XDR evolution from
signature-based detection toward network-wide behavioural modelling, and
Berisha's point on strategic cost, into a single coherent argument, while
also tying back explicitly to material from two earlier units:
Walton's (2024) framing of computing as the transformation of data into
societal value from Unit 1, and the discrete logic and mathematical
isolation of subsets discussed in Unit 2. That backward synthesis across
the whole module, not just this unit's own reading, is what a genuine
summary post is supposed to demonstrate.

**Evaluating methodologies and their suitability.** This piece is
honestly thinner here than the brief's own SDLC framing (Waterfall,
Agile, DevOps) would suggest; the argument instead evaluates
*architectural resilience practices* directly, treating availability as
a non-functional requirement demanding the same engineering discipline
as structural safety factors, and arguing for mandatory, air-gapped,
immutable recovery environments as a specific practice worth adopting.
That's a real evaluation of engineering trade-offs, but it isn't a
comparison of development methodologies in the sense this unit's own
outcome describes, worth naming that gap directly rather than implying
broader coverage than the post actually provides.
