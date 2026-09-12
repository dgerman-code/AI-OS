# Exemplar 4 — A cancellation, and two results that arrive afterwards

Status: PROPOSED — Phase 11 exemplar execution run
Inherits: `standard.orchestration.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders.

**Proves:** that a late result is recorded rather than applied — and that a late **review** result and a late **decision** result are not the same case, because one is an assessment and the other is an exercise of authority.

## The run

`run.2026.tender_response.0355` · `workflow.tender_response` @ v3 · scope `project.eta` · criticality **Enhanced Decision-Grade**.

At 14:02 a human cancelled it: the tender was withdrawn by the counterparty. `intervention.0912` recorded the person, the act, the reason and the resulting state. Run: `WAITING` → **`CANCELLED`**.

Two things were in flight.

## The late model result — race 8, then race 9

A routing request had been submitted at 13:47. `rd.2026.tender.0771` returned at 14:06, with produced content.

**Outcome: `IGNORE_AS_STALE`.** The Routing Decision is recorded against the Model Invocation Request that asked for it — it is a true record of what the Router decided — and it changes nothing in a cancelled run. The content enters nothing: it was produced for a stage that no longer has a successor.

## The late decision result — race 6

A Decision Request for `decision.contract_commitment` had been created at 13:30. At 14:11 an eligible human, who had not seen the cancellation, exercised the Right and a Decision Record was produced.

**Outcome: `RECONCILE`, then `ESCALATE`.** Not `IGNORE_AS_STALE`, and the asymmetry with the model result is the whole exemplar:

| | Late review or model result | Late Decision Record |
|---|---|---|
| What it is | An assessment or a production | **An exercise of authority by a human** |
| Did it happen? | Yes, about work now superseded | **Yes, and it is a governed act** |
| May it be discarded as stale? | Yes — recorded against its request | **No.** A governed act is not discarded because a coordinator moved on |
| Result here | Recorded, applied nowhere | **Stands as a record**; whether its effect survives is escalated to a human |

The Decision Record **stands**. What is escalated is the question a coordinator has no business answering: a commitment was authorised for a tender that was withdrawn nine minutes earlier — did anything act on it, and if so, what compensates?

## The check that mattered

Before escalating, the run determined whether the authorised act had produced an **external effect**. It had not: no submission had been sent. Had it been sent, the path would have been **compensation** — a new, recorded, separately-authorised act — and never "roll it back", because nothing that has left the system can be rolled back.

## What this shows

Two late results, two different outcomes, and the difference is not timing. **A record of what someone concluded can be set aside as no longer relevant; a record of what someone was authorised to do cannot.** Collapsing them — discarding both as stale, or honouring both as current — would be the easier implementation and would destroy one of the two separations this architecture is built on.
