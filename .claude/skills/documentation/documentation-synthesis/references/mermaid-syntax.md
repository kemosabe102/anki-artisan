# Mermaid Diagram Syntax

Syntax patterns and examples for generating Mermaid diagrams.

---

## Architecture Diagrams (graph)

**Purpose**: Show system components and their relationships

**Syntax**: `graph [direction]` where direction = TD (top-down), LR (left-right), BT, RL

### Basic Example

```mermaid
graph TD
    A[User Interface] --> B[API Gateway]
    B --> C[Service Layer]
    C --> D[(Database)]
```

### With Styling

```mermaid
graph LR
    UI[User Interface]:::frontend
    API[API Gateway]:::middleware
    DB[(Database)]:::storage
    
    UI --> API
    API --> DB
    
    classDef frontend fill:#e1f5ff,stroke:#01579b
    classDef middleware fill:#fff3e0,stroke:#e65100
    classDef storage fill:#f1f8e9,stroke:#33691e
```

### Node Shapes

```mermaid
graph TD
    A[Rectangle - Default]
    B(Rounded Rectangle)
    C([Stadium Shape])
    D[[Subroutine]]
    E[(Database)]
    F((Circle))
    G>Asymmetric]
    H{Diamond - Decision}
```

**Use**:
- Rectangle: Default components/services
- Rounded: User-facing elements
- Database: Data storage
- Diamond: Decision points
- Circle: Start/end points

---

## Flow Diagrams (flowchart)

**Purpose**: Show process flow with decision points

**Syntax**: `flowchart [direction]`

### Example

```mermaid
flowchart LR
    Start([Start]) --> Input[/Receive Input/]
    Input --> Validate{Valid?}
    Validate -->|Yes| Process[Process Data]
    Validate -->|No| Error[/Return Error/]
    Process --> Save[(Save to DB)]
    Save --> Success([Success])
    Error --> End([End])
    Success --> End
```

### Special Nodes

```mermaid
flowchart TD
    Input[/Input - Parallelogram/]
    Output[\Output - Inverted Parallelogram\]
    Manual[Manual Operation - Trapezoid]
    Data[(Database - Cylinder)]
```

**Best Practices**:
- Use decision diamonds for branching
- Label edges with conditions (|Yes|, |No|, |Error|)
- Keep flow unidirectional (avoid backward arrows unless loop)
- Start/end with stadium shapes

---

## Sequence Diagrams

**Purpose**: Show interactions between actors/components over time

**Syntax**: `sequenceDiagram`

### Example

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant DB as Database
    
    Client->>API: POST /data
    activate API
    API->>Service: validate(data)
    activate Service
    Service->>DB: query()
    DB-->>Service: result
    Service-->>API: validation result
    deactivate Service
    API-->>Client: 200 OK
    deactivate API
```

### Arrow Types

```mermaid
sequenceDiagram
    A->>B: Solid arrow (request)
    B-->>A: Dotted arrow (response)
    A-)B: Async message
    B-xA: Failed call
    A->>+B: Activate
    B-->>-A: Deactivate
```

**Notes and Boxes**:

```mermaid
sequenceDiagram
    Client->>Server: Request
    Note right of Server: Processing...
    Note over Client,Server: Communication established
    rect rgb(200, 220, 250)
        Server->>DB: Query
        DB-->>Server: Data
    end
    Server-->>Client: Response
```

**Best Practices**:
- Participant names at top (use aliases for long names)
- Use activation bars for processing
- Group related interactions in boxes
- Add notes for complex logic

---

## Class Diagrams

**Purpose**: Show component relationships and structure

**Syntax**: `classDiagram`

### Example

```mermaid
classDiagram
    class Component {
        -private_field
        +public_field
        #protected_field
        +method()
        -private_method()
    }
    
    class Interface {
        <<interface>>
        +method()
    }
    
    class Implementation {
        +method()
    }
    
    Component *-- Interface : composition
    Interface <|.. Implementation : implements
    Component --> Implementation : uses
```

### Relationship Types

```mermaid
classDiagram
    A <|-- B : Inheritance
    C *-- D : Composition
    E o-- F : Aggregation
    G <-- H : Association
    I <|.. J : Realization
    K ..> L : Dependency
    M -- N : Link
```

**Use**:
- Inheritance: Subclass relationships
- Composition: "Has-a" (strong ownership)
- Aggregation: "Has-a" (weak ownership)
- Dependency: Uses temporarily

---

## State Diagrams

**Purpose**: Show state transitions

**Syntax**: `stateDiagram-v2`

### Example

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Success : complete
    Processing --> Failed : error
    Success --> [*]
    Failed --> Retry : retry
    Retry --> Processing
    Failed --> [*] : give up
    
    state Processing {
        [*] --> Validate
        Validate --> Transform
        Transform --> Save
        Save --> [*]
    }
```

