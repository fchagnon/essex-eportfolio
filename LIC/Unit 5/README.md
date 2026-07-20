# Unit 5: Data Science and Storage

## Unit Topic

This unit covers data science and storage technologies: structured
versus unstructured data, relational versus non-relational databases,
and the ethical and legal considerations (GDPR, data security) around
data management.

## Learning Outcomes

On completion of this unit, I should be able to:

- Identify challenges and processes in storing and analyzing data within
  business systems.
- Gather and synthesize information from multiple sources to apply data
  storage and analysis techniques.
- Critically evaluate data storage models and data science tools for
  enterprise needs.
- Articulate the ethical and legal considerations in data management.

## Formative Assignment

Download a public dataset, load and clean it, conduct basic analysis
(mean, median, trends, correlations), create visualizations, and write a
200-word reflection comparing two storage models based on the dataset's
structure and use case.

Full submission: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%205

## Reading List

Chang, V. (2022) *Novel AI and Data Science Advancements for
Sustainability in the Era of COVID-19*. London: Academic Press.
Chapters 1-2.

Walton, D.J. (2024) *Culturally Responsive Computing: An Introduction
into Computer Science, Security, and Technology*. Boston, MA: ROTEL.
Chapter 4.

## Reflection

I chose the historical finisher data for Paris-Brest-Paris, the 1,200km
randonneuring event I intend to ride in its 2027 edition, over a generic
public dataset, since it let me answer a question I actually cared
about: what finishing time would keep me ahead of the largest mass of
riders.

**Identifying challenges in storing and analyzing data.** The raw files
sourced from the BC Randonneurs Cycling Club's archive contained real
"data debt": finish times rendered as scientific decimals, and orphaned
records. Cleaning this wasn't an abstract exercise, it directly
determined whether the 25th-percentile calculation I actually needed
would be trustworthy.

**Gathering and synthesising information from multiple sources.** The
data itself came from a community-maintained archive (BC Randonneurs)
rather than the official governing body (Audax Club Parisien) directly,
since the community archive provided accessible Excel and CSV formats
where the official source did not. That's a genuine, practical data
science problem: the most authoritative source is not always the most
usable one, and knowing which to draw from for a given task is itself a
skill.

**Critically evaluating storage models.** SQL is the better model for
historical analysis specifically, its strict schema enforcement and data
typing act as gatekeepers, ensuring every entry conforms to a standard
format before being committed to disk (Ramakrishnan and Gehrke, 2003, p.
60), which is exactly what let me trust the cleaned data enough to
identify a 72-hour finish time as the practical threshold to stay ahead
of the "blob," the high-density rider mass, where being caught has a real
adverse effect on finish time and crash risk. But the same event, viewed
through a different use case, argues for the opposite model: a real-time
dashboard serving live GPS and heart-rate telemetry to thousands of
concurrent dotwatchers during the actual 2027 event would be a
high-velocity, write-heavy, sparse-data workload, exactly what NoSQL's
horizontal scalability is built for (Silberschatz, Korth and Sudarshan,
2020, pp. 905-910). The real lesson wasn't that one model is better, it's
that the same dataset can demand genuinely different storage
architectures depending on whether the use case is historical analysis
or live operations, "polyglot persistence," using different databases for
different needs within the same system, is the practical resolution
(Fowler and Sadalage, 2012, p. 143).

**Articulating ethical and legal considerations.** This submission
doesn't directly address GDPR or data privacy, since PBP finisher data is
already public and non-personal beyond a rider's name and finish time.
Worth naming as a genuine gap relative to this unit's own learning
outcome, rather than implying coverage the work doesn't actually have.
