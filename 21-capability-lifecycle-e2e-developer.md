# CMPSBL® Capability Lifecycle — Developer Reference

**Version:** v2.1.0  
**Date:** April 11, 2026  
**Classification:** PUBLIC — Developer Documentation  
**Author:** CMPSBL®

---

## 1. Overview

Every capability CMPSBL discovers in your code follows a strict 5-stage lifecycle. This lifecycle ensures that every claim in your export artifacts — reports, scores, certificates — is backed by evidence at the appropriate level.

This document explains the lifecycle end-to-end so you know exactly what your artifacts contain and what action (if any) is required on your part.

---

## 2. The 5-Stage Lifecycle

When CMPSBL processes your source code through Ascension, each discovered primitive progresses through these stages:

| Stage | What Happens | Your Action |
|-------|-------------|-------------|
| **1. Detected** | The scanner identifies structural signals in your code that match a primitive's signature. | None — automatic. |
| **2. Generated** | Layer 2 orchestration code is produced — wrappers that can provide governance, resilience, and observability for the matched capability. | None — automatic. |
| **3. Bound** | The generated wrappers are structurally linked to specific function boundaries in your original source. Your code (Layer 1) is never modified. | None — automatic. |
| **4. Activated** | The wrappers are integrated into a runtime environment and confirmed to be executing. | **You do this** — by integrating the exported artifact into your application. |
| **5. Behaviorally Verified** | Observable effects (state changes, interception, telemetry) are confirmed through deterministic probes. | **You do this** — by running the included verification script after integration. |

### Key Principle

**Stages 1–3 happen automatically during Ascension.** Stages 4–5 require you to integrate the artifact and run verification. Your export reports will always be honest about which stage each primitive has reached.

---

## 3. What's in Your Export

Every Ascension export includes lifecycle-aware artifacts:

### Capability Activation Ledger (`capability-ledger.json`)

A machine-readable JSON file that records the exact state of every primitive in your artifact. Each entry includes:

- **State**: The highest confirmed lifecycle stage
- **Targets**: Which functions in your code are wrapped
- **Evidence**: Machine-readable proof of each stage reached
- **Gaps**: What has NOT been proven — explicitly listed, never hidden

This ledger is the single source of truth. All reports and scores are derived from it.

### Reports

Generated reports are **constrained** by the ledger. Claims in your report are validated against evidence:

- If a primitive is **Bound but not Activated**, the report will say "Wrapper generated and structurally bound" — never "capability enabled" or "protection active."
- If a primitive is **Activated but not Behaviorally Verified**, the report will say "Runtime activation confirmed" — never "behavior verified."
- Only **Behaviorally Verified** primitives can carry unrestricted claims.

### CJPI Score (Decomposed)

Your CJPI score is broken into 5 transparent components:

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Structural | 25% | Were primitives detected and code generated? |
| Binding | 25% | Are wrappers structurally attached to your code? |
| Activation | 25% | Are wrappers executing at runtime? |
| Behavioral | 20% | Are observable effects confirmed? |
| Security | 5% | Are security-specific primitives behaviorally proven? |

If your artifact has not been integrated (Stages 4–5 incomplete), your CJPI score will include a "structural only" qualifier. This is not a limitation — it's honesty about what has been proven.

### Activation Guide (`ACTIVATION_GUIDE.html`)

A step-by-step guide showing you exactly how to move each primitive from its current state to full activation. Each entry includes:

- **Current state** and **target state**
- **Activation mode**: Automatic (nothing to do), Assisted (copy-paste a few lines), or Manual (integration work required)
- **Code snippets** — copy-paste ready
- **Before vs. after** behavior comparison
- **Verification instructions** — how to confirm activation worked
- **Safety notes** — rollback instructions if needed

### Verification Script (`RUN_VERIFICATION.ts`)

A self-contained script you run after integration to verify your artifact's integrity. It performs 4 checks:

1. **Fingerprint verification** — Confirms the artifact hasn't been tampered with
2. **Primitive coverage** — Confirms every expected primitive was tested (fail-closed — no silent omissions)
3. **Tamper detection** — Warns if unexpected primitives appear (injection detection)
4. **Delta summary** — Shows expected vs. observed primitive counts for quick assessment

---

## 4. Integration Workflow

