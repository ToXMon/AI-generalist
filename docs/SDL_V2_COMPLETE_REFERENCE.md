# Akash SDL v2.0 - Complete Reference & Your Deployment Fix

## Executive Summary

Your Akash deployment files had **2 critical validation errors**:

1. **Wrong deployment syntax**: Using array syntax instead of nested objects
2. **Duplicated placement section**: Placement was incorrectly placed inside the deployment section

Both files have been **corrected** and are now ready for deployment.

---

## Part 1: SDL v2.0 Complete Structure

### High-Level Architecture

```
SDL v2.0 File Structure:
├── version: "2.0"
├── services: {}           ← Container definitions
├── profiles:
│   ├── compute: {}       ← Resource requirements
│   └── placement: {}     ← Pricing & attributes
└── deployment: {}        ← Service-to-Profile mapping
```

### The Three Critical Sections Explained

#### 1. SERVICES - What containers to run

```yaml
services:
  frontend:                    # Service name
    image: frontend:v1.0       # Docker image
    expose:                    # Network exposure
      - port: 80              # Container port
        as: 80                # Exposed as
        to:
          - global: true      # Public (or: - service: backend)
    env:                       # Environment variables
      - KEY=value
    depends_on:                # Dependencies
      - backend
```

**Key Points**:
- One `services:` section for all containers
- Services can reference each other by name
- `depends_on` declares ordering requirements
- `expose` controls network access (public vs. private)

---

#### 2. PROFILES - Resource specs and pricing

This section has TWO parts:

**Part A: Compute Profiles** (Resources)
```yaml
profiles:
  compute:
    frontend-profile:        # Profile name
      resources:
        cpu:
          units: "0.5"       # CPU cores (0.1 = 100m)
        memory:
          size: "512Mi"      # RAM (Mi or Gi)
        storage:
          size: "512Mi"      # Disk space (Mi or Gi)
```

**Part B: Placement Profiles** (Where & Cost)
```yaml
  placement:
    global:                  # Placement name
      attributes:            # Optional provider requirements
        host: akash
        region: us
      pricing:               # Bid prices per compute profile
        frontend-profile:
          denom: uakt
          amount: "10000"    # uAKT per block (6 sec)
        backend-profile:
          denom: uakt
          amount: "20000"
```

**Key Points**:
- Compute profiles define resources needed per service
- Placement profiles define bid amounts for compute profiles
- Placement can have multiple entries (different bids/providers)
- Pricing is PER BLOCK (6 seconds), not per day

**Pricing Examples**:
```
10,000 uAKT/block = ~144 AKT/day ≈ $1.44 USD/day (at $0.01/AKT)
20,000 uAKT/block = ~288 AKT/day ≈ $2.88 USD/day
5,000 uAKT/block = ~72 AKT/day ≈ $0.72 USD/day
```

---

#### 3. DEPLOYMENT - Link services to profiles

This section maps:
- **Service name** → What to run
- **Placement name** → Where to run it (which bid pricing)
- **Compute profile** → How many resources
- **Count** → How many instances

```yaml
deployment:
  service_name:              # Service from services: section
    placement_name:          # Placement from profiles.placement:
      profile: profile_name  # Compute profile from profiles.compute:
      count: 1               # Number of instances
```

**Example with multiple services**:
```yaml
deployment:
  frontend:
    global:
      profile: frontend-profile
      count: 1
  backend:
    global:
      profile: backend-profile
      count: 1
  mongo:
    global:
      profile: db-profile
      count: 1
```

---

## Part 2: Complete Correct Example

Here's a fully correct, production-ready SDL v2.0 file:

