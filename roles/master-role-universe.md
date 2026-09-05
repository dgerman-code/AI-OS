# Master Role Universe v1.1

Status: APPROVED — Phase 2 complete; nomenclature update approved 2026-09-05

This document contains the approved professional delivery role universe for AI-OS Phase 2. It intentionally excludes System Control Profiles, Review Profiles and Human Decision Rights, which are separate architectural entities.

A role is a reusable professional methodology profile, not a permanently running agent and not a model binding. Workflows later activate only the roles required for a task.

Seniority (Junior / Senior / Lead / Principal), criticality and assignment responsibility are attributes of an assignment, not separate roles.

## 1. Portfolio / Programme / Project Governance
1. Portfolio / Programme Manager
2. Project / Delivery Lead
3. Knowledge & Evidence Steward

## 2. Strategy / Research / General Business
4. Strategy & Business Analyst
5. Research / Market Intelligence Analyst
6. Sales / Business Development Specialist
7. Marketing / Growth Specialist
8. Operations / Service Delivery Specialist
9. People / Organisation Specialist
10. Customer / CRM Specialist
11. Supply Chain & Procurement Operations Specialist

## 3. EU / Institutional / Programme
12. EU Policy & Institutional Affairs Specialist
13. EU Enlargement / Governance Specialist
14. Institutional Affairs & Stakeholder Specialist
15. Programme / Partnership Manager
16. EU Grants & Programmes Specialist
17. EU Programme Implementation & Grant Management Specialist
18. Consortium / Partner Coordination Specialist
19. Grant Financial Compliance / Budget Specialist
20. Deliverables / Reporting Specialist
21. Learning / VET Design Specialist
22. Social Dialogue Specialist
23. Monitoring, Evaluation & Learning Specialist

Note: Labour-market analysis, skills forecasting and skills intelligence are treated as a specialisation / skill pack under Research / Market Intelligence rather than folded into Learning / VET Design.

## 4. Project Development / Technical / Commercial
24. Project Development Lead
25. Technical / Feasibility Lead
26. Sector Technical Expert
27. Commercial & Demand Specialist
28. CAPEX / Cost Engineering Specialist
29. Asset O&M / Technical Operations Specialist

Note: Corporate operating-model design belongs to Operations / Service Delivery. Asset O&M strategy for infrastructure and industrial projects belongs to the technical project-preparation domain.

## 5. Economics / Finance / Transaction
30. Financial Modelling Specialist
31. Economic / CBA Specialist
32. FP&A / Management Finance Specialist
33. Funding & Bankability Architect
34. Project Finance / Transaction Specialist
35. IFI / DFI Project Preparation Specialist
36. PPP / Concession Specialist
37. Tax Specialist
38. Accounting / Financial Due Diligence Specialist
39. Insurance / Risk Transfer Specialist

Funding & Bankability and Project Finance / Transaction remain separate: the former designs financing strategy and bankability pathways; the latter executes financing structures, lender processes and transaction work toward close.

## 6. Legal / Compliance / ESG / Risk
40. Legal & Regulatory Lead
41. Procurement / State Aid Specialist
42. ESG / E&S Specialist
43. Enterprise / Project Risk Specialist
44. Integrity / Due Diligence Specialist
45. Data Protection / GDPR Specialist

## 7. Digital Product / Software / Data
46. Product Manager / Business Analyst
47. UX / UI & Information Architecture Specialist
48. Institutional Communications / Editorial Specialist
49. Solution Architect
50. Full-Stack Software Engineer
51. Integration / API Engineer
52. Platform / DevOps Engineer
53. Data & Database Architect
54. Database / Data Engineer
55. Data / Business Analytics Specialist
56. AI / Knowledge Systems Engineer
57. Security Engineer
58. Software QA / Test Automation Specialist

## 8. Knowledge / Documentation / Transaction Disclosure
59. Data Room & Disclosure Manager

Knowledge & Evidence Steward and Data Room & Disclosure Manager remain separate because they govern different things: epistemic status / canonicality versus controlled confidential disclosure and access.

## Reusable specialisations currently NOT first-class roles

These are candidates for the Skill / Specialisation Registry rather than separate roles:

- Bid / Proposal Management
- Labour Market & Skills Intelligence
- Change Management / Adoption
- Technical Writing / Documentation
- Version Control / Document Configuration
- EU programme-specific packs (e.g. Erasmus+, CoVE, LIFE, Horizon Europe)
- IFI-specific packs (e.g. EIB, EBRD, World Bank, IFC, BGK, InvestEU, Ukraine Facility)
- Technology-specific packs (e.g. Supabase, PostgreSQL, Vercel)
- Sector packs (e.g. solar, BESS, water, waste, transport, industrial, health, real estate)
- Metrics and modelling packs (e.g. DSCR, LLCR, PLCR, tariff modelling, affordability)

## Explicit exclusions from the Role Registry

The following are intentionally modelled elsewhere:

- Chief Orchestrator -> System Control Profile
- Context Manager -> System Control Profile
- Workflow Controller -> System Control Profile
- Model Router -> System Control Profile
- Financial Model Reviewer, Technical Reviewer, Legal Reviewer, ESG Reviewer, Code Reviewer, etc. -> Review Profiles
- Final Approver / Investment Approver / Legal Approver, etc. -> Decision Rights Register
- Junior / Senior / Lead / Principal -> assignment attributes

## Design rule

A separate first-class role is justified only when at least one is true:

- it requires a distinct professional methodology;
- it has a materially different authority boundary;
- it recurrently produces a distinct professional artifact or decision-grade output;
- it needs independent review separation that cannot be represented cleanly by a Review Profile.

## Approved change log

### 2026-09-05
`Project / Workflow Lead` renamed to `Project / Delivery Lead` to avoid namespace and responsibility ambiguity with the System Control Profile `Workflow Controller`. The professional role integrates delivery; System Control orchestrates routing, context allocation and runtime execution.

The professional role count remains 59.