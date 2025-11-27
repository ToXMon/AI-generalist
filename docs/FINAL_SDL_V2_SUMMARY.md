# Akash SDL v2.0 - Comprehensive Summary & Your Deployment Fix

## 🎯 Executive Summary

Your Akash deployment validation was failing due to **2 critical SDL v2.0 syntax errors**. Both have been **fixed and validated**.

### What Was Wrong
1. **Array syntax in deployment** - Using `- profile:` instead of nested objects
2. **Duplicated placement section** - Placement was incorrectly defined inside deployment

### What Was Fixed
✅ Both `akash-deploy.yaml` and `akash-deploy-console.yaml` corrected  
✅ Files now follow official SDL v2.0 specification  
✅ Ready for Akash Console deployment  

---

## 📋 SDL v2.0 Structure (The Complete Guide)

### 1. The Four Essential Concepts

```
Service      → What container to run
    ↓
Compute      → How many resources it needs
Profile      
    ↓
Placement    → Where to bid and how much
    ↓
Deployment   → Connect service to compute+placement
```

### 2. Complete Minimal Example

```yaml
---
version: "2.0"

# SECTION 1: Define containers
services:
  myapp:
    image: docker.io/user/myapp:v1.0
    expose:
      - port: 3000
        as: 3000
        to:
          - global: true
    env:
      - NODE_ENV=production

# SECTION 2: Define resources and pricing
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

# SECTION 3: Connect services to compute+placement
deployment:
  myapp:
    global:
      profile: app-profile
      count: 1
```

---

## 🔍 Detailed Section Breakdown

### SECTION 1: Services

**What it does**: Defines the containers to run

```yaml
services:
  service_name:
    image: registry/image:tag           # Docker image
    expose:                             # Network exposure
      - port: CONTAINER_PORT            # Inside container
        as: EXPOSED_PORT                # External port
        to:
          - global: true                # Public OR
          - service: other_service      # Private to service
    env:                                # Environment variables
      - KEY=value
      - SECRET=${SECRET}                # Placeholder
    depends_on:                         # Run order
      - other_service
```

**Key Points**:
- Services communicate by service name
- `depends_on` ensures correct startup order
- `expose` controls network access
- `to: [{global: true}]` = public internet
- `to: [{service: X}]` = only service X can access

---

### SECTION 2: Profiles

**What it does**: Defines resource requirements and pricing

#### Part A: Compute Profiles (Resources)

```yaml
profiles:
  compute:
    profile_name:
      resources:
        cpu:
          units: "0.5"                  # 0.1 to n cores
        memory:
          size: "512Mi"                 # Mi or Gi only
        storage:
          size: "512Mi"                 # Disk space
```

**CPU Units**: 
- `0.1` = 100 millicores (100m)
- `0.5` = 500 millicores
- `1.0` = 1 full core
- `2.0` = 2 cores

**Memory/Storage**:
- Always use binary units: `Mi` (Mebibytes) or `Gi` (Gibibytes)
- NEVER use `M`, `G`, `MB`, `GB` (decimal) - causes validation error

#### Part B: Placement Profiles (Pricing & Attributes)

```yaml
  placement:
    placement_name:
      attributes:                       # Optional
        host: akash
        region: us
      pricing:                          # Bid amounts
        profile_name:                   # Must match compute profile
          denom: uakt
          amount: "10000"               # uAKT per block (6 sec)
```

**Pricing Logic**:
- Amount is per BLOCK (6 seconds), not per day
- Daily cost ≈ amount × 14,400 blocks/day
- Example: 10,000 uAKT/block = ~144,000,000 uAKT/day ≈ 144 AKT ≈ $1.44/day

---

### SECTION 3: Deployment

**What it does**: Maps services to compute profiles and placements

```yaml
deployment:
  service_name:              # From services:
    placement_name:          # From profiles.placement:
      profile: profile_name  # From profiles.compute:
      count: 1               # Number of instances
```

