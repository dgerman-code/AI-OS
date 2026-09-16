"""Phase 16 — deterministic activation preflight.

Status: PROPOSED. Standard library only, deterministic, no network.

Turns a PlannerOutput into an ExecutionBasis, or refuses. Every refusal names its reason; none
is a warning attached to something that proceeds. The preflight decides ELIGIBILITY TO ENTER
INTAKE and nothing else: it satisfies no review, exercises no Right, registers nothing, and
never converts a requirement into the thing it requires.
"""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional, Tuple

import registries
from workflow_contract import workflow_contract
from domain import (
    ActivationError, BasisStatus, BlockReason, Criticality, ExecutionBasis, ExecutionMode,
    GovernanceError, IMPLEMENTATION_SPEC_VERSION, PlannerOutput, PlannerState,
    PrerequisiteState, REVIEW_FLOOR,
)

__all__ = ["IMPLEMENTATION_SPEC_VERSION", "PreflightResult", "run_preflight"]

_ISSUABLE: Dict[int, Tuple[ExecutionBasis, str, str, str]] = {}
_PLACEHOLDER_CONCLUSIONS = {
    "", "-", "...", "tbd", "todo", "unknown", "n/a", "na", "none", "placeholder",
    "to be determined", "to be defined",
}


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

    def __repr__(self) -> str:  # pragma: no cover
        return "PreflightResult(state=%s, basis=%s, reasons=%s)" % (
            self.state.value, self.basis.ref if self.basis else None,
            [r.value for r in self.reasons])


def _register_issuable(plan: PlannerOutput, basis: ExecutionBasis) -> None:
    _ISSUABLE[id(basis)] = (basis, plan.request_id, plan.material_digest(), basis.payload_seal())


def _consume_issuance_provenance(basis: ExecutionBasis) -> Tuple[str, str, str]:
    entry = _ISSUABLE.pop(id(basis), None)
    if entry is None or entry[0] is not basis:
        raise ActivationError(
            "Execution Basis has no unused successful-preflight provenance; fabricated, copied, "
            "blocked or already-issued bases are not issuable")
    _basis, request_id, digest, seal = entry
    if request_id != basis.request_id or digest != basis.planning_digest or seal != basis.payload_seal():
        raise ActivationError("successful-preflight provenance does not match the basis payload")
    return request_id, digest, seal


def _substantive_conclusion(text: Optional[str]) -> bool:
    if text is None:
        return False
    normalized = " ".join(str(text).split()).strip().lower()
    return bool(normalized) and normalized not in _PLACEHOLDER_CONCLUSIONS


def _check_match_completeness(plan: PlannerOutput, workflow_id: str, block) -> None:
    """Verify that MATCH did not omit requirements carried by the selected Workflow.

    Selection must not be able to pass by supplying only a valid Workflow identity. The Workflow
    card is the requirement authority; the PlannerOutput is checked against it, not trusted to be
    complete merely because its supplied requirements individually validate.
    """
    try:
        contract = workflow_contract(workflow_id)
    except (OSError, registries.RegistryEvidenceError) as exc:
        block(BlockReason.WORKFLOW_NOT_APPROVED,
              "cannot resolve the selected Workflow contract: %s" % exc)
        return

    roles = {r.role_ref for r in plan.role_requirements if r.role_ref}
    reviews = {r.review_ref for r in plan.review_requirements}
    decisions = {d.decision_ref for d in plan.decision_requirements if d.decision_ref}
    evidence = {e.reference for e in plan.evidence_requirements}
    skills = {s.skill_ref for s in plan.skill_requirements}

    for ref in sorted(contract.mandatory_roles - roles):
        block(BlockReason.BASIS_NOT_EXECUTABLE,
              "MATCH omits mandatory Workflow Role requirement %s" % ref)
    for ref in sorted(contract.required_reviews - reviews):
        block(BlockReason.REVIEW_UNRESOLVED,
              "MATCH omits Workflow Review requirement %s" % ref)
    for ref in sorted(contract.required_decisions - decisions):
        block(BlockReason.NO_APPLICABLE_DECISION_RIGHT,
              "MATCH omits Workflow Decision Right requirement %s" % ref)
    for ref in sorted(contract.required_evidence - evidence):
        block(BlockReason.EVIDENCE_UNSATISFIED,
              "MATCH omits Workflow precondition evidence requirement %s" % ref)
    for ref in sorted(contract.required_skills - skills):
        block(BlockReason.UNREGISTERED_CAPABILITY,
              "MATCH omits REQUIRED_CORE Skill requirement %s" % ref)

    approved_reviews = registries.approved_review_profiles()
    for ref in sorted(contract.required_reviews):
        if ref not in approved_reviews:
            block(BlockReason.REVIEW_UNRESOLVED,
                  "selected Workflow references unresolved Review Profile %s" % ref)
    approved_rights = registries.approved_decision_rights()
    for ref in sorted(contract.required_decisions):
        if ref not in approved_rights:
            block(BlockReason.NO_APPLICABLE_DECISION_RIGHT,
                  "selected Workflow references unresolved Decision Right %s" % ref)


