# Phase 15 Self-Check

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

> **This is a producer self-check.** The party that wrote an architecture is the last party who
> should certify it. What follows records what was checked and what was found; it approves nothing
> and replaces no independent review.

## 1. Non-production status

| Claim | Status |
|---|---|
| Any Phase 15 artifact is `APPROVED` or `CANONICAL` | **No.** All 16 documents are `PROPOSED` |
| Any approved Phase 1–13 artifact is modified | **No.** The branch adds files; it changes none |
| Any Phase 14 file is modified | **No** |
| Any runtime, migration, SDK, queue, worker, scheduler, IaC or secret is created | **No** |
| Any Decision Right, Role, Skill, Review Profile or Workflow is created | **No** |
| Any human approval is claimed | **No** |
| Anything here has been executed | **No.** No planner exists, and no exemplar is a fixture |

## 2. Completeness against the commissioning prompt

| Required | Artifact | Present |
|---|---|:---:|
| Architecture | `planning/intent-work-planning-architecture.md` | ✓ |
| Request / intent model | `planning/request-intent-model.md` | ✓ |
| Context / scope resolution | `planning/context-scope-resolution.md` | ✓ |
| Work classification / criticality | `planning/work-classification-and-criticality.md` | ✓ |
| Role / Skill inference | `planning/role-skill-requirement-inference.md` | ✓ |
| Workflow matching / composition | `planning/workflow-matching-and-composition.md` | ✓ |
| Work Plan object model | `planning/work-plan-object-model.md` | ✓ |
| Clarification policy | `planning/clarification-policy.md` | ✓ |
| Governance preflight | `planning/governance-preflight.md` | ✓ |
| Orchestrator handoff | `planning/orchestrator-handoff-contract.md` | ✓ |
| Failure / escalation | `planning/failure-and-escalation-model.md` | ✓ |
| Learning boundary | `planning/workflow-candidate-learning-boundary.md` | ✓ |
| UX contract | `planning/user-experience-contract.md` | ✓ |
| Exemplars | `planning/exemplars.md` | ✓ — six, fully worked |
| Open items | `planning/open-items.md` | ✓ |
| Self-check | `planning/phase-15-self-check.md` | ✓ |
| Validator | `validation/phase_15_validation.py` | ✓ |
| Mutation probes | `validation/phase_15_mutation_probes.py` | ✓ |

### 2a. One deviation from the recommended filenames, and why

The commissioning prompt recommended `architecture/intent-work-planning-architecture.md`. The
document is at **`planning/intent-work-planning-architecture.md`** instead.

Adding **any** file under `architecture/` changes the result of the **approved Phase 12
validator**, whose containment check treats every path under `architecture/` and `orchestration/`
as inherited material that this branch must leave untouched — tracked or untracked, added or
modified. Placing the document there took Phase 12 from `55/55` to `54/55`, and a proposal branch
that degrades an approved validator's result has modified approved architecture in the only sense
that check cares about.

The prompt permits filename adjustment where coherence requires it. Keeping an approved
validator's result intact is the stronger obligation, and the whole package now sits in one
directory, which is arguably more coherent anyway. Phase 12 is back to `55/55`.

## 3. The prohibitions, and where each is enforced

| # | Never | Enforced by | Checked by |
|---:|---|---|---|
| N-1 | Invent a governed primitive | RS-3, MC-9 | `the planner invents no Role, Skill, Review Profile, Right or Workflow` |
| N-2 | Turn a plan into a Workflow | WL-1, WL-2, WL-4, MC-14 | `a Work Plan never acquires Workflow identity` |
| N-3 | Select or exercise human authority | GP-4, GP-9 | `the planner never grants, exercises or substitutes for authority` |
| N-4 | Treat confidence as authority | OM-13, OM-14 | `confidence never grants authority, waives review or crosses scope` |
| N-5 | Downgrade an inherited requirement | WC-2, WC-10, MC-11 | `no inherited criticality, sensitivity or review floor is lowered` |
| N-6 | Silently cross a scope boundary | CS-4, CS-5, CS-7 | `scope is never crossed by inference, similarity or confidence` |
| N-7 | Infer a missing Decision Right | GP-5 | `a missing applicable Decision Right fails closed` |
| N-8 | Convert AI output into approved knowledge | OM-9, OM-11, RI-11 | `generated planning knowledge stays correctly typed` |
| N-9 | Create a permanent autonomous agent | PL-2, UX-11 | Structural: no persona is specified anywhere |
| N-10 | Choose a Model Profile | HO-4, HO-8, G-14 | `the planner never selects a Model Profile`; `no planning object selects a model, spec included` |
| N-11 | Instantiate a Phase 11 runtime `Work Item`, or define a Task | HO-6, HO-13, HO-14, HO-16, OM-16 | `planned work item specs are never runtime Work Items`; `Task, planned spec and Work Item stay three separate things`; `no approved contract is claimed to consume a planned spec` |

