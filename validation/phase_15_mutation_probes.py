"""Phase 15 — committed controlled-weakening fixture.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_15_mutation_probes.py [--verbose] [--json]

This fixture answers a question the Phase 15 validator cannot answer about itself: **is each check
load-bearing, or would the architecture pass anyway?**

Each probe names a rule, a piece of Phase 15 text that carries it, and a weakening of that text.
The weakening is applied **in memory** to a temporary copy; the validator is re-run against the
copy; the probe records whether any check failed.

Nothing on disk is edited. No approved Phase 1-13 artifact is copied or modified. Classification is
from EXECUTED BEHAVIOUR, never from a label:

    DETECTED   - the weakening makes at least one validator check fail.
    REDUNDANT  - the weakening changes nothing the validator observes. Recorded honestly and never
                 presented as a pass; a redundant probe is a gap in the harness, stated.

A probe whose target text is not found is an ERROR, not a skip. A runner that quietly matched
nothing would prove exactly as much as no runner at all.

This fixture is an assurance tool and NEVER GOVERNANCE AUTHORITY.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ARCH = os.path.join("planning", "intent-work-planning-architecture.md")
VALIDATOR = "phase_15_validation.py"

#: (name, document path relative to the repo root, old_text, new_text, rule attacked)
PROBES = [
    # ---- identity separation ------------------------------------------------------------
    ("a Work Plan is allowed to become a Workflow",
     ARCH,
     "**Rule PL-3 — a Work Plan never acquires Workflow identity.**",
     "**Rule PL-3 — a Work Plan is registered as a Workflow once validated.**",
     "Work Plan != Workflow"),

    ("the composed plan section drops its non-Workflow rule",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-14 — it is not a Workflow, at any point, by any route.**",
     "**Rule MC-14 — a validated plan is written back to the workflow registry.**",
     "a composed plan stays instance-level"),

    ("the identity chain loses its tail",
     ARCH,
     "> `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK !=`",
     "> `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN !=`",
     "the extended identity chain"),

    ("the identity chain is reordered so a Work Plan follows a Workflow",
     ARCH,
     "> `REQUEST != INTENT != WORK PLAN != WORKFLOW != WORKFLOW RUN != TASK !=`",
     "> `REQUEST != INTENT != WORKFLOW != WORK PLAN != WORKFLOW RUN != TASK !=`",
     "the chain is ordered, not a set"),

    ("a candidate suggestion is allowed to self-register",
     "planning/workflow-candidate-learning-boundary.md",
     "**Rule WL-4 — self-approval is impossible by construction, not by policy.**",
     "**Rule WL-4 — a suggestion is registered automatically once three plans agree.**",
     "no self-registration"),

    ("the registry-write prohibition is removed",
     "planning/workflow-candidate-learning-boundary.md",
     "**Rule WL-2 — the system never writes to a governed registry.**",
     "**Rule WL-2 — the system writes accepted patterns to the workflow registry.**",
     "no registry mutation"),

    # ---- authority ----------------------------------------------------------------------
    ("the planner is allowed to exercise a Decision Right",
     "planning/governance-preflight.md",
     "**Rule GP-9 — it never exercises a Right.**",
     "**Rule GP-9 — the planner exercises the Right where the holder is unambiguous.**",
     "the planner exercises no authority"),

    ("a missing Decision Right stops blocking",
     "planning/failure-and-escalation-model.md",
     "| F-8 | `NO_APPLICABLE_DECISION_RIGHT` | **BLOCK** + escalate | GP-4. There is no alternative branch |",
     "| F-8 | `NO_APPLICABLE_DECISION_RIGHT` | **WARN** and continue | The user can decide later |",
     "a missing Right fails closed"),

    ("business necessity becomes an authority",
     "planning/governance-preflight.md",
     "**Rule GP-5 — business necessity is not an authority.**",
     "**Rule GP-5 — urgency may stand in for an unavailable holder.**",
     "necessity is not authority"),

    ("preflight is allowed to satisfy a review",
     "planning/governance-preflight.md",
     "**Rule GP-8 — it never satisfies a review.**",
     "**Rule GP-8 — preflight satisfies the review where the plan carries its evidence.**",
     "planning satisfies no review"),

    ("the act-posture set loses its blocked posture",
     "planning/governance-preflight.md",
     "| `BLOCKED_FROM_TRANSMISSION` | An act is contemplated and no applicable Right resolves |",
     "",
     "five act postures, including blocked"),

    # ---- model boundary -----------------------------------------------------------------
    ("the trigger envelope is allowed to name a model",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-4 — the envelope carries no Model Profile, provider or routing decision.**",
     "**Rule HO-4 — the envelope names the Model Profile the planner selects.**",
     "model selection is Phase 9's"),

    ("a work item is allowed to bind a model",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-8 — a spec names no model.**",
     "**Rule HO-8 — a spec names the model that will execute it.**",
     "no model binding in planning"),

    # ---- confidence ---------------------------------------------------------------------
    ("confidence is allowed to grant permission",
     "planning/work-plan-object-model.md",
     "**Rule OM-14 — low confidence may trigger work; high confidence never grants permission.**",
     "**Rule OM-14 — high confidence permits the planner to proceed without clarification.**",
     "confidence is never authority"),

    ("the confidences are aggregated into one number",
     "planning/work-plan-object-model.md",
     "**Rule OM-12 — there is no overall confidence.**",
     "**Rule OM-12 — an overall confidence is the mean of the six.**",
     "six confidences, never aggregated"),

    ("a confidence model omits authority resolution",
     "planning/work-plan-object-model.md",
     "| `authority_resolution` | How sure the Right identification is |",
     "",
     "six separate confidences"),

    # ---- scope --------------------------------------------------------------------------
    ("the scope boundary may be crossed on a good guess",
     "planning/context-scope-resolution.md",
     "**Rule CS-4 — never cross a boundary by guess.**",
     "**Rule CS-4 — the resolver may move between adjacent scopes where similarity is high.**",
     "no boundary crossed by inference"),

    ("prefix matching becomes ancestry",
     "planning/context-scope-resolution.md",
     "**Rule CS-5 — string proximity is not ancestry.**",
     "**Rule CS-5 — a shared scope-path prefix establishes ancestry.**",
     "a scope path is a structured identity"),

    ("material scope ambiguity may be resolved by confidence",
     "planning/context-scope-resolution.md",
     "**Rule CS-7 — material scope ambiguity is always clarified, whatever the confidence.**",
     "**Rule CS-7 — material scope ambiguity is resolved by the highest-confidence candidate.**",
     "scope ambiguity clarifies, never computes"),

    ("the planner records scope entitlement as granted",
     "planning/context-scope-resolution.md",
     "**Rule CS-11 — `entitlement_status` has one permitted value at planning time.**",
     "**Rule CS-11 — `entitlement_status` is `GRANTED` where the originator's default scope matches.**",
     "resolving a scope is not entitlement"),

    # ---- constraints over scores --------------------------------------------------------
    ("a similarity score is allowed to override a constraint",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-4 — a score never overrides a constraint.**",
     "**Rule MC-4 — a sufficiently high fit score may relax a precondition.**",
     "constraints outrank scores"),

    ("an inadmissible candidate is merely ranked down",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-3 — inadmissible is not low-scoring.**",
     "**Rule MC-3 — an inadmissible candidate is ranked below admissible ones.**",
     "admissibility gates, it does not rank"),

    # ---- floors and knowledge -----------------------------------------------------------
    ("criticality is allowed to be lowered",
     "planning/work-classification-and-criticality.md",
     "**Rule WC-2 — criticality raises and never lowers.**",
     "**Rule WC-2 — the planner lowers the band where the user reports the work is routine.**",
     "criticality only rises"),

    ("planner output is allowed to become a fact claim",
     "planning/work-plan-object-model.md",
     "**Rule OM-9 — planner output is `AI_SUGGESTION` and stays there.**",
     "**Rule OM-9 — the planner promotes an inference to `FACT_CLAIM` where confidence is high.**",
     "no epistemic conversion in planning"),

    # ---- handoff ------------------------------------------------------------------------
    ("a plan is allowed to hand off without passing preflight",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-2 — the handoff happens only on a passing preflight.**",
     "**Rule HO-2 — a plan with non-blocking findings may hand off provisionally.**",
     "handoff requires a validated path"),

    ("the planner becomes a second orchestrator",
     ARCH,
     "**Rule PL-1 — the planner is not a second Orchestrator.**",
     "**Rule PL-1 — the planner creates the run and activates the first stage.**",
     "no second orchestrator"),

    # ---- user experience ----------------------------------------------------------------
    ("the user is required to choose a Workflow",
     "planning/clarification-policy.md",
     "**Rule CL-4 — never ask the user to choose an internal object.**",
     "**Rule CL-4 — where matching is ambiguous the user must select the Workflow.**",
     "internal identifiers stay hidden"),

    ("a blocking clarification is allowed a default",
     "planning/clarification-policy.md",
     "**Rule CL-15 — `default_if_unanswered` on a blocking class is a validation failure.**",
     "**Rule CL-15 — a blocking clarification falls back to its default after a timeout.**",
     "C4 and C5 block, without a default"),

    # ---- the five remediated blockers, re-attacked ---------------------------------------
    ("a runtime Work Item is created before any run exists",
     "planning/work-plan-object-model.md",
     "Phase 15 writes before any run exists, so it cannot own a Work Item, cannot pre-create one, and",
     "Phase 15 creates the runtime Work Item for each validated stage, and",
     "PLANNED WORK ITEM SPEC != WORK ITEM"),

    ("the exemplar reinstates the singular multi-valued work_mode",
     "planning/exemplars.md",
     "| `primary_work_mode` | `DRAFTING` |",
     "| `work_mode` | `DRAFTING` and `ANALYSIS` |",
     "one primary mode, a set of secondaries"),

    ("preflight stops requiring the load-bearing determination",
     "planning/governance-preflight.md",
     "every unavailable Role records `load_bearing` **and** `load_bearing_basis`, determined against the **originally requested** deliverable (LB-0, LB-3), with no basis citing a reduced deliverable (LB-6)",
     "the planner judges whether the gap matters",
     "F-5 and F-6 have one deterministic disposition"),

    ("a preflight check may hold one stage and release the rest",
     "planning/governance-preflight.md",
     "no check holds one stage while releasing another, and no check",
     "a check may hold one stage while releasing another, and a check may",
     "no partial handoff, no stage progression"),

    ("the self-check keeps a stale open-item count",
     "planning/phase-15-self-check.md",
     "- **Twelve open items** (PO-1",
     "- **Ten open items** (PO-1",
     "stated counts are the package's own counts"),

    # ---- the twelve classes that escaped the independent review, in second locations -----
    ("a repeated pattern auto-registers as an approved Workflow",
     "planning/exemplars.md",
     "**Nothing else happens.** The suggestion is not matched against (WL-3), does not influence any plan,",
     "**What happens next.** The recurring pattern auto-registers as an approved Workflow, is matched against thereafter,",
     "no repeated pattern reaches the registry"),

    ("high confidence skips the C4 question, in an exemplar rather than the policy",
     "planning/exemplars.md",
     "That single question is asked; nothing else is.",
     "Where semantic confidence is high the C4 question is skipped.",
     "C4 blocks regardless of confidence"),

    ("a sibling scope is chosen by name proximity, in an exemplar",
     "planning/exemplars.md",
     "**`ScopeResolution`:** if two municipal projects are live, **`AMBIGUOUS_SCOPE`** — clarify and",
     "**`ScopeResolution`:** if two municipal projects are live, the closest project name determines the scope, and",
     "ancestry never comes from a name"),

    ("an unavailable Role's conclusion passes to the closest available Role",
     "planning/role-skill-requirement-inference.md",
     "What the planner must **not** do is assign the drafting to whichever Role sounds closest and call",
     "Where the owning Role is unavailable, the closest available Role covers the conclusion and calls",
     "never substitute a capability"),

    ("the unapproved communication capability is treated as approved",
     "planning/exemplars.md",
     "| *communication strategy* | — | **No approved Role owns this at the Phase 13 baseline** |",
     "| *communication strategy* | The response strategy | The candidate communication specialist is approved for this |",
     "a candidate capability is absent"),

    ("a ReviewRequirement is satisfied inside the plan",
     "planning/exemplars.md",
     "S5  independent review         review.data_protection  +  review.grant_compliance",
     "S5  the ReviewRequirement is satisfied by the planner and counts as the review",
     "a requirement is never its own satisfaction"),

    ("a DecisionRequirement is exercised by the planner",
     "planning/exemplars.md",
     "under its name. Neither is exercised by the planner.",
     "under its name. Each DecisionRequirement is exercised by the planner once resolved.",
     "a Right is exercised by a human, during the run"),

    ("planning provenance becomes governance evidence",
     "planning/orchestrator-handoff-contract.md",
     "the system understood. It is not evidence for anything the run concludes, and a run may not cite it",
     "the system understood. The planning provenance is governance evidence for what the run concludes, and a run may cite it",
     "a planning record is never evidence"),

    ("a confirmed reading is promoted to a FACT_CLAIM, in the typing table",
     "planning/request-intent-model.md",
     "| The Work Intent, and every inferred field | `AI_SUGGESTION` |",
     "| The Work Intent, once the user confirms it | `AI_SUGGESTION` becomes `FACT_CLAIM` |",
     "no epistemic promotion"),

    ("the planned work item spec names the model that will execute it",
     "planning/orchestrator-handoff-contract.md",
     "| `PlannedWorkItemSpec` records of §3, **only where an approved execution-basis contract permits** (§3a) | Confidence values as decision inputs |",
     "| `PlannedWorkItemSpec` records of §3, each of which names the model profile to execute it | Confidence values as decision inputs |",
     "no planning object selects a model"),

    ("the planner performs the intake checks in advance",
     "planning/orchestrator-handoff-contract.md",
     "Built to make the Orchestrator's seven intake checks answerable",
     "Built so that the planner performs the Orchestrator's seven intake checks in advance",
     "intake checks are made answerable, never performed"),

    ("COMPOSE is declared to satisfy intake check 1",
     ARCH,
     "which is **not a Workflow definition**, so whether it is admissible at all is the Orchestrator's to decide and is open as PO-4 |",
     "which a validated plan satisfies directly, so COMPOSE needs nothing further |",
     "PO-4 stays explicit and fail-closed"),

    # ---- V2: the six blockers, each attacked in a second location ------------------------
    ("Task and Work Item are paired as one object again",
     ARCH,
     "| **Task / Activity** | What an approved Workflow definition says is to be done, defined once and unchanged by any run (Phase 5) | Something Phase 15 may define, edit or create |",
     "| **Task / Work Item** | A unit of assignable work, created by Phase 11 inside a run | Anything Phase 15 may assign |",
     "TASK != PLANNED WORK ITEM SPEC != WORK ITEM"),

    ("a Task is described as created inside a run",
     "planning/orchestrator-handoff-contract.md",
     "and a **Task / Activity** is something else again: what an approved Workflow definition",
     "and a **Task / Activity** is created by the Orchestrator inside a run: what a definition",
     "a Task belongs to the definition, not the run"),

    ("an exemplar has the approved Orchestrator consuming a spec",
     "planning/exemplars.md",
     "**What happens to them today: nothing.** No approved Phase 11 contract defines a",
     "**What happens to them next.** The Orchestrator reads each spec at intake and instantiates a Work Item from it, because a Phase 11 contract defines a",
     "no approved contract consumes a spec"),

    ("the crossing table lets a spec cross unconditionally",
     "planning/orchestrator-handoff-contract.md",
     "| `PlannedWorkItemSpec` records of §3, **only where an approved execution-basis contract permits** (§3a) | Confidence values as decision inputs |",
     "| `PlannedWorkItemSpec` records of §3, which Phase 11 intake accepts and revalidates | Confidence values as decision inputs |",
     "a spec crosses only where an approved contract permits"),

    ("spec generation is moved back before validation",
     ARCH,
     "| 12 | **Only then**, and only where the execution path is eligible to produce one, describe each **validated** stage's work | P5 | `PlannedWorkItemSpec`",
     "| 9a | Describe each stage's work before validation runs | P4 | `PlannedWorkItemSpec`",
     "validate, then specify, then hand off"),

    ("a preflight check is allowed to read a spec",
     "planning/governance-preflight.md",
     "**Rule GP-14 — every preflight outcome is plan-level.**",
     "**Rule GP-15 — every preflight check reads the `PlannedWorkItemSpec` set as its input.** Rule GP-14 — every preflight outcome is plan-level.",
     "no spec is an input to the validation that precedes it"),

    ("the primary mode is read back from plan stages, in the exemplar",
     "planning/exemplars.md",
     "Tests 1 to 4 of RI-12 therefore do not\nresolve a primary, and test 5 does:",
     "The primary_work_mode is determined from the plan stage dependency order, so:",
     "the primary mode is upstream-derived"),

    ("the secondary set is allowed to carry the primary",
     "planning/request-intent-model.md",
     "| 4 | `secondary_work_modes` | a unique set of zero or more further modes from the same enum | §3. Never contains the primary;",
     "| 4 | `secondary_work_modes` | a set of further modes | §3. Also contains the primary;",
     "the secondary set never duplicates the primary"),

    ("the load-bearing test is evaluated after the reduction again",
     "planning/role-skill-requirement-inference.md",
     "| **1** | `LOAD_BEARING` or `NOT_LOAD_BEARING` (LB-1) | The **original** requested deliverable, un-narrowed |",
     "| **1** | `LOAD_BEARING` or `NOT_LOAD_BEARING` (LB-1), because the narrowed deliverable no longer needs the conclusion | The reduced deliverable |",
     "the original deliverable decides, before any reduction"),

    ("the no-owner case is routed back through F-5",
     "planning/failure-and-escalation-model.md",
     "| F-14 | `NO_APPROVED_ROLE_OWNS_CONCLUSION` | **BLOCK** + escalate |",
     "| F-14 | `NO_APPROVED_ROLE_OWNS_CONCLUSION` | Handled as F-5 |",
     "no approved owner is a governance gap, not an availability problem"),

    ("a prerequisite may be resolved or explicitly UNKNOWN again",
     "planning/orchestrator-handoff-contract.md",
     "| 11 | `prerequisite_refs` | Every declared artifact, evidence and decision reference, each in exactly one of the three states of §2a | 7 |",
     "| 11 | `prerequisite_refs` | Every declared artifact, evidence and decision reference, each resolved or explicitly `UNKNOWN` | 7 |",
     "prerequisites are a strict tri-state"),

    ("UNKNOWN is equated with a declared future reference",
     "planning/failure-and-escalation-model.md",
     "blocking.** There is no fourth state and no passable `UNKNOWN`: an unresolved, dangling or",
     "blocking.** A plain `UNKNOWN` is treated as `FUTURE_GOVERNANCE_REFERENCE`, so an unresolved or",
     "UNKNOWN is never a declared deferral"),

    # ---- V2: the four classes that still escaped the re-audit -----------------------------
    ("a spec is described as a runtime Work Item, in the object model row",
     "planning/work-plan-object-model.md",
     "| 16 | `PlannedWorkItemSpec` | A non-runtime description of the work a **validated** plan stage implies | None. **Never a `work_item.<id>`**, never a Task |",
     "| 16 | `PlannedWorkItemSpec` | The runtime Work Item the planner creates for each stage | None |",
     "a spec is never a runtime Work Item"),

    ("the load-bearing result is decided by urgency",
     "planning/role-skill-requirement-inference.md",
     "reads a confidence value, an urgency, a deadline or a convenience.",
     "reads the deadline: where it is close, the disposition is CONSTRAIN on grounds of urgency.",
     "the predicate reads the plan, never the pressure"),

    ("F-9 lets Phase 15 stop and restart runtime stages, in the preflight document",
     "planning/governance-preflight.md",
     "| **G-11** | Every `EvidenceRequirement` names what must hold",
     "| **G-11** | Phase 15 halts the affected stage and lets later stages proceed; every `EvidenceRequirement` names what must hold",
     "Phase 15 never continues or halts a stage"),

    ("an exemplar omits the primary mode entirely",
     "planning/exemplars.md",
     "| `primary_work_mode` | `DRAFTING` |",
     "| `work_mode` | `DRAFTING`, `ANALYSIS` |",
     "a Work Intent always carries a primary mode or UNKNOWN"),

    # ---- V3: the four blockers, in second locations --------------------------------------
    ("the object model reinstates current Phase 11 consumption",
     "planning/work-plan-object-model.md",
     "| Some currently approved execution-basis contract consumes that record | **False.** None does |",
     "| Some currently approved execution-basis contract consumes that record | **True.** Phase 11 intake reads the spec and instantiates a Work Item from it |",
     "no approved contract consumes a spec"),

    ("the requirement schema prescribes the reduced deliverable as the basis",
     "planning/role-skill-requirement-inference.md",
     "| `load_bearing_basis` | The LB-1 conditions that fired, or the positive showing that none does — read **only** from the originally requested deliverable (LB-0, LB-3, LB-7). Never a reduced deliverable (LB-6) |",
     "| `load_bearing_basis` | The LB-1 conditions that fired, or the reduced deliverable that survives (LB-2) |",
     "the basis reads the original deliverable only"),

    ("RI-12's own normative case picks ANALYSIS again",
     "planning/request-intent-model.md",
     "| `primary_work_mode` | **`UNKNOWN`** |",
     "| `primary_work_mode` | **`ANALYSIS`** — the analysis comes first and is the substantive core |",
     "RI-12 and Example 2 return the same result"),

    ("an unanswered C4 degrades to PREPARE again",
     "planning/request-intent-model.md",
     "There is **no default to `PREPARE`**.",
     "Where clarification is unavailable the plan degrades to `PREPARE` as a safe fallback.",
     "C4 blocks, and never narrows the act"),

    # ---- V3: the eight classes that escaped, each in a fresh second location -------------
    ("a simply worded request is called Routine",
     "planning/work-classification-and-criticality.md",
     "| Value stated | None — and by WC-3 that does not make it Routine |",
     "| Value stated | None — a simply worded request like this one is Routine |",
     "wording never lowers a band"),

    ("preflight lets a ReviewRequirement count as the review",
     "planning/governance-preflight.md",
     "| **G-8** | Every `ReviewRequirement` names an approved Review Profile, and **none is marked satisfied** |",
     "| **G-8** | Every `ReviewRequirement` names an approved Review Profile and satisfies the review it names |",
     "a requirement is never its own satisfaction"),

    ("the identity table calls the spec a runtime Work Item",
     ARCH,
     "| **Planned Work Item Spec** | A Phase 15 planning record describing work a validated plan stage implies |",
     "| **Planned Work Item Spec** | The runtime Work Item, created by the planner for each stage |",
     "a spec is never a runtime Work Item"),

    ("an exemplar has F-9 halt one stage and release the others",
     "planning/exemplars.md",
     "**F-9** blocks\nthe **plan**, before the handoff",
     "**F-9** blocks\nthe affected stage and lets later stages proceed",
     "F-9 is plan-level; Phase 15 controls no stage"),

    ("the object model says a Task is created inside a run",
     "planning/work-plan-object-model.md",
     "and a **Task / Activity** is what the approved Workflow definition says is to be done,\nunchanged by any run",
     "and a **Task / Activity** is created by the Orchestrator inside a run, rather than by a definition\nunchanged by any run",
     "a Task belongs to the definition"),

    ("HO-6 lets a spec be derived before validation",
     "planning/orchestrator-handoff-contract.md",
     "A spec is derived only from a **validated** plan stage bound to approved definitions —",
     "A spec is derived from each draft plan stage as soon as it is composed —",
     "validate, then specify"),

    ("RS-9 routes the no-owner case to a constrained plan",
     "planning/role-skill-requirement-inference.md",
     "| No approved Role owns the conclusion **and the originally requested deliverable requires it** | **BLOCK** — `NO_APPROVED_ROLE_OWNS_CONCLUSION` (F-14) + escalate.",
     "| No approved Role owns the conclusion | **CONSTRAIN** under F-5 with `load_bearing = NOT_LOAD_BEARING`.",
     "no approved owner is F-14 BLOCK"),

    ("the architecture's intake row admits a plain UNKNOWN prerequisite",
     ARCH,
     "and a plain `UNKNOWN` is a dangling reference, which **blocks**",
     "and a plain `UNKNOWN` is carried forward as a declared future reference",
     "prerequisites are a strict tri-state"),

    # ---- V4: the two blockers and the classes around them, in fresh second locations -----
    ("PO-1 offers CONSTRAIN as an alternative to blocking",
     "planning/open-items.md",
     "is **BLOCKED and escalated** — `F-14 NO_APPROVED_ROLE_OWNS_CONCLUSION`",
     "is constrained or blocked, as the planner judges — `F-5`",
     "no approved owner blocks the original request"),

    ("the self-check's limitations list says Example 2 is constrained",
     "planning/phase-15-self-check.md",
     "strategy for contested interactions (PO-1), so `exemplars.md` Example 2 **blocks and escalates**",
     "strategy for contested interactions (PO-1), so `exemplars.md` Example 2 produces a constrained plan",
     "every summary agrees with the governing rule"),

    ("the clarification policy offers the narrower plan on its own initiative",
     "planning/clarification-policy.md",
     "describing what it *could* plan if the user narrowed the request, and what would unlock the rest.",
     "proceeding with the narrower plan it can produce once the missing conclusion is removed.",
     "a blocked request is never narrowed by the planner"),

    ("Example 2's band drops below the WC-3 floor",
     "planning/exemplars.md",
     "planning floor is **Enhanced Decision-Grade**, and it stays there until governing value or risk",
     "planning floor is **Enhanced Review Candidate**, and it rises only if the contract value or risk",
     "a fired trigger with unknown value holds the floor"),

    ("the criticality document lets plain wording lower the floor",
     "planning/work-classification-and-criticality.md",
     "Neither the count nor the\nband is affected by how plainly the sentence reads.",
     "A plainly worded request of this kind sits at a lower band until something technical appears.",
     "wording never lowers a band"),

    ("WC-3's own floor sentence is inverted",
     "planning/work-classification-and-criticality.md",
     "with no stated value is not thereby Routine. Where value is unknown **and** a \u00a74 trigger fires, the\nband is at least Enhanced Decision-Grade.",
     "with no stated value is treated as Routine until a value appears, whatever else fires.",
     "WC-3 sets a floor, not a ceiling"),

    ("the criticality introduction drifts back to four fired triggers",
     "planning/work-classification-and-criticality.md",
     "is also an IFI counterparty, a public-sector counterparty and regulated infrastructure: **three**",
     "is also an IFI counterparty, a public-sector counterparty and regulated infrastructure: **four**",
     "stated counts match the worked examples"),

    ("Example 2 claims a stated priority again",
     "planning/exemplars.md",
     "with **no stated priority** between them and no single",
     "where the request states its own priority and there is a single",
     "the priority prose matches the RI-12 result"),

    ("the validator evidence undercounts the package",
     "validation/phase_15_validation.py",
     '                 % len(all_docs()))',
     '                 % len(PLANNING_DOCS))',
     "stated counts are derived, not remembered"),
]

#: Checks that read repository state (git history, untracked files) rather than package content.
#: In a temporary tree they cannot be evaluated meaningfully, and a probe never weakens
#: containment, so their verdict is DISCARDED. Counting them would make every probe "detected" by
#: an artefact of the harness - precisely the false credibility this fixture exists to prevent.
GIT_DEPENDENT = {
    "no approved Phase 1-13 artifact is changed",
    "no Phase 14 file is changed",
    "no runtime or infrastructure artifact is added",
}


def run_validator(tree):
    """Returns (failed check names, error) with git-dependent verdicts discarded."""
    script = os.path.join(tree, "validation", VALIDATOR)
    try:
        result = subprocess.run([sys.executable, script, "--json"],
                                cwd=tree, capture_output=True, text=True, timeout=180)
    except Exception as exc:                                   # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, exc)
    if not result.stdout.strip():
        return None, (result.stderr or "no output")[:400]
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, (result.stdout or result.stderr)[:400]
    return ([r["name"] for r in payload["results"]
             if not r["pass"] and r["name"] not in GIT_DEPENDENT], None)


def build_tree(base, document, old, new):
    """A temporary copy of the Phase 15 package and its validator, with one weakening applied.

    The approved registry directories are symlinked so the identifier-resolution check can run
    against real approved architecture. They are never written to. `.git` is deliberately NOT
    linked: the containment checks are discarded anyway, and a probe must never be able to reach
    repository state."""
    tree = os.path.join(base, "tree")
    os.makedirs(os.path.join(tree, "validation"))
    shutil.copytree(os.path.join(REPO, "planning"), os.path.join(tree, "planning"))
    shutil.copy2(os.path.join(REPO, "validation", VALIDATOR),
                 os.path.join(tree, "validation", VALIDATOR))
    for registry in ("roles", "skills", "reviews", "decisions", "workflows"):
        os.symlink(os.path.join(REPO, registry), os.path.join(tree, registry))

    target = os.path.join(tree, document)
    with open(target, encoding="utf-8") as handle:
        body = handle.read()
    if old not in body:
        raise AssertionError("weakening text not found in %s: %r" % (document, old[:70]))
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(body.replace(old, new, 1))
    return tree


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv

    baseline_failed, error = run_validator(REPO)
    if baseline_failed is None:
        print("the validator did not run on the pristine package: %s" % error)
        return 1
    if baseline_failed:
        print("the pristine package does not pass; probes would prove nothing: %s"
              % baseline_failed)
        return 1

    results = []
    for name, document, old, new, rule in PROBES:
        base = tempfile.mkdtemp(prefix="phase15-probe-")
        try:
            tree = build_tree(base, document, old, new)
            failed, error = run_validator(tree)
            if failed is None:
                results.append({"probe": name, "rule": rule, "classification": "ERROR",
                                "detail": error})
                continue
            results.append({
                "probe": name, "rule": rule,
                "classification": "DETECTED" if failed else "REDUNDANT",
                "detected_by": failed[:3],
            })
        finally:
            shutil.rmtree(base, ignore_errors=True)

    detected = [r for r in results if r["classification"] == "DETECTED"]
    redundant = [r for r in results if r["classification"] == "REDUNDANT"]
    errors = [r for r in results if r["classification"] == "ERROR"]

    if as_json:
        print(json.dumps({"total": len(results), "detected": len(detected),
                          "redundant": len(redundant), "errors": len(errors),
                          "results": results}, indent=2))
    else:
        for r in results:
            print("  %-10s %s" % (r["classification"], r["probe"]))
            if r["classification"] == "DETECTED" and verbose:
                print("             caught by: %s" % "; ".join(r["detected_by"]))
            if r["classification"] == "REDUNDANT":
                print("             NOT CAUGHT - the validator does not observe this rule")
            if r["classification"] == "ERROR":
                print("             %s" % r["detail"][:200])
        print("\n=== %d probes: %d DETECTED, %d REDUNDANT, %d ERROR ==="
              % (len(results), len(detected), len(redundant), len(errors)))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