```yaml
---
version: "2.0"

# ============================================================
# SECTION 1: SERVICES - Define containers
# ============================================================
services:
  frontend:
    image: docker.io/youruser/frontend:v1.0
    expose:
      - port: 80
        as: 80
        to:
          - global: true         # Publicly accessible
    env:
      - REACT_APP_BACKEND_URL=http://backend:8000
    depends_on:
      - backend                  # Runs after backend

  backend:
    image: docker.io/youruser/backend:v1.0
    expose:
      - port: 8000
        as: 8000
        to:
          - service: frontend    # Only accessible from frontend
    env:
      - DATABASE_URL=mongodb://mongo:27017
      - REDIS_URL=redis://redis:6379
      - API_KEY=${API_KEY}       # Use environment variable
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:latest
    expose:
      - port: 27017
        as: 27017
        to:
          - service: backend     # Only from backend
    env:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secure_password_here

  redis:
    image: redis:latest
    expose:
      - port: 6379
        as: 6379
        to:
          - service: backend     # Only from backend


# ============================================================
# SECTION 2: PROFILES - Resources and pricing
# ============================================================
profiles:
  # Compute: What resources each service needs
  compute:
    frontend-profile:
      resources:
        cpu:
          units: "0.5"           # Half a CPU
        memory:
          size: "512Mi"          # 512 Mebibytes
        storage:
          size: "512Mi"          # 512 MB disk

    backend-profile:
      resources:
        cpu:
          units: "1.0"           # 1 full CPU
        memory:
          size: "1Gi"            # 1 Gigabyte
        storage:
          size: "1Gi"            # 1 GB disk

    db-profile:
      resources:
        cpu:
          units: "0.5"
        memory:
          size: "512Mi"
        storage:
          size: "5Gi"            # More storage for database

    cache-profile:
      resources:
        cpu:
          units: "0.25"          # Quarter CPU
        memory:
          size: "256Mi"          # 256 MB RAM
        storage:
          size: "512Mi"

  # Placement: Where to deploy and how much to bid
  placement:
    global:                       # Global placement (any provider)
      pricing:                    # Bid prices
        frontend-profile:
          denom: uakt
          amount: "10000"         # uAKT per block
        backend-profile:
          denom: uakt
          amount: "20000"
        db-profile:
          denom: uakt
          amount: "15000"
        cache-profile:
          denom: uakt
          amount: "5000"

    # Optional: Region-specific placement
    us-only:
      attributes:
        region: us               # US providers only
      pricing:
        frontend-profile:
          denom: uakt
          amount: "8000"         # Bid lower for specific region


# ============================================================
# SECTION 3: DEPLOYMENT - Service to Profile mapping
# ============================================================
deployment:
  frontend:
    global:                      # Use 'global' placement
      profile: frontend-profile  # Use 'frontend-profile' compute profile
      count: 1                   # 1 instance

  backend:
    global:
      profile: backend-profile
      count: 1

  mongo:
    global:
      profile: db-profile
      count: 1

  redis:
    global:
      profile: cache-profile
      count: 1
```

---

## Part 3: Common Mistakes & How to Fix Them

### ❌ Mistake 1: Array Syntax in Deployment

**WRONG**:
```yaml
deployment:
  frontend:
    - profile: frontend-profile
      count: 1
```

**RIGHT**:
```yaml
deployment:
  frontend:
    global:                    # Placement name as key (not array)
      profile: frontend-profile
      count: 1
```

**Why**: SDL v2.0 uses object nesting, not arrays, for service deployment.

---

### ❌ Mistake 2: Duplicating Placement in Deployment

**WRONG**:
```yaml
profiles:
  placement:
    global:
      pricing: {...}

deployment:
  frontend:
    global:
      profile: frontend-profile
      count: 1
  placement:                     # ← WRONG! Don't duplicate
    global:
      pricing: {...}
```

**RIGHT**:
```yaml
profiles:
  placement:
    global:
      pricing: {...}

deployment:
  frontend:
    global:                     # Just reference, don't redefine
      profile: frontend-profile
      count: 1
```

**Why**: Placement is defined once in `profiles.placement`. The `deployment` section only references it.

---

### ❌ Mistake 3: Wrong Expose Syntax

**WRONG**:
```yaml
expose:
  - port: 8000
    to: global: true           # ← Syntax error
```

**RIGHT**:
```yaml
expose:
  - port: 8000
    as: 8000
    to:
      - global: true           # ← Correct: list structure
```

---

### ❌ Mistake 4: Profile Name Mismatches

**WRONG**:
```yaml
profiles:
  compute:
    web-profile:               # Defined as 'web-profile'
      resources: {...}

deployment:
  frontend:
    global:
      profile: frontend-profile  # ← Mismatch! Should be 'web-profile'
```

**RIGHT**:
```yaml
profiles:
  compute:
    frontend-profile:          # Consistent naming
      resources: {...}

deployment:
  frontend:
    global:
      profile: frontend-profile  # ← Matches
```

---

### ❌ Mistake 5: Missing Compute Profile Pricing

**WRONG**:
```yaml
profiles:
  compute:
    my-profile:
      resources: {...}

  placement:
    global:
      pricing:
        other-profile:         # ← Not defined in compute!
          denom: uakt
          amount: "10000"
```

**RIGHT**:
```yaml
profiles:
  compute:
    my-profile:
      resources: {...}

  placement:
    global:
      pricing:
        my-profile:            # ← Matches compute profile
          denom: uakt
          amount: "10000"
```

---

### ❌ Mistake 6: Wrong Memory/Storage Units

**WRONG**:
```yaml
memory:
  size: "512M"    # M is not valid
storage:
  size: "1G"      # G is not valid
```

**RIGHT**:
```yaml
memory:
  size: "512Mi"   # Mebibytes (binary)
storage:
  size: "1Gi"     # Gibibytes (binary)
```

**Units Reference**:
- `256Mi` = 256 Mebibytes (256 × 1024 × 1024 bytes)
- `1Gi` = 1 Gibibyte (1024 × 1024 × 1024 bytes)
- Always use `Mi` or `Gi` notation

