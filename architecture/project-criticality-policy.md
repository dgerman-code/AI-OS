# Project Scale & Criticality Policy

Status: PROPOSED — Phase 3 architecture policy
Version: 0.1

## Purpose
AI-OS must not treat project value as the only proxy for complexity, risk or review intensity. Monetary size is a useful trigger, but regulated, multi-party, public-sector, IFI, PPP, ESG-sensitive or technically complex projects can require decision-grade preparation even below a nominal threshold.

## Default scale trigger

**Projects with total investment / enterprise / transaction value of €50m or more automatically enter Enhanced Decision-Grade Project Mode.**

This replaces earlier architecture stress-tests that used €200m+ / €250m+ only as examples of major-project preparation.

## Below €50m

A project below €50m may also enter Enhanced Decision-Grade Project Mode when one or more material complexity / risk triggers are present.

Typical triggers include:
- IFI / DFI or multi-lender financing;
- PPP, concession, project-finance or blended-finance structure;
- public-sector / municipal / sovereign counterparty;
- regulated infrastructure or licensed activity;
- significant procurement, State Aid or public-funding exposure;
- cross-border or multi-jurisdiction legal structure;
- material ESG / E&S, land, resettlement, biodiversity or stakeholder risk;
- novel / first-of-a-kind technology or material technical uncertainty;
- complex CAPEX / OPEX or long construction schedule;
- material guarantees, security package, covenant or offtake dependencies;
- external submission to lender, investor, regulator, granting authority or board;
- high reputational, integrity, sanctions, AML/KYC or political-exposure risk;
- data, cybersecurity or safety criticality;
- human owner or workflow explicitly classifies the project as decision-grade.

## Suggested operating bands

These bands are guidance, not hard limits:

- **Routine / Standard** — typically below €10m and without material complexity triggers.
- **Enhanced Review Candidate** — typically €10m–€50m, or any smaller project with meaningful complexity / external-decision exposure.
- **Enhanced Decision-Grade** — automatically at €50m+; also below €50m when risk / complexity triggers justify it.
- **Major / Systemic** — very large, strategic or systemically important projects; requires the Enhanced mode plus workflow-specific specialist and review escalation.

## Architecture rule

Scale must affect:
- workflow depth;
- required specialist roles;
- minimum input knowledge state;
- independent review intensity;
- decision-right gates;
- evidence and data-room requirements;
- model/runtime assurance requirements;
- human professional validation.

Scale must **not** create separate role identities. The same Role Registry is reused; assignment attributes, skill packs, review profiles and workflows increase or decrease in depth.

## Examples

A €7m municipal water project with EIB-style financing, public procurement and environmental permitting may require Enhanced Decision-Grade Project Mode.

A €35m BESS project with project finance, grid connection risk, lender due diligence and external investor submission may require Enhanced Decision-Grade Project Mode.

A €60m straightforward corporate expansion automatically enters Enhanced Decision-Grade Project Mode because it crosses the monetary trigger, even if its final workflow is later simplified after risk assessment.

## Change control

The €50m automatic trigger is a governance default, not a claim that projects below it are low-risk. Future changes to the threshold require architecture review and human approval.