# Unit 12: Future Trends and Concepts in Computing (End of Module Assignment)

## Unit Topic

This final unit explores transformative technologies, Quantum Computing,
Blockchain, AI, and Edge Computing, and their impact on enterprise IT,
alongside the ethical, legal, and societal considerations of adopting
them. It also houses the End of Module Assignment, submitted in two
parts weighted at 40% each.

## Learning Outcomes

**Part A** (Individual Programming Exercise):

- Critically evaluate appropriate methodologies, tools, and techniques
  to mitigate and/or solve computing issues and their business impact.
- Articulate the legal, social, ethical, and professional issues faced
  by computing professionals.

**Part B** (Individual Reflection Presentation):

- Gather and synthesize information from multiple sources to aid in the
  systematic design and analysis of computing challenges.
- Critically evaluate appropriate methodologies, tools, and techniques
  to mitigate and/or solve computing issues and their business impact.
- Articulate the legal, social, ethical, and professional issues faced
  by computing professionals.

## Formative Assignment

*(Summative: 82%, Distinction)*

**Part A** (3,000 words equivalent): given two tutor-provided scripts
(one Python, one JavaScript, later substituted with C) performing the
same simple task, run and lightly modify both, compare their syntax and
structure, write a 1,100-word language comparison report, and a
1,200-word professional reflection on readable, ethical code and its
real-world business and legal impact.

**Part B** (15-minute presentation, 1,000 words equivalent): a
tutor-specified question on emerging technology and its ethical and
security risks, addressed with at least eight peer-reviewed sources.

Full submission: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%2012

## Reflection

### Part A: Comparing Programming Languages

I extended this exercise well beyond its literal brief: rather than a
trivial demonstration script, I scaled both implementations to sort
800,000 real records, and added a third implementation, a Python
Quicksort, specifically to isolate whether performance differences came
from language choice or algorithm choice.

**Evaluating methodologies and their business impact.** The empirical
result was decisive and counterintuitive: Python Quicksort outperformed
C Bubble Sort at every tested size, by 92x at 100,000 records and 624x at
800,000. C Bubble Sort's *O(n²)* complexity meant an 8x increase in
dataset size produced a roughly 83x increase in runtime, 35 minutes at
800,000 records, while Python Quicksort's *O(n log n)* complexity kept
that same growth nearly flat on a logarithmic scale, finishing in 3.37
seconds. The finding I actually wanted to demonstrate: a compiled
language cannot compensate for an inefficient algorithm, algorithmic
choice, not language choice, is the primary determinant of scalability.

**Articulating professional and ethical issues.** The framing here
deliberately went past "this code is slow" into genuine professional
stakes. An *O(n²)* algorithm processing customer-facing data at scale is
not just a performance inefficiency, it is measurable energy waste with
real environmental cost, and a genuine Denial of Service vulnerability:
an attacker submitting a sufficiently large dataset could exploit the
same quadratic growth to exhaust server resources deliberately. C's
manual memory management (`malloc`/`realloc`) is also a direct security
liability, a single missed pointer check is the class of bug behind
real-world buffer overflow vulnerabilities, while Python's managed
memory model mitigates that risk by design. I also drew a deliberate
contrast using Art Ramos's 1996 "one-liner" Perl article, arguing that
prioritizing clever conciseness over readable logic is a genuine
anti-pattern, obscure code resists the transparent auditing needed to
catch both security flaws and algorithmic bias.

### Part B: Toward a Science of Cybersecurity

Rather than covering AI, Quantum Computing, or Blockchain directly as
the brief's own examples suggested, I argued for something more
structural: that cybersecurity itself is transitioning from a craft
practiced on individual intuition into an engineering science, using the
historical transition from alchemy to chemistry as the framing device.

**Gathering and synthesizing information across sources.** The argument
was built on current, quantified evidence rather than general assertion:
a 2025 average adversary breakout time of 29 minutes, with the fastest
recorded at 27 seconds (CrowdStrike, 2026), 67% of analysts citing alert
fatigue as their primary barrier (Ponemon Institute, 2023), and SOCs
receiving nearly 3,000 alerts daily while addressing only 38% (Vectra
AI, 2026). Each statistic supported a specific structural claim, not
just a general sense of things being difficult.

