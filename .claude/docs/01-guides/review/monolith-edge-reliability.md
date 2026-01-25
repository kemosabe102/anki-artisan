In a monolith, the principles of systems thinking still apply, but the **"Edges" shift from Physical (Network) to Logical (Memory & Database)**.

In a microservices architecture, the edges are obvious because they are network calls. In a monolith, the edges are invisible—they are method calls, shared transactions, and thread pools. This makes them *more* dangerous because they look like simple code but act like system boundaries.

Here are the three "Monolith-Specific" edges you must review for reliability, followed by what becomes *less* important.

### 1. The Transactional Edge (The "Logical Lock")
*Instead of network timeouts, you have database locks.*

In a distributed system, if Service A calls Service B, they usually have separate databases. In a monolith, Component A and Component B often share the same ACID transaction. This is the single biggest reliability risk in monoliths.

*   **The Risk:** "Long Transactions." If Component A does some heavy processing (or worse, calls an external API) while inside a transaction, it holds a database connection and row locks. If Component B needs those rows or a connection, it starves.
*   **Review Checklist:**
    *   **The Sandwich Rule:** Is the transactional part the *meat* (small, in the middle) or the *bread* (wrapping the whole function)? Ensure you fetch data (read), calculate (processing), and then save (write). Do *not* calculate while holding the write lock.
    *   **External Calls inside Transactions:** Does this code call a 3rd party API (e.g., Stripe, SendGrid) while `@Transactional` is active? If the API waits 30s, you just froze a database connection for 30s.
    *   **Deadlock Potential:** Do Component A and Component B update tables in the same order? (e.g., Users then Orders). If A does Users->Orders and B does Orders->Users, you will deadlock the DB.

### 2. The Shared Resource Edge (The "Starvation" Edge)
*Instead of one service crashing, the whole process dies.*

In microservices, if the "Image Resizer" runs out of memory, only that service dies. In a monolith, if the "Image Resizer" leaks memory, it kills the "Checkout" component too because they share the same Heap and Thread Pool.

*   **The Risk:** "No Bulkheading." A minor background feature consuming all threads or memory, causing the critical path to fail (OOM or Thread Pool Starvation).
*   **Review Checklist:**
    *   **Thread Hygiene:** Does this heavy task run on the main web server thread pool? It should be offloaded to a separate, isolated thread pool (a "Bulkhead").
    *   **Memory unbound:** Is this code loading a list into memory (e.g., `findAll()`) without a hard limit? In a monolith, one `List<BigObject>` can trigger a Full Garbage Collection pause that freezes the entire application for seconds.
    *   **Static State:** Are we using static caches (Maps/Lists) without eviction policies? This is a memory leak waiting to happen.

### 3. The Coupling Edge (The "Side Effect" Edge)
*Instead of schema drift, you have state mutation.*

In microservices, you pass a *copy* of data (JSON) over the wire. In a monolith, you often pass a *reference* to an object in memory. If Component A changes a field on that object, Component B sees the change instantly, often unexpectedly.

*   **The Risk:** "Spooky Action at a Distance." You pass a `User` object to a `NotificationService`. The Notification code modifies `user.lastEmailSent`. The `UserService` unknowingly saves that change to the DB because Hibernate/ORM tracked the object.
*   **Review Checklist:**
    *   **Defensive Copying:** If this component accepts a mutable object, does it rely on it staying unchanged? If so, does it make a defensive copy?
    *   **Side-Effect Isolation:** Does this "Get" method also "Set" something? (e.g., `calculateTotal()` which also updates `lastAccessedDate`). These hidden writes cause phantom bugs in other components relying on clean reads.
    *   **Global State:** Are we relying on ThreadLocals or Static Singletons that might be polluted by a previous request on the same thread?

***

### What is LESS important in a Monolith?

You can relax on these "Distributed System" concerns:

1.  **Serialization Compatibility:** You don't need to worry if "Service A v1 can talk to Service B v2." In a monolith, the whole system is deployed at once. The compiler guarantees that Method A can call Method B.
2.  **Network Partitions (CAP Theorem):** You rarely have to handle "The database is unreachable *only* for Component A." If the DB is down, the whole monolith is usually down. You don't need complex "Eventual Consistency" patterns; you can just use ACID transactions.
3.  **Network Latency & Serialization Cost:** In microservices, every edge adds 20-100ms. In a monolith, function calls are nanoseconds. You don't need to obsess over "Batching calls" or "GraphQL field selection" for performance reasons *inside* the backend.

### Summary: The "Monolith" Graph Review

| Aspect | Microservices Focus | Monolith Focus |
| :--- | :--- | :--- |
| **The Edge** | Network Call (HTTP/gRPC) | Method Call / Transaction |
| **Primary Risk** | Latency / Partial Failure | Shared Resource Starvation |
| **Data Flow** | Pass by Value (Copy) | Pass by Reference (Pointer) |
| **Review Question** | "What if the network fails?" | "What if this thread hangs?" |
| **Critical Review** | Timeout & Retry Logic | Transaction Boundaries & Memory Usage |
