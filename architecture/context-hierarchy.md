# Context Hierarchy

Status: PROPOSED

AI-OS must distinguish durable organisational context from project-specific and task-specific context.

```text
GLOBAL
│
├── ORGANISATION
│   ├── PERMANENT FUNCTION / BUSINESS AREA
│   ├── PROGRAMME / PORTFOLIO
│   │   └── PROJECT
│   │       └── WORKSTREAM
│   │           └── TASK
│   ├── PROJECT
│   │   └── WORKSTREAM
│   │       └── TASK
│   ├── PRODUCT / PLATFORM
│   │   └── WORKSTREAM
│   │       └── TASK
│   └── OPERATIONAL WORKSTREAM
│       └── TASK
│
├── INDEPENDENT BUSINESS / VENTURE
│   └── PROJECT / PRODUCT / WORKSTREAM / TASK
│
└── PERSONAL / AD-HOC INITIATIVE
    └── WORKSTREAM / TASK
```

## Canonical knowledge classes

The system must distinguish at minimum:

- FACT
- SOURCE
- ASSUMPTION
- CALCULATION
- AI_SUGGESTION
- DRAFT
- REVIEWED
- APPROVED
- CANONICAL
- SUPERSEDED
- CONFLICT_DETECTED
- UNKNOWN

An AI suggestion must never become canonical automatically.
