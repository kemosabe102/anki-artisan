# Performance Checks Reference

Detailed performance review patterns for Python code. Covers algorithmic efficiency, async correctness, resource management, and common bottlenecks.

## Table of Contents

1. [Algorithmic Efficiency](#algorithmic-efficiency)
2. [Async Correctness](#async-correctness)
3. [Resource Management](#resource-management)
4. [Database Performance](#database-performance)
5. [Code Examples](#code-examples)

---

## Algorithmic Efficiency

### Data Structure Selection

**Check:** Appropriate data structures for the access pattern

```python
# ❌ BAD - O(n) lookup in loop = O(n²) total
for item in items:
    if item in large_list:  # Linear search each time
        process(item)

# ✅ GOOD - O(1) lookup with set
item_set = set(large_list)
for item in items:
    if item in item_set:  # Hash lookup
        process(item)
```

### Unnecessary Recomputation

**Check:** Expensive operations not repeated in loops

```python
# ❌ BAD - Regex compiled every iteration
for line in lines:
    match = re.match(r"\d{4}-\d{2}-\d{2}", line)

# ✅ GOOD - Compile once, use many times
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
for line in lines:
    match = DATE_PATTERN.match(line)
```

### Generator vs List

**Check:** Use generators for large sequences processed once

```python
# ❌ BAD - Loads entire file into memory
lines = open("huge_file.txt").readlines()
for line in lines:
    process(line)

# ✅ GOOD - Generator processes line by line
with open("huge_file.txt") as f:
    for line in f:
        process(line)

# ❌ BAD - Creates intermediate list
squared = [x**2 for x in range(1_000_000)]
total = sum(squared)

# ✅ GOOD - Generator expression
total = sum(x**2 for x in range(1_000_000))
```

---

## Async Correctness

### Blocking Calls in Async Functions

**CRITICAL:** Blocking I/O in async functions freezes the event loop

```python
# ❌ BAD - Blocks entire event loop
async def fetch_data(url: str):
    response = requests.get(url)  # BLOCKING!
    time.sleep(1)  # BLOCKING!
    return response.json()

# ✅ GOOD - Use async libraries
async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    await asyncio.sleep(1)
    return response.json()
```

### Common Blocking Operations

| Blocking Call | Async Alternative |
|---------------|-------------------|
| `requests.get()` | `httpx.AsyncClient().get()` |
| `time.sleep()` | `asyncio.sleep()` |
| `open().read()` | `aiofiles.open()` |
| `subprocess.run()` | `asyncio.create_subprocess_exec()` |
| SQLAlchemy sync | SQLAlchemy async or `asyncpg` |

### Structured Concurrency (Python 3.11+)

**Check:** Use TaskGroup for concurrent operations

```python
# ❌ BAD - gather doesn't handle cancellation well
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    fetch_preferences(user_id),
)

# ✅ GOOD - TaskGroup cancels all on failure
async with asyncio.TaskGroup() as tg:
    user_task = tg.create_task(fetch_user(user_id))
    orders_task = tg.create_task(fetch_orders(user_id))
    prefs_task = tg.create_task(fetch_preferences(user_id))

results = (user_task.result(), orders_task.result(), prefs_task.result())
```

### Fire-and-Forget Tasks

**Check:** Background tasks maintain references

```python
# ❌ BAD - Task may be garbage collected
async def handle_request():
    asyncio.create_task(send_notification())  # May be lost!
    return response

# ✅ GOOD - Store reference until completion
background_tasks: set[asyncio.Task] = set()

async def handle_request():
    task = asyncio.create_task(send_notification())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return response
```

---

## Resource Management

### Context Managers

**Check:** Resources properly acquired and released

```python
# ❌ BAD - Resource may leak on exception
f = open("file.txt")
data = f.read()
f.close()  # Never reached if read() raises

# ✅ GOOD - Guaranteed cleanup
with open("file.txt") as f:
    data = f.read()

# For async resources
async with aiofiles.open("file.txt") as f:
    data = await f.read()
```

### Connection Pooling

**Check:** Database/HTTP connections use pools

```python
# ❌ BAD - New connection per request
async def get_user(user_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    finally:
        await conn.close()

# ✅ GOOD - Use connection pool
pool: asyncpg.Pool = None

async def get_user(user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
```

---

## Database Performance

### N+1 Query Problem

**Check:** Related data loaded efficiently

```python
# ❌ BAD - N+1 queries (1 + N additional queries)
users = session.query(User).all()
for user in users:
    print(user.profile.avatar)  # Lazy load triggers query each time

# ✅ GOOD - Eager load with selectinload (for collections)
from sqlalchemy.orm import selectinload
users = session.query(User).options(selectinload(User.orders)).all()

# ✅ GOOD - Eager load with joinedload (for single relations)
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.profile)).all()
```

### Loading Strategy Decision Matrix

| Relationship | Best Strategy | Why |
|--------------|---------------|-----|
| Many-to-One | `joinedload` | Single JOIN, no extra queries |
| One-to-One | `joinedload` | Single JOIN, no extra queries |
| One-to-Many | `selectinload` | Avoids Cartesian product |
| Many-to-Many | `selectinload` | Avoids Cartesian product |

### Query Optimization

**Check:** Queries select only needed columns

```python
# ❌ BAD - Loads entire objects
users = session.query(User).all()
names = [u.name for u in users]

# ✅ GOOD - Select only needed columns
names = session.query(User.name).all()
```

---

## Code Examples

### Efficient Batch Processing

```python
from typing import Iterator, TypeVar
from itertools import islice

T = TypeVar("T")

def batched(iterable: Iterator[T], size: int) -> Iterator[list[T]]:
    """Yield successive batches from iterable."""
    iterator = iter(iterable)
    while batch := list(islice(iterator, size)):
        yield batch

async def process_large_dataset(items: Iterator[Item]) -> None:
    """Process items in efficient batches."""
    async with asyncpg.create_pool(DATABASE_URL) as pool:
        for batch in batched(items, size=1000):
            async with pool.acquire() as conn:
                await conn.executemany(
                    "INSERT INTO items (id, data) VALUES ($1, $2)",
                    [(item.id, item.data) for item in batch]
                )
```

### Async HTTP Client with Concurrency Limit

```python
import asyncio
import httpx

async def fetch_all(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    """Fetch URLs with bounded concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
        async with semaphore:
            response = await client.get(url)
            return response.json()
    
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, url)) for url in urls]
        
        return [task.result() for task in tasks]
```
