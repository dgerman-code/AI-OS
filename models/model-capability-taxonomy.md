# Model Capability Taxonomy

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Why a taxonomy rather than prose

A Model Profile that describes capability in prose cannot be matched against a requirement. "Good at analysis" and "needs analytical depth" are the same sentence twice, and no rule can be written over them. The taxonomy exists so that a Workflow stage, a Review Profile or a Routing Policy can state a requirement in the **same vocabulary** a profile uses to make a claim, and so eligibility can be determined rather than argued.

**A capability is a named dimension on which a claim may be made and evidence may be offered.** It is not a score, not a ranking, and not a promise.

## 2. Capability families

| ID | Capability | What a claim on it means |
|---|---|---|
| `capability.general_reasoning` | General reasoning | Coherent multi-step inference on ordinary material |
| `capability.advanced_reasoning` | Advanced reasoning | Sustained multi-step inference where an error early invalidates the result |
| `capability.long_context_analysis` | Long-context analysis | Holding a large body of material in one pass **and using its distant parts** — not merely accepting it |
| `capability.coding` | Coding | Producing working code in the languages declared |
| `capability.code_review` | Code review | Finding defects in code, which is a different act from writing it |
| `capability.mathematical_reasoning` | Mathematical reasoning | Quantitative derivation where arithmetic and method both matter |
| `capability.structured_extraction` | Structured extraction | Pulling declared fields out of unstructured material |
| `capability.structured_generation` | Structured generation / schema adherence | Emitting output that conforms to a declared shape, **every time and not usually** |
| `capability.document_analysis` | Document analysis | Working over documents as documents — layout, tables, cross-references |
| `capability.vision` | Vision | Interpreting images |
| `capability.multimodal_reasoning` | Multimodal reasoning | Reasoning **across** modalities, not merely accepting several |
| `capability.multilingual` | Multilingual | Working in the declared languages at the declared level |
| `capability.summarisation` | Summarisation | Compression that preserves what mattered |
| `capability.research_synthesis` | Research synthesis | Combining many sources into a position, with the sources still traceable |
| `capability.planning` | Planning | Decomposing work into ordered steps with dependencies |
| `capability.tool_calling` | Tool calling | Selecting and invoking declared tools appropriately |
| `capability.structured_tool_use` | Structured / function tool use | Tool invocation conforming to declared signatures |
| `capability.low_latency_interaction` | Low-latency interaction | Responsiveness suitable for conversational use |
| `capability.high_reliability_output` | High-reliability constrained output | Conformance under adversarial or unusual input, not just typical input |
| `capability.large_file_handling` | Large-file handling | Ingesting large artifacts without silent truncation |
| `capability.instruction_fidelity` | Instruction fidelity | Doing what was asked, including the constraints, including the negative ones |
| `capability.citation_evidence_handling` | Citation / evidence handling | Attributing claims to sources without inventing the attribution |
| `capability.safety_sensitive_handling` | Safety-sensitive handling | Appropriate behaviour on material where error carries physical, legal or welfare consequence |

Twenty-three families. The list is extensible by governed amendment; a Routing Policy may not invent a capability inline, because a requirement nothing can claim is a requirement nothing can satisfy.

### `capability.privacy_sensitive_suitability` was removed

The first draft listed it and conceded in its own description that it was "a deployment and contractual property as much as a model one". The audit was right: **it duplicated a provider and deployment governance decision as a model capability**, and a capability token that can be satisfied by signing a contract is not a capability.

Privacy suitability is now expressed only where it is actually determined — on the **Deployment Profile**, as supported sensitivity labels, handling controls and effective posture, tested by `SUPPORTED_SENSITIVITY_CLASSES`, `REQUIRED_HANDLING_CONTROLS` and `REQUIRED_DATA_HANDLING_POSTURE` (`models/routing-constraint-model.md` §3).

**No intrinsic model capability is being hidden by this removal.** Were one to be identified later — a genuine technical property of a model bearing on privacy-preserving processing — it would be named narrowly for that property and kept explicitly distinct from contractual and data-handling eligibility. Nothing currently evidenced requires it.

**No capability token duplicates a provider or deployment governance decision**, and this is the rule the removal establishes.

## 3. Capability classes

A claim is made at a **class**, not a score:

```
NOT_CLAIMED  <  BASELINE  <  STRONG  <  SPECIALISED
```

| Class | Meaning |
|---|---|
| `NOT_CLAIMED` | No claim is made. **Not a claim of absence** — nobody has asserted or evidenced anything |
| `BASELINE` | Usable for ordinary work in this dimension |
| `STRONG` | Usable where this dimension is the difficulty of the task |
| `SPECIALISED` | Claimed as a distinguishing strength, with evidence proportionate to the claim |

**`NOT_CLAIMED` is not `NOT_CAPABLE`.** A profile that has never been evaluated for vision is not a profile that fails at vision, and a requirement for vision is unsatisfied by it either way — but the record must not assert a finding nobody made. Where a limitation is actually known, it is recorded as a **limitation** (§5), not as a low class.

## 4. A claim is not a truth

**A capability claim is a claim.** It carries evidence and a confidence, and it becomes eligibility only through a Routing Policy that says which evidence classes and which confidence it accepts (`models/evaluation-evidence-model.md`).

Four rules hold everywhere:

1. **A provider's assertion is evidence of a provider's assertion.** It is admissible and it is not proof.
2. **A benchmark score is not authority.** It is evidence about a benchmark, whose relationship to the work is itself a claim.
3. **Confidence does not create eligibility.** High confidence in a claim about `capability.coding` does not make a model eligible for work that also requires `capability.structured_generation` — and it reaches no deployment-governed requirement at all, since those are not capabilities (§2).
4. **A capability claim never becomes canonical knowledge** and is never evidence about the world. It is evidence about a tool.

## 5. Limitations and prohibited contexts

Every Model Profile carries **known limitations** and **prohibited contexts** as first-class content, separate from its capability claims.

- A **limitation** is an observed or declared weakness — a failure mode, a degradation at some boundary, a condition under which claims do not hold.
- A **prohibited context** is a bounded use the profile must not be routed to at all, whatever its capability claims say.

A limitation **narrows** a claim; a prohibited context **overrides** it. A profile claiming `SPECIALISED` document analysis and prohibiting use on personal data is exactly consistent, and the prohibition wins wherever both apply.

## 6. What the taxonomy deliberately does not do

It produces **no composite score, no ranking and no ordering of models.** There is no "best model" expressible in this vocabulary, by construction: a profile is a vector of claims across twenty-three dimensions with evidence of differing classes and ages, and collapsing that to one number would discard exactly the information a routing decision needs.

It also defines no benchmark, no test, no evaluation procedure and no threshold. Thresholds belong to Routing Policies, which state what they require; evidence semantics belong to `models/evaluation-evidence-model.md`.

## 7. Status

`PROPOSED`. Declares no model, names no provider, implements nothing.
