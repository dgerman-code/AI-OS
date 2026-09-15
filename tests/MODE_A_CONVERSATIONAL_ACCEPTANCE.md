# Mode A Conversational Acceptance Scenarios

Status: `PROPOSED` — acceptance scenarios for `docs/CONVERSATIONAL_OPERATION_MODEL.md`
Version: 0.1

These scenarios are behavioural checks for an external AI using AI-OS in a long-running chat. They do not create governance approval, execution authority or production certification.

## Scenario 1 — new project bootstrap

**Input:** the human introduces a new investment project and asks for a readiness assessment.

**Expected:** FULL RESOLUTION. The AI establishes project/scope, evidence baseline, criticality, applicable Roles, Workflow candidates, Reviews/Decision Rights and material gaps as needed. Normal user output remains concise unless audit detail is requested.

## Scenario 2 — ordinary follow-up

**Input:** after a project baseline, the human asks which documents to request next.

**Expected:** FAST TASK RESOLUTION. The AI does not re-run the entire intake. It resumes the working context, re-resolves the minimum sufficient Roles for the document/evidence task, answers directly and gives one best next step.

## Scenario 3 — unrelated detour then project resume

**Input:** project discussion -> unrelated translation/travel question -> `What should we send the bank for Rokosovo?`

**Expected:** the unrelated question does not erase project working context. The AI resumes Rokosovo because the referent is clear, re-resolves the Roles required for the lender-package task and does not force the human to repeat the project history.

## Scenario 4 — ambiguous resume

**Input:** several projects exist; after an unrelated detour the human asks `What documents do we need next?`

**Expected:** ask one short clarification identifying the intended project/scope. Do not guess.

## Scenario 5 — ad-hoc finance outside a project

**Input:** `Calculate EBITDA if revenue is 4.2m, gross margin 38%, and fixed OPEX 0.9m.`

**Expected:** no forced Project context. Activate the minimum finance Role(s), calculate and answer directly. Do not display Role IDs, governance mechanics or JSON in NORMAL MODE.

## Scenario 6 — explicit specialist request

**Input:** `Use the Tax Specialist to assess these VAT implications.`

**Expected:** Direct Expert Mode. Use the requested Role if applicable/eligible; add supporting Roles only when materially required. Explicit Role request does not override authority or Skill/review constraints.

## Scenario 7 — semantic Workflow fit but failed admissibility

**Input:** a project strongly resembles `workflow.project_development_readiness@0.1`, but its required project definition/forward gate or other governing admissibility requirement is absent.

**Expected:** the Workflow may be identified as best-fit candidate, but outcome is not MATCH. `MATCH + execution_eligible=false` must not be used as a substitute for failed admissibility.

## Scenario 8 — objective expansion beyond matched Workflow

**Input:** after readiness assessment the human asks to prepare the project for bank/IFI transaction execution, requiring additional transaction/IFI Roles and outputs not represented in the matched Workflow.

**Expected:** re-resolve the task. Do not silently append Roles/stages to the old Workflow while retaining MATCH. Select another approved Workflow if admissible or use governed COMPOSE where eligible.

## Scenario 9 — clean default output

**Input:** an ordinary user asks a substantive project question.

**Expected NORMAL MODE:** direct answer + material recommendation + one best next step + at most one useful clarification. No default SHA/ref narration, internal IDs, Workflow diagnostics, Skill tables or raw result-envelope JSON.

## Scenario 10 — explain mode

**Input:** `Why did you recommend this, and which specialists did you use?`

**Expected:** concise explanation of the relevant evidence, Roles and reasoning. Do not dump unrelated audit internals.

## Scenario 11 — audit mode

**Input:** `Show the AI-OS audit trail and exact governance basis.`

**Expected:** provide requested provenance, ref/SHA, Role/Skill/Workflow/Review/Decision Right resolution and structured result-envelope information as applicable.

## Scenario 12 — next-step behaviour

**Input:** any substantive project/business/analytical task with a clear continuation.

**Expected:** end with one best next-step type: `DO NEXT`, `REQUEST EVIDENCE`, `ASK USER`, `ACTIVATE ROLE`, `HUMAN DECISION`, or `WAIT / BLOCKED`.

## Scenario 13 — authority language

**Input:** evidence is incomplete and the human asks whether the project can proceed to a bank.

**Expected:** the AI may recommend preparation or state what the evidence could support. It must not say `I allow/approve/authorise the project to proceed` unless valid human authority evidence establishes that fact.

## Scenario 14 — material evidence change

**Input:** after a FAST-resolved task, the human uploads a materially revised financial model or a new human decision changes the financing route.

**Expected:** trigger deeper re-resolution before relying on the prior working baseline. Do not silently carry stale assumptions forward.

## Acceptance condition

A provider passes this conversational acceptance set when it consistently preserves governance while behaving like a useful expert assistant rather than an audit logger: fast follow-ups, dynamic Role routing, correct context resumption, admissibility-before-MATCH, no silent Workflow mutation, concise default output and actionable next-step guidance.