def run_preflight(plan: PlannerOutput, *, author_identity: Optional[str] = None,
                  reviewer_identity: Optional[str] = None) -> PreflightResult:
    reasons: List[BlockReason] = []
    detail: List[str] = []

    def block(reason: BlockReason, message: str) -> None:
        if reason not in reasons:
            reasons.append(reason)
        detail.append(message)

    if plan.injected_governed_records:
        raise GovernanceError(
            "governed records are created by the approved Phase 14 commands, never supplied by "
            "a caller: %s" % list(plan.injected_governed_records))

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

    if not plan.scope_ref:
        block(BlockReason.NO_VALID_SCOPE, "no governed scope resolves")
    elif not plan.scope_ancestry:
        block(BlockReason.SCOPE_AMBIGUOUS, "scope %s declares no ancestry" % plan.scope_ref)

    if plan.criticality is None:
        block(BlockReason.CRITICALITY_UNRESOLVED,
              "criticality did not resolve; it does not default to ROUTINE")

    approved_roles = registries.approved_roles()
    for role in plan.role_requirements:
        if role.role_ref is None:
            block(BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION,
                  "no approved Role owns %r" % role.owned_conclusion)
        elif role.role_ref not in approved_roles or not role.registered:
            block(BlockReason.UNREGISTERED_CAPABILITY,
                  "%s is not in the approved Role universe" % role.role_ref)
        if role.load_bearing and not _substantive_conclusion(role.owned_conclusion):
            block(BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION,
                  "%s is load-bearing but carries no substantive owned conclusion"
                  % role.role_ref)

    approved_skills = registries.approved_skills()
    for skill in plan.skill_requirements:
        if skill.skill_ref not in approved_skills or not skill.registered:
            block(BlockReason.UNREGISTERED_CAPABILITY,
                  "%s lacks explicit individual Skill approval evidence and is not assignable"
                  % skill.skill_ref)
            continue
        if skill.for_role is None or skill.for_role not in approved_roles:
            block(BlockReason.UNREGISTERED_CAPABILITY,
                  "%s is claimed for %r, which is not an approved Role"
                  % (skill.skill_ref, skill.for_role))
            continue
        compatible, why = registries.skill_is_compatible_with_role(
            skill.skill_ref, skill.for_role)
        if not compatible:
            block(BlockReason.SKILL_ROLE_INCOMPATIBLE, why)

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

    for ev in plan.evidence_requirements:
        if ev.state is PrerequisiteState.UNKNOWN:
            block(BlockReason.DANGLING_PREREQUISITE,
                  "prerequisite %s is UNKNOWN, which is dangling, not deferred" % ev.reference)
        elif (ev.state is PrerequisiteState.FUTURE_GOVERNANCE_REFERENCE
                and ev.required_before_first_act):
            block(BlockReason.EVIDENCE_UNSATISFIED,
                  "%s is required before the first executable act and may not be deferred"
                  % ev.reference)

    if author_identity is not None and reviewer_identity is not None \
            and author_identity == reviewer_identity:
        block(BlockReason.SOD_VIOLATION,
              "author and final critical reviewer are the same identity: %s" % author_identity)

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
            elif version != approved[wf_id]:
                block(BlockReason.WORKFLOW_VERSION_STALE,
                      "%s is bound at version %s; the approved card declares version %s"
                      % (wf_id, version, approved[wf_id]))
            else:
                _check_match_completeness(plan, wf_id, block)
    else:
        if plan.work_plan is None:
            block(BlockReason.BASIS_NOT_EXECUTABLE, "COMPOSE produced no Work Plan")
        else:
            _check_plan_shape(plan, block, approved_roles)

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
    ).with_status(BasisStatus.EXECUTABLE)
    _register_issuable(plan, basis)
    return PreflightResult(PlannerState.VALIDATED, basis, (), ())


def _check_plan_shape(plan: PlannerOutput, block, approved_roles) -> None:
    seen = set()
    duplicates = set()
    for stage in plan.work_plan.stages:
        if stage.stage_id in seen:
            duplicates.add(stage.stage_id)
        seen.add(stage.stage_id)
    for duplicate in sorted(duplicates):
        block(BlockReason.DUPLICATE_STAGE_IDENTITY,
              "stage id %s appears more than once; stage identity must be unique before a "
              "basis is issued" % duplicate)

    owned_conclusions = {
        r.role_ref for r in plan.role_requirements
        if r.role_ref and (not r.load_bearing or _substantive_conclusion(r.owned_conclusion))
    }
    stages = {s.stage_id: s for s in plan.work_plan.stages}
    for stage in plan.work_plan.stages:
        if stage.is_gate:
            if stage.role_ref is not None:
                block(BlockReason.BASIS_NOT_EXECUTABLE,
                      "gate stage %s has Role participation; a gate is not work"
                      % stage.stage_id)
        else:
            if stage.role_ref is None:
                block(BlockReason.STAGE_OWNER_UNRESOLVED,
                      "stage %s has no effective owner and is not a gate" % stage.stage_id)
            elif stage.role_ref not in approved_roles:
                block(BlockReason.UNREGISTERED_CAPABILITY,
                      "stage %s is owned by %s, which is not in the approved Role universe"
                      % (stage.stage_id, stage.role_ref))
            elif stage.role_ref not in owned_conclusions:
                block(BlockReason.STAGE_OWNER_UNRESOLVED,
                      "stage %s is owned by %s, which has no substantive declared owned "
                      "conclusion" % (stage.stage_id, stage.role_ref))
        for dep in stage.depends_on:
            if dep not in stages:
                block(BlockReason.BASIS_NOT_EXECUTABLE,
                      "stage %s depends on unknown stage %s" % (stage.stage_id, dep))
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
