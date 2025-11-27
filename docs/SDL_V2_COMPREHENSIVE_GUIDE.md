# Akash SDL v2.0 Comprehensive Guide

## Overview

Akash SDL (Stack Definition Language) v2.0 is used to define containerized applications for deployment on the Akash Network. This guide covers the correct structure, syntax, and best practices based on official Akash documentation.

---

## 1. SDL v2.0 Complete Structure Overview

```yaml
---
version: "2.0"

# 1. SERVICES SECTION - Defines the containers to run
services:
  service_name:
    image: image:tag
    expose:
      - port: CONTAINER_PORT
        as: EXPOSED_PORT
        to:
          - global: true  # OR specific service: service_name
    env:
      - KEY=value
    depends_on:
      - other_service

# 2. PROFILES SECTION - Defines compute and placement configurations
profiles:
  # 2a. COMPUTE PROFILES - Resource requirements
  compute:
    profile_name:
      resources:
        cpu:
          units: "0.5"
        memory:
          size: "512Mi"
        storage:
          size: "512Mi"
  
  # 2b. PLACEMENT PROFILES - Where and how much to bid
  placement:
    placement_name:
      attributes:
        key: value
      pricing:
        profile_name:
          denom: uakt
          amount: "10000"

# 3. DEPLOYMENT SECTION - Links services to profiles and placement
deployment:
  service_name:
    placement_name:
      profile: profile_name
      count: 1
```

---

## 2. Detailed Section Breakdown

### 2.1 SERVICES Section

**Purpose**: Define containerized applications

**Key Points**:
- Each service represents a container
- Services can communicate via `expose` section
- Order of services matters for `depends_on`

**Example - Frontend Service**:
```yaml
services:
  frontend:
    image: docker.io/your-username/frontend:v1.0
    expose:
      - port: 80           # Container port
        as: 80             # Exposed port (usually same)
        to:
          - global: true   # Publicly accessible
    env:
      - REACT_APP_API_URL=http://backend:8000
```

**Example - Backend Service**:
```yaml
  backend:
    image: docker.io/your-username/backend:v1.0
    expose:
      - port: 8000
        as: 8000
        to:
          - service: frontend  # Only accessible from frontend
    env:
      - DATABASE_URL=mongodb://mongo:27017
    depends_on:
      - mongo
```

**Expose Options**:
```yaml
expose:
  - port: 8000                    # Container port
    as: 8000                      # Exposed port
    to:
      - global: true              # Public: Anyone on Internet
      # OR
      - service: other_service    # Private: Only another service
```

---

### 2.2 PROFILES Section

**Purpose**: Define resource requirements and placement pricing

#### 2.2a Compute Profiles

**Structure**:
```yaml
profiles:
  compute:
    profile_name:
      resources:
        cpu:
          units: "0.5"       # 0.1 to n CPUs, decimals allowed
        memory:
          size: "512Mi"      # RAM: 128Mi to nGi
        storage:
          size: "512Mi"      # Disk: 512Mi to nGi
```

**Resource Guidelines**:
- **CPU units**: 0.1 = 100 millicores, 1.0 = 1 full CPU
- **Memory sizes**: Use Mi (Mebibytes), Gi (Gibibytes) notation
- **Storage**: Persistent storage allocated to the service

**Example - Development Profile**:
```yaml
compute:
  dev-profile:
    resources:
      cpu:
        units: "0.25"
      memory:
        size: "256Mi"
      storage:
        size: "256Mi"
```

**Example - Production Profile**:
```yaml
compute:
  prod-profile:
    resources:
      cpu:
        units: "2.0"
      memory:
        size: "4Gi"
      storage:
        size: "2Gi"
```

#### 2.2b Placement Profiles

**Structure**:
```yaml
placement:
  placement_name:
    attributes:              # Optional: Provider requirements
      key: value
    pricing:                 # Bid amounts per profile
      profile_name:
        denom: uakt         # Token denomination (always uakt)
        amount: "10000"     # uAKT per block (6 sec)
```

**Attributes** (optional):
```yaml
attributes:
  host: akash              # Standard Akash provider
  region: us               # Region (if available)
  tier: community          # Provider tier
```

**Pricing Calculation**:
- Amounts are in **uAKT** (micro-AKT)
- Calculated per **block** (6 seconds)
- Daily cost ≈ amount × 14,400 blocks/day
- Example: 10,000 uAKT/block × 14,400 = 144,000,000 uAKT/day ≈ $0.14/day

**Example - Global Placement**:
```yaml
placement:
  global:
    pricing:
      frontend-profile:
        denom: uakt
        amount: "10000"
      backend-profile:
        denom: uakt
        amount: "20000"
```

---

### 2.3 DEPLOYMENT Section

**Purpose**: Links services to compute profiles and placement profiles

**⚠️ CRITICAL - Most Common Mistakes Here**

