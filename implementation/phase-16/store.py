"""Phase 16 — in-memory reference store for basis issuance, lineage and trigger idempotency.

Status: PROPOSED. In-memory only. No database, no migration, no persistence configuration, no
Supabase, no deployment. It exists to make the issuance, integrity, version, lineage and
duplicate-trigger invariants testable, not to be a storage layer.

WHAT CHANGED AND WHY. The first version stored MUTABLE bases and handed the same object back to
every caller, so "the issued basis" and "whatever the last holder edited" were the same thing:
a holder could flip a STALE basis back to EXECUTABLE, repoint its scope, or drop a review
requirement, and no downstream check could tell. The store now keeps IMMUTABLE SNAPSHOTS and a
SEAL taken at issue. `issued()` is the only authority on what was issued, a transition writes a
new snapshot beside the old one rather than over it, and the trigger builder verifies a
presented basis against the seal instead of trusting the object it was handed.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from domain import ActivationError, BasisStatus, ExecutionBasis, GovernanceError


class _Issued:
    """One issued basis: the snapshot exactly as issued, its seal, and its lifecycle."""

    __slots__ = ("payload", "seal", "status", "superseded_by", "stale_reason", "transitions")

    def __init__(self, payload: ExecutionBasis):
        self.payload = payload
        self.seal = payload.payload_seal()
        self.status = payload.status
        self.superseded_by: Optional[str] = None
        self.stale_reason: Optional[str] = None
        self.transitions: List[str] = [payload.status.value]

    def snapshot(self) -> ExecutionBasis:
        """The issued payload at its current lifecycle status. A new object every time."""
        return self.payload.with_status(self.status)

    def _transition(self, status: BasisStatus) -> None:
        self.status = status
        self.transitions.append(status.value)


class ActivationStore:
    def __init__(self) -> None:
        self._issued: Dict[str, _Issued] = {}
        self._by_request: Dict[str, List[str]] = {}
        self._triggers: Dict[str, str] = {}
        self._candidates: List[dict] = []

    # -- execution bases ---------------------------------------------------------------------

    def issue(self, basis: ExecutionBasis) -> ExecutionBasis:
        """Issue a candidate basis, superseding any live basis for the same request.

        Superseding is not deletion: the prior basis stays readable, in SUPERSEDED, with the
        reference of the one that replaced it. Governed history is append-only.
        """
        if basis.is_approval or basis.is_authority:
            raise GovernanceError(
                "an Execution Basis is neither an approval nor an authority; a candidate "
                "claiming to be one is refused rather than stored")
        # Versioning follows the LATEST basis for the request, whatever its status. Reading only
        # the live one lost the lineage the moment a basis went STALE: the replacement started
        # again at v1 with no supersedes link, which is exactly the history a governed record
        # may not lose.
        previous = self._latest(basis.request_id)
        version = 1
        supersedes = None
        if previous is not None:
            if previous.payload.planning_digest == basis.planning_digest \
                    and previous.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE):
                return previous.snapshot()     # idempotent reuse: same request, same version
            version = previous.payload.version + 1
            supersedes = previous.payload.ref

        issued = _Issued(basis.with_status(basis.status, version=version,
                                           supersedes=supersedes))
        if previous is not None and previous.status is not BasisStatus.SUPERSEDED:
            previous._transition(BasisStatus.SUPERSEDED)
            previous.superseded_by = issued.payload.ref
        self._issued[issued.payload.ref] = issued
        self._by_request.setdefault(basis.request_id, []).append(issued.payload.ref)
        return issued.snapshot()

    def issued(self, ref: str) -> Optional[ExecutionBasis]:
        """What was issued at this ref, at its current status, or None if nothing ever was."""
        entry = self._issued.get(ref)
        return entry.snapshot() if entry else None

    def verify(self, basis: ExecutionBasis) -> Tuple[bool, str]:
        """Is this object the basis the store issued, unedited? (ok, why-not).

        This is the whole answer to a fabricated or tampered basis. It compares the presented
        object's seal with the seal taken at issue, so an edit to any sealed field - scope,
        digest, spec version, requirements, the false authority flags - fails here by evidence.
        """
        entry = self._issued.get(basis.ref)
        if entry is None:
            return False, ("no Execution Basis was ever issued at %s; a basis that the store "
                           "cannot produce is fabricated" % basis.ref)
        if entry.payload.version != basis.version:
            return False, ("basis version mismatch at %s: issued v%d, presented v%d"
                           % (basis.basis_id, entry.payload.version, basis.version))
        if entry.seal != basis.payload_seal():
            return False, ("the presented basis does not match the payload sealed at issue; "
                           "%s has been altered" % basis.ref)
        if entry.status is not basis.status:
            return False, ("basis %s is %s in the store, presented as %s"
                           % (basis.ref, entry.status.value, basis.status.value))
        return True, "matches the payload sealed at issue"

    def _latest(self, request_id: str) -> Optional[_Issued]:
        refs = self._by_request.get(request_id, [])
        return self._issued[refs[-1]] if refs else None

    def latest_basis(self, request_id: str) -> Optional[ExecutionBasis]:
        """The most recently issued basis for the request, whatever its status."""
        entry = self._latest(request_id)
        return entry.snapshot() if entry else None

    def live_basis(self, request_id: str) -> Optional[ExecutionBasis]:
        for ref in reversed(self._by_request.get(request_id, [])):
            entry = self._issued[ref]
            if entry.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE):
                return entry.snapshot()
        return None

    def history(self, request_id: str) -> Tuple[ExecutionBasis, ...]:
        return tuple(self._issued[r].snapshot() for r in self._by_request.get(request_id, []))

    def lineage(self, request_id: str) -> Tuple[Tuple[str, str, Optional[str]], ...]:
        """(ref, current status, superseded-by) per issued basis, oldest first."""
        return tuple(
            (self._issued[r].payload.ref, self._issued[r].status.value,
             self._issued[r].superseded_by)
            for r in self._by_request.get(request_id, []))

    def invalidate_on_material_change(self, request_id: str, new_digest: str) -> List[str]:
        """Any live basis issued against different planning inputs becomes STALE."""
        stale: List[str] = []
        for ref in self._by_request.get(request_id, []):
            entry = self._issued[ref]
            if entry.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE) \
                    and entry.payload.planning_digest != new_digest:
                entry._transition(BasisStatus.STALE)
                entry.stale_reason = "material planning change"
                stale.append(ref)
        return stale

    # -- triggers ----------------------------------------------------------------------------

    def record_trigger(self, idempotency_key: str, basis_ref: str) -> Tuple[str, bool]:
        """Returns (run lineage id, created). A repeat under the same key creates nothing."""
        if basis_ref not in self._issued:
            raise ActivationError(
                "a trigger may not be recorded against a basis that was never issued: %s"
                % basis_ref)
        if idempotency_key in self._triggers:
            return self._triggers[idempotency_key], False
        lineage = "run_lineage." + idempotency_key.split(".", 1)[1][:12]
        self._triggers[idempotency_key] = lineage
        return lineage, True

    # -- workflow candidates -----------------------------------------------------------------

    def observe_composed_pattern(self, signature: str, work_plan_ref: str) -> Optional[dict]:
        """A repeated COMPOSE shape may emit a PROPOSED candidate. It promotes nothing.

        There is no method on this store that registers a Workflow, and none that sets a
        candidate to APPROVED. That is by construction, not by policy.
        """
        for candidate in self._candidates:
            if candidate["signature"] == signature:
                candidate["observed_plans"].append(work_plan_ref)
                return candidate
        candidate = {
            "candidate_id": "workflow_candidate.%s" % signature[:12],
            "signature": signature,
            "status": "PROPOSED",
            "observed_plans": [work_plan_ref],
            "is_approved": False,
            "is_matchable": False,
        }
        self._candidates.append(candidate)
        return candidate

    @property
    def candidates(self) -> Tuple[dict, ...]:
        return tuple(self._candidates)
