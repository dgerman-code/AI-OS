"""Phase 16 — in-memory reference store for basis issuance, lineage and trigger idempotency.

Status: PROPOSED. In-memory only. No database, no migration, no persistence configuration, no
Supabase, no deployment. It exists to make issuance, integrity, lineage and replay invariants
testable. An Execution Basis is issuable only if the actual Phase 16 preflight produced that exact
immutable object and its one-time provenance has not been consumed.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from domain import ActivationError, BasisStatus, ExecutionBasis, GovernanceError


class _Issued:
    __slots__ = ("payload", "seal", "status", "superseded_by", "stale_reason", "transitions")

    def __init__(self, payload: ExecutionBasis):
        self.payload = payload
        self.seal = payload.payload_seal()
        self.status = payload.status
        self.superseded_by: Optional[str] = None
        self.stale_reason: Optional[str] = None
        self.transitions: List[str] = [payload.status.value]

    def snapshot(self) -> ExecutionBasis:
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

    def issue(self, basis: ExecutionBasis) -> ExecutionBasis:
        """Issue only an exact, one-time successful-preflight output.

        Sealing arbitrary caller input is not validation. The private provenance consumed below
        proves only that the actual Phase 16 preflight returned this exact basis object after all
        blocking checks passed. It is not approval, authority or a Decision Right.
        """
        from preflight import _consume_issuance_provenance

        if basis.status is not BasisStatus.EXECUTABLE:
            raise ActivationError("only an EXECUTABLE successful-preflight basis is issuable")
        if basis.is_approval or basis.is_authority:
            raise GovernanceError(
                "an Execution Basis is neither an approval nor an authority; a candidate "
                "claiming to be one is refused rather than stored")

        request_id, digest, seal = _consume_issuance_provenance(basis)
        if request_id != basis.request_id or digest != basis.planning_digest \
                or seal != basis.payload_seal():
            raise ActivationError("preflight provenance and basis payload diverged before issuance")

        previous = self._latest(basis.request_id)
        version = 1
        supersedes = None
        if previous is not None:
            if previous.payload.planning_digest == basis.planning_digest \
                    and previous.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE):
                return previous.snapshot()
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
        entry = self._issued.get(ref)
        return entry.snapshot() if entry else None

    def verify(self, basis: ExecutionBasis) -> Tuple[bool, str]:
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
        return tuple(
            (self._issued[r].payload.ref, self._issued[r].status.value,
             self._issued[r].superseded_by)
            for r in self._by_request.get(request_id, []))

    def invalidate_on_material_change(self, request_id: str, new_digest: str) -> List[str]:
        stale: List[str] = []
        for ref in self._by_request.get(request_id, []):
            entry = self._issued[ref]
            if entry.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE) \
                    and entry.payload.planning_digest != new_digest:
                entry._transition(BasisStatus.STALE)
                entry.stale_reason = "material planning change"
                stale.append(ref)
        return stale

    def record_trigger(self, idempotency_key: str, basis_ref: str) -> Tuple[str, bool]:
        if basis_ref not in self._issued:
            raise ActivationError(
                "a trigger may not be recorded against a basis that was never issued: %s"
                % basis_ref)
        if idempotency_key in self._triggers:
            return self._triggers[idempotency_key], False
        lineage = "run_lineage." + idempotency_key.split(".", 1)[1][:12]
        self._triggers[idempotency_key] = lineage
        return lineage, True

    def observe_composed_pattern(self, signature: str, work_plan_ref: str) -> Optional[dict]:
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