#### CORRECT Structure (v2.0):
```yaml
deployment:
  service_name:
    placement_name:
      profile: compute_profile_name
      count: number_of_instances
```

#### Structure Breakdown:
```yaml
deployment:
  frontend:              # ← Service name (from services section)
    global:             # ← Placement name (from profiles.placement)
      profile: frontend-profile  # ← Compute profile (from profiles.compute)
      count: 1           # ← Number of instances
```

**Complete Example**:
```yaml
deployment:
  # Deploy frontend service
  frontend:
    global:              # Use 'global' placement
      profile: frontend-profile
      count: 1
  
  # Deploy backend service
  backend:
    global:              # Use 'global' placement
      profile: backend-profile
      count: 1
  
  # Deploy database service
  mongo:
    global:
      profile: db-profile
      count: 1
```

**Multiple Placements Example**:
```yaml
deployment:
  frontend:
    global:              # Global placement
      profile: frontend-profile
      count: 1
    us-only:             # US-specific placement
      profile: frontend-profile
      count: 1
```

---

## 3. COMPLETE CORRECT EXAMPLE

```yaml
---
version: "2.0"

# ============================================================
# SECTION 1: SERVICES
# ============================================================
services:
  frontend:
    image: docker.io/myusername/frontend:v1.0
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - REACT_APP_BACKEND_URL=http://backend:8000

  backend:
    image: docker.io/myusername/backend:v1.0
    expose:
      - port: 8000
        as: 8000
        to:
          - service: frontend
    env:
      - DATABASE_URL=mongodb://mongo:27017
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:latest
    expose:
      - port: 27017
        as: 27017
        to:
          - service: backend
    env:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password123

  redis:
    image: redis:latest
    expose:
      - port: 6379
        as: 6379
        to:
          - service: backend

# ============================================================
# SECTION 2: PROFILES
# ============================================================
profiles:
  # Compute profiles: Define resource requirements
  compute:
    frontend-profile:
      resources:
        cpu:
          units: "0.5"
        memory:
          size: "512Mi"
        storage:
          size: "512Mi"
    
    backend-profile:
      resources:
        cpu:
          units: "1.0"
        memory:
          size: "1Gi"
        storage:
          size: "1Gi"
    
    db-profile:
      resources:
        cpu:
          units: "0.5"
        memory:
          size: "512Mi"
        storage:
          size: "2Gi"  # More storage for database
    
    cache-profile:
      resources:
        cpu:
          units: "0.25"
        memory:
          size: "256Mi"
        storage:
          size: "512Mi"

  # Placement profiles: Where and how much to bid
  placement:
    global:
      pricing:
        frontend-profile:
          denom: uakt
          amount: "10000"    # Per block (6 sec)
        backend-profile:
          denom: uakt
          amount: "20000"
        db-profile:
          denom: uakt
          amount: "10000"
        cache-profile:
          denom: uakt
          amount: "5000"

# ============================================================
# SECTION 3: DEPLOYMENT
# ============================================================
deployment:
  # Frontend deployment
  frontend:
    global:
      profile: frontend-profile
      count: 1
  
  # Backend deployment
  backend:
    global:
      profile: backend-profile
      count: 1
  
  # Database deployment
  mongo:
    global:
      profile: db-profile
      count: 1
  
  # Cache deployment
  redis:
    global:
      profile: cache-profile
      count: 1
```

---

## 4. COMMON MISTAKES TO AVOID

### ❌ MISTAKE 1: Wrong Deployment Structure

**WRONG** (uses array syntax):
```yaml
deployment:
  frontend:
    - profile: frontend-profile  # ← Array syntax, WRONG!
      count: 1
      placement: global
```

**CORRECT** (nested object):
```yaml
deployment:
  frontend:
    global:                       # ← Placement name as key
      profile: frontend-profile
      count: 1
```

---

### ❌ MISTAKE 2: Duplicating Placement in Deployment

**WRONG** (placement defined twice):
```yaml
profiles:
  placement:
    global:
      pricing:
        # ...

deployment:
  placement:              # ← DON'T duplicate placement here!
    global:
      pricing:
        # ...
```

**CORRECT** (placement referenced, not duplicated):
```yaml
profiles:
  placement:
    global:
      pricing:
        # ...

deployment:
  frontend:
    global:             # ← Just reference the placement name
      profile: frontend-profile
      count: 1
```

---

### ❌ MISTAKE 3: Pricing in Wrong Section

**WRONG** (pricing in compute):
```yaml
profiles:
  compute:
    frontend-profile:
      resources:
        # ...
      pricing:           # ← WRONG location!
        denom: uakt
        amount: "10000"
```

**CORRECT** (pricing in placement):
```yaml
profiles:
  placement:
    global:
      pricing:           # ← CORRECT location!
        frontend-profile:
          denom: uakt
          amount: "10000"
```

---