```
Step 1: Run Ascension on your source code
        → Receive export ZIP with lifecycle artifacts
        → Primitives are at Stage 3 (Bound)

Step 2: Review your Activation Guide
        → Identify which primitives need manual integration
        → Most are Automatic or Assisted

Step 3: Integrate the artifact into your application
        → Follow the guide's code snippets
        → Primitives advance to Stage 4 (Activated)

Step 4: Run the Verification Script
        → Confirms runtime behavior
        → Primitives advance to Stage 5 (Behaviorally Verified)
        → Your CJPI score updates to reflect full coverage
```

---

## 5. What CMPSBL Guarantees

| Guarantee | Details |
|-----------|---------|
| **Layer 1 integrity** | Your original source code is never modified. SHA-256 hash is computed at intake and embedded in the proof certificate. Tampering is detectable. |
| **Deterministic classification** | Same source code + same engine version = same results. Always. |
| **Honest reporting** | Reports never claim more than the ledger can prove. Gaps are explicit. |
| **Zero post-export dependency** | Your exported artifact runs standalone. No callbacks, no license servers, no subscriptions required. |
| **Inspectable output** | The generated Layer 2 code is readable. You can inspect every wrapper, every dispatch entry. |

---

## 6. What CMPSBL Does NOT Do

- **Does not execute your code during scanning.** Analysis is structural/static.
- **Does not guarantee runtime outcomes without integration.** Wrappers are structural until you activate them.
- **Does not require external AI.** The Ascension engine uses zero external AI calls. All classification is deterministic.
- **Does not store your code for training.** Source code is stored in session records for retrieval only.

---

## 7. Reading Your Verification Results

When you run `RUN_VERIFICATION.ts`, you'll see output like:

```
━━━ CMPSBL® Artifact Verification ━━━━━━━━━━━
Fingerprint: abc123...
Expected primitives: 12

✓ Fingerprint verified: identity bound to execution

🔍 Probe Delta:
   Expected: 12
   Observed: 12
   Extra:    0

✓ 12/12 primitives behaviorally verified
✓ 12/12 primitives accounted for (fail-closed)
```

**If you see mismatches:**

- **Fingerprint mismatch** → The artifact has been modified since export. Re-export from Ascension.
- **Missing primitives** → Some primitives weren't tested. Check your integration matches the Activation Guide.
- **Unexpected probes** → Additional primitives appeared at runtime that weren't in the original export. This may indicate environmental interference — review your runtime dependencies.
- **Extra > 0** → Not necessarily an error, but worth investigating. The delta summary helps you assess quickly.

---

## 8. Verification Model

CMPSBL verification has two independent components:

### Provenance Verification

Confirms your artifact's origin and integrity:
- Artifact was produced by the CMPSBL Ascension engine
- Original source code hasn't been modified (SHA-256)
- Declared primitives were bound at stated chain positions
- CJPI scores were computed deterministically

### Behavioral Verification

Confirms runtime behavior through deterministic probes:
- Wrappers are executing (interception confirmed)
- Observable effects are occurring (state changes, telemetry)
- Each primitive's claimed capability is actually happening

Both are required for full verification. Provenance without behavior proves origin but not function. Behavior without provenance proves function but not origin.

---

## 9. Generic Activation (Universal Baseline)

Every primitive — not just the 12 specialized ones — can reach full Activated and Behaviorally Verified status through the **Generic Primitive Activation Engine**.

If a primitive doesn't have a specialized runtime (like DEFENSE or GOVERNANCE do), a universal wrapper is applied automatically:

1. **Import** `wrapGeneric` from `@cmpsbl/runtime/generic-wrapper`
2. **Wrap** your target function: `const wrapped = wrapGeneric('PRIMITIVE_NAME', yourFunction)`
3. **Run** `npx ts-node RUN_VERIFICATION.ts` to confirm activation

The generic wrapper:
- Observes every call (emits `call_interception`)
- Emits telemetry after execution (emits `telemetry_emit`)
- **Never alters** original function behavior
- **Never blocks** execution
- Is fully reversible — remove the wrap call to restore original behavior

Specialized primitives (DEFENSE, MEMORY, BEACON, etc.) still use their richer, hand-written activation logic. The generic engine is the baseline that ensures nothing gets stuck.

---

## 10. Patent Attribution

CMPSBL artifacts are protected under two U.S. patent applications:

- **U.S. Patent App. No. 64/029,678** — "Autonomous Primitive-Based Code Hardening Without Source Modification"
- **U.S. Patent App. No. 64/031,637** — "Governed Silent Software Symbiosis via Behavioral Proxy Attachment"

Inventor: Kenneth E. Sweet Jr.

---

*© 2025–2026 CMPSBL®. All rights reserved.*