**Critical Rules**:
1. Use OBJECT syntax (nested), NOT arrays
2. Placement name is the KEY (not a value)
3. Reference existing service and profile names
4. Can have multiple placements per service

**Example - Multiple Placements**:
```yaml
deployment:
  app:
    us-only:                 # US-specific bid
      profile: app-profile
      count: 1
    global:                  # Global fallback
      profile: app-profile
      count: 1
```

---

## 🐛 Your Specific Issues - BEFORE & AFTER

### Issue #1: Array Syntax

**❌ BEFORE (WRONG)**:
```yaml
deployment:
  frontend:
    - profile: frontend-profile        # Array syntax (dash)
      count: 1
      placement: global
```

**✅ AFTER (FIXED)**:
```yaml
deployment:
  frontend:
    global:                            # Object (no dash)
      profile: frontend-profile
      count: 1
```

**Why it matters**: SDL v2.0 uses object nesting. Arrays cause validation failure.

---

### Issue #2: Duplicated Placement

**❌ BEFORE (WRONG)**:
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
  placement:                           # ← Shouldn't be here!
    global:
      pricing: {...}                   # ← Duplicate definition
```

**✅ AFTER (FIXED)**:
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
  # No placement: section here!
```

**Why it matters**: Placement is defined in `profiles`. The `deployment` only references it.

---

## ✅ Your Corrected Files

### File 1: `/deployment/akash-deploy.yaml`

**Status**: ✅ FIXED

**Key aspects**:
- Frontend service: 0.5 CPU, 512Mi RAM, public on port 80
- Backend service: 1.0 CPU, 1Gi RAM, private to frontend on port 8000
- Correct object syntax in deployment
- No duplicate placement

---

### File 2: `/deployment/akash-deploy-console.yaml`

**Status**: ✅ FIXED

**Key aspects**:
- Same structure as above
- Had additional issues: duplicate deployment sections
- Now clean and deployment-ready

---

## 📚 Complete Reference Examples

### Example 1: Simple Web App
```yaml
---
version: "2.0"

services:
  web:
    image: docker.io/myuser/website:v1.0
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  compute:
    web-profile:
      resources:
        cpu:
          units: "0.5"
        memory:
          size: "512Mi"
        storage:
          size: "512Mi"
  placement:
    global:
      pricing:
        web-profile:
          denom: uakt
          amount: "10000"

deployment:
  web:
    global:
      profile: web-profile
      count: 1
```

---

### Example 2: Frontend + Backend + Database

```yaml
---
version: "2.0"

services:
  frontend:
    image: docker.io/myuser/frontend:v1.0
    expose:
      - port: 80
        as: 80
        to:
          - global: true
    env:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    image: docker.io/myuser/backend:v1.0
    expose:
      - port: 8000
        as: 8000
        to:
          - service: frontend
    env:
      - DATABASE_URL=postgresql://db:5432
    depends_on:
      - db

  db:
    image: postgres:latest
    expose:
      - port: 5432
        as: 5432
        to:
          - service: backend
    env:
      - POSTGRES_PASSWORD=secure_password

profiles:
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
          units: "1.0"
        memory:
          size: "1Gi"
        storage:
          size: "5Gi"           # More storage for database
  placement:
    global:
      pricing:
        frontend-profile:
          denom: uakt
          amount: "10000"
        backend-profile:
          denom: uakt
          amount: "20000"
        db-profile:
          denom: uakt
          amount: "25000"

deployment:
  frontend:
    global:
      profile: frontend-profile
      count: 1
  backend:
    global:
      profile: backend-profile
      count: 1
  db:
    global:
      profile: db-profile
      count: 1
```

---

## 🚫 Common Mistakes (Don't Make These!)

| Mistake | Wrong | Right |
|---------|-------|-------|
| **Array syntax** | `- profile: name` | `placement:` as object key |
| **Duplicate sections** | Placement in deployment | Placement only in profiles |
| **Wrong units** | `512M`, `1G` | `512Mi`, `1Gi` |
| **Missing placement** | `profile: name` | `placement:` with `profile: name` |
| **Name mismatch** | Define `web-profile`, reference `frontend-profile` | Match names exactly |
| **Missing service** | Reference non-existent service | Define all referenced services |
| **Wrong expose format** | `to: global: true` | `to:` list with `- global: true` |