**Best Practices**:
- Start/end with `[*]`
- Label transitions clearly
- Use composite states for complex processes
- Keep flat (avoid deep nesting)

---

## Entity Relationship Diagrams

**Purpose**: Show database schema relationships

**Syntax**: `erDiagram`

### Example

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    
    USER {
        int id PK
        string email UK
        string name
    }
    
    ORDER {
        int id PK
        int user_id FK
        datetime created_at
        decimal total
    }
    
    LINE_ITEM {
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }
    
    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

### Cardinality

```
||--|| : One to One
||--o{ : One to Many
}o--o{ : Many to Many
}|--|{ : One or More to One or More
```

---

## General Best Practices

### Complexity Management

**Keep diagrams focused**:
- Max 10-12 nodes (architecture/flow)
- Max 5-6 participants (sequence)
- Max 8-10 classes (class diagram)

**If too complex**:
- Split into multiple diagrams (by layer, by feature)
- Use "..." to indicate omitted components
- Create overview + detail diagrams

### Labeling

**Good labels**:
- Descriptive: "User Service" not "Service1"
- Consistent: Same terminology as codebase
- Concise: 2-4 words maximum
- Action-oriented for edges: "validates", "sends", "queries"

**Bad labels**:
- Generic: "Component A", "Thing"
- Verbose: "The service that handles user authentication and authorization"
- Inconsistent: "UserSvc" in one place, "User Service" in another

### Layout

**Direction selection**:
- `TD` (top-down): Hierarchies, flows with clear start/end
- `LR` (left-right): Timelines, pipelines, sequences
- `BT` (bottom-up): Rarely used, avoid unless specific need
- `RL` (right-left): Rarely used, avoid unless specific need

**Spacing**: Mermaid auto-layouts, but you can influence:
- Group related components together in code
- Use subgraphs for logical grouping
- Minimize edge crossings (order nodes thoughtfully)

### Styling

**When to use**:
- Highlight different component types (frontend, backend, data)
- Distinguish critical paths
- Show error/success states

**How**:
```mermaid
graph TD
    A[Normal]:::highlight
    B[Also Highlighted]:::highlight
    
    classDef highlight fill:#ffeb3b,stroke:#f57f17,stroke-width:3px
```

**Don't overdo it**: Max 3-4 style classes per diagram

---

## Diagram Type Selection

| Need | Diagram Type | Use When |
|------|--------------|----------|
| System components | graph TD/LR | Showing architecture layers, services |
| Process flow | flowchart | Showing workflow, decision logic |
| Interactions | sequenceDiagram | API calls, message passing |
| Class structure | classDiagram | OOP design, interfaces |
| State changes | stateDiagram-v2 | Lifecycle, status transitions |
| Data model | erDiagram | Database schema, entities |

---

## Validation Checklist

**Before finalizing diagram**:
- [ ] Renders without syntax errors
- [ ] All nodes have clear labels
- [ ] Direction appropriate for content
- [ ] Complexity manageable (<12 nodes)
- [ ] Terminology matches codebase
- [ ] Edge labels clear (where applicable)
- [ ] Styling enhances (not distracts)
- [ ] Legend included if needed

---

## Common Syntax Errors

**Avoid**:
```mermaid
graph TD
    A --> B[Missing arrow direction]  ❌
    C ->D[Wrong arrow syntax]  ❌
    E[Unclosed bracket  ❌
    F(Mismatched parens]  ❌
```

**Correct**:
```mermaid
graph TD
    A --> B[Proper syntax]  ✅
    C --> D[Another node]  ✅
    E[Closed properly]  ✅
    F(Matched parens)  ✅
```

**Special characters**: Use quotes for labels with special chars:
```mermaid
graph TD
    A["Label with: special chars!"]
    B["Another [bracketed] label"]
```

---

## Quick Reference

### Arrows
- `-->` : Solid arrow
- `-.->` : Dotted arrow
- `==>` : Thick arrow
- `--text-->` : Labeled arrow

### Nodes
- `[text]` : Rectangle
- `(text)` : Rounded
- `([text])` : Stadium
- `[[text]]` : Subroutine
- `[(text)]` : Database
- `((text))` : Circle
- `{text}` : Diamond
- `{{text}}` : Hexagon

### Subgraphs
```mermaid
graph TD
    subgraph "Title"
        A --> B
    end
```
