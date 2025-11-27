# Akash SDL v2.0 - Quick Reference Card

## SDL File Structure at a Glance

```
version: "2.0"
├── services:
│   └── service_name:
│       ├── image: ...
│       ├── expose: [{port, as, to}]
│       ├── env: [KEY=VALUE]
│       └── depends_on: [service_names]
│
├── profiles:
│   ├── compute:
│   │   └── profile_name:
│   │       └── resources: {cpu, memory, storage}
│   │
│   └── placement:
│       └── placement_name:
│           ├── attributes: {key: value}
│           └── pricing:
│               └── profile_name: {denom, amount}
│
└── deployment:
    └── service_name:
        └── placement_name:
            ├── profile: profile_name
            └── count: N
```

---

## One-Page SDL v2.0 Template

```yaml
---
version: "2.0"

services:
  app:
    image: yourregistry/yourapp:tag
    expose:
      - port: 3000
        as: 3000
        to:
          - global: true
    env:
      - NODE_ENV=production
      - API_KEY=${API_KEY}

profiles:
  compute:
    app-profile:
      resources:
        cpu:
          units: "1.0"
        memory:
          size: "1Gi"
        storage:
          size: "1Gi"

  placement:
    global:
      pricing:
        app-profile:
          denom: uakt
          amount: "20000"

deployment:
  app:
    global:
      profile: app-profile
      count: 1
```

---

## Critical Dos & Don'ts

### ✅ DO

- ✅ Use object syntax in deployment (not arrays)
- ✅ Define placement ONCE in `profiles.placement:`
- ✅ Reference placement in deployment, don't duplicate
- ✅ Use `Mi` and `Gi` for memory/storage
- ✅ Use `global:` or named placement in deployment
- ✅ Match profile names exactly across sections
- ✅ Include `as:` in expose sections

### ❌ DON'T

- ❌ Use array syntax in deployment (`- profile:`)
- ❌ Put `placement:` inside `deployment:` section
- ❌ Use `M` or `G` for units (must be `Mi` or `Gi`)
- ❌ Reference non-existent profiles or services
- ❌ Omit the placement key in deployment
- ❌ Duplicate placement definitions
- ❌ Mix old v1 syntax with v2.0

---

## Common Patterns

### Pattern 1: Simple Web App
```yaml
services:
  web:
    image: myimage:latest
    expose: [{port: 80, as: 80, to: [{global: true}]}]

profiles:
  compute:
    web-profile:
      resources:
        cpu: {units: "0.5"}
        memory: {size: "512Mi"}
        storage: {size: "512Mi"}
  placement:
    global:
      pricing:
        web-profile: {denom: uakt, amount: "10000"}

deployment:
  web:
    global:
      profile: web-profile
      count: 1
```

### Pattern 2: Frontend + Backend
```yaml
services:
  frontend:
    image: frontend:latest
    expose: [{port: 80, as: 80, to: [{global: true}]}]
    depends_on: [backend]

  backend:
    image: backend:latest
    expose: [{port: 8000, as: 8000, to: [{service: frontend}]}]

profiles:
  compute:
    frontend-profile:
      resources: {cpu: {units: "0.5"}, memory: {size: "512Mi"}, storage: {size: "512Mi"}}
    backend-profile:
      resources: {cpu: {units: "1.0"}, memory: {size: "1Gi"}, storage: {size: "1Gi"}}
  placement:
    global:
      pricing:
        frontend-profile: {denom: uakt, amount: "10000"}
        backend-profile: {denom: uakt, amount: "20000"}

deployment:
  frontend:
    global:
      profile: frontend-profile
      count: 1
  backend:
    global:
      profile: backend-profile
      count: 1
```

### Pattern 3: Multi-Placement Strategy
```yaml
deployment:
  app:
    us-only:              # US bid
      profile: app-profile
      count: 1
    global:               # Global fallback
      profile: app-profile
      count: 1

profiles:
  placement:
    us-only:
      attributes: {region: us}
      pricing: {app-profile: {denom: uakt, amount: "15000"}}
    global:
      pricing: {app-profile: {denom: uakt, amount: "20000"}}
```

---

## Resource Size Examples

| Use Case | CPU | Memory | Storage | Daily Cost |
|----------|-----|--------|---------|-----------|
| Static site | 0.1 | 128Mi | 256Mi | ~$0.07 |
| Small API | 0.5 | 512Mi | 512Mi | ~$0.36 |
| Node.js app | 1.0 | 1Gi | 1Gi | ~$0.72 |
| Database | 2.0 | 2Gi | 5Gi | ~$1.44 |
| Full stack | 2.0 | 3Gi | 3Gi | ~$1.44 |

*Approximate costs (varies by provider and AKT price)*

---

## Environment Variables

### Setting Inline
```yaml
env:
  - DATABASE_URL=postgresql://localhost
  - NODE_ENV=production
```

### Using Placeholders
```yaml
env:
  - DATABASE_URL=${DATABASE_URL}  # Set at deployment time
  - API_KEY=${API_KEY}
```

---

## Port Exposure Types

### Public (Internet Accessible)
```yaml
expose:
  - port: 80
    as: 80
    to:
      - global: true
```

### Private (Service-to-Service)
```yaml
expose:
  - port: 8000
    as: 8000
    to:
      - service: frontend
      - service: other-service
```

### Multiple Exposures
```yaml
expose:
  - port: 80
    as: 80
    to: [{global: true}]           # Public HTTP
  - port: 443
    as: 443
    to: [{global: true}]           # Public HTTPS
  - port: 5432
    as: 5432
    to: [{service: backend}]       # Private DB
```

---

## Pricing Quick Calc

```
uAKT per block × 14,400 blocks/day = Daily cost in uAKT
÷ 1,000,000 = Daily cost in AKT

Examples:
10,000 × 14,400 = 144,000,000 uAKT = 144 AKT/day ≈ $1.44
20,000 × 14,400 = 288,000,000 uAKT = 288 AKT/day ≈ $2.88
5,000 × 14,400 = 72,000,000 uAKT = 72 AKT/day ≈ $0.72
```

---

## Validation Checklist

- [ ] `version: "2.0"` at the top
- [ ] Three sections: services, profiles, deployment
- [ ] All service names are referenced in deployment
- [ ] All profile names match between sections
- [ ] Deployment uses object syntax (not arrays)
- [ ] No `placement:` inside `deployment:`
- [ ] All units use `Mi` or `Gi`
- [ ] All pricing in `uakt`
- [ ] No duplicate section definitions

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Invalid SDL format" | Array syntax in deployment | Use object syntax: `placement_name:` not `-` |
| "Unknown profile" | Profile name mismatch | Match names exactly across sections |
| "Invalid resource" | Wrong units (M, G) | Use `Mi` and `Gi` |
| "Placement not found" | Missing from profiles | Define in `profiles.placement:` |
| "Service not found" | Typo in deployment | Match service name exactly |

---

## Key Differences: v1 vs v2.0

| Aspect | v1 | v2.0 |
|--------|-----|------|
| Deployment syntax | Service-based groups | Service → Profile mapping |
| Structure | Flatter | More nested |
| Placement | Inline with services | Separate section |
| Pricing | Per service | Per compute profile |
| Validation | Lenient | Strict schema |

---

## Resources

- **Docs**: https://docs.akash.network/readme/stack-definition-language
- **Examples**: https://github.com/akash-network/awesome-akash
- **Console**: https://console.akash.network
- **CLI**: https://docs.akash.network/guides/cli
