"""Communication specialist package — deterministic package validator.

Status: PROPOSED. Standard library only, deterministic, no network, no third-party imports.

    python3 validation/communication_package_validation.py [--verbose] [--json]

This harness is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY. A passing check is evidence
that a check passed. It approves nothing, satisfies no review, creates no Decision Right, and
decides neither OG-1 nor OG-2.

It checks that the PROPOSED communication-specialist package says what the approved architecture
requires it to say, that it does not quietly acquire authority, and that the defects an
independent review found are not reachable again. It cannot check that the package is *correct*;
that is what the independent review is for.

It modifies no approved validator and reads no Phase 14 artifact.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PKG = os.path.join(REPO, "proposals", "communication-difficult-conversations-specialist")

RESULTS = []

DOCS = (
    "README.md",
    "role-card.md",
    "methodology-card.md",
    "skill-pack.md",
    "workflow-difficult-interaction-response.md",
    "workflow-meeting-preparation.md",
    "workflow-boundary-setting.md",
    "workflow-refusal.md",
    "workflow-formal-escalation.md",
    "workflow-thread-diagnostics.md",
    "review-profile-communication-strategy.md",
    "review-profile-high-stakes-external-communication.md",
    "trigger-routing-spec.md",
    "communication-control-filter.md",
    "conversation-diagnostics-contract.md",
    "runtime-prompt-assembly.md",
    "decision-right-gap-analysis.md",
    "evaluation-spec.md",
    "examples.md",
    "self-check.md",
    "governance-decision-note.md",
    "role-skill-mapping-candidates.md",
)

#: The human governance decision record. It is NOT a candidate artifact: it is a record of a
#: decision a human authority made, and it is legitimately `APPROVED — HUMAN DECISION`. It is held
#: separately so that the PROPOSED and no-APPROVED checks keep their meaning for everything else,
#: and so that its own content can be checked for the one thing that matters - that it approves
#: OG-1 and OG-2 and nothing else.
DECISION_RECORD = "human-governance-decisions-og1-og2.md"

#: The ten factors are normative. They are listed once, here, and every comparison derives from
#: the filter document rather than from this tuple - the tuple exists only so that a document
#: that lost all ten at once still fails.
FILTER_FACTORS = ("GOAL", "EMOTION", "CLARITY", "BREVITY", "BOUNDARY",
                  "DEFENSIVENESS", "CONTROL", "RELEVANCE", "ESCALATION", "NEXT_STEP")


def doc(name):
    with open(os.path.join(PKG, name), encoding="utf-8") as handle:
        return handle.read()


def flat(text):
    """Markdown-insensitive form: emphasis stripped, whitespace collapsed, lowercased."""
    text = text.replace("*", "").replace("`", "").replace("—", " ")
    text = re.sub(r"(?m)^\s*>+\s?", " ", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", " ", text)
    return " ".join(text.split()).lower()


def statements(name):
    """(line, statement): a table ROW is one statement, prose is split by sentence.

    A row's columns answer each other - an evaluation row's scenario cell is answered by its
    expected cell - so splitting a row reads its scenario as a claim. Prose is the opposite: one
    corrective clause must not exempt the sentences around it."""
    fenced = False
    buffer, start = [], None
    units = []
    corrected = corrected_line_numbers(name)
    for i, line in enumerate(doc(name).splitlines(), 1):
        if i in corrected:
            continue
        if line.lstrip().startswith("```"):
            fenced = not fenced
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            continue
        if fenced:
            units.append((i, line))          # JSON contract lines are read literally
            continue
        if line.lstrip().startswith("|"):
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            units.append((i, line))
            continue
        # A bullet is its own statement. A stage's "Mandatory at:" line merged into the
        # paragraph around it acquires every qualifier its neighbours carry, and a weakening
        # planted in one bullet was exempted by a word in the next.
        if re.match(r"\s*[-*+]\s+\S", line):
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            units.append((i, line))
            continue
        if not line.strip():
            if buffer:
                units.append((start, " ".join(buffer)))
                buffer, start = [], None
            continue
        if start is None:
            start = i
        buffer.append(line)
    if buffer:
        units.append((start, " ".join(buffer)))
    for i, unit in units:
        if unit.lstrip().startswith("|") or unit.lstrip().startswith("\"") \
                or unit.lstrip().startswith("{"):
            yield i, unit
        else:
            for sentence in re.split(r"(?<=[.;])\s+", unit):
                if sentence.strip():
                    yield i, sentence


#: A sentence that DESCRIBES a defect in order to reject it. The package has to be able to say
#: what it corrected; a scan that could not tell correction from assertion would forbid that.
CORRECTIVE = re.compile(
    r"\b(earlier revision|an earlier|previously|used to|was wrong|is corrected|no longer|"
    r"deprecated|withdrawn|not used|revision 1|would have|is a failure|failure \(HF|"
    r"is removed|prior reading|misread\w*|HF-\d+|hard fail)\b|not `FACT`",
    re.IGNORECASE)


#: Section headings whose tables PAIR a wrong assertion with its correction, column by column.
#: A package has to be able to record what it got wrong; these are named explicitly rather than
#: inferred, so the exclusion cannot quietly widen.
CORRECTION_SECTIONS = (
    "what the independent review corrected",
    "the independent review findings, and how each was closed",
)


def corrected_line_numbers(name):
    skip, inside = set(), False
    for i, line in enumerate(doc(name).splitlines(), 1):
        if line.startswith("#"):
            inside = any(h in flat(line) for h in CORRECTION_SECTIONS)
        if inside:
            skip.add(i)
    return skip


def check(group, name, fn):
    try:
        ok, evidence = fn()
    except Exception as exc:                                   # noqa: BLE001
        ok, evidence = False, "%s: %s" % (type(exc).__name__, exc)
    RESULTS.append({"group": group, "name": name, "pass": bool(ok),
                    "evidence": str(evidence)[:400]})


def says(name, *phrases):
    body = flat(doc(name))
    return [p for p in phrases if flat(p) not in body]


# =========================================================== structure


def the_package_is_exactly_its_declared_artifacts():
    present = sorted(f for f in os.listdir(PKG) if not f.startswith("."))
    missing = [d for d in DOCS + (DECISION_RECORD,) if d not in present]
    unexpected = [f for f in present if f not in DOCS + (DECISION_RECORD,)]
    problems = []
    if missing:
        problems.append("missing: %s" % missing)
    if unexpected:
        problems.append("unexpected: %s" % unexpected)
    return (not problems, str(problems) if problems
            else "%d candidate documents and one human decision record, and nothing else"
                 % len(DOCS))


check("structure", "the package is exactly its declared artifact set",
      the_package_is_exactly_its_declared_artifacts)


def every_artifact_remains_proposed():
    wrong = [d for d in DOCS if "Status: `PROPOSED`" not in doc(d)[:700]]
    return (not wrong, str(wrong) if wrong else "all %d artifacts are PROPOSED" % len(DOCS))


check("structure", "every package artifact remains PROPOSED", every_artifact_remains_proposed)


def nothing_claims_approved_or_canonical():
    pattern = re.compile(r"^\s*Status:.*\b(APPROVED|CANONICAL)\b", re.MULTILINE)
    offenders = [d for d in DOCS if pattern.search(doc(d))]
    return (not offenders, str(offenders) if offenders
            else "no artifact declares itself APPROVED or CANONICAL")


check("structure", "no artifact claims APPROVED or CANONICAL status",
      nothing_claims_approved_or_canonical)


def the_decision_record_approves_only_og1_and_og2():
    """One file in the package is APPROVED, and only because a human decided two questions.

    The risk a recorded decision creates is over-reading: a reader, or a later drafting pass,
    treating "a human approved something here" as "the package is approved". The record says
    otherwise in terms, and this check holds it to that."""
    record = doc(DECISION_RECORD)
    problems = []
    if "Status: `APPROVED — HUMAN DECISION`" not in record:
        problems.append("the decision record does not declare itself a human decision")
    for token in ("DECIDE OG-1: NORMALIZE IDENTIFIERS",
                  "DECIDE OG-2: PROFESSIONAL DELIVERY ROLE"):
        if token not in record:
            problems.append("the record does not carry %r" % token)
    low = flat(record)
    for denial in ("approve the communication-specialist package",
                   "approve or activate the candidate role",
                   "approve candidate skills, skill packs, workflows or review profiles",
                   "create or approve any decision right",
                   "grant publication, sending, contractual, legal or other authority",
                   "claim runtime, production or deployment readiness"):
        if denial not in low:
            problems.append("the record does not deny %r" % denial[:44])
    if "requires an independent package re-audit" not in low:
        problems.append("the record does not require a re-audit before package approval")
    # And no candidate artifact may cite it as approving anything beyond the two items.
    overread = re.compile(
        r"(human (?:decision|authority)|og-[12]|decision record|903c58)[^.|]{0,80}?"
        r"(approves?|approved|activat\w*|registers?|authoris\w*)[^.|]{0,40}?"
        r"(the package|the role|the skills?|the capability|activation|production)",
        re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if overread.search(sentence) and not CORRECTIVE.search(sentence) \
                    and not re.search(r"\b(not|never|no|nothing|neither|does not|did not)\b",
                                      sentence, re.IGNORECASE):
                problems.append("%s:%d over-reads the human decision" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "the record decides OG-1 and OG-2, denies approving anything else")


check("structure", "the human decision record approves only OG-1 and OG-2",
      the_decision_record_approves_only_og1_and_og2)


#: The approved Phase 13 architecture baseline. Containment is measured against approved
#: architecture, not against the repository's first commit - measuring from init would report
#: every approved artifact as "changed" and the check would prove nothing.
BASELINE = "2c4b90def9a60f8b384feef10f8428c5b437597c"


def merge_base():
    """Where this branch left approved architecture.

    A raw diff against the Phase 13 baseline would report every artifact that landed on the
    Phase 14 branch AFTER this one forked as "deleted here", which is a fact about branch
    topology and not about anything this package did. The comparison point is therefore the
    merge base. That bounds the claim honestly: this check shows the branch changed no approved
    artifact, NOT that the branch carries the latest approved architecture."""
    result = subprocess.run(["git", "merge-base", "HEAD", BASELINE],
                            cwd=REPO, capture_output=True, text=True)
    return result.stdout.strip() or BASELINE


def changed_paths():
    tracked = subprocess.run(["git", "diff", "--name-only", merge_base(), "--"],
                             cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    return sorted({n for n in tracked + untracked if n.strip()})


def no_approved_artifact_is_touched():
    """The package adds files. It changes nothing that is already approved architecture."""
    allowed = ("proposals/", "prompts/", "validation/communication_package_")
    offenders = [n for n in changed_paths() if not n.startswith(allowed)]
    return (not offenders, str(offenders[:6]) if offenders
            else "only the proposal, its prompts and its own validator are added")


check("structure", "no approved Phase 1-13 artifact is changed", no_approved_artifact_is_touched)


def no_phase_14_file_is_touched():
    offenders = [n for n in changed_paths()
                 if n.startswith("implementation-spec/") or "phase_14" in n]
    return (not offenders, str(offenders[:6]) if offenders
            else "no Phase 14 specification or validator file is touched")


check("structure", "no Phase 14 file is changed", no_phase_14_file_is_touched)


# =========================================================== epistemic model


def no_deprecated_fact_vocabulary_is_active():
    """`FACT` is the upstream label; `FACT_CLAIM` is the approved epistemic type.

    The independent review found the package defining new contracts in the deprecated
    vocabulary. Every active use fails; a sentence that says the label is deprecated does not."""
    problems = []
    for name in DOCS:
        for i, sentence in statements(name):
            if not re.search(r"`FACT`", sentence):
                continue
            if CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d uses the deprecated `FACT` label actively" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "the deprecated `FACT` label is active nowhere in the package")


check("epistemic", "no deprecated FACT vocabulary is active",
      no_deprecated_fact_vocabulary_is_active)


def no_epistemic_type_mutation_is_described():
    """A source is cited, never promoted. There is no SOURCE -> claim transition."""
    mutation = re.compile(
        r"(`?SOURCE`?\s*(?:→|->|to)\s*`?(?:FACT|FACT_CLAIM|EVIDENCE|CLAIM)"
        r"|promot\w*\s+(?:the\s+)?source"
        r"|convert\w*\s+(?:a\s+|the\s+)?source"
        r"|relabel\w*\s+(?:a\s+|the\s+)?source)", re.IGNORECASE)
    problems = []
    for name in DOCS:
        for i, sentence in statements(name):
            if not mutation.search(sentence):
                continue
            if CORRECTIVE.search(sentence) or re.search(
                    r"\b(no|never|not|cannot|prohibit\w*)\b", sentence, re.IGNORECASE):
                continue
            problems.append("%s:%d describes an epistemic type mutation" % (name, i))
    for phrase, name in (("a claim is a new linked item; nothing is converted",
                          "conversation-diagnostics-contract.md"),
                         ("nothing is converted; a claim is a new linked item", "role-card.md")):
        if says(name, phrase):
            problems.append("%s does not state the no-mutation rule" % name)
    if "EVIDENCE" not in doc("conversation-diagnostics-contract.md"):
        problems.append("the diagnostic contract has no EVIDENCE layer between source and claim")
    return (not problems, str(problems)[:400] if problems
            else "source stays source; a claim is a new linked FACT_CLAIM with its evidence")


check("epistemic", "no SOURCE-to-claim epistemic mutation is described",
      no_epistemic_type_mutation_is_described)


# =========================================================== review trigger


def rc5_conditions():
    """The four RC-5 conditions, parsed from the Role Card that owns them."""
    body = doc("role-card.md")
    if "**Rule RC-5 " not in body:
        return {}
    section = body.split("**Rule RC-5 ")[1].split("**Rule RC-5a")[0]
    found = {}
    for line in section.splitlines():
        m = re.match(r"^\|\s*\**(RC-5\.\d)\**\s*\|(.+?)\|", line)
        if m:
            found[m.group(1)] = flat(m.group(2))
    return found


def the_review_trigger_is_one_rule_everywhere():
    """One trigger, owned by the Role Card, referenced - never restated - elsewhere.

    The independent review found the Review Profile mandating review whenever another Role's
    conclusion was carried or a consequential boundary stated, while the Role Card and workflows
    mandated it at high/critical stakes only. Two rules meant the fail-closed one applied only
    where a reader happened to look."""
    conditions = rc5_conditions()
    problems = []
    if len(conditions) != 4:
        problems.append("RC-5 does not state exactly four conditions (%d found)"
                        % len(conditions))
    for key, expect in (("RC-5.1", "high"), ("RC-5.2", "conclusion"),
                        ("RC-5.3", "boundary"), ("RC-5.4", "workflow")):
        if key in conditions and expect not in conditions[key]:
            problems.append("%s no longer covers %r" % (key, expect))
    if says("role-card.md", "the single review trigger, stated once and referenced everywhere"):
        problems.append("the Role Card does not declare RC-5 authoritative")
    if says("role-card.md", "stakes never lower the trigger"):
        problems.append("RC-5a is missing: stakes could lower the obligation")
    profile = doc("review-profile-communication-strategy.md")
    if "RC-5" not in profile:
        problems.append("the Review Profile does not reference RC-5")
    trigger = profile.split("## Applicability / Trigger")[1].split("## Required Evidence")[0]
    for key in ("RC-5.1", "RC-5.2", "RC-5.3", "RC-5.4"):
        if key not in trigger:
            problems.append("the Profile's trigger omits %s" % key)
    # A document may not describe a NARROWER trigger of its own.
    narrower = re.compile(r"(required|mandatory)[^.]{0,60}?"
                          r"(only (?:where|when|at)|where stakes are high or critical"
                          r"|at high (?:and|or) critical (?:stakes|bands?) only)",
                          re.IGNORECASE)
    # The subject may be the word "review" or a stage's own "Mandatory at:" line - a workflow
    # narrows the trigger by rewriting the second without mentioning the first, and a scan
    # keyed only on "review" could not see it.
    subject = re.compile(r"(review|mandatory at)", re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if not subject.search(sentence):
                continue
            if not narrower.search(sentence):
                continue
            # A neighbouring bullet mentioning RC-5 must NOT exempt this one: a narrowed
            # "Mandatory at:" line sitting beside a correct RC-5 reference is exactly the
            # shape a stage-level narrowing takes, and a blanket exemption was blind to it.
            if CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d states a narrower review trigger than RC-5" % (name, i))
    return (not problems, str(problems)[:400] if problems
            else "one trigger, four conditions, referenced by the Profile and every workflow")


check("review", "the communication-strategy review trigger is one rule everywhere",
      the_review_trigger_is_one_rule_everywhere)


# =========================================================== gate semantics


def gate_status_distinguishes_not_applicable_from_authority_absent():
    """Nothing to authorise, and nobody to authorise it, are opposite findings."""
    contract = doc("conversation-diagnostics-contract.md")
    problems = []
    for token in ("NOT_APPLICABLE", "AUTHORITY_ABSENT", "NO_EXTERNAL_ACT_CONTEMPLATED",
                  "human_gate_status"):
        if token not in contract:
            problems.append("the diagnostic contract does not define %s" % token)
    if says("conversation-diagnostics-contract.md",
            "the gate has three statuses, and two of them are not each other"):
        problems.append("DC-7 does not distinguish the three statuses")
    if says("conversation-diagnostics-contract.md", "not_applicable never travels"):
        problems.append("nothing stops NOT_APPLICABLE being inherited by a later workflow")
    diagnostics = doc("workflow-thread-diagnostics.md")
    if "NOT_APPLICABLE" not in diagnostics:
        problems.append("the read-only diagnostics workflow does not record NOT_APPLICABLE")
    if "no external act, no gate" not in flat(diagnostics):
        problems.append("the read-only workflow does not state why no gate applies")
    # A read-only artifact must never be required to report AUTHORITY_ABSENT.
    for name in ("workflow-thread-diagnostics.md", "conversation-diagnostics-contract.md"):
        for i, sentence in statements(name):
            low = flat(sentence)
            if "authority_absent" not in low:
                continue
            if CORRECTIVE.search(sentence):
                continue
            if "external act" in low and ("is contemplated" in low or "requires authority" in low):
                continue
            if "reason" in low or "three statuses" in low or "|" in sentence:
                continue
            problems.append("%s:%d may require AUTHORITY_ABSENT without an external act"
                            % (name, i))
    if says("decision-right-gap-analysis.md", "authority_absent is not the resting state"):
        problems.append("DG-5a is missing: AUTHORITY_ABSENT could be the ordinary outcome")
    return (not problems, str(problems)[:400] if problems
            else "three statuses; a read-only artifact reports NOT_APPLICABLE, never a gap")


check("gates", "a gate-free artifact reports NOT_APPLICABLE, not AUTHORITY_ABSENT",
      gate_status_distinguishes_not_applicable_from_authority_absent)


# =========================================================== filter / diagnostics schema


def filter_factor_names():
    """The ten factors, parsed from the filter document that owns them."""
    body = doc("communication-control-filter.md")
    section = body.split("## 2. The ten factors")[1].split("## 3.")[0]
    return [m.group(1) for m in
            (re.match(r"^\|\s*\d+\s*\|\s*\*\*([A-Z ]+?)\*\*\s*\|", line)
             for line in section.splitlines()) if m]


def the_filter_and_diagnostic_schemas_agree_exactly():
    """One rubric, one owner, one field set - and risks in their own namespace.

    The independent review found the diagnostic carrying a nine-field object that mixed four
    filter factors with five risk measures and called it the filter's scores. That object was a
    third rubric nobody owned."""
    owned = [f.strip().replace(" ", "_") for f in filter_factor_names()]
    problems = []
    if len(owned) != 10:
        problems.append("the filter declares %d factors, not ten" % len(owned))
    for expected in FILTER_FACTORS:
        if expected not in owned:
            problems.append("the filter no longer declares %s" % expected)
    contract = doc("conversation-diagnostics-contract.md")
    if "## 4a." not in contract or "## 4b." not in contract:
        problems.append("the diagnostic contract does not separate the two namespaces")
        return False, str(problems)
    filter_ns = contract.split("## 4a.")[1].split("## 4b.")[0]
    risks_ns = contract.split("## 4b.")[1].split("## 5.")[0]
    declared = re.findall(r'"([A-Z_]+)":', filter_ns)
    for expected in owned:
        if expected not in declared:
            problems.append("the diagnostic's filter namespace omits %s" % expected)
    for found in declared:
        if found not in owned:
            problems.append("the diagnostic's filter namespace invents %s" % found)
    # The risk namespace must not carry a filter factor name.
    # Case-insensitively: a factor smuggled into the risk namespace in its own casing is the
    # same collision, and a lowercase-only scan was blind to exactly that.
    for found in re.findall(r'"([A-Za-z_]+)":', risks_ns):
        if found.upper() in owned:
            problems.append("the risk namespace reuses the filter factor %s" % found)
    for phrase in ("the filter has one owner and one field set",
                   "the diagnostic invents no competing rubric",
                   "no score in either namespace becomes authority"):
        if says("conversation-diagnostics-contract.md", phrase):
            problems.append("missing %r" % phrase[:40])
    return (not problems, str(problems)[:400] if problems
            else "ten factors in one namespace, risks in another, compared both directions")


check("schema", "the filter and diagnostic schemas agree exactly, in both directions",
      the_filter_and_diagnostic_schemas_agree_exactly)


def no_score_becomes_authority_or_selects_a_model():
    score = re.compile(r"(score|filter|rubric|risk (?:score|dimension))", re.IGNORECASE)
    authority = re.compile(
        r"(satisf\w*\s+(?:a\s+|the\s+)?review|grants?\s+(?:a\s+)?(?:right|authority)"
        r"|approv\w*\s+the\s+(?:draft|message)|select\w*\s+(?:a\s+)?model"
        r"|choos\w*\s+(?:a\s+)?model|is (?:governance )?evidence|exercis\w*\s+(?:a\s+)?right)",
        re.IGNORECASE)
    problems = []
    for name in DOCS:
        for i, sentence in statements(name):
            if not (score.search(sentence) and authority.search(sentence)):
                continue
            # A fragment that carries the tail of a rule heading and the head of the next
            # sentence is not a claim; the two halves belong to different statements.
            if "**" in sentence and sentence.count("**") % 2 == 1:
                continue
            if re.search(r"\b(never|not|no|cannot|must|prohibit\w*|refus\w*|forbid\w*)\b",
                         sentence, re.IGNORECASE) or CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d lets a score confer authority" % (name, i))
    for phrase in ("the filter is never a gate", "the filter is not evidence",
                   "the filter is not a reviewer", "the filter is not a routing input"):
        if says("communication-control-filter.md", phrase):
            problems.append("missing %r" % phrase[:38])
    if says("trigger-routing-spec.md", "the orchestrator routes; the router selects models"):
        problems.append("the routing spec does not deny model selection")
    return (not problems, str(problems)[:400] if problems
            else "no score satisfies a review, grants a Right or selects a model")


check("authority", "no score grants authority, satisfies a review or selects a model",
      no_score_becomes_authority_or_selects_a_model)


# =========================================================== decision rights


def approved_decision_ids():
    ids = set()
    root = os.path.join(REPO, "decisions")
    for base, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(base, f), encoding="utf-8") as handle:
                    ids |= set(re.findall(r"`(decision\.[a-z_0-9]+)`", handle.read()))
    return ids


def ta7_does_not_assume_private_is_outside_the_approved_right():
    """The approved subject has four elements, and publicity is not one of them."""
    analysis = doc("decision-right-gap-analysis.md")
    problems = []
    if says("decision-right-gap-analysis.md",
            "there is no element requiring the audience to be the public"):
        problems.append("the analysis does not read the approved subject as written")
    if says("decision-right-gap-analysis.md", "a right's name is not its subject"):
        problems.append("DG-3 is missing")
    if "WITHDRAWN_FROM_CURRENT_PACKAGE" not in analysis:
        problems.append("the candidate Right is not recorded as withdrawn")
    # No location may assert the old premise.
    premise = re.compile(r"(private|not published|neither published)[^.]{0,90}?"
                         r"(outside|not (?:within|covered)|uncovered|no applicable right)",
                         re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if not premise.search(sentence):
                continue
            if CORRECTIVE.search(sentence):
                continue
            problems.append("%s:%d assumes private correspondence is outside the Right"
                            % (name, i))
    # The withdrawn candidate must never be presented as available.
    available = re.compile(r"(applies|is required|resolves to|gate is|use it|available|"
                           r"is proposed|candidate right)", re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if "external_high_stakes_communication_send" not in sentence:
                continue
            if CORRECTIVE.search(sentence) or re.search(
                    r"\b(withdrawn|no authority|not proposed|confers nothing|"
                    r"confers no|must not)\b", sentence, re.IGNORECASE):
                continue
            if available.search(sentence):
                problems.append("%s:%d presents the withdrawn Right as available" % (name, i))
    approved = approved_decision_ids()
    cited = set()
    for name in DOCS:
        cited |= set(re.findall(r"`(decision\.[a-z_0-9]+)`", doc(name)))
    unknown = sorted(c for c in cited
                     if c not in approved and c != "decision.external_high_stakes_communication_send")
    if unknown:
        problems.append("cites Decision Rights that are in no register: %s" % unknown)
    return (not problems, str(problems)[:400] if problems
            else "TA-1..TA-7 resolve against the approved subject; the candidate is withdrawn")


check("rights", "TA-7 is assessed against the approved subject, not against publicity",
      ta7_does_not_assume_private_is_outside_the_approved_right)


def no_candidate_is_treated_as_available():
    """A candidate Skill, Role or Review is not a registered one, and never activates."""
    problems = []
    if says("skill-pack.md", "a candidate skill is not a skill"):
        problems.append("SP-1 is missing: a candidate Skill could be activated")
    pack = doc("skill-pack.md")
    if "candidate" not in flat(pack.split("### Candidate Skills")[1][:400]):
        problems.append("the candidate skill list does not mark its entries as candidates")
    if says("role-card.md", "candidate only"):
        problems.append("the Role Card does not declare itself a candidate")
    for name in ("review-profile-communication-strategy.md",
                 "review-profile-high-stakes-external-communication.md"):
        if "Status: `PROPOSED`" not in doc(name)[:400]:
            problems.append("%s does not declare itself PROPOSED" % name)
    return (not problems, str(problems)[:300] if problems
            else "candidate Skills, Role and Review Profiles are all non-activatable")


check("rights", "no candidate Skill, Role or Review Profile is treated as available",
      no_candidate_is_treated_as_available)


# =========================================================== identity and assembly


def no_alias_becomes_a_canonical_identity():
    canonical = {"jefferson-fisher-communication": "role.communication_difficult_conversations_specialist",
                 "fisher mode": "calm direct mode",
                 "fisher communication filter": "communication control filter"}
    problems = []
    # An alias is introduced and qualified in the same paragraph or row - "the same applies to
    # Fisher Mode, whose canonical name is Calm Direct Mode" is one statement split across two
    # sentences - so the unit of judgement here is the paragraph, not the sentence.
    for name in DOCS:
        units = {}
        for i, sentence in statements(name):
            units.setdefault(i, []).append(sentence)
        for i, parts in units.items():
            low = flat(" ".join(parts))
            for alias, real in canonical.items():
                if alias not in low:
                    continue
                if re.search(r"(alias|compatibility|research|migration|never canonical|"
                             r"not the canonical|canonical .{0,30}name|discovery)", low) \
                        or real.split(".")[-1].replace("_", " ") in low \
                        or CORRECTIVE.search(" ".join(parts)):
                    continue
                problems.append("%s:%d uses %r without marking it an alias" % (name, i, alias))
    for phrase in ("no impersonation, no endorsement",
                   "the alias is a migration aid, not an identity"):
        if says("README.md", phrase):
            problems.append("README missing %r" % phrase[:34])
    return (not problems, str(problems)[:400] if problems
            else "three aliases, each marked as one wherever it appears")


check("identity", "no compatibility alias becomes a canonical identity",
      no_alias_becomes_a_canonical_identity)


def prompt_assembly_is_projection_only_and_narrowing_only():
    problems = []
    for phrase in ("the registry is the source of truth; the prompt is a projection of it",
                   "narrowing only, checked at assembly",
                   "assembly is per-assignment and disposable",
                   "assembly does not select a model"):
        if says("runtime-prompt-assembly.md", phrase):
            problems.append("missing %r" % phrase[:44])
    body = doc("runtime-prompt-assembly.md")
    widen = [ln for ln in body.splitlines()
             if ln.startswith("|") and "may it widen" not in flat(ln)
             and re.search(r"\|\s*\*\*Yes\*\*\s*\|?\s*$", ln)]
    if widen:
        problems.append("a prompt layer may widen a higher one: %s" % flat(widen[0])[:60])
    return (not problems, str(problems)[:300] if problems
            else "nine layers, narrowing only, disposable, model-agnostic")


check("identity", "runtime prompt assembly stays projection-only and narrowing-only",
      prompt_assembly_is_projection_only_and_narrowing_only)


# =========================================================== governance


def og1_and_og2_are_recorded_human_decisions():
    """Both were decided by a human authority. The package records them; it decided neither.

    Two failure directions, and the check covers both: drifting back to "undecided", which would
    make the package contradict a record it cites; and the package deciding a governance item for
    itself, which is what the earlier version of this check existed to prevent and still is."""
    note = doc("governance-decision-note.md")
    problems = []
    for token in ("HUMAN DECISION RECORDED: NORMALIZE IDENTIFIERS",
                  "HUMAN DECISION RECORDED: PROFESSIONAL DELIVERY ROLE"):
        if token not in note:
            problems.append("the note does not record %r" % token)
    if "HUMAN GOVERNANCE DECISION REQUIRED" in note:
        problems.append("the note still shows a decided item as requiring a decision")
    # The record and its commit must be cited wherever the status is claimed.
    for name in ("governance-decision-note.md", "self-check.md", "README.md"):
        body = doc(name)
        if "903c58df" not in body:
            problems.append("%s claims a decision without citing the record's commit" % name)
        if "human-governance-decisions-og1-og2.md" not in body:
            problems.append("%s claims a decision without citing the record" % name)
    # The package still decides nothing of its own.
    decided = re.compile(r"(this (?:package|note) decides|we (?:decide|choose|adopt)|"
                         r"hereby decid|option [ab] is (?:adopted|chosen|selected) here|"
                         r"is decided here)", re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if decided.search(sentence) and not CORRECTIVE.search(sentence):
                problems.append("%s:%d decides a governance item for itself" % (name, i))
    if says("governance-decision-note.md", "this note **decides nothing**"):
        problems.append("the note does not disclaim deciding")
    if "no role is created, registered or approved here" not in flat(note):
        problems.append("the note does not deny creating the Role")
    # A decision that settled the modelling question did not register or approve anything.
    for phrase in ("does not register the Role", "remains 59"):
        if says("role-card.md", phrase):
            problems.append("the Role Card does not bound the decision: missing %r" % phrase)
    # The history must survive: the earlier baseline deferred both, correctly.
    for phrase in ("The earlier baseline was right to defer this",
                   "The earlier baseline was right to defer this too"):
        if says("governance-decision-note.md", phrase):
            problems.append("the note rewrites history: missing %r" % phrase[:40])
    return (not problems, str(problems)[:400] if problems
            else "OG-1 and OG-2 recorded as human decisions, cited, bounded, and decided elsewhere")


check("governance", "OG-1 and OG-2 are recorded human decisions, not package decisions",
      og1_and_og2_are_recorded_human_decisions)


def identifiers_are_normalized_with_one_canonical_form_each():
    """OG-1 applied: the approved registry shapes, one identity per object, no dotted survivors."""
    problems = []
    dotted = re.compile(r"`?(?:pack|method|workflow|skill_pack|review|role|skill)"
                        r"\.[a-z0-9_]+\.[a-z0-9_]+", re.IGNORECASE)
    traceability = doc("README.md")
    marker = "### Historical identifiers — traceability metadata only"
    historical = traceability.split(marker)[1].split("\n\n**One correction")[0] \
        if marker in traceability else ""
    if not historical:
        problems.append("README has no historical-identifier traceability section")
    for name in DOCS:
        body = doc(name)
        for i, line in enumerate(body.splitlines(), 1):
            if name == "README.md" and line in historical:
                continue
            m = dotted.search(line)
            if m:
                problems.append("%s:%d keeps a dotted identifier %r" % (name, i, m.group(0)))
    # Exactly one canonical ID per object: the dual-identity lines must be gone everywhere.
    for name in DOCS:
        if "Registry-normalised alternative" in doc(name):
            problems.append("%s still carries a second canonical identity" % name)
    # The normalized IDs must actually be present where they belong.
    expected = {
        "skill-pack.md": "skill_pack.communication_difficult_conversations@0.1",
        "methodology-card.md": "method.communication_calm_direct_control@0.1",
        "workflow-difficult-interaction-response.md":
            "workflow.communication_difficult_interaction_response@0.1",
        "workflow-meeting-preparation.md": "workflow.communication_meeting_preparation@0.1",
        "workflow-boundary-setting.md": "workflow.communication_boundary_setting@0.1",
        "workflow-refusal.md": "workflow.communication_refusal@0.1",
        "workflow-formal-escalation.md": "workflow.communication_formal_escalation@0.1",
        "workflow-thread-diagnostics.md": "workflow.communication_thread_diagnostics@0.1",
        "review-profile-communication-strategy.md": "review.communication_strategy@0.1",
    }
    for name, identifier in expected.items():
        if identifier not in doc(name):
            problems.append("%s does not carry its canonical ID %s" % (name, identifier))
    # And the traceability table may not be read as a live alias.
    for phrase in ("are **not** identities", "may not be used in any reference"):
        if says("README.md", phrase):
            problems.append("the historical IDs are not disclaimed: missing %r" % phrase[:34])
    return (not problems, str(problems)[:400] if problems
            else "one canonical identifier per object, in the approved shape, no dotted survivors")


check("identity", "identifiers are normalized to one canonical form each",
      identifiers_are_normalized_with_one_canonical_form_each)


def the_role_is_a_candidate_professional_delivery_role():
    """OG-2 applied: a Role, candidate, bounded - and never quietly demoted to a pack again."""
    card = doc("role-card.md")
    problems = []
    # The Identity line is the one a reader and a registry pass both take the Role Type from.
    # Testing the whole document let the type survive in the decision blockquote while the
    # Identity line said "Specialisation" - which is exactly the weakening a probe planted.
    type_rows = [ln for ln in card.splitlines() if ln.startswith("- Role Type:")]
    if not type_rows:
        problems.append("the Role Card has no Role Type line")
    for row in type_rows:
        if "professional delivery role" not in flat(row):
            problems.append("the Role Type line does not state the decided type: %r" % row[:70])
        if re.search(r"specialisation|specialization|skill pack", flat(row)):
            problems.append("the Role Type line names a specialisation: %r" % row[:70])
    position = [ln for ln in card.splitlines() if ln.startswith("- Position in the Role universe:")]
    if not position:
        problems.append("the Role Card does not state its proposed position in the universe")
    if says("role-card.md", "HUMAN DECISION RECORDED: PROFESSIONAL DELIVERY ROLE"):
        problems.append("the Role Card does not record the OG-2 decision")
    if says("role-card.md", "60th"):
        problems.append("the Role Card does not state its proposed position")
    # The mapping proposal must exist, and must disclaim being a Phase 4 record.
    mapping = doc("role-skill-mapping-candidates.md")
    for phrase in ("This is a proposal surface, not a mapping record",
                   "authorises no activation", "a candidate Skill is unavailable",
                   "this document authorises nothing",
                   "no approved registry is edited by this package"):
        if says("role-skill-mapping-candidates.md", phrase):
            problems.append("the candidate mapping does not say %r" % phrase[:40])
    # The candidate REQUIRED_CORE block must say, in its own words, that none of them exists.
    if "### REQUIRED_CORE — candidate Skills" in mapping:
        block = flat(mapping.split("### REQUIRED_CORE — candidate Skills")[1]
                     .split("### REQUIRED_FOR_CONTEXT")[0])
        if "none of these exists" not in block:
            problems.append("the candidate Skill block does not say none of them exists")
        if "skill registry change control" not in block:
            problems.append("the candidate Skill block does not require Skill Registry change "
                            "control")
        if re.search(r"available for activation|activatable|ready to activate", block):
            problems.append("the candidate Skill block presents them as activatable")
    else:
        problems.append("the candidate mapping has no candidate REQUIRED_CORE block")
    for candidate in ("skill.interaction_response_triage", "skill.boundary_formulation",
                      "skill.refusal_design", "skill.de_escalation_framing",
                      "skill.communication_reactivity_detection", "skill.conversational_control",
                      "skill.non_response_strategy", "skill.communication_control_filtering"):
        if candidate not in mapping:
            problems.append("the candidate mapping omits %s" % candidate)
        row = [ln for ln in mapping.splitlines() if candidate in ln]
        if row and "candidate" not in flat(row[0]):
            problems.append("%s is listed without being marked a candidate" % candidate)
    # No statement may reduce the decided Role back to a specialisation or pack-only capability.
    demoted = re.compile(
        r"(the )?(capability|role|communication specialist)[^.|]{0,60}?"
        r"(is|remains|should be|stays)[^.|]{0,30}?"
        r"(only a|just a|merely a)?\s?(specialisation|specialization|skill pack|pack)\b",
        re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if demoted.search(sentence) and not CORRECTIVE.search(sentence) \
                    and not re.search(r"\b(not|never|rather than|instead of)\b", sentence,
                                      re.IGNORECASE):
                problems.append("%s:%d demotes the decided Role to a specialisation"
                                % (name, i))
    # The approved universe is untouched.
    if says("role-card.md", "roles/master-role-universe.md` is untouched"):
        problems.append("the Role Card does not say the approved universe is untouched")
    return (not problems, str(problems)[:400] if problems
            else "a candidate Professional Delivery Role, 60th proposed, registering nothing")


check("governance", "the capability is a candidate Professional Delivery Role",
      the_role_is_a_candidate_professional_delivery_role)


def the_role_never_overrides_a_substantive_conclusion():
    problems = []
    if says("role-card.md", "phrasing may change, conclusions may not"):
        problems.append("RC-1 is missing")
    override = re.compile(r"(may|can|is permitted to)[^.]{0,60}?"
                          r"(overrid\w*|adjust|amend|improve|correct)[^.]{0,40}?"
                          r"(conclusion|position of another role)", re.IGNORECASE)
    for name in DOCS:
        for i, sentence in statements(name):
            if not override.search(sentence):
                continue
            if CORRECTIVE.search(sentence) or re.search(
                    r"\b(never|not|no|cannot|must not|prohibit\w*)\b",
                    sentence, re.IGNORECASE):
                continue
            problems.append("%s:%d lets the Role change another Role's conclusion" % (name, i))
    return (not problems, str(problems)[:300] if problems
            else "expression may change; the supplied conclusion may not")


check("governance", "the Role never overrides another domain's substantive conclusion",
      the_role_never_overrides_a_substantive_conclusion)


def the_harness_contains_no_vacuous_check():
    """A check that cannot fail is a check that proves nothing."""
    source = open(os.path.abspath(__file__), encoding="utf-8").read()
    bodies = re.findall(r"\ndef ([a-z0-9_]+)\(\):\n(.*?)(?=\ndef |\ncheck\()", source, re.S)
    vacuous = [n for n, b in bodies
               if "return True" in b and "problems" not in b and "missing" not in b]
    return (not vacuous, str(vacuous) if vacuous
            else "%d checks, none unconditionally passing" % len(RESULTS))


check("governance", "the harness contains no vacuous or unconditional-pass check",
      the_harness_contains_no_vacuous_check)


def the_validator_disclaims_governance_authority():
    source = open(os.path.abspath(__file__), encoding="utf-8").read()
    missing = [p for p in ("NEVER GOVERNANCE AUTHORITY", "approves nothing",
                           "decides neither OG-1 nor OG-2")
               if p not in source]
    return (not missing, str(missing) if missing
            else "the harness disclaims authority in its own docstring")


check("governance", "the validator disclaims governance authority",
      the_validator_disclaims_governance_authority)


# =========================================================== main


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    passed = sum(1 for r in RESULTS if r["pass"])
    if as_json:
        print(json.dumps({"total": len(RESULTS), "passed": passed, "results": RESULTS},
                         indent=2))
    else:
        order = []
        for r in RESULTS:
            if r["group"] not in order:
                order.append(r["group"])
        for group in order:
            print("\n[%s]" % group)
            for r in [x for x in RESULTS if x["group"] == group]:
                print("  %s  %s" % ("PASS" if r["pass"] else "FAIL", r["name"]))
                if (verbose or not r["pass"]) and r["evidence"]:
                    print("        %s" % r["evidence"])
        print("\n=== %d/%d PASS ===" % (passed, len(RESULTS)))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
