# Unit 7 Collaborative Discussion: Secure Authentication System

This formative Collaborative Discussion starts and ends in this unit week.

You are provided with a simple User Authentication System written in Python. The code has several security vulnerabilities.

## Discussion Tasks

### 1. Identify the vulnerabilities in the code

- **Plaintext Password Storage**
  - Passwords are stored in plaintext (no hashing/salting).
  - Risk: If the database is compromised, attackers gain direct access to passwords.

- **SQL Injection (Logic Flaw)**
  - The `authenticate()` method compares strings directly, allowing injection (e.g., `admin' OR '1'='1` bypasses authentication).

- **Weak Password Policy**
  - No enforcement of strong passwords (e.g., `"admin123"` is allowed).

- **No Input Validation**
  - Usernames/passwords are not sanitized (e.g., empty strings or malicious payloads are accepted).

- **No Rate Limiting**
  - Brute-force attacks are possible due to unlimited login attempts.

### 2. Refactor with Secure Practices

1. Hash Passwords (using bcrypt or argon2).
2. Sanitise Inputs (prevent injection).
3. Secure Authentication (compare hashes).
4. Enforce Password Policies.
5. Add Rate Limiting (prevent brute-force).

## Code Snippet

```python
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AuthenticationSystem:
    def __init__(self):
        self.users = []

    def add_user(self, username, password):
        self.users.append(User(username, password))

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False


# Usage
auth_system = AuthenticationSystem()
auth_system.add_user("admin", "admin123")  # Weak password
auth_system.add_user("user1", "password")  # Weak password
