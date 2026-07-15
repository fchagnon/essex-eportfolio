# Unit 7: Secure Coding Practices
### Secure User Authentication System

## Task

Implement a secure user authentication system in Python, addressing password
storage, input validation, password policy, and rate limiting against
brute-force attacks.

## Artefact

auth_system.py: AuthenticationSystem manages user registration and login,
with Password handling hashing and policy validation, and rate limiting
applied per-user against repeated failed attempts.

```python
def hash(self, password):
    self._check_input(password)
    self._check_length(password)
    self._check_blocklist(password)
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def validate(self, hash, password):
    return bcrypt.checkpw(password.encode("utf-8"), hash)
```

## Design Decisions

**Hashed password storage.** The most significant remediation over an
insecure baseline was replacing plaintext password storage with bcrypt
hashing. A compromised database otherwise grants an attacker immediate
access to all credentials (Baker, 2022). Salting, handled automatically by
bcrypt and embedded within the stored hash, ensures the same password never
produces the same hash twice, defeating rainbow table attacks (Baker, 2022).
The User class only ever holds a hash, never a cleartext password, so no
code path in the system has access to the original value after
registration.

**Password policy and standards alignment.** The policy was built directly
against NIST SP 800-63B Rev. 4: a minimum length of 15 characters for
single-factor authentication, mandatory blocklist screening against known
compromised credentials, and explicit rejection of arbitrary complexity
rules such as forced special characters (NIST, 2024). This reflects NIST's
position, echoed by Baker (2022), that length is the primary driver of
password strength, not enforced character variety.

**Rate limiting.** Failed attempts are tracked per username in memory, with
exponential backoff and a lockout after seven consecutive failures.
Brute-force and dictionary attacks are primary threats against
authentication systems, and artificial delay combined with account lockout
is a standard defence (Baker, 2022). OWASP (2025) frames exponential
backoff, lockout thresholds, and CAPTCHA as complementary, defence-in-depth
layers rather than standalone solutions; the logic here forms the
foundation those additional controls would build on.

## Challenges Faced

The assignment's brief identified a SQL injection vulnerability in the
original authenticate() method, using a malicious string input. On
inspection, this does not hold: Python string comparison treats the input
literally rather than interpreting embedded logic the way a SQL engine
would, so it returns False, not True as the brief suggested. Recognizing
that discrepancy, while still implementing the intended defence, was itself
a useful exercise. Input validation remains a legitimate safeguard against
malformed input if the system is later extended with a real database
backend, regardless of whether this specific example was a true SQL
injection (Shah, 2023).

## Trade-off

Storing lockout state in an in-memory dictionary is simple and sufficient
for demonstrating the rate-limiting logic, but does not persist across
restarts and would not scale across multiple server instances. A production
system would need this state in shared storage. This was an accepted
simplification to keep the security logic itself legible, consistent with
the same avoid-production-grade-noise principle applied in the Unit 6
banking system.

## References

Baker, M. (2022) *Secure Web Application Development: A Hands-On Guide with
Python and Django*. 1st edn. Berkeley, CA: Apress.

National Institute of Standards and Technology (2024) *Digital Identity
Guidelines: Authentication and Lifecycle Management*. NIST Special
Publication 800-63B-4.

OWASP (2025) *Authentication Cheat Sheet*.

Shah, M. (2023) *Cloud Native Software Security Handbook: Unleash the Power
of Cloud Native Tools for Robust Security in Modern Applications*. 1st edn.
Birmingham: Packt Publishing.

## Reflection

This assignment let me feel at home with cybersecurity principles.
Leveraging NIST as a means of establishing a password policy, and directly
applying hashing algorithms rather than just reading about them in
principle, genuinely engaged me in the formative assignment. This came
through in my interactions with peers in the forum.
