Now we must look at the **Node** (the component) itself. Even if a component is perfectly isolated—never talking to a network or database—it can still be "unreliable" if its internal logic is fragile. For the component itself, you should verify its **"Internal Physics."**

Here are the three reliability categories for the **Component Node**:

### 1. The Invariant Core (Design by Contract)
*Does the component defend its own validity?*

Reliable components behave like a fortress: they refuse to enter an invalid state. A common reliability failure is "Gullible Code"—code that accepts a `null` or a negative `price` and tries to process it, leading to a crash deep in the stack where debugging is impossible.

*   **Review Checklist:**
    *   **Preconditions (Input Defense):** Does the public method explode *immediately* if inputs are invalid? (e.g., `Assert.notNull(userId)` at line 1). This is "Fail Fast."
    *   **Postconditions (Output Guarantees):** Does the component guarantee the return value is valid? (e.g., "This method will never return a null list, only an empty one").
    *   **Class Invariants:** Can an object ever exist in a "half-broken" state? (e.g., A `DateRange` object where `startDate > endDate`). The constructor and setters must strictly prevent this.

### 2. The Resource Bound (Algorithmic Safety)
*Does the component respect physics (CPU/RAM) limits?*

A component can be logically correct (it sorts the list) but effectively unreliable (it takes 10 seconds to sort a large list, hanging the thread). This is a "Logical Denial of Service" vulnerability.

*   **Review Checklist:**
    *   **Unbounded Allocations:** Does the code do `new ArrayList(userInput.size())`? A malicious (or buggy) user can send a size of 10 million, triggering an immediate OutOfMemory error.
    *   **Accidental Complexity:** Is there a nested loop ($O(n^2)$) on a collection that could grow large? (e.g., checking for duplicates in a list by iterating through it twice).
    *   **Regex Safety:** Does the component use a regular expression on user input? "Catastrophic Backtracking" in regex is a common way to freeze a CPU core to 100%.

### 3. The Failure Strategy (Exception Hierarchy)
*When it fails, does it confuse the operator?*

Reliability is also about *recoverability*. If a component fails by throwing a generic `System.Exception` or `Error`, the upstream system cannot react intelligently (e.g., "Retry" vs. "Abort").

*   **Review Checklist:**
    *   **Typed Exceptions:** Does it throw `PaymentDeclinedException` (recoverable by asking user for new card) or just `RuntimeException: 400 Bad Request`?
    *   **Atomic Failure:** If the method throws an exception halfway through, did it leave the object in a dirty state? (e.g., It incremented the `retryCount` but failed to send the retry). The component should be **Transactionally Atomic** (all or nothing) even in memory.
    *   **Error Context:** Does the exception message contain the *values* that caused the error? (Bad: `IndexOutOfBounds`. Good: `Index 5 out of bounds for size 4`).

### Summary: The "Node" Reliability Review

| Aspect | Edge Review | Node (Component) Review |
| :--- | :--- | :--- |
| **Focus** | Interaction & Latency | Logic & State |
| **Key Risk** | Network Failure / Timeout | Invalid State / Resource Exhaustion |
| **Philosophy** | "The network is unreliable" | "The inputs are potential attacks" |
| **Golden Rule** | Handle Timeouts | Enforce Invariants |

**Final Recommendation:**
When you review a specific component file, act like a **hostile lawyer**. Look for the contract (inputs/outputs) and try to find loopholes where you can force the component into an illegal state or freeze it by sending a massive input. If you can't break it, it's reliable.