## 4. Identifier integrity — checked, not asserted

Every `role.<id>`, `skill.<id>`, `review.<id>`, `decision.<id>` and `workflow.<id>` cited anywhere
in the package is resolved against the approved registries on this branch. **There are no
unresolved identifiers.** The package cites 20 approved Roles, 5 approved Workflows, and the
Review Profiles and Decision Rights the exemplars name. It creates none.

This is the check that would catch the most plausible failure of a planning layer: describing a
capability instead of naming one, and then having no way to tell that the capability does not exist.

## 5. What this self-check did **not** check

1. **Whether the architecture is correct.** Whether the five functions are the right five, whether
   the seventeen records are the right seventeen, whether the five ambiguity classes carve the space
   correctly, and whether the preflight checks are the right ones are questions for an
   independent review.
2. **Whether the COMPOSE path can execute.** Open item **PO-4** is unresolved and is load-bearing:
   the approved intake check 1 requires a Workflow definition, and a Work Plan is not one. The
   MATCH path is compatible with the approved Orchestrator; **the COMPOSE path is specified and not
   yet executable**, and this phase deliberately does not amend an approved Phase 11 check to make
   it so. The independent review classified it **`APPROVABLE WITH EXPLICIT BLOCKED IMPLEMENTATION
   DEPENDENCY`**, and `open-items.md` §2a preserves that classification rather than resolving it:
   not a blocker to approving the architecture while it stays explicit and fail-closed, and a
   blocker to **activating or executing COMPOSE** until Phase 11 change control says otherwise.
3. **Whether inference is achievable.** The architecture says what an interpreter must produce and
   what it may never do. Whether any system can derive those fields reliably from ordinary language
   is an empirical question no document settles.
4. **Whether the criticality triggers fire correctly.** The sixteen triggers are transcribed from
   the approved policy. Whether a planner would detect them in real requests is untested.
5. **Whether the user experience works.** UX-contract compliance is checkable; whether the result
   is usable is not, and no user has seen it.

## 6. Known limitations

- **Twelve open items** (PO-1…PO-12, the canonical inventory being `open-items.md` itself, from
  which `validation/phase_15_validation.py` now derives this count rather than trusting the prose).
  One of them, PO-4, determines whether half this phase is buildable at all.
  It is stated in full rather than resolved, because resolving it would mean amending an approved
  Phase 11 check from a proposal branch.
- **The package names a capability gap it cannot fill.** No approved Role owns communication
  strategy for contested interactions (PO-1), so `exemplars.md` Example 2 produces a *constrained*
  plan. That is the architecture working, and it is also a real functional limit.
- **Confidence has no production method** (PO-8). The model specifies what confidence may never do
  and leaves how it is computed undefined — deliberately, since specifying it would specify an
  inference runtime this phase excludes.
- **Planning records have nowhere approved to live** (PO-2, PO-6). Phase 10's ten data domains do
  not include planning, and adding one is a Phase 10 act.
- **Nothing has been executed.** Every exemplar is worked on paper. No fixture exists.

## 6a. What the independent review returned, and what was changed

The review returned **`FAIL`**, at **`HIGH`** credibility, with five blockers and a harness it
judged weak. It also ran 16 second-location mutations — weakenings planted in an active statement
that carries a rule without being the rule's canonical owner — and **12 escaped**. None of that is
softened here.

