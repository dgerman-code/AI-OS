# Registry Eligibility Contract

Status: `PROPOSED` — Phase 16 candidate. Approves nothing, registers nothing.

What makes an identity eligible to appear in an Execution Basis. This document exists because
the first Phase 16 implementation answered that question by **parsing mentions**, and
mention-based parsing invents eligibility.

## 1. What went wrong, exactly

Two defects, both of them the same mistake in different clothes.

**Slugged Role IDs.** Role identities were derived by lower-casing and slugging the display
names in the approved master universe. Three names contain an ampersand, and the slugger split
each one into separate words:

| Approved display name | What the slugger produced | What the Role Card declares |
|---|---|---|
| Asset O&M / Technical Operations Specialist | `role.asset_o_m_technical_operations_specialist` | `role.asset_om_technical_operations_specialist` |
| ESG / E&S Specialist | `role.esg_e_s_specialist` | `role.esg_es_specialist` |
| FP&A / Management Finance Specialist | `role.fp_a_management_finance_specialist` | `role.fpa_management_finance_specialist` |

The count was still 59, so the check that asserted "59 Roles" passed. Three of the 59 were
identities that exist nowhere in the repository, and the three real ones were unassignable.

**Scraped everything else.** Skills, Review Profiles, Decision Rights and Workflows were
derived by collecting every backticked `` `prefix.id` `` token from whole documents. That
counted prose references, candidates explicitly held in consolidation and overlap groups,
worked examples, counter-examples, and `Supersedes:` lines naming **retired** identities. The
reported registries were 224 Skills, 44 Review Profiles, 97 Decision Rights and 57 Workflows.
The **carded** sets are 6, 6, 8 and 4 — and carded is not the same question as approved; see §2a.

Both defects fail **open**: they make more things assignable than governance ever approved.
That is the wrong direction for a registry check to be wrong in.

## 2. The rule

An identity is eligible only when all three hold. Each is evidence; none is inference.

| # | Condition | Where the evidence is |
|---:|---|---|
| RE-1 | A **card declares** the identity, in its Identity block, as `- <Kind> ID: `<prefix>.<id>`` | the card file |
| RE-2 | The card declares a **Version**, and is not superseded | the card's `Version:` and `Superseded By:` lines |
| RE-3 | A **human approval record** covers that card class, in its own approved-scope wording | `reviews/phase-<n>-final-approval.md` |

Emphasis is typography, not meaning: `- Decision ID: **`decision.x`**` declares exactly what
`- Decision ID: `decision.x`` declares.

### Approval evidence, per kind

| Kind | Approval record | The phrase relied on |
|---|---|---|
| Role | Phase 3 final approval | "59 unique Role IDs" |
| Workflow | Phase 5 final approval | "the four exemplar Workflow Cards" |
| Review Profile | Phase 6 final approval | "the six exemplar Review Profiles" |
| Decision Right | Phase 7 final approval | "the eight exemplar Decision Right Cards" |
| Skill | **none** — see §2a | — |

## 2a. Carded is not approved: the Skill case

This section corrects a reading this document originally got wrong. An earlier version listed
the Phase 4 approval phrase "the current selective exemplar card set" as approval evidence for
Skills, and so reported six **approved** Skills. That is not what the Phase 4 record says. It
says the opposite, in terms:

> Existing Phase 4 cards may remain individually `PROPOSED` unless and until their own governed
> approval state is explicitly changed. This Phase-level decision must not be interpreted as a
> mass status promotion of all cards or universe entries.

So there are two different questions, and they get two different views:

| Question | View | Answer today |
|---|---|---|
| Does a card for this Skill exist, versioned and unsuperseded? | `carded_skills()` | **6** |
| Is this Skill individually approved for execution? | `approved_skills()` | **none** |

**Rule RE-4 — architecture approval never becomes individual approval.** A phase-level record
that approves a registry's *architecture* cannot satisfy individual approval for a card inside
it. The implementation excludes `phase-4-final-approval.md` from the individual-approval search
by name, so the phase record cannot be read as the card's approval even accidentally.

**Rule RE-5 — individual Skill approval needs the card marked `APPROVED` and a separate human
approval record naming that identity.** No card meets that today, so `approved_skills()` is
legitimately empty, and any plan naming a Skill requirement **blocks** with
`UNREGISTERED_CAPABILITY`.

That is a real consequence and it is the correct one: it means the Phase 16 bridge currently
cannot assign any Skill, and a reviewer should read that as the registry failing closed rather
than as a gap to be worked around. A carded Skill's mapping to a Role is evidence of
**applicability**, never of eligibility; the two gates stand in that order.

If the record is unreadable, is not marked `APPROVED — HUMAN DECISION`, or no longer contains
the phrase its scope was read from, that whole kind resolves to the **empty set**. Fail closed,
never fail open: a registry that cannot prove its approval evidence has no entries, rather than
quietly keeping the ones it remembers.

### Roles, additionally

Roles are cross-checked in both directions against the approved master universe, by display
name, and against the count the Phase 3 approval record states. A carded Role absent from the
approved universe is not approved; an approved universe entry with no card has no resolvable
identity. Either mismatch empties the Role registry rather than reporting 58 or 60.

## 3. What is NOT eligible

| Not eligible | Why |
|---|---|
| An uncarded entry in a candidate universe | The Review-Profile and Decision-Right universes call themselves candidate lists in their own opening paragraphs; the Phase 5 approval states a carding boundary of 4 carded and 45 uncarded |
| A prose reference or a worked example | A document mentioning an identity is not a document registering one |
| A candidate held in a consolidation or overlap group | Its disposition is a proposal for a later governed pass |
| A retired identity named by a `Supersedes:` line | It is named precisely because it no longer exists |
| A template | `_templates/` and `_standards/` hold shapes, not identities |
| A slug derived from a display name | Display names are for people; IDs are declared |

## 4. Versions are evidence too

The approved version of a Workflow is the version its **card declares**. The first
implementation returned the integer `1` for every Workflow, so a MATCH at a version nobody ever
approved resolved cleanly. Under this contract a MATCH must name the declared version exactly;
`workflow.<id>@1` against a card declaring `0.1` is `WORKFLOW_VERSION_STALE`.

## 5. Role-to-Skill compatibility

Registration alone was never enough: a registered Skill bound to the wrong Role is an
unassignable binding. The Phase 4 mapping records state in terms that they are "the sole
authoritative source for relationship type", so compatibility is read from them and from
nowhere else:

| Relationship | Assignable |
|---|---|
| `REQUIRED_CORE`, `REQUIRED_FOR_CONTEXT`, `OPTIONAL`, `ALTERNATIVE` | yes |
| `PROHIBITED_IN_CONTEXT` | no — this is the case the check exists for |
| the pair appears in no record | no — silence in the authoritative record is not permission |

## 6. What this contract does not do

It does not approve a card, promote a candidate, widen a universe, or change any registry. It
reads. Every view in `implementation/phase-16/registries.py` is read-only, and the module has
no function that could add an entry. Individual cards remain `PROPOSED` exactly as their own
phase approval records say they do — which is part of why an Execution Basis is itself
`PROPOSED` and authorises only entry to intake.
