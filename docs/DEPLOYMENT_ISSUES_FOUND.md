# Issues Found in Your Akash Deployment Files

## Critical Issues

### 1. **DEPLOYMENT SECTION: Wrong Syntax Structure**

**Location**: `deployment:` section in both files

**Problem**: Using array syntax instead of nested object syntax

```yaml
# ❌ CURRENT (WRONG)
deployment:
  frontend:
    - profile: frontend-profile      # ← Array syntax, not valid!
      count: 1
      placement: global

  backend:
    - profile: backend-profile       # ← Array syntax, not valid!
      count: 1
      placement: global
```

**Reason**: SDL v2.0 expects nested object structure where placement is a key, not an array.

**Fix**:
```yaml
# ✅ CORRECT
deployment:
  frontend:
    global:                          # ← Placement name as key
      profile: frontend-profile
      count: 1

  backend:
    global:                          # ← Placement name as key
      profile: backend-profile
      count: 1
```

---

### 2. **DEPLOYMENT SECTION: Duplicating Placement**

**Location**: Bottom of `deployment:` section

**Problem**: The `placement:` key appears within `deployment:` section

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
  placement:                         # ← SHOULD NOT BE HERE!
    global:
      attributes:
        host: akash
      pricing:
        frontend-profile:
          denom: uakt
          amount: "10000"
        backend-profile:
          denom: uakt
          amount: "20000"
```

**Reason**: 
- Placement is defined in `profiles.placement:` section
- The `deployment:` section should only map services to placements
- Duplicating placement here causes validation errors

**Fix**: Remove the `placement:` subsection from `deployment:` entirely

---

## Summary of All Issues

| Issue | Location | Status | Fix |
|-------|----------|--------|-----|
| Array syntax in deployment | `deployment.frontend/backend` | CRITICAL | Use object syntax with placement as key |
| Duplicated placement section | Bottom of `deployment:` | CRITICAL | Remove entirely |
| Missing `as:` in expose | N/A | OK | Your files are correct |
| Profile naming | OK | OK | frontend-profile and backend-profile are correct |
| Pricing amounts | OK | OK | 10000 and 20000 are valid |

---

## Validation Errors These Issues Cause

1. **YAML Parse Error**: Array syntax doesn't match schema
2. **Schema Validation Failure**: Placement should not be in deployment
3. **Akash Console Error**: "Invalid SDL format"
4. **CLI Error**: "deployment validation failed"

---

## File-by-File Issues

### `/workspaces/AI-generalist/deployment/akash-deploy.yaml`

**Issues**:
1. Lines 54-63: Array syntax `- profile:` should be object `placement_name:`
2. Lines 64-74: Remove entire `placement:` subsection

### `/workspaces/AI-generalist/deployment/akash-deploy-console.yaml`

**Issues**: Same as above (if present)

---

## How to Fix

The deployment section should be:

```yaml
deployment:
  frontend:
    global:                    # placement name (from profiles.placement)
      profile: frontend-profile  # compute profile (from profiles.compute)
      count: 1               # number of instances

  backend:
    global:                    # placement name (from profiles.placement)
      profile: backend-profile   # compute profile (from profiles.compute)
      count: 1               # number of instances
```

**Nothing else should be in the `deployment:` section.**

---

## Verification Checklist

After fixing, verify:

```yaml
---
version: "2.0"                 # ✅ Correct

services:
  # ✅ All services defined

profiles:
  compute:
    # ✅ All profiles defined
  placement:
    # ✅ All placements with pricing

deployment:
  service_name:
    placement_name:            # ✅ No array, uses placement as key
      profile: profile_name    # ✅ References compute profile
      count: 1                 # ✅ Instance count
  # ✅ NO placement: section here
```