| # | Blocker | What was wrong | What it is now |
|---:|---|---|---|
| 1 | Runtime `Work Item` ownership | §3 of the handoff contract treated the Phase 11 runtime identity as something Phase 15 could produce, before any run existed | `PlannedWorkItemSpec` in its own identifier space, with `PLANNED WORK ITEM SPEC != WORK ITEM` stated in two documents, no runtime state of any kind (HO-13), Phase 11 as the sole instantiator (HO-14), and a new prohibition **N-11** |
| 2 | Work-mode cardinality | The retired `work_mode` field was one enum value while an exemplar carried two | `primary_work_mode` (exactly one) + `secondary_work_modes` (a unique, possibly empty set), with a deterministic derivation and a stated rule for downstream logic that needs one leading mode (**RI-12**) |
| 3 | F-5 / F-6 disposition | CONSTRAIN-or-BLOCK turned on "load-bearing", which nothing defined and nothing recorded | The **LB-1…LB-5** predicate over declared deliverables, owned conclusions, stage dependencies and required gates — never confidence — recorded in `load_bearing` and `load_bearing_basis`, and enforced by G-5 and G-6 |
| 4 | F-9 against G-11 / HO-2 | F-9 blocked a stage and let others proceed; Phase 15 can do neither | Plan-level **BLOCK** before handoff, or a reference declared `FUTURE_GOVERNANCE_REFERENCE` under the approved intake check 7 — **FE-11**, **FE-12**, **GP-14**, and HO-2 all say the same thing |
| 5 | Stale inventory count | The prose said ten, against a PO-1…PO-11 inventory | Corrected, and the count is now **derived in validation** from `open-items.md`, along with the record and failure-mode counts. Prose that disagrees with the package fails |

Two things were corrected that the review did not raise, because they were adjacent and wrong:
GP-6 was headed *"the four act postures"* above a list of five, and the EIB exemplar claimed T-11
on the ground that a meeting is "submission-adjacent". T-11 is an **external submission**; a meeting
is not one, and claiming it is, is exactly what WC-4 forbids. The rigour that exemplar needs comes
from conservative escalation under WC-2 and WC-6, and it now says so in those terms — in the
exemplar and in `work-classification-and-criticality.md` §8 alike.

### Assurance added

Twelve new checks, one per escaped class plus the five blockers, and **17 new probes**, every one
of them planted in a **second location** — an exemplar row, a code-fence stage line, a typing-table
row, a crossing-boundary row — rather than in the rule's own sentence. The validator also gained a
stricter negation test (`denied_near`) that asks whether the prohibited verb itself is negated,
rather than whether a denial appears somewhere in the statement; the loose test is what let a
weakening inherit cover from its neighbours.

**This does not make the harness credible.** It makes it less obviously weak against one review's
attack set. §7 stands as written, with one addition: an independent reviewer found five blockers
and 12 escapes in a package whose own harness reported 32/32 and 28/28. The producer's green board
was worth what §7 says it is worth.

## 6b. What the V2 re-audit returned, and what was changed

The V2 independent re-audit of `fa9447dedc8077783ab61f116988371128de8476` returned **`FAIL`** at
**`HIGH`** credibility, with six blockers, and found **4 of 21** second-location mutations still
escaping. Four of the six blockers were introduced by the V1 remediation itself — the object that
fixed the first review's ownership error brought three new errors with it. That is the more useful
fact about this package's assurance, and §7 now says so.

| # | Blocker | What was wrong | What it is now |
|---:|---|---|---|
| 1 | `TASK != WORK ITEM` was lost | The identity table gave the two objects a single shared row, implying neither belongs where the approved model puts it: a Task in the Workflow **definition**, unchanged by any run, and a Work Item in the **run** | Three rows, three objects, and `TASK != PLANNED WORK ITEM SPEC != WORK ITEM` stated on its own line in two documents. Scans reject the pairing and reject a Task created in a run |
| 2 | A consumption claim with no approved basis | HO-14 described the approved Orchestrator handling the record at intake and creating a runtime identity from it. No approved contract defines `PlannedWorkItemSpec` as an intake object, so that was a claim about behaviour nobody has approved | §3a states the boundary in full: Phase 15 may **produce** a spec; it crosses only where an approved execution-basis contract permits, **and none currently does**; the consumption semantics need explicit Phase 11 change control; COMPOSE stays non-executable under PO-4; MATCH keeps to the approved Workflow-based path. **HO-16**: a spec is not a bridge over PO-4. New open item **PO-12** |
| 3 | Spec generation preceded validation | Step 9a produced a spec before requirements and preflight, while HO-6 said a spec derives from a **validated** stage — a cycle | Step **12**, after validation, conditional on the execution path being eligible. **PL-8** states the ordering, and a check rejects any preflight rule that reads a spec |
| 4 | `primary_work_mode` was derived downstream | The tie-break read plan stage dependency order, which does not exist when `WorkIntent` is built | Five ordered tests over the Request and stated intent fields only — stated priority, single end result, execution verb, main-clause target, else `UNKNOWN` with the **complete** set of applicable modes in `secondary_work_modes` (**RI-13**) |
| 5 | The load-bearing example was circular | It removed the missing conclusion, called the remainder the deliverable, and concluded the removed conclusion had not been needed | **LB-0**: every test reads the **originally requested** deliverable, before any reduction. **LB-6**: a reduced deliverable is a consequence, never evidence. **RS-12 / RS-13** and new failure mode **F-14** separate *no approved owner* from *approved owner unavailable*; G-20 enforces it |
| 6 | Prerequisites were "resolved or explicitly `UNKNOWN`" | Which conflicts with approved intake check 7 | Three states — `RESOLVED`, `FUTURE_GOVERNANCE_REFERENCE`, and a plain `UNKNOWN` that **blocks** — in §2a of the handoff contract, **HO-15**, **FE-13** and new preflight check **G-19**. `UNKNOWN` is never relabelled as a declared deferral |

