"""Phase 16 — deterministic activation preflight.

Status: PROPOSED. Standard library only, deterministic, no network.

Turns a PlannerOutput into an ExecutionBasis, or refuses. Every refusal names its reason; none
is a warning attached to something that proceeds. The preflight decides ELIGIBILITY TO ENTER
INTAKE and nothing else: it satisfies no review, exercises no Right, registers nothing, and
never converts a requirement into the thing it requires.
"""

from __future__ import annotations

import hashlib
from typing import List, Optional, Tuple

import registries
from domain import (
    ActivationError, BasisStatus, BlockReason, Criticality, ExecutionBasis, ExecutionMode,
    GovernanceError, PlannerOutput, PlannerState, PrerequisiteState, REVIEW_FLOOR,
)

#: The Phase 14 implementation-specification baseline this bridge is written against.
IMPLEMENTATION_SPEC_VERSION = "phase-14@ba9e3fee"


class PreflightResult:
    def __init__(self, state: PlannerState, basis: Optional[ExecutionBasis],
                 reasons: Tuple[BlockReason, ...], detail: Tuple[str, ...]):
        self.state = state
        self.basis = basis
        self.reasons = reasons
        self.detail = detail

    @property
    def executable(self) -> bool:
        return self.basis is not None and self.basis.status is BasisStatus.EXECUTABLE

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "PreflightResult(state=%s, basis=%s, reasons=%s)" % (
            self.state.value, self.basis.ref if self.basis else None,
            [r.value for r in self.reasons])


