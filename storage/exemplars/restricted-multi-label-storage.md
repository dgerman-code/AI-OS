# Exemplar 4 — Restricted material, three locations, three different answers

Status: PROPOSED — Phase 10 exemplar storage record
Inherits: `standard.storage.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that storage eligibility is a **multi-label subset test on the location**, not a comparison against a ceiling — and that unknown support is not support.

## The artifact

`artifact.works_council_case_file`, scope `project.gamma`.

**Sensitivity labels: {`PERSONAL_DATA`, `CONFIDENTIAL`, `THIRD_PARTY_RESTRICTED`}.** Three labels, three independent obligation sets. **Phase 8 orders none of them, and Phase 10 introduces no order.**

Residency: allowed jurisdictions, two named; cross-border `FORBIDDEN`. Required handling controls per label. Required posture: no retention beyond the retention class, no secondary use.

## The same bytes, three candidate locations

| Location | Eligible? | Why |
|---|---|---|
| `bkt.public_shared` | **No** | Approved for {`PUBLIC`, `INTERNAL`} — **none** of the three required labels |
| `bkt.governed.eu` | **Yes** | Approved for all three, **each explicitly**; handling controls met per label; in the allowed jurisdiction set with cross-border `FORBIDDEN`; posture satisfied |
| `bkt.regional.enterprise` | **No** | Approved for {`CONFIDENTIAL`, `TRADE_SECRET`, `PERSONAL_DATA`} — **`THIRD_PARTY_RESTRICTED` is unassessed.** Unknown support is not support |

## The row that carries the lesson

**The third.** It would pass a ceiling test — a test **no** part of this architecture defines. A location approved for `PERSONAL_DATA` looks like the strictest of the three it holds, and under a ceiling model it would be eligible while being **unassessed for `THIRD_PARTY_RESTRICTED`**, whose obligations arise from someone else's terms entirely.

**Support for one label implies support for no other**, and no label outranks another by being "higher", because there is no higher. This is Phase 9's exemplar-4 reasoning applied to storage without modification, and it is applied without modification on purpose: a second sensitivity model would be a second answer to the same question.

## Metadata centrally, payload not

The **artifact record** — identity, labels, provenance, lineage, retention class — is held in the operational database with the rest of the `artifact` domain. The **payload** is not: it sits only at `bkt.governed.eu`, and it is not copied to a lower environment, a derived report, a backup outside the approved regime, or an export.

The distinction is deliberate. Knowing that a restricted object exists, who produced it and what cites it is what makes governance possible; holding its contents everywhere that knowledge travels is what makes governance fail.

## If no location were eligible

**BLOCK.** There is no nearest-approved location, no partial eligibility and no "best available" — the outcome would be a recorded block naming the unsatisfiable combination, exactly as Phase 9 blocks routing. An outage at `bkt.governed.eu` would not change this: failure mode 12 is explicit that unavailability never makes a non-compliant location acceptable.