### ❌ MISTAKE 4: Mismatched Profile Names

**WRONG** (profile name mismatch):
```yaml
profiles:
  compute:
    web-profile:        # ← Defined as 'web-profile'
      resources: ...

deployment:
  frontend:
    global:
      profile: frontend-profile  # ← Referenced as 'frontend-profile' - MISMATCH!
```

**CORRECT** (consistent naming):
```yaml
profiles:
  compute:
    frontend-profile:   # ← Defined as 'frontend-profile'
      resources: ...

deployment:
  frontend:
    global:
      profile: frontend-profile  # ← Same name - CORRECT!
```

---

### ❌ MISTAKE 5: Missing Service Dependencies

**WRONG** (backend needs mongo but not listed):
```yaml
services:
  backend:
    image: backend:latest
    # No depends_on!
    env:
      - DATABASE_URL=mongodb://mongo:27017
```

**CORRECT** (dependencies declared):
```yaml
services:
  backend:
    image: backend:latest
    depends_on:
      - mongo           # ← Explicit dependency
    env:
      - DATABASE_URL=mongodb://mongo:27017
```

---

### ❌ MISTAKE 6: Wrong Expose Syntax

**WRONG**:
```yaml
expose:
  - port: 8000
    to: global: true    # ← Syntax error
```

**CORRECT**:
```yaml
expose:
  - port: 8000
    as: 8000
    to:
      - global: true    # ← Correct structure
```

---

### ❌ MISTAKE 7: Inconsistent Resource Units

**WRONG** (mixed units):
```yaml
profiles:
  compute:
    profile1:
      resources:
        memory:
          size: "512M"   # ← Should be Mi, Gi, not M
```

**CORRECT** (proper units):
```yaml
profiles:
  compute:
    profile1:
      resources:
        memory:
          size: "512Mi"  # ← Mebibytes format
```

---

## 5. VALIDATION CHECKLIST

Before deploying, verify:

- [ ] **Version**: File starts with `version: "2.0"`
- [ ] **Services**: Each service has `image`, `expose`, `env`
- [ ] **Compute Profiles**: All have `cpu`, `memory`, `storage` under `resources`
- [ ] **Placement Profiles**: All pricing amounts in uAKT
- [ ] **Deployment**: 
  - [ ] References valid service names
  - [ ] References valid placement names
  - [ ] References valid compute profile names
  - [ ] All pricing entries match compute profiles
- [ ] **Naming**: No mismatches between sections
- [ ] **Dependencies**: Services with `depends_on` are correctly referenced

---

## 6. YAML Formatting Rules

1. **Indentation**: Use 2 spaces (not tabs)
2. **Colons**: Space after `:` in key-value pairs
3. **Dashes**: Use `-` for lists, space after `-`
4. **Quotes**: Use `"` for string values with special characters
5. **Dashes in names**: Allowed and recommended

---

## 7. Resource Sizing Guide

| Profile | CPU | Memory | Storage | Use Case |
|---------|-----|--------|---------|----------|
| **Tiny** | 0.1 | 128Mi | 256Mi | Static content, CDN edge |
| **Small** | 0.5 | 512Mi | 512Mi | Frontend, small APIs |
| **Medium** | 1.0 | 1Gi | 1Gi | Backend services |
| **Large** | 2.0 | 2Gi | 5Gi | Databases, heavy processing |
| **XLarge** | 4.0+ | 4Gi+ | 10Gi+ | Big data, ML models |

---

## 8. Pricing Estimation

```
Daily Cost = (amount_per_block × 14,400 blocks/day) / 1,000,000 uAKT per AKT

Examples:
- 10,000 uAKT/block = ~144 AKT/day ≈ $1.44/day (at $0.01/AKT)
- 20,000 uAKT/block = ~288 AKT/day ≈ $2.88/day
- 5,000 uAKT/block = ~72 AKT/day ≈ $0.72/day
```

---

## 9. Official References

- **Akash Docs**: https://docs.akash.network/
- **SDL Specification**: https://docs.akash.network/readme/stack-definition-language
- **Awesome Akash**: https://github.com/akash-network/awesome-akash
- **CLI Guide**: https://docs.akash.network/guides/cli

---

## Summary Table

| Section | Contains | Links To |
|---------|----------|----------|
| **services** | Container definitions | Used by `deployment` |
| **profiles.compute** | Resource specs | Used by `deployment` as `profile` |
| **profiles.placement** | Bid amounts & attributes | Used by `deployment` as placement name |
| **deployment** | Service→Profile mapping | References services and profiles |

**Deployment Flow**:
```
Service (frontend)
    ↓
Deployment references Service "frontend"
    ↓
Deployment links to Placement "global"
    ↓
Deployment links to Compute Profile "frontend-profile"
    ↓
Placement has pricing for "frontend-profile"
    ↓
Compute Profile has resource requirements
```