---

### ❌ Mistake 7: Forgetting Placement in Deployment

**WRONG**:
```yaml
deployment:
  frontend:
    profile: frontend-profile  # ← Missing placement key!
    count: 1
```

**RIGHT**:
```yaml
deployment:
  frontend:
    global:                    # ← Placement name required
      profile: frontend-profile
      count: 1
```

---

## Part 4: Your Deployment Files - BEFORE & AFTER

### What Was Wrong

**File**: `/workspaces/AI-generalist/deployment/akash-deploy.yaml`

**Problem 1**: Array syntax in deployment section
```yaml
# ❌ WRONG
deployment:
  frontend:
    - profile: frontend-profile      # Array syntax
      count: 1
      placement: global
```

**Problem 2**: Duplicated placement section
```yaml
  placement:                          # Shouldn't be here!
    global:
      pricing:
        frontend-profile:
          denom: uakt
          amount: "10000"
```

### The Fix

```yaml
# ✅ CORRECT
deployment:
  frontend:
    global:                          # Object, not array
      profile: frontend-profile
      count: 1
  backend:
    global:
      profile: backend-profile
      count: 1
  # No placement: section here
```

---

## Part 5: Pre-Deployment Validation Checklist

Before deploying to Akash, verify:

### Structure Checks
- [ ] File starts with `---` and `version: "2.0"`
- [ ] Four main sections exist: `services`, `profiles`, `deployment`
- [ ] No syntax errors (proper YAML indentation)

### Services Checks
- [ ] Every service has `image`, `expose`, `env`
- [ ] All service names are valid (alphanumeric, hyphens, underscores)
- [ ] Expose ports are valid (1-65535)
- [ ] `depends_on` references existing services

### Profiles Checks
- [ ] Every compute profile has `cpu`, `memory`, `storage` under `resources`
- [ ] CPU units are valid decimals (0.1, 0.5, 1.0, etc.)
- [ ] Memory/storage use `Mi` or `Gi` (not `M` or `G`)
- [ ] Every placement profile has `pricing` entries
- [ ] All pricing entries reference existing compute profiles
- [ ] All pricing amounts are in `uakt` denomination

### Deployment Checks
- [ ] Every service name in deployment exists in `services:`
- [ ] Every placement name in deployment exists in `profiles.placement:`
- [ ] Every compute profile reference exists in `profiles.compute:`
- [ ] No array syntax (no dashes before `profile:`)
- [ ] No `placement:` section inside `deployment:`

### Content Checks
- [ ] All image names are correct and accessible
- [ ] All environment variables are set (or use `${}` placeholders)
- [ ] No hardcoded credentials (use environment variables)
- [ ] Resource requests are reasonable for your workload

---

## Part 6: Testing Your SDL

### Option 1: Akash Console Validation
1. Go to https://console.akash.network
2. Paste your YAML
3. Console will highlight any validation errors

### Option 2: Akash CLI Validation
```bash
akash tx deployment create akash-deploy.yaml --from mykey --dry-run
```

### Option 3: YAML Linter
```bash
# Install yamllint
pip install yamllint

# Check your file
yamllint akash-deploy.yaml
```

---

## Part 7: Deployment Workflow

```
1. Create SDL file (akash-deploy.yaml)
   ↓
2. Validate syntax (console or CLI)
   ↓
3. Create deployment on Akash
   akash deployment create akash-deploy.yaml
   ↓
4. View bids from providers
   akash deployment bids <deployment-id>
   ↓
5. Accept a bid
   akash deployment lease <deployment-id> <bid-id>
   ↓
6. Monitor deployment
   akash provider lease-logs <provider> <deployment-id> <lease-id>
   ↓
7. Get your domain
   akash provider lease-status <provider> <deployment-id> <lease-id>
   ↓
8. Update if needed
   akash deployment update <deployment-id> akash-deploy.yaml
   ↓
9. Close when done
   akash deployment close <deployment-id>
```

---

## Part 8: Resources & Documentation

| Resource | URL |
|----------|-----|
| **Official Akash Docs** | https://docs.akash.network |
| **SDL Specification** | https://docs.akash.network/readme/stack-definition-language |
| **Akash Console** | https://console.akash.network |
| **Awesome Akash** | https://github.com/akash-network/awesome-akash |
| **Community Discord** | https://discord.gg/akash |

---

## Summary

**Your files have been fixed and are now SDL v2.0 compliant.**

| Aspect | Status |
|--------|--------|
| Services section | ✅ Correct |
| Profiles section | ✅ Correct |
| Deployment section | ✅ Fixed |
| Syntax | ✅ Valid |
| Ready to deploy | ✅ Yes |

**Next Steps**:
1. Update image tags and environment variables as needed
2. Validate in Akash Console
3. Create deployment on Akash Network
4. Monitor logs and access your application