def run_preflight(plan: PlannerOutput, *, author_identity: Optional[str] = None,
                  reviewer_identity: Optional[str] = None) -> PreflightResult:
    """The whole gate. Ordered so that the cheapest fail-closed checks come first."""
    reasons: List[BlockReason] = []
    detail: List[str] = []

    def block(reason: BlockReason, message: str) -> None:
        if reason not in reasons:
            reasons.append(reason)
        detail.append(message)

    # G-1  A caller may not hand over a pre-formed governed record.
    if plan.injected_governed_records:
        raise GovernanceError(
            "governed records are created by the approved Phase 14 commands, never supplied by "
            "a caller: %s" % list(plan.injected_governed_records))

    # G-2  Clarification blocks, and a blocking class carries no default.
    for clar in plan.clarifications:
        if clar.blocking and clar.default_if_unanswered is not None:
            raise ActivationError(
                "a blocking clarification may carry no default_if_unanswered: %r" % clar.question)
    if any(c.blocking for c in plan.clarifications):
        return PreflightResult(
            PlannerState.CLARIFICATION_REQUIRED, None,
            (BlockReason.CLARIFICATION_REQUIRED,),
            tuple("unresolved blocking clarification: %s" % c.question
                  for c in plan.clarifications if c.blocking))

    # G-3  Exactly one governed scope, with declared ancestry.
    if not plan.scope_ref:
        block(BlockReason.NO_VALID_SCOPE, "no governed scope resolves")
    elif not plan.scope_ancestry:
        block(BlockReason.SCOPE_AMBIGUOUS, "scope %s declares no ancestry" % plan.scope_ref)

    # G-4  Criticality resolves. It never defaults to Routine.
    if plan.criticality is None:
        block(BlockReason.CRITICALITY_UNRESOLVED,
              "criticality did not resolve; it does not default to ROUTINE")

    # G-5  Roles: approved, registered, and an owned conclusion with no owner blocks.
    approved_roles = registries.approved_roles()
    for role in plan.role_requirements:
        if role.role_ref is None:
            block(BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION,
                  "no approved Role owns %r" % role.owned_conclusion)
        elif role.role_ref not in approved_roles or not role.registered:
            block(BlockReason.UNREGISTERED_CAPABILITY,
                  "%s is not in the approved Role universe" % role.role_ref)

    # G-6  Skills: approved and registered, or non-assignable.
    approved_skills = registries.approved_skills()
    for skill in plan.skill_requirements:
        if skill.skill_ref not in approved_skills or not skill.registered:
            block(BlockReason.UNREGISTERED_CAPABILITY,
                  "%s is not a registered Skill and is not assignable" % skill.skill_ref)

    # G-7  Reviews are requirements. Planning never marks one satisfied.
    approved_reviews = registries.approved_review_profiles()
    for review in plan.review_requirements:
        if review.satisfied:
            raise GovernanceError(
                "planning may not mark a review satisfied: %s" % review.review_ref)
        if review.review_ref not in approved_reviews:
            block(BlockReason.REVIEW_UNRESOLVED,
                  "%s is not an approved Review Profile" % review.review_ref)
    if plan.criticality in REVIEW_FLOOR:
        if not any(r.mandatory for r in plan.review_requirements):
            block(BlockReason.REVIEW_UNRESOLVED,
                  "band %s requires an independent review and none is required by the plan"
                  % plan.criticality.value)

    # G-8  Rights are requirements. Planning never exercises one, and a missing Right blocks.
    approved_rights = registries.approved_decision_rights()
    for need in plan.decision_requirements:
        if need.exercised:
            raise GovernanceError(
                "planning may not exercise a Decision Right: %s" % need.decision_ref)
        if need.decision_ref is None:
            block(BlockReason.NO_APPLICABLE_DECISION_RIGHT,
                  "no applicable approved Right resolves for act %r" % need.act)
        elif need.decision_ref not in approved_rights:
            block(BlockReason.NO_APPLICABLE_DECISION_RIGHT,
                  "%s is not an approved Decision Right" % need.decision_ref)

    # G-9  Prerequisites are a strict tri-state; a plain UNKNOWN is dangling and blocks.
    for ev in plan.evidence_requirements:
        if ev.state is PrerequisiteState.UNKNOWN:
            block(BlockReason.DANGLING_PREREQUISITE,
                  "prerequisite %s is UNKNOWN, which is dangling, not deferred" % ev.reference)
        elif (ev.state is PrerequisiteState.FUTURE_GOVERNANCE_REFERENCE
                and ev.required_before_first_act):
            block(BlockReason.EVIDENCE_UNSATISFIED,
                  "%s is required before the first executable act and may not be deferred"
                  % ev.reference)

    # G-10 Separation of duties, at identity level.
    if author_identity is not None and reviewer_identity is not None \
            and author_identity == reviewer_identity:
        block(BlockReason.SOD_VIOLATION,
              "author and final critical reviewer are the same identity: %s" % author_identity)

    # G-11 Execution mode. MATCH binds an approved Workflow at an approved version; COMPOSE
    #      binds an instance-level Work Plan and creates no Workflow definition.
    if plan.execution_mode is ExecutionMode.MATCH:
        if not plan.workflow_ref:
            block(BlockReason.WORKFLOW_NOT_APPROVED, "MATCH names no Workflow")
        else:
            wf_id, _, version = plan.workflow_ref.partition("@")
            approved = registries.approved_workflows()
            if wf_id not in approved:
                block(BlockReason.WORKFLOW_NOT_APPROVED,
                      "%s is not an approved Workflow" % wf_id)
            elif not version:
                block(BlockReason.WORKFLOW_VERSION_STALE,
                      "%s is bound without a version" % wf_id)
            else:
                try:
                    bound = int(version)
                except ValueError:
                    bound = -1
                if bound != approved[wf_id]:
                    block(BlockReason.WORKFLOW_VERSION_STALE,
                          "%s is bound at v%s; the approved version is v%d"
                          % (wf_id, version, approved[wf_id]))
    else:
        if plan.work_plan is None:
            block(BlockReason.BASIS_NOT_EXECUTABLE, "COMPOSE produced no Work Plan")
        else:
            _check_plan_shape(plan, block)

    if reasons:
        return PreflightResult(PlannerState.BLOCKED, None, tuple(reasons), tuple(detail))

    basis = ExecutionBasis(
        basis_id="execution_basis." + hashlib.sha256(
            (plan.request_id + "|" + plan.scope_ref).encode()).hexdigest()[:16],
        version=1,
        request_id=plan.request_id,
        intent_id=plan.intent_id,
        scope_ref=plan.scope_ref,
        scope_ancestry=plan.scope_ancestry,
        execution_mode=plan.execution_mode,
        criticality=plan.criticality,
        planning_digest=plan.material_digest(),
        implementation_spec_version=IMPLEMENTATION_SPEC_VERSION,
        orchestrator_policy_ref=plan.orchestrator_policy_ref,
        status=BasisStatus.VALIDATED,
        workflow_ref=plan.workflow_ref,
        work_plan_ref=plan.work_plan.ref if plan.work_plan else None,
        role_bindings=tuple(r.role_ref for r in plan.role_requirements),
        skill_bindings=tuple(s.skill_ref for s in plan.skill_requirements),
        review_requirements=tuple(r.review_ref for r in plan.review_requirements),
        decision_requirements=tuple(d.decision_ref for d in plan.decision_requirements),
        evidence_requirements=tuple((e.reference, e.state.value)
                                    for e in plan.evidence_requirements),
    )
    # VALIDATED -> EXECUTABLE is the whole of what this phase adds. It says intake MAY accept
    # the trigger. It says nothing about whether any gate is satisfied or any act permitted.
    basis.status = BasisStatus.EXECUTABLE
    return PreflightResult(PlannerState.VALIDATED, basis, (), ())


def _check_plan_shape(plan: PlannerOutput, block) -> None:
    """A composed plan is acyclic, and its gate stage has no Role participation."""
    stages = {s.stage_id: s for s in plan.work_plan.stages}
    for stage in plan.work_plan.stages:
        if stage.is_gate and stage.role_ref is not None:
            block(BlockReason.BASIS_NOT_EXECUTABLE,
                  "gate stage %s has Role participation; a gate is not work" % stage.stage_id)
        for dep in stage.depends_on:
            if dep not in stages:
                block(BlockReason.BASIS_NOT_EXECUTABLE,
                      "stage %s depends on unknown stage %s" % (stage.stage_id, dep))
    # Cycle detection, iterative rather than recursive.
    colour = {s: 0 for s in stages}
    for start in list(stages):
        if colour[start]:
            continue
        stack = [(start, iter(stages[start].depends_on))]
        colour[start] = 1
        while stack:
            node, children = stack[-1]
            advanced = False
            for child in children:
                if child not in colour:
                    continue
                if colour[child] == 1:
                    block(BlockReason.BASIS_NOT_EXECUTABLE,
                          "the composed plan has a dependency cycle at %s" % child)
                    return
                if colour[child] == 0:
                    colour[child] = 1
                    stack.append((child, iter(stages[child].depends_on)))
                    advanced = True
                    break
            if not advanced:
                colour[node] = 2
                stack.pop()
