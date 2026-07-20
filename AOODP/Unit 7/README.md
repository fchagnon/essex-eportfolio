# Unit 7: Secure Coding Practices in Object-Oriented Programming

## Unit Topic

This unit covers secure coding practices in an object-oriented context:
common vulnerabilities in OO systems (injection, weak authentication,
insufficient input validation) and the techniques used to eliminate them,
applied hands-on by refactoring an insecure authentication system.

## Learning Outcomes

By the end of this unit, I should be able to:

- Understand and explain the importance of secure coding in software
  development.
- Identify common vulnerabilities in object-oriented systems, such as
  injection attacks and buffer overflows.
- Apply secure coding techniques, including input validation, proper
  authentication, and exception handling.
- Refactor a codebase to eliminate security vulnerabilities through a
  practical exercise.

## Formative Assignment

*(Formative, collaborative discussion format)*

Identify the vulnerabilities in a provided authentication system
(plaintext password storage, a claimed SQL injection flaw, weak password
policy, no input validation, no rate limiting), then refactor it using
bcrypt hashing, input sanitization, hash-based authentication, an
enforced password policy, and rate limiting.

Full post: https://github.com/fchagnon/essex-eportfolio/tree/main/AOODP/Unit%207

## Reading List

Shah, M. (2023) *Cloud Native Software Security Handbook: Unleash the
Power of Cloud Native Tools for Robust Security in Modern Applications*.
1st edn. Birmingham: Packt Publishing. Chapters 2, 3, 6, and 7.

Baker, M. (2022) *Secure Web Application Development: A Hands-On Guide
with Python and Django*. 1st edn. Berkeley, CA: Apress. Chapters 9, 10,
11, and 12.

## Reflection

This exercise took theoretical concepts I already knew, password
hashing, exponential backoff, and developed my practical understanding of
how they're actually implemented programmatically.

**Understanding the importance of secure coding.** Storing passwords as
plaintext means a compromised database grants an attacker immediate
access to all credentials (Baker, 2022, ch.9). Passwords are hashed with
a unique salt at the point of creation and never stored in plaintext;
salting defeats rainbow table attacks by ensuring the same password never
produces the same hash twice, bcrypt handles this automatically,
embedding the salt within the stored hash.

**Identifying common vulnerabilities.** The assignment's own claim of a
SQL injection vulnerability in the original `authenticate()` method
doesn't hold: Python's string comparison treats `admin' OR '1'='1` as a
literal string and returns `False`, not `True` as the brief suggested.
The underlying concern is still legitimate, unvalidated input remains the
standard vector for injection attacks once a real database backend is
involved (Shah, 2023, ch.6). A genuinely sharper vulnerability came from
peer discussion rather than the brief itself: Joseph identified a timing
attack risk in naive string comparison (`==` short-circuits on the first
mismatched character, letting an attacker infer correct characters from
response-time differences). I confirmed this risk is already mitigated at
a lower level, `bcrypt.checkpw()` is implemented to run in constant time
specifically to defeat this class of attack, so both our implementations
were immune without either of us needing to handle it explicitly.

**Applying secure coding techniques.** The password policy follows NIST
SP 800-63B Rev. 4: a minimum length of 15 characters, blocklist screening
against known compromised credentials, and no arbitrary complexity rules.
Rate limiting uses exponential backoff, a 30-minute lockout after seven
consecutive failures. Comparing this against Joseph's sliding-window
approach (a hard cap of attempts within a rolling time window) surfaced a
genuine trade-off: a sliding window is harder to pace around in short
bursts, while exponential backoff is intended to frustrate a more
persistent, longer-running attacker. OWASP treats both as complementary
defence-in-depth controls rather than competing choices, which resolved
what initially looked like a question of which approach was correct.

**Refactoring to eliminate vulnerabilities.** The full refactor replaced
plaintext storage, unvalidated input, and unlimited login attempts with
`Password` and `AuthenticationSystem` classes enforcing hashing, policy
checks, and rate limiting as structural properties of the design, not
something a caller could accidentally bypass.