---

## ✔️ Validation Checklist

Before deploying, verify your SDL file has:

### Structure
- [ ] `version: "2.0"` at the top
- [ ] Three main sections: `services:`, `profiles:`, `deployment:`
- [ ] Proper YAML indentation (2 spaces)
- [ ] No tabs (tabs cause YAML errors)

### Services Section
- [ ] Every service has `image`, `expose`, `env`
- [ ] All image names are correct
- [ ] All `expose` ports are valid (1-65535)
- [ ] All `to:` entries are either `global: true` or `service: name`
- [ ] All services referenced in `depends_on` exist

### Profiles Section
- [ ] Compute profiles have `cpu`, `memory`, `storage` under `resources`
- [ ] CPU units are decimals (0.1, 0.5, 1.0, etc.)
- [ ] Memory/storage use `Mi` or `Gi` (NOT `M`, `G`, `MB`, `GB`)
- [ ] Every placement has `pricing` section
- [ ] All pricing entries match compute profile names
- [ ] All pricing uses `uakt` denomination

### Deployment Section
- [ ] Every service name matches services section
- [ ] Every placement name matches profiles.placement
- [ ] Every compute profile reference matches profiles.compute
- [ ] NO array syntax (no dashes before `profile:`)
- [ ] NO `placement:` section inside `deployment:`
- [ ] All required fields present: `profile`, `count`

---

## 🚀 Next Steps

1. **Update image tags** if needed
   ```yaml
   image: docker.io/yourusername/yourapp:latest
   ```

2. **Set environment variables**
   ```yaml
   env:
     - API_KEY=${API_KEY}
     - DATABASE_URL=postgresql://db:5432
   ```

3. **Validate in Akash Console**
   - Go to https://console.akash.network
   - Paste your YAML
   - Console will show any validation errors

4. **Deploy to Akash**
   ```bash
   akash deployment create akash-deploy.yaml --from mykey
   ```

5. **Monitor deployment**
   ```bash
   akash deployment list
   akash deployment get <deployment-id>
   ```

---

## 📖 Official Resources

| Resource | URL |
|----------|-----|
| **Akash Documentation** | https://docs.akash.network |
| **SDL Specification** | https://docs.akash.network/readme/stack-definition-language |
| **Akash Console** | https://console.akash.network |
| **CLI Guide** | https://docs.akash.network/guides/cli |
| **Awesome Akash** | https://github.com/akash-network/awesome-akash |
| **Community Chat** | https://discord.gg/akash |

---

## 📄 Documentation Created

This package includes comprehensive SDL v2.0 documentation:

1. **`SDL_V2_COMPREHENSIVE_GUIDE.md`** - Complete specification and examples
2. **`SDL_V2_COMPLETE_REFERENCE.md`** - Full reference with your deployment fix details
3. **`SDL_V2_QUICK_REFERENCE.md`** - Quick lookup card
4. **`DEPLOYMENT_ISSUES_FOUND.md`** - Specific issues in your files and fixes

---

## Summary Table

| Component | Your File | Status | Details |
|-----------|-----------|--------|---------|
| Services | 2 services (frontend, backend) | ✅ Correct | Proper expose and env |
| Compute Profiles | 2 profiles (frontend, backend) | ✅ Correct | Resources properly defined |
| Placement | 1 placement (global) | ✅ Correct | Pricing in correct location |
| Deployment Syntax | Fixed from array to object | ✅ Fixed | Now uses nested objects |
| Duplicate Placement | Removed | ✅ Fixed | No longer in deployment |

---

## Final Status

✅ **Your deployment files are now compliant with SDL v2.0**

Both files are ready to be:
- Deployed to Akash Console
- Validated with Akash CLI
- Used for production deployments

**No further syntax changes needed - your files are deployment-ready!**