### The exemplar that had to change its answer

Example 2 — *"prepare a firm but professional response. I do not want to damage the relationship."* —
previously produced a narrower plan and offered it as the answer. Under LB-0 it **blocks**: the user asked for a
communication-strategy conclusion in terms, no approved Role owns it, and the earlier reasoning
reached CONSTRAIN only by narrowing the deliverable first and then reading the narrowed version as
proof that nothing had been lost. The narrower plan is still shown, as what a **different** request
would compose — not as what a blocked plan quietly becomes.

### Assurance added in V2

Six new cross-document checks (53 total) and sixteen new probes (61 total), each planted in a second
location. The validator gained two further repairs to its own machinery: a numbered list item is now
a statement in its own right rather than being merged into its neighbours, and the forward half of
the negation test now reads only as far as a row's answering cell.

## 6c. What the V3 re-audit returned, and what was changed

The V3 re-audit of `9b95c3e0025a4ca63c9ec425b68fddea68fa10de` returned **`FAIL`**, with credibility
`HIGH` for its baseline-specific findings and **`LOW`** for this package's own validator assurance.
Four blocking contradictions, and **8 of 30** second-location mutations escaping. Every one of the
four was a place where V2 fixed a rule in its owner document and left an active contradiction
somewhere else.

| # | Blocker | What was wrong | What it is now |
|---:|---|---|---|
| 1 | The object model still had approved Phase 11 consuming a spec | The handoff contract said no approved contract consumes one; OM-16 and the record row said the Orchestrator reads it, re-validates it and instantiates from it | **OM-17** states the boundary as a table of five claims, three of them false-by-declaration. The record row's execution column reads **inert**. The withdrawn description is named as withdrawn rather than left implied |
| 2 | The load-bearing basis was still circular in the schema | LB-0 and LB-6 were right; LB-3 and the `RoleRequirement` schema still prescribed the reduced deliverable *as* the `load_bearing_basis` | Two fields. `load_bearing_basis` reads **only** pre-reduction material; **`reduced_deliverable_basis`** is written only after an independent `NOT_LOAD_BEARING` and proves admissibility, never the determination. **LB-7** makes `NOT_LOAD_BEARING` a positive finding, never a residual; **LB-8** confines the second field |
| 3 | RI-12's own example contradicted Example 2 | The rule's normative case still yielded `ANALYSIS` for the unprioritised analysis-plus-drafting request while the exemplar yielded `UNKNOWN` | RI-12 carries the worked case in full, test by test, and returns `primary_work_mode = UNKNOWN` with `secondary_work_modes = {ANALYSIS, DRAFTING}`. It says in terms why sequence, dependency and "feels central" are not tests. A check reads **both** tables and compares them |
| 4 | RI-6 degraded an unanswered C4 to `PREPARE` | Which contradicted CL-2, and silently substituted a different act for the one the user asked for | RI-6 follows CL-2 exactly: `AWAITING_CLARIFICATION`, then `BLOCKED`. There is no default to `PREPARE`; a later preparation-only request is a **new linked `Request`**, decided by the user |

### Stale reporting corrected

The preflight count in §5 and the failure-mode count in the document map were left behind by V2 and
are now unstated or derived rather than duplicated in prose; the EIB exemplar's closing line still
said "four triggers"; Example 2's outcome was still described as a constrained plan in one place.

