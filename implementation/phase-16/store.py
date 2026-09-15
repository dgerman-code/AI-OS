"""Phase 16 — in-memory reference store for basis lineage and trigger idempotency.

Status: PROPOSED. In-memory only. No database, no migration, no persistence configuration,
no Supabase, no deployment. It exists to make the version, lineage and duplicate-trigger
invariants testable, not to be a storage layer.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from domain import ActivationError, BasisStatus, ExecutionBasis


class ActivationStore:
    def __init__(self) -> None:
        self._bases: Dict[str, ExecutionBasis] = {}
        self._by_request: Dict[str, List[str]] = {}
        self._triggers: Dict[str, str] = {}
        self._candidates: List[dict] = []

    # -- execution bases ---------------------------------------------------------------------

    def issue(self, basis: ExecutionBasis) -> ExecutionBasis:
        """Issue a basis, superseding any live basis for the same request.

        Superseding is not deletion: the prior basis stays readable, in SUPERSEDED, with the
        reference of the one that replaced it. Governed history is append-only.
        """
        # Versioning follows the LATEST basis for the request, whatever its status. Reading only
        # the live one lost the lineage the moment a basis went STALE: the replacement started
        # again at v1 with no supersedes link, which is exactly the history a governed record
        # may not lose.
        previous = self.latest_basis(basis.request_id)
        if previous is not None:
            if previous.planning_digest == basis.planning_digest \
                    and previous.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE):
                return previous                   # idempotent reuse: same request, same version
            basis.version = previous.version + 1
            basis.supersedes = previous.ref
            if previous.status is not BasisStatus.SUPERSEDED:
                previous.mark_superseded(basis.ref)
        self._bases[basis.ref] = basis
        self._by_request.setdefault(basis.request_id, []).append(basis.ref)
        return basis

    def latest_basis(self, request_id: str) -> Optional[ExecutionBasis]:
        """The most recently issued basis for the request, whatever its status."""
        refs = self._by_request.get(request_id, [])
        return self._bases[refs[-1]] if refs else None

    def live_basis(self, request_id: str) -> Optional[ExecutionBasis]:
        for ref in reversed(self._by_request.get(request_id, [])):
            basis = self._bases[ref]
            if basis.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE):
                return basis
        return None

    def history(self, request_id: str) -> Tuple[ExecutionBasis, ...]:
        return tuple(self._bases[r] for r in self._by_request.get(request_id, []))

    def invalidate_on_material_change(self, request_id: str, new_digest: str) -> List[str]:
        """Any live basis issued against different planning inputs becomes STALE."""
        stale: List[str] = []
        for ref in self._by_request.get(request_id, []):
            basis = self._bases[ref]
            if basis.status in (BasisStatus.VALIDATED, BasisStatus.EXECUTABLE) \
                    and basis.planning_digest != new_digest:
                basis.mark_stale()
                stale.append(basis.ref)
        return stale

    # -- triggers ----------------------------------------------------------------------------

    def record_trigger(self, idempotency_key: str, basis_ref: str) -> Tuple[str, bool]:
        """Returns (run lineage id, created). A repeat under the same key creates nothing."""
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
