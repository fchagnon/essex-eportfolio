import bcrypt
import re
import time
import string

LOCKOUT_DURATION = 1800
MAX_ATTEMPTS = 7

class User:
""" User class never sees a password. Only stores a hash """
    def __init__(self, username, hash):
        self.username = username
        self.hash = hash

class Password:
""" Password class contains public methods to hash() a password, 
    and validate() a password. Validation uses several private 
    methods to enforce NOST standard password policies """
    def __init__(self,blocklist):
        self.blocklist = blocklist

    def _check_length(self, password):
        # Enforce NIST standard password lengths - 15-64 characters. 
        if len(password) < 15:
            raise ValueError("Password must be at least 15 characters.")
        if len(password) > 64:
            raise ValueError("Password must be fewer than 64 characters.")

    def _check_blocklist(self, password):
        # Make sure the password isn't love, sex, secret or god (among other things)
        # ref: Hackers (1995)
        for blocked in self.blocklist:
            if password.lower() == blocked.lower():
                raise ValueError("Password is too common. Please choose another.")

    def _check_input(self,password):
        # Input validation on password. 
        # Can't be empty, or contain non-printable characters
        if not password:  
            raise ValueError("Password cannot be empty.")
        if not all(c in string.printable for c in password):
            raise ValueError("Password contains invalid characters.")

    def hash(self,password):
        # Checks a series of policies, and then returns a salted hash. 
        self._check_input(password)
        self._check_length(password)
        self._check_blocklist(password)
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def validate(self,hash,password):
        # True if the hased password matches the stored hash. False otherwise. 
        return bcrypt.checkpw(password.encode("utf-8"), hash)

class AuthenticationSystem:
""" AuthenticationSystem class """
    def __init__(self):
        self.lockouts = {}
        self.users = {}
        with open("blocklist.txt", "r") as f:
            blocklist = [line.strip() for line in f]
        self.password = Password(blocklist)

    def _check_input(self,username):
        if not re.match(r"^[a-zA-Z0-9_-]{1,8}$", username):
            raise ValueError("Invalid username.")
        return True

    def _authlimit(self,user,password):
        # First we check to make sure the user isn't already locked out
        # If they are, we just delay 30 seconds (backoff) and act like a normal fail
        # If they're in the lockout file, but it's been 30 minutes, we remove them and proceed
        # normally. 
        if user.username in self.lockouts:
            if self.lockouts[user.username]["lockout_time"] is not None:
                if time.time() - self.lockouts[user.username]["lockout_time"] > LOCKOUT_DURATION:
                    del self.lockouts[user.username]
                else:
                    time.sleep(2 ** 7)
                    return False

        # This is the exponential backoff logic. If the password validation fails 
        # we record the number of attempts and we sleep() for 2 to the order of n-1
        # where n is the number of attempts. Up to 7 times. Then we lock the account
        # for 30 minutes. 
        if not self.password.validate(user.hash, password):
            if user.username not in self.lockouts:
                self.lockouts[user.username] = {"attempts": 1, "lockout_time": None}
            else:
                self.lockouts[user.username]["attempts"] += 1
            time.sleep(2 ** (self.lockouts[user.username]["attempts"] - 1)) 
            if self.lockouts[user.username]["attempts"] >= 7:
                self.lockouts[user.username]["lockout_time"] = time.time()
            return False
        else: 
            return True

    # Note here that the User instance is called and never sees the cleartext password. 
    def add_user(self, username, password):
        if self._check_input(username): 
            hash = self.password.hash(password)  
            self.users[username] = User(username, hash)

    def authenticate(self, username, password):
        if username in self.users:
            user = self.users[username]
        else:
            return False
        return self._authlimit(user, password)

""" ----------------------------------------------------- """
# Usage
auth_system = AuthenticationSystem()

try:
    auth_system.add_user("admin", "admin123")
except ValueError as e:
    print(f"Error: {e}") # Shouldn't be allowed. Blocklisted. 

malicious_input = "admin' OR '1'='1"
try:
    print(auth_system.authenticate(malicious_input, "anything"))
except ValueError as e:
    print(f"Error: {e}") # Should fail input validation

try:
    auth_system.add_user("user1", "password")
except ValueError as e:
    print(f"Error: {e}") # Shouldn't be allowed. Blocklisted. 

try:
    auth_system.add_user("user2", "@ll_y0ur_b4s3_4r3_b3l0ng_2_U$")
except ValueError as e:
    print(f"Error: {e}")
print(auth_system.authenticate("user2", "@ll_y0ur_b4s3_4r3_b3l0ng_2_U$"))  # Should print True
print(auth_system.authenticate("user2", "wrongpassword"))  # Should print False