**Evaluating methodologies and their impact.** Following Simon (1996), I
argued cybersecurity specifically fits an engineering science rather
than a natural science, since its governing "laws" are specified through
design rather than discovered in nature, success means a system behaving
according to its design axioms under adversarial conditions, not
uncovering an immutable truth. I applied this directly to three real
failure points: SOC operations moving from analyst intuition to
auditable, deterministic workflows; vulnerability management moving from
periodic scanning to Continuous Threat and Exposure Management, since a
quarterly scan cannot respond to a two-to-three-day exploit window
(CrowdStrike, 2026); and compliance moving from periodic attestation to
continuous assurance, directly reflected in NIST CSF 2.0's new Govern
function (NIST, 2024).

**Articulating ethical and professional considerations.** I was
deliberate about not overstating the case for automation: following
Brundage et al.'s (2018) "automation paradox," removing humans entirely
to achieve machine-speed defence risks brittleness against exactly the
creative, non-linear threats a system was never trained to classify. The
human role shifts from analyst working in the system to engineer working
on the system, auditing the machine and validating its axioms. I also
connected this back to Walton's (2024) point on diversity directly: a
homogeneous team encoding autonomous security systems will encode its
own blind spots into the axioms themselves, which is an ethical risk,
not merely a technical one.

## Tutor Feedback and Response

**Feedback.** Among the strongest submissions received: one of the best
discussions of algorithmic differences seen, with effective use of
logarithmic-scale graphs; well-written and well-commented code in both
languages; a well-structured report with strong charts; good citations
throughout. For Part B: praised as picking up cutting-edge concepts and
synthesizing them succinctly, notably not another AI-focused
presentation; engaging delivery with only minor stumbles; the central
challenge to preconceived cybersecurity assumptions was specifically
highlighted as a strong point, alongside the alchemy parallel. Two
constructive notes: citations could have appeared directly on the slides
at key argumentative points for more impact, and the source list, while
reasonable, would have benefited from more academic texts specifically,
on falsifiability, graph theory in security, and formal validation
methods.

**My response.** Both notes are genuinely actionable rather than
cosmetic. Moving citations onto the slides themselves, not just the
transcript, is a presentation-craft fix with no real cost. The deeper
note, formal validation and falsifiability literature specifically,
points at exactly the kind of source that would have strengthened the
central engineering-science argument on its own terms: if cybersecurity
is genuinely maturing into a discipline with falsifiable claims, citing
the formal methods and falsifiability literature directly, rather than
only citing evidence of the craft model's failure, would have made the
argument's own philosophical foundation more rigorous.

## Real-World Impact

This assignment did not stay confined to the module. The central
argument, cybersecurity transitioning from a craft to an engineering
science, went on to shape real professional output beyond the
coursework itself.

**LinkedIn article.** "From Craft to Science: Is Cybersecurity On Its
Way?" (April 2026) developed the same alchemy-to-chemistry argument for
a professional audience, grounded in the same sources (Wootton, 2015;
Simon, 1996; CrowdStrike, 2026; Vectra AI, 2026; Ponemon Institute, 2023;
Brundage et al., 2018), but written from thirty years of direct
professional experience rather than as an academic exercise. The
article makes the personal stakes explicit in a way the presentation
itself, constrained by the tutor-specified brief, could not: "the
clever admin who could magic a fix will not be able to magic a fix at
quantum speed."

**Keynote address.** The same craft-to-engineering framing was developed
into a keynote speech for Info-Tech LIVE, my employer's marquee
industry conference, aimed at inspiring CISOs to embrace this
transition rather than resist it.

**Applied research.** Most significantly, I have since begun developing
a new security operations operating model professionally, whose origins
trace directly back to this summative assignment. What began as a
15-minute presentation answering a tutor-specified question became the
conceptual foundation for real applied research.

Full article: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%2012
