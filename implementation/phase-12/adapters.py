"""Phase 12 MVP — provider and runtime boundaries, with in-memory stubs.

Status: PROPOSED (implementation-equivalent non-approved status).

Everything the approved architecture treats as *outside* the orchestrator lives behind an
adapter here: the Router, the reviewer desk, the decision authority, and model execution. Each
adapter is a narrow protocol with an in-memory reference implementation.

No network, no provider SDK, no credentials, no live model call. The stubs return recorded
fixtures. That is deliberate: the MVP's claim is about the control model, and a real provider
would prove nothing about it while coupling governance objects to a vendor.
"""

from typing import Dict, List, Optional, Tuple

from domain import (
    Canonicality, DecisionRecord, DecisionRecordRef, DecisionRequest, DecisionRightRef,
    GateOutcome, GovernanceError, HumanAuthorityRef, ModelInvocationRequest, ModelProfileRef,
    ModelRef, ModelResult, Origin, ReviewInstance, ReviewInstanceRef, ReviewProfileRef,
    ReviewRequest, RouterOutcome, RouterRef, RoutingDecision, RoutingDecisionRef,
    RoutingRequest, require,
)


# ===========================================================================================
# Router boundary
# ===========================================================================================


class RouterAdapter:
    """Answers exactly one question: which execution capability is eligible and preferred.

    It never sets a gate state, never decides whether work is done, and never sees the run's
    phase. The orchestrator asks; the Router answers; the answer is a separate object."""

    def route(self, request: RoutingRequest) -> RoutingDecision:  # pragma: no cover - protocol
        raise NotImplementedError


class InMemoryRouter(RouterAdapter):
    """A Router stub driven by a declared eligible set.

    There is no fallback outside the eligible set. When nothing is eligible the answer is
    `NO_ELIGIBLE_MODEL`, which the orchestrator turns into a block - not into a second attempt
    with the constraints relaxed."""

    def __init__(self, ref: RouterRef,
                 eligible: Optional[Dict[str, Tuple[ModelRef, ModelProfileRef]]] = None,
                 missing_right_for: Tuple[str, ...] = ()):
        self.ref = require(ref, RouterRef, "router")
        self.eligible = eligible or {}
        self.missing_right_for = missing_right_for
        self.requests: List[RoutingRequest] = []
        self._serial = 0

    def route(self, request: RoutingRequest) -> RoutingDecision:
        if not isinstance(request, RoutingRequest):
            raise GovernanceError("the Router only answers a Routing Request")
        self.requests.append(request)
        self._serial += 1
        ref = RoutingDecisionRef("rd-%d" % self._serial)
        if request.capability in self.missing_right_for:
            return RoutingDecision(ref, request.work_item,
                                   RouterOutcome.NO_APPLICABLE_DECISION_RIGHT,
                                   decided_by=self.ref)
        candidate = self.eligible.get(request.capability)
        if candidate is None:
            return RoutingDecision(ref, request.work_item, RouterOutcome.NO_ELIGIBLE_MODEL,
                                   decided_by=self.ref)
        model, profile = candidate
        return RoutingDecision(ref, request.work_item, RouterOutcome.ELIGIBLE_CANDIDATE,
                               model=model, model_profile=profile, decided_by=self.ref)


# ===========================================================================================
# Model execution boundary
# ===========================================================================================


class ModelAdapter:
    def execute(self, request: ModelInvocationRequest) -> ModelResult:  # pragma: no cover
        raise NotImplementedError


class StubModel(ModelAdapter):
    """Returns a fixed string. No network call, no provider client, no credential.

    Whatever it returns is an `AI_SUGGESTION` with origin `AI_GENERATED`, because `ModelResult`
    admits nothing else."""

    def __init__(self, text: str = "draft produced by a model"):
        self.text = text
        self.invocations: List[ModelInvocationRequest] = []

    def execute(self, request: ModelInvocationRequest) -> ModelResult:
        self.invocations.append(request)
        return ModelResult(request.work_item, request.model, self.text,
                           origin=Origin.AI_GENERATED,
                           canonicality=Canonicality.AI_SUGGESTION)


# ===========================================================================================
# Review boundary (Phase 6)
# ===========================================================================================


class ReviewerAdapter:
    def review(self, request: ReviewRequest) -> ReviewInstance:  # pragma: no cover - protocol
        raise NotImplementedError


class InMemoryReviewerDesk(ReviewerAdapter):
    """A reviewer desk holding pre-recorded review outcomes by Review Profile.

    A reviewer is a human authority. There is no code path here that lets an Agent Instance or
    a model stand in for one: `ReviewInstance` requires a `HumanAuthorityRef`."""

    def __init__(self, outcomes: Dict[str, Tuple[GateOutcome, HumanAuthorityRef, str]]):
        self.outcomes = outcomes
        self.requests: List[ReviewRequest] = []
        self._serial = 0

    def review(self, request: ReviewRequest) -> ReviewInstance:
        require(request.review_profile, ReviewProfileRef, "review request")
        self.requests.append(request)
        recorded = self.outcomes.get(request.review_profile.id)
        if recorded is None:
            raise GovernanceError(
                "no reviewer is available for %s; the gate stays unsatisfied"
                % request.review_profile)
        outcome, reviewer, independence = recorded
        self._serial += 1
        return ReviewInstance(ReviewInstanceRef("ri-%d" % self._serial), request.work_item,
                              request.review_profile, outcome, reviewer, independence)


# ===========================================================================================
# Decision authority boundary (Phase 7)
# ===========================================================================================


class DecisionAuthorityAdapter:
    def decide(self, request: DecisionRequest):  # pragma: no cover - protocol
        raise NotImplementedError


class InMemoryDecisionDesk(DecisionAuthorityAdapter):
    """Holds the approved Decision Rights and the humans who hold them.

    When no approved Right covers the act, the desk returns `NO_APPLICABLE_DECISION_RIGHT` and
    **no Decision Record at all**. That absence is the point: there is nothing for the
    orchestrator to mistake for an approval, and the run goes to BLOCKED and ESCALATED with
    posture AUTHORITY_ABSENT."""

    def __init__(self, rights: Dict[str, Tuple[HumanAuthorityRef, GateOutcome]]):
        self.rights = rights
        self.requests: List[DecisionRequest] = []
        self._serial = 0

    def decide(self, request: DecisionRequest):
        require(request.decision_right, DecisionRightRef, "decision request")
        self.requests.append(request)
        held = self.rights.get(request.decision_right.id)
        if held is None:
            return (GateOutcome.NO_APPLICABLE_DECISION_RIGHT, None)
        holder, outcome = held
        self._serial += 1
        record = DecisionRecord(DecisionRecordRef("dr-%d" % self._serial), request.work_item,
                                request.decision_right, outcome, holder)
        return (outcome, record)
