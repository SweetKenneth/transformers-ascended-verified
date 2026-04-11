# Ascension Integration

---

## Overview

The Ascension Engine lets you upload working source code and have the substrate's 40-primitive matrix discover, augment, and export enhanced capabilities. This guide covers the developer workflow.

---

## Requirements

- **Creator tier** or above
- API key with `ascension` scope
- Source files in any of 90+ supported languages

---

## Workflow

### 1. Upload

```bash
# Via CLI
cmpsbl ascension upload ./my-trading-bot.py

# Via API
curl -X POST https://api.cmpsbl.com/api/v1/ascension/upload \
  -H "Authorization: Bearer pf_live_xxx" \
  -F "file=@my-trading-bot.py"
```

### 2. Monitor Discovery

```bash
# Check status
cmpsbl ascension status <discovery-id>

# Or watch in real-time
cmpsbl ascension watch <discovery-id>
```

The 40-primitive matrix tests your code. Each primitive asks whether your code's behavior combines meaningfully with its capabilities. Results include:

- **CJPI Score** — novelty, utility, complexity, composability
- **Execution trace** — exactly which primitives participated
- **Execution strategy** — native, bridge, or simulated

### 3. Export

```bash
cmpsbl ascension export <discovery-id> --format zip
```

The export contains:
1. Original source code (untouched)
2. Convex Core™ Processing Layer
3. Cognitive layer (substrate augmentations)
4. Auto-generated documentation
5. Test bench

---

## Supported Languages (90+ extensions)

**Web / Scripting (16):** JavaScript, TypeScript, Python, Ruby, PHP, Lua, Perl, R, Julia, Groovy, CoffeeScript, Elm, PureScript, Racket, Scheme, Lisp

**Systems (8):** Rust, Go, C, C++, Zig, Nim, Crystal, D

**JVM (4):** Java, Kotlin, Scala, Clojure

**.NET (4):** C#, F#, Visual Basic, PowerShell

**Apple / Mobile (3):** Swift, Dart, Objective-C

**Functional (5):** Haskell, OCaml, Erlang, Elixir, PureScript

**Blockchain (5):** Solidity, Vyper, Move, Cairo, Fe

**Hardware Description (7):** VHDL, Verilog, SystemVerilog, Chisel, Bluespec, SPICE, FIRRTL

**Scientific / HPC (4):** Fortran, MATLAB, Mathematica, Wolfram

**Shell (4):** Bash, Zsh, Fish, Batch

**GPU / Shaders (6):** GLSL, HLSL, WGSL, CUDA, OpenCL, Metal

**Infrastructure (6):** Terraform/HCL, Protobuf, SQL, GraphQL, Prisma, Dockerfile

**WebAssembly (2):** WAT, WAST

---

## Execution Strategies

| Strategy | When Used | How It Works |
|----------|----------|-------------|
| **Native** | JavaScript/TypeScript | Code runs directly in substrate runtime |
| **Bridge** | Other languages | Substrate wraps execution, captures I/O |
| **Simulated** | HDL / edge cases | Behavioral modeling of code patterns |

---

## Best Practices

1. **Upload working code** — Ascension evolves functional software, not broken scripts
2. **Use descriptive file names** — helps the discovery engine understand context
3. **Start with familiar code** — verify discoveries against known behavior
4. **Check execution traces** — understand exactly what the substrate found
5. **Review exported capabilities** — verify the augmented code matches your expectations

---

© 2025–2026 CMPSBL®. All rights reserved.