**And a correction this package owes twice over:** both previous rounds reported that no separate
Phase 12 unit suite existed. It does — `implementation/phase-12/tests`, 157 tests — and it passes.
The claim came from listing one directory and was then repeated without being rechecked.

### Assurance added in V3

Two new checks and twelve new probes, each probe planted in a **fresh** second location rather than
one an existing check already happened to cover. Five of the twelve came back `REDUNDANT` on their
first run, and all five were closed **structurally** rather than by another phrase match: the worked
classification's own value and band rows, the architecture's identity row for the spec, HO-6's own
wording, RS-9's no-owner row, and the architecture's intake-check-7 row are now parsed and their
cells checked. That is the pattern the V3 review asked for — invariants over table rows, not single
sentences — and it is what the three prior rounds kept getting wrong.

**One of those five redundancies was caused by the denial test itself**: the worked-classification
row opens with the value "None", which the negation test read as a denial of the claim that
followed. A cell's *value* is not an argument, and a scan cannot tell the difference — which is why
that row is now read structurally instead.

## 7. Harness credibility

**Not high, and the reasons are specific rather than modest.**

1. **The validator and the architecture were written by the same party in the same pass.** It tests
   the architecture against the constraints its author was already trying to satisfy, which is the
   weakest possible form of assurance.
2. **Text-consistency checks cannot test an architecture.** Every check here reads documents. None
   executes a planner, because there is no planner. A package can be perfectly self-consistent and
   architecturally wrong, and this harness would report `PASS`.
3. **The pattern has now repeated inside Phase 15 itself, three times.** 32/32 and 28/28 → five
   blockers and 12 escapes. 47/47 and 45/45 → six blockers and four escapes, four of the six
   introduced by the previous remediation. 53/53 and 61/61 → four blockers and eight escapes, every
   one of the four a rule fixed in its owner document and left contradicted somewhere else. The V3
   reviewer rated this validator's assurance **`LOW`**, and on that record the rating is correct. A
   green board from this harness has three times meant nothing about whether the architecture is
   right, and there is no reason to treat the fourth as different. In Phases 12–14 the same pattern
   held.
4. **The probes test the checks, not the architecture.** A high detection rate means the checks are
   load-bearing against the weakenings the same author thought to write. It says nothing about the
   weakenings nobody thought of, and those are the ones independent reviewers keep finding.

**Results are reported in §8 exactly as executed**, including any probe that came back redundant on
its first run.

## 8. Validation results

| Run | Result |
|---|---|
| `validation/phase_15_validation.py` | **55/55 PASS** on default, `--verbose` and `--json` |
| `validation/phase_15_mutation_probes.py` | **73 probes, 73 DETECTED, 0 REDUNDANT, 0 ERROR** |
| Phase 8 validator | `119/119 PASS` |
| Phase 9 validator | `277/277 PASS` |
| Phase 10 validator | `145/147 PASS` — **inherited**, unchanged, not repaired here |
| Phase 11 validator | `159/160 PASS` — **inherited**, unchanged, not repaired here |
| Phase 12 validator | `55/55 PASS` |
| Phase 12 unit suite — `implementation/phase-12/tests` | **157 tests, OK** (`python3 -m unittest discover -s implementation/phase-12/tests`) |
| `git diff --check` | clean |
| Containment | only `planning/`, `prompts/` and `validation/phase_15_*` differ from the merge base |

**A correction to the two previous rounds' reporting.** Both said there was no separate Phase 12
unit suite and that `validation/phase_12_validation.py` was the whole of it. That was wrong: the
suite is at `implementation/phase-12/tests`, it is 157 tests, and it passes. The error came from
looking only inside `validation/` — a claim made from one directory listing and repeated without
being rechecked, which is the same failure mode as the architecture defects this package keeps
finding.

### V3: five probes came back REDUNDANT, and what that says

Five of the twelve new probes were `REDUNDANT` on their first run — the worst first-run rate of the
three rounds, and it is worth being plain about why. Every one of the five attacked a **fresh**
second location rather than one an existing check already covered, which is exactly what the V3
review asked for and exactly what the previous rounds' probe placement had been quietly avoiding. A
probe set that keeps returning DETECTED while an independent reader keeps finding escapes was
measuring its author's imagination, not the harness. All five are closed structurally.

### V2: three probes came back REDUNDANT, and three more validator defects

Three of the sixteen new probes were `REDUNDANT` on their first run, and each exposed a defect in a
check rather than in the architecture:

