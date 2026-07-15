# Unit 4: Design Patterns II — Structural Patterns
### Collaborative Discussion
*(Formative — not assessed; collaborative discussion format)*

## Task

Using Structural Design Patterns, address three discussion tasks, each with a
real-world scenario, an explanation, and a Python code example:

1. **Adapter Pattern** — integrating a legacy SOAP-based payment system with
   a modern RESTful e-commerce platform.
2. **Bridge Pattern** — managing different devices (TV, Radio) and different
   remote controls (Basic, Advanced), decoupling abstraction from
   implementation.
3. **Composite Pattern** — managing a file system where files and folders
   are treated uniformly through a shared interface.

## My Original Post

**"Structural Design Patterns in Autonomous Security Operations"**

Structural design patterns, as defined by Gamma et al. (1994), address how
classes and objects are composed to form larger, more flexible structures.
This post explores Adapter, Composite, and Bridge through the lens of an
AI-driven Security Operations Centre (SOC), where autonomous agents must
ingest heterogeneous data, reason over complex threat models, and execute
containment actions within defined policy boundaries. As Srinivas et al.
(2025) observe, autonomous SOC agents must detect, classify, and respond to
threats with minimal human intervention — a capability that depends heavily
on sound architectural design.

**Adapter Pattern.** An AI agent's reasoning is only as good as the data it
consumes. Legacy data sources, network sensors, and endpoint tools each
produce telemetry in different formats — delimiter-separated strings,
proprietary syslog variants, structured JSON. An adapter per data source
translates raw output into a shared `NormalizedAlert()` structure, so the
agent reasons uniformly regardless of source. Adding a new data source means
writing a new adapter; the agent itself is untouched.

```python
class LegacySIEMAdapter(AlertSource):
    def __init__(self, siem): self.siem = siem
    def get_alert(self):
        # Translates the legacy pipe-delimited string into a NormalizedAlert —
        # the only format the AI agent knows how to consume.
        p = self.siem.fetch_raw_event().split("|")
        return NormalizedAlert(p[0], p[1], p[2], p[3])
```

**Composite Pattern.** The MITRE ATT&CK framework — a structured knowledge
base of adversary tactics and techniques (Strom et al., 2018) — is inherently
hierarchical: individual techniques roll up into tactics, which compose into
kill chains. Modelling this with Composite lets an agent reason at any
level — predicting next steps from a single technique, or projecting a full
campaign trajectory — using identical logic.

```python
class Technique(ATTACKNode):
    # Leaf node — returns its own next-step predictions directly.
    def predicted_next(self): return self.next_steps

class Tactic(ATTACKNode):
    # Composite node — delegates to each child and aggregates the results.
    # The agent calls predicted_next() identically on both; it cannot tell them apart.
    def predicted_next(self):
        return list({s for c in self.children for s in c.predicted_next()})
```

**Bridge Pattern.** The agent must decide *what* action to take (isolate a
host, block an IP, remediate a vulnerability) independently of *how and
where* that action executes, which varies across cloud EDR platforms,
on-premise firewalls, and network infrastructure. Policy guardrails —
defining which actions the agent may execute autonomously, and at what
severity threshold — must be enforced at the seam between decision and
execution. Srinivas et al. (2025) note that automating security operations
requires rules of engagement and a degree of certainty before execution,
particularly for irreversible actions; the Bridge pattern enforces exactly
this separation.

```python
class IsolateHostAction:
    def execute(self, host, severity):
        # Policy is checked before the execution target is invoked.
        # The action (what) is decoupled from the target (how and where)
        # and neither proceeds without Policy's approval.
        if self.policy.approve("IsolateHost", severity):
            self.target.isolate_host(host)
```

## Peer Engagement

Replied to Reena's post, which implemented Composite via a file/folder system
and Adapter via a `PaymentAdapter`.

**On Composite** — noted that her file/folder implementation and my own
Composite solution (a MITRE ATT&CK threat hierarchy, traversed identically
across individual techniques and tactic groupings by an AI reasoning agent)
arrived at the same structural approach from very different problem domains —
evidence that the pattern generalises as an architectural principle rather
than being tied to any one kind of hierarchy.

**On Adapter** — identified that her `PaymentAdapter` hardcoded `"GBP"` as the
currency, meaning the adapter was making a business decision rather than
purely translating between interfaces. Traced this to a Single Responsibility
Principle violation: the class had two reasons to change — SOAP/REST
translation logic, and currency policy — where a clean adapter should have
only the first. Recommended passing currency through from the calling
context instead, keeping the adapter reusable across markets. Cited Martin
(2003) as the canonical source for SOLID, noting the principles were
formally introduced there and only later popularised in *Clean Code* (2008).

**On Bridge** — acknowledged a fair point raised by Joseph regarding the
distinction between dependency injection and a true Bridge pattern (two
independently evolving class hierarchies), flagged as worth revisiting.

## Reference

Feuerriegel, S., Shrestha, Y.R., von Krogh, G. and Zhang, C. (2025) 'A survey
of agentic AI and cybersecurity: Challenges, opportunities and use-case
prototypes', *arXiv preprint*, arXiv:2601.05293.

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns:
Elements of Reusable Object-Oriented Software*. Boston: Addison-Wesley.

Martin, R.C. (2003) *Agile Software Development: Principles, Patterns, and
Practices*. Upper Saddle River, NJ: Prentice Hall.

Srinivas, S., Kirk, B., Zendejas, J., Espino, M., Boskovich, M., Bari, A.,
Dajani, K. and Alzahrani, N. (2025) 'AI-augmented SOC: A survey of LLMs and
agents for security automation', *Journal of Cybersecurity and Privacy*,
5(4), p. 95.

Strom, B.E., Applebaum, A., Miller, D.P., Nickels, K.C., Pennington, A.G. and
Thomas, C.B. (2018, revised 2020) *MITRE ATT&CK: Design and Philosophy*.
Technical report. McLean, VA: The MITRE Corporation.

## Reflection

To this point, I'd been wondering why an object-oriented programming course
belonged in a postgraduate degree focused on cybersecurity. This formative
assignment was my first real attempt to bridge the cybersecurity world — and
my own professional research work, currently focused on autonomous security
operations — with this postgraduate pursuit. Prior to this, a SIEM was, to
me, just a piece of infrastructure: a log dumping ground. An AI agent was
just another automation tool. But through the lens of the Adapter, Bridge,
and Composite patterns, I started to appreciate a little more about the
inner workings of these SOC components, and how architectural thinking
applies to a domain I already thought I understood well.
