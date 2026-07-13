# =============================================================================
# Task 5: Constructor and Destructor
# =============================================================================
# Objective:
#   - Define a Person class with __init__(self, name) as the constructor
#   - Add __del__(self) as the destructor, printing a farewell message
#   - Test with explicit del, going out of scope, and multiple instances
#
# Key Concepts:
#   - Constructor (__init__): called automatically when an object is CREATED.
#     Sets up the initial state of the object (attributes, resources, etc.).
#   - Destructor (__del__): called automatically when an object is DESTROYED —
#     i.e. when its reference count drops to zero and Python's garbage collector
#     reclaims the memory.
#   - Reference counting: Python tracks how many variables point to an object.
#     The object is only destroyed when NO variables reference it anymore.
#   - 'del' keyword: removes a variable name (reference), which MAY trigger
#     __del__ immediately if it was the last reference to the object.
#
# Important caveat:
#   Python does NOT guarantee WHEN __del__ runs — only that it runs before
#   the object's memory is reclaimed. In CPython (the standard interpreter)
#   it typically fires immediately on del or scope exit, but other Python
#   implementations (PyPy, Jython) may delay it. For resource cleanup (files,
#   sockets, DB connections), prefer context managers (with / __enter__ /
#   __exit__) over __del__ in production code.
# =============================================================================


class Person:

    def __init__(self, name):
        """
        Constructor — runs the moment a Person object is created.

        Responsible for initializing all instance attributes.
        'self.name = name' stores the provided name on this specific object,
        so each Person instance carries its own independent name.

        The print statement makes the construction event visible in the demo,
        helping illustrate the exact moment __init__ fires relative to __del__.
        """
        self.name = name
        print(f"  [__init__] Person '{self.name}' has been created.")

    def __del__(self):
        """
        Destructor — runs automatically when this object is about to be
        destroyed (reference count reaches zero).

        Common use cases for __del__ in real systems:
          - Closing file handles or network connections
          - Releasing hardware resources (cameras, sensors)
          - Logging object lifecycle events for debugging

        Here it prints a farewell message to make the destruction event
        clearly visible. 'self.name' is still accessible at this point —
        the object's attributes remain valid until __del__ finishes.
        """
        print(f"  [__del__]  Goodbye, {self.name}!")

    def greet(self):
        """A simple concrete method to interact with the object while alive."""
        print(f"  [greet]    Hello, my name is {self.name}.")


# =============================================================================
# --- Demo / Test ---
# =============================================================================

# -----------------------------------------------------------------------------
# Test 1: Explicit deletion with del
# -----------------------------------------------------------------------------
# 'del' removes the variable name (the reference) from the current namespace.
# Since 'person1' is the ONLY reference to this object, removing it drops
# the reference count to zero — Python destroys the object and calls __del__.
print("=" * 50)
print("Test 1: Explicit deletion with del")
print("=" * 50)

person1 = Person("Alice")   # __init__ fires here
person1.greet()             # Object is alive and usable
del person1                 # Reference removed → __del__ fires immediately
print("  (person1 has been deleted)\n")

# -----------------------------------------------------------------------------
# Test 2: Going out of scope
# -----------------------------------------------------------------------------
# A variable created inside a function is local to that function.
# When the function returns, its local scope is torn down, all local references
# are released, and any objects with no remaining references are destroyed.
print("=" * 50)
print("Test 2: Going out of scope (function exit)")
print("=" * 50)

def create_temporary_person():
    """
    'temp' is a local variable — it exists only within this function's scope.
    When the function returns, 'temp' goes out of scope, the reference count
    for the Person object drops to zero, and __del__ is called automatically.
    """
    temp = Person("Bob")    # __init__ fires here
    temp.greet()            # Use the object while it's in scope
    print("  (function about to return — temp will go out of scope)")
    # No explicit del needed; scope exit handles cleanup

create_temporary_person()   # __del__ fires as the function exits
print("  (function has returned)\n")

# -----------------------------------------------------------------------------
# Test 3: Multiple references — del only destroys when the LAST reference goes
# -----------------------------------------------------------------------------
# This test shows that del on ONE variable does NOT destroy the object if
# another variable still holds a reference to it.
# The object survives as long as at least one reference remains.
print("=" * 50)
print("Test 3: Multiple references — last reference triggers destruction")
print("=" * 50)

person3       = Person("Carol")     # Reference count: 1
person3_alias = person3             # Reference count: 2 — same object, two names

del person3         # Reference count drops to 1 — object SURVIVES, __del__ NOT called yet
print("  (del person3 called — but person3_alias still holds a reference)")
print(f"  (object still alive: person3_alias.name = '{person3_alias.name}')")

del person3_alias   # Reference count drops to 0 — NOW __del__ fires
print("  (del person3_alias called — last reference gone)\n")

# -----------------------------------------------------------------------------
# Test 4: Automatic cleanup at program end
# -----------------------------------------------------------------------------
# Objects that are still alive when the script finishes are destroyed by
# Python's interpreter shutdown. __del__ is typically called for each,
# though the order is not guaranteed during interpreter teardown.
print("=" * 50)
print("Test 4: Automatic cleanup at program end")
print("=" * 50)

person4 = Person("Diana")
person5 = Person("Evan")
print("  (person4 and person5 created — no explicit del)")
print("  (they will be destroyed automatically when the script ends)\n")

print("=" * 50)
print("End of explicit test code — interpreter cleanup follows:")
print("=" * 50)

# person4 and person5 go out of scope here as the module finishes,
# triggering their __del__ calls automatically.