1. **A spec crossing the boundary unconditionally was not caught.** The weakening read *"specs …
   which Phase 11 intake accepts and revalidates"* — object before subject, which a
   subject-then-verb scan cannot match. The crossing row is now checked structurally: it must carry
   its condition.
2. **The load-bearing test moved back behind the reduction was not caught.** The forward half of the
   negation test read past the row's answering cell and found a *later* cell's denial of something
   else. The forward look now stops at the answering cell.
3. **The object-model row describing the spec AS a runtime Work Item was not caught**, for the same
   word-order reason as (1). That row is now checked structurally too.

### V1: one probe REDUNDANT, three validator defects

Recorded in full rather than dropped: the runtime-Work-Item probe was excused by a neighbouring
clause's denial; a G-5 test for `load_bearing` was satisfied by the failure column; and a scan could
not cross the dot inside `` `work_plan.<id>` ``. Two of those three were introduced by V1's own
remediation.

### The first round's probes and defects, retained

**Three of the seventeen new probes were `REDUNDANT` on their first run.** Each exposed a defect in
a check rather than a defect in the architecture, and each is recorded here rather than quietly
repaired:

1. **A runtime Work Item created before any run existed was not caught.** The new forward-looking
   half of the negation test excused it: the mutated sentence's *next* clause denied something
   else — *"…and cannot hold one in a pre-runtime state"* — and a denial anywhere in the window
   read as a denial of the claim. The forward window is now enabled only for a table row, where
   the answer genuinely follows the claim; prose is judged on what precedes the verb.
2. **Deleting the load-bearing requirement from preflight G-5 was not caught.** The check tested
   for `load_bearing` anywhere in the row, and the row's *failure* column still said
   `LOAD_BEARING`. It now tests for `load_bearing_basis`, which only the requirement names.
3. **The intake-check-1 probe was not caught.** The scan is bounded to a table cell and stops at a
   full stop, and `` `work_plan.<id>` `` contains one — so the pattern could not reach the verb it
   was looking for. That row is now checked structurally: the architecture's intake-check-1 row must say
   a Work Plan is **not** a Workflow definition and must carry the PO-4 dependency.

All three are the same class of error the first round produced: a check that tested the shape its
author expected rather than the shape the document has. Two of the three were introduced by *this
round's own* remediation, which is the more useful fact.

### Defects found in the first round, retained for the record

One probe was `REDUNDANT` on its first run then: the clarification check verified the record table
constraining `default_if_unanswered` while the probe rewrote the rule and left the table intact.
Three validator defects were found by running it, before any probe: a blockquote read one line at a
time, a column whose one affirmative cell reads "**Gates** the handoff", and a corrective pattern
missing the word *nothing*.

## 9. Readiness

This package is ready for an **independent architecture re-audit**, not for approval. The four V3
blockers are closed and nothing here approves anything. The questions a re-auditor should press
hardest:

1. **PO-4**, still — is a validated Work Plan an admissible execution basis for the approved
   Orchestrator, and if not, what is the COMPOSE path for? It is preserved as an explicit blocked
   implementation dependency, not resolved.
2. **Whether `PlannedWorkItemSpec` should exist at all before a consumer does.** It now produces a
   record no approved contract reads (PO-12). That is honest, and it may also be premature: an
   object defined without its consumer tends to acquire one by assumption, which is exactly the
   V2 blocker this round closed.
3. **Whether the LB-0…LB-6 predicate is decidable in practice.** It is deterministic on paper, and
   its hardest question is now the one LB-0 makes load-bearing: what *was* the originally requested
   deliverable, as opposed to what the planner understood it to be? That reading is itself
   `AI_SUGGESTION`, and the predicate rests on it.
4. **Whether a rule fixed in one document stays fixed.** All four V3 blockers were a rule
   corrected in its owner document and left contradicted in an active second location. Three rounds
   have now produced that same shape. A reviewer should assume it is present again and look for it
   first, in the documents this round touched least.
5. **Whether the planning layer can stay a planning layer.** Every pressure on a system like this
   pushes it toward re-planning mid-run, remembering across requests, and turning repeated patterns
   into registry entries. The boundaries here are structural (HO-11, HO-12, WL-4) precisely because
   policy boundaries erode — and a reviewer should check whether they are structural enough.

## 10. Non-Runtime Statement

This document is declarative architecture. It specifies no implementation and binds no provider or
runtime technology.
