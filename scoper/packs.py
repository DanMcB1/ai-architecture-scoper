"""Industry content packs for the 4-week SOW.

Each pack is plain structured text with format placeholders. The engine
fills those placeholders from the detected profile. Keeping this data
separate from detection logic makes it easy to explain and to extend.
"""

from __future__ import annotations

from typing import Any


def _common_out_of_scope() -> list[str]:
    return [
        "A full production rollout across every site or department.",
        "Replacing or re-platforming core systems of record.",
        "Training a foundation model from scratch, or fine-tuning on the customer's full historical data warehouse.",
        "24/7 production support, an SLA, or a multi-year transformation program.",
        "A formal legal review, penetration test, or certified compliance audit (the threat model here is a starting discussion, not an assessment).",
        "Any write-back that changes production records in week 1–3; write-back, if considered at all, is a week-4 recommendation only.",
    ]


def _common_assumptions() -> list[str]:
    return [
        "A named business owner and a technical counterpart will be available for workshops in each of the four weeks.",
        "The engagement can start with read-only access or a safely extracted, minimized dataset from {systems} — not live write access.",
        "The first pilot will be limited to a small number of users and sites rather than all of {sites} at once.",
        "Success metrics listed in this SOW are proposed starting points; baselines will be confirmed with the customer in week 1.",
        "This plan assumes English-language workflows and a US regulatory context unless discovery says otherwise.",
    ]


def _common_risks() -> list[dict[str, str]]:
    return [
        {
            "risk": "System access or data extracts arrive late, shrinking the prototype window.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "Request extract samples in week 1 day 1; have a synthetic/sample-data fallback so week 3 can still demo a thin slice.",
        },
        {
            "risk": "Scope expands mid-engagement ('can it also do X?').",
            "likelihood": "High",
            "impact": "Medium",
            "mitigation": "Keep a visible parking lot. Anything new is logged and triaged in the week-4 recommendations, not added to the thin slice.",
        },
        {
            "risk": "End users do not trust or adopt the assistant.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "Sit with real users in week 1 and week 3. Design the prototype around one painful workflow, not a generic chatbot.",
        },
        {
            "risk": "Compliance or legal review takes longer than the four-week window.",
            "likelihood": "Medium",
            "impact": "Medium",
            "mitigation": "Engage compliance in week 2 with a written data-handling note. Use de-identified or synthetic data for the demo if production data cannot be cleared in time.",
        },
    ]


AUTOMOTIVE: dict[str, Any] = {
    "problem_summary": (
        "{customer} is an automotive retail group ({size_hint}) asking for AI help "
        "in {departments}. The stated need is to improve {use_cases}. Today those "
        "workflows sit on {systems}, and they touch {data_types}. That puts this "
        "work in a {sensitivity} data class: deal jackets and consumer credit "
        "information cannot be treated like a casual chatbot project.\n\n"
        "The business problem underneath the 'we want AI' ask is consistency and "
        "time. F&I product presentation and service write-ups vary by store and by "
        "manager. A four-week scoping engagement will map the current path from "
        "desk to DMS, pick one thin slice that can show value without writing back "
        "into production, and leave the group with a plan they can take to IT, "
        "compliance, and store leadership. This is a scoping and proof-of-value "
        "engagement, not a 40-rooftop rollout."
    ),
    "assumptions": _common_assumptions()
    + [
        "F&I menu / product data and a representative set of service write-up examples can be provided (live, extracted, or synthetic).",
        "Store-level process variation is expected; the prototype will target a shared pattern, not every rooftop's custom workflow.",
    ],
    "in_scope": [
        "Discovery with {departments} stakeholders and a current-state map of how work flows through {systems}.",
        "A proposed target architecture for {use_cases}, including integration style (read-only first) and data-minimization choices.",
        "A simple STRIDE-style threat model focused on deal-jacket, consumer-credit, and customer PII exposure.",
        "A thin-slice prototype or clickable workflow on sample or minimized data that illustrates {use_cases}.",
        "A pilot recommendation for a small subset of rooftops, with staffing, KPIs, and a go/no-go checklist.",
    ],
    "out_of_scope": _common_out_of_scope()
    + [
        "Changing how lenders, product providers, or the DMS itself calculates terms or rates.",
        "A group-wide F&I playbook rewrite or a full service-lane staffing redesign.",
    ],
    "weeks": [
        {
            "week": 1,
            "title": "Discovery and current-state mapping",
            "goals": [
                "Turn the vague 'we want AI' ask into one or two measurable workflows in {departments}.",
                "Inventory {systems} and the data that would actually have to move.",
            ],
            "activities": [
                "Kickoff with the group operator / GM sponsor, F&I director, and service director.",
                "Sit with two or three F&I managers and service advisors (not just leadership) and watch a live deal or RO write-up.",
                "Document systems, reports, and shadow tools (spreadsheets, shared drives, lender portals).",
                "Confirm what 'good' looks like: PVR / product penetration, time in the F&I office, write-up completeness, no-show rate.",
                "Agree the thin-slice candidate and the data we are allowed to touch.",
            ],
            "deliverables": [
                "Current-state workflow map for {departments}.",
                "System and data inventory (what exists, who owns it, what is sensitive).",
                "Confirmed week-3 prototype scope and a short list of explicit non-goals.",
            ],
        },
        {
            "week": 2,
            "title": "Architecture, data handling, and threat model",
            "goals": [
                "Propose a target architecture that can sit beside {systems} without replacing them.",
                "Write down how credit data, deal jackets, and customer PII will be handled — and what will be kept out of the prototype.",
            ],
            "activities": [
                "Draft the architecture: users, existing systems, a read-only connector, access control, audit log, assistant.",
                "Define data minimization (no full SSN or raw credit reports in the prototype; tokenize or redact where possible).",
                "Walk a STRIDE-style threat model with IT / the DMS owner and, if available, a compliance contact.",
                "Choose integration mechanics: file extract vs. API vs. read replica; prefer the path that can be stood up in days, not months.",
            ],
            "deliverables": [
                "Target architecture diagram and a one-page narrative.",
                "Data-handling note (sources, retention, access, redaction).",
                "STRIDE threat model table with agreed mitigations for the four-week slice.",
            ],
        },
        {
            "week": 3,
            "title": "Thin-slice prototype",
            "goals": [
                "Show one working slice of {use_cases} that a real F&I manager or service advisor can react to.",
                "Prove the architecture path (ingest → govern → assist) on sample or minimized data.",
            ],
            "activities": [
                "Build a narrowly scoped assistant: for example, a menu-building / product-talk track helper for F&I, or a write-up completeness helper for service — not both unless week 1 said the data is already clean.",
                "Load only the agreed sample or redacted extract.",
                "Review with 3–5 end users. Capture what they would trust, what they would ignore, and what would slow them down.",
                "Log defects and scope questions in a parking lot; do not widen the slice.",
            ],
            "deliverables": [
                "Working prototype (demo-quality) and a short demo script for store leaders.",
                "User feedback notes and a list of must-fix items before any pilot.",
                "Updated architecture if the prototype taught us something week 2 missed.",
            ],
        },
        {
            "week": 4,
            "title": "Pilot plan, metrics, and handoff",
            "goals": [
                "Leave the group with a plan they can say yes or no to — not a slide that says 'phase 2 TBD'.",
                "Recommend a pilot on a small number of rooftops, not {sites} all at once.",
            ],
            "activities": [
                "Draft the pilot design: sites, users, duration (typically 4–6 weeks after this engagement), support model, and rollback.",
                "Lock KPIs and how baselines will be pulled from {systems}.",
                "Write residual risks, compliance follow-ups, and a go/no-go checklist.",
                "Handoff readout with sponsor, IT, and department leaders.",
            ],
            "deliverables": [
                "Pilot SOW addendum: staffing, timeline, KPIs, training, and support.",
                "Go/no-go checklist and residual risk register.",
                "Final architecture, threat model, and demo recording or live readout.",
            ],
        },
    ],
    "architecture_narrative": (
        "The proposed slice does not replace {systems}. It sits beside them. "
        "A read-only connector pulls a minimized extract — never a live write "
        "into the DMS during this engagement. Access control and an audit log "
        "sit in front of the assistant so we can see who asked what, and so "
        "credit and deal-jacket fields can be redacted or excluded. "
        "{departments} users work in a narrow assistant scoped to {use_cases}. "
        "Data class is {sensitivity}; relevant controls include {compliance}. "
        "If a later pilot needs write-back (for example, drafting a note on a "
        "repair order), that is a separate, explicitly approved path — not part "
        "of weeks 1–3."
    ),
    "threats": [
        {
            "stride": "Spoofing",
            "threat": "A staff member or vendor uses someone else's DMS or CRM login to query deals or customer credit data through the assistant.",
            "mitigation": "SSO or named accounts, no shared store logins, session timeout, and the assistant inherits the user's existing role — it does not become a back door.",
            "priority": "High",
        },
        {
            "stride": "Tampering",
            "threat": "Prompt input or a compromised connector is used to alter deal terms, product menus, or RO text if write-back is ever enabled.",
            "mitigation": "Read-only in this engagement. Any future write-back would be drafted as a suggestion, require a human confirm, and be logged.",
            "priority": "High",
        },
        {
            "stride": "Repudiation",
            "threat": "A manager disputes what the assistant recommended on a deal or a service write-up, and there is no record of the interaction.",
            "mitigation": "Audit log of prompts, retrieved sources, and outputs, retained for an agreed period, with store and central IT access.",
            "priority": "Medium",
        },
        {
            "stride": "Information disclosure",
            "threat": "Deal jackets, consumer credit data, or customer PII leak into logs, a model provider, or another store's context.",
            "mitigation": "Data minimization and redaction; no raw SSNs or full credit reports in the prototype; store-level access boundaries; no training on customer data by default; prefer local or contractual endpoints.",
            "priority": "High",
        },
        {
            "stride": "Denial of service",
            "threat": "The assistant or its connector is unavailable during peak Saturday traffic, and staff have no fallback.",
            "mitigation": "The assistant is an aid, not a gate. Store process still works in the DMS alone. Rate-limit the prototype and document a fallback.",
            "priority": "Medium",
        },
        {
            "stride": "Elevation of privilege",
            "threat": "A service advisor or a less-privileged role uses the assistant to see F&I deal terms or credit data they cannot see in the DMS today.",
            "mitigation": "Role-aware retrieval. The assistant only surfaces fields the user's existing DMS/CRM role already permits.",
            "priority": "High",
        },
    ],
    "kpis": [
        {
            "metric": "Time in the F&I office (selected product presentation steps)",
            "baseline": "Confirm in week 1 from a sample of deals (often 45–90 minutes door-to-door; we will measure the specific steps the slice touches).",
            "target": "A realistic pilot target is a 15–25% reduction on the steps in scope, without a drop in compliance completeness.",
            "how_measured": "Timestamps from the DMS / F&I log plus a short observer sample at pilot stores.",
        },
        {
            "metric": "F&I product penetration / PVR consistency across pilot stores",
            "baseline": "Current penetration and PVR, and the spread between stores, pulled from existing F&I reports.",
            "target": "Narrow the gap between the lowest and highest pilot store; do not set a 'sell more product' target that conflicts with fair-lending or customer-fit standards.",
            "how_measured": "Existing F&I reports, compared pre/post, with a clear definition of which products are in scope.",
        },
        {
            "metric": "Service write-up completeness (required fields / customer concern quality)",
            "baseline": "Sample of repair orders scored against a simple completeness checklist agreed in week 1.",
            "target": "A higher share of ROs that meet the checklist on first write-up (target set once the baseline sample is scored).",
            "how_measured": "Checklist scoring on a weekly sample of ROs at pilot stores.",
        },
        {
            "metric": "Service appointment no-show rate (if that use case is in the slice)",
            "baseline": "Current no-show rate from the scheduler / DMS.",
            "target": "A modest, agreed reduction (for example 10–20% relative) over the pilot window, not a one-week spike.",
            "how_measured": "Scheduler reports; keep marketing promotions constant so the metric is not confounded.",
        },
        {
            "metric": "User trust / adoption",
            "baseline": "Zero (new tool). Week 3 will capture a first reaction score.",
            "target": "A majority of pilot users say they would use the slice in a real deal or write-up at least weekly, and can name one thing it saved them.",
            "how_measured": "Short weekly pulse (3 questions) plus qualitative notes from ride-alongs.",
        },
    ],
    "risks": _common_risks()
    + [
        {
            "risk": "Store-to-store process variation makes a single prototype feel 'wrong' at some rooftops.",
            "likelihood": "High",
            "impact": "Medium",
            "mitigation": "Pilot 2–3 stores that already share a DMS playbook. Treat local exceptions as configuration, not as a reason to customize everything in week 3.",
        },
        {
            "risk": "Fair-lending, product-pressure, or OEM/compliance concerns if the assistant is seen as a 'sell more' tool.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "Frame the slice as consistency, completeness, and time — not as maximizing product penetration. Keep a human in the loop. Document this in the data-handling and KPI notes.",
        },
    ],
    "staffing": [
        {
            "role": "Forward Deployed / Solutions Engineer (lead)",
            "time": "Full-time, 4 weeks",
            "responsibilities": "Discovery, architecture, prototype, threat model, stakeholder management, and the final readout.",
        },
        {
            "role": "Customer sponsor (group operator, GM, or director of F&I / Service)",
            "time": "2–3 hours per week",
            "responsibilities": "Decisions on scope, access to stores, and go/no-go at the end of week 4.",
        },
        {
            "role": "DMS / IT owner",
            "time": "4–6 hours per week",
            "responsibilities": "Extracts, access, integration constraints, and review of the architecture and threat model.",
        },
        {
            "role": "F&I and Service end-user reviewers (3–5 people)",
            "time": "2–4 hours across weeks 1 and 3",
            "responsibilities": "Show the real workflow, test the thin slice, and give plain-language feedback.",
        },
        {
            "role": "Compliance or office-of-the-general-counsel contact (as available)",
            "time": "2–4 hours in weeks 2–4",
            "responsibilities": "Review data-handling, consumer-credit exposure, and any later pilot conditions.",
        },
    ],
}


HEALTHCARE: dict[str, Any] = {
    "problem_summary": (
        "{customer} is a healthcare organization ({size_hint}) asking for AI help "
        "with {use_cases} in {departments}. Those workflows live in {systems} and "
        "involve {data_types}. That is a {sensitivity} engagement: PHI and HIPAA "
        "obligations shape the architecture from day one, not as an afterthought.\n\n"
        "The business problem underneath the ask is time and burnout — intake is "
        "slow, and clinicians are still finishing charts after hours — not 'add a "
        "chatbot to the EHR.' A four-week scoping engagement will map the real "
        "intake and documentation path, design a HIPAA-aware thin slice on "
        "de-identified or tightly controlled data, and leave clinical, IT, and "
        "compliance leaders with a pilot plan they can accept or reject. This is "
        "not a three-campus go-live."
    ),
    "assumptions": _common_assumptions()
    + [
        "A privacy / compliance counterpart will review the data-handling note in week 2.",
        "The week-3 prototype will use de-identified, synthetic, or otherwise approved data unless a documented exception is granted.",
        "No prototype output will be written into the legal medical record during this four-week engagement.",
    ],
    "in_scope": [
        "Discovery with {departments}, HIM / clinical informatics, and IT security, and a current-state map of intake and documentation in {systems}.",
        "A HIPAA-aware target architecture for {use_cases}, including BAA considerations if a vendor processes PHI.",
        "A STRIDE-style threat model focused on PHI disclosure, auditability, and inappropriate access.",
        "A thin-slice prototype on de-identified or approved sample data that illustrates {use_cases}.",
        "A pilot recommendation for one clinic, unit, or campus, with quality and safety metrics and a compliance follow-up list.",
    ],
    "out_of_scope": _common_out_of_scope()
    + [
        "Autonomous clinical decision-making, diagnosis, or treatment recommendations presented as medical advice.",
        "Any change to the legal medical record, coding, or billing without a separate, compliance-approved path.",
        "IRB submission or a formal research protocol (we will only flag whether one might be needed).",
    ],
    "weeks": [
        {
            "week": 1,
            "title": "Discovery and current-state mapping",
            "goals": [
                "Pin the ask to specific intake and/or documentation steps that clinicians and front-desk staff actually feel.",
                "Inventory {systems}, identity, and where PHI moves today.",
            ],
            "activities": [
                "Kickoff with a clinical sponsor, informatics, IT, and compliance / privacy.",
                "Shadow intake and after-hours documentation for a short session — watch the work, don't just interview about it.",
                "Collect the current metrics (door-to-provider, intake cycle time, after-hours EHR time if available).",
                "Agree what is in the thin slice and what must never appear in a demo (direct identifiers, minors, sensitive encounter types, etc.).",
            ],
            "deliverables": [
                "Current-state workflow map for {use_cases}.",
                "PHI data-flow sketch and system inventory.",
                "Confirmed prototype scope, including an explicit list of excluded data classes.",
            ],
        },
        {
            "week": 2,
            "title": "HIPAA-aware architecture and threat model",
            "goals": [
                "Design a target architecture that can sit beside {systems} with least-privilege access and a full audit trail.",
                "Get a first compliance reaction before any prototype is built on real data.",
            ],
            "activities": [
                "Draft architecture: identity / SSO, EHR and scheduler read-only paths, de-identification, access control, audit log, assistant.",
                "Write a data-handling note covering BAAs, minimum necessary, retention, and where prompts and outputs live.",
                "Facilitate a STRIDE-style threat model with IT security and privacy.",
                "Decide the week-3 data source: synthetic, de-identified extract, or a tightly provisioned sandbox.",
            ],
            "deliverables": [
                "Target architecture diagram and narrative.",
                "Data-handling and HIPAA considerations note.",
                "STRIDE threat model for the four-week slice.",
            ],
        },
        {
            "week": 3,
            "title": "Thin-slice prototype on approved data",
            "goals": [
                "Show one working slice of {use_cases} that a front-desk user or clinician can react to.",
                "Keep PHI risk low enough that the demo can actually be shown.",
            ],
            "activities": [
                "Build a narrow prototype (for example, intake questionnaire structuring, or a documentation draft the clinician must edit) on the approved dataset only.",
                "Review with a small group of end users and a compliance observer if available.",
                "Capture safety issues: hallucinated history, missed allergies, over-confident wording, or anything that looks like a diagnosis.",
                "Do not write back to the EHR.",
            ],
            "deliverables": [
                "Working prototype (demo-quality) and a demo script for clinical and compliance leaders.",
                "Safety and usability notes, including any 'do not show this output to a patient' rules.",
                "Updated architecture if needed.",
            ],
        },
        {
            "week": 4,
            "title": "Pilot plan, quality metrics, and handoff",
            "goals": [
                "Propose a limited pilot (one unit, clinic, or campus) with clear human-in-the-loop rules.",
                "Leave a go/no-go path that compliance and clinical leadership can stand behind.",
            ],
            "activities": [
                "Draft pilot design: location, users, duration, supervision, and what happens when the tool is wrong.",
                "Lock quality and operations KPIs and how baselines will be measured.",
                "List residual HIPAA follow-ups, training, and whether a later IRB or formal security review is needed.",
                "Handoff readout with the sponsor, informatics, IT, and privacy.",
            ],
            "deliverables": [
                "Pilot plan with staffing, KPIs, safety rails, and training.",
                "Go/no-go checklist and residual risk register.",
                "Final architecture, threat model, and readout.",
            ],
        },
    ],
    "architecture_narrative": (
        "The proposed slice does not replace {systems} and does not become the "
        "legal record. A read-only, least-privilege path — preferably through "
        "existing identity / SSO — feeds a minimized or de-identified dataset "
        "into an assistant used by {departments} for {use_cases}. Access control "
        "and an audit log are mandatory, not optional, because the data class is "
        "{sensitivity}. Relevant frameworks include {compliance}. Outputs are "
        "drafts or structured intake support that a human must review. No "
        "autonomous clinical action, and no write-back to the EHR, in this "
        "four-week engagement."
    ),
    "threats": [
        {
            "stride": "Spoofing",
            "threat": "A shared workstation or borrowed credentials lets the wrong person query or generate content about a patient.",
            "mitigation": "SSO, no shared clinical logins for the assistant, automatic timeout, and the same break-glass rules the EHR already uses.",
            "priority": "High",
        },
        {
            "stride": "Tampering",
            "threat": "A generated note is written into the legal medical record with incorrect history, meds, or allergies.",
            "mitigation": "No write-back in this engagement. Any later draft-to-EHR path must require an attested clinician edit and leave an audit trail.",
            "priority": "High",
        },
        {
            "stride": "Repudiation",
            "threat": "A clinician or staff member cannot show what the assistant proposed versus what was filed.",
            "mitigation": "Immutable audit log of prompts, sources, and outputs, retained per the organization's health-record and HIPAA policies.",
            "priority": "High",
        },
        {
            "stride": "Information disclosure",
            "threat": "PHI appears in prompts, model-provider logs, screenshots, or a demo deck, or is visible to staff who do not have a need to know.",
            "mitigation": "Minimum necessary and de-identification for the prototype; no production PHI in slides; BAA if a vendor processes PHI; role-based access; ban of unsanctioned copy/paste into public tools.",
            "priority": "High",
        },
        {
            "stride": "Denial of service",
            "threat": "Intake or documentation depends on a tool that is down during a busy clinic session.",
            "mitigation": "The assistant is optional. Existing EHR and intake process remain the system of record and the fallback.",
            "priority": "Medium",
        },
        {
            "stride": "Elevation of privilege",
            "threat": "A front-desk role uses the assistant to retrieve clinical data their EHR role does not allow.",
            "mitigation": "The assistant inherits EHR/identity roles. Retrieval is role-aware. Sensitive encounter types can be excluded entirely from the slice.",
            "priority": "High",
        },
    ],
    "kpis": [
        {
            "metric": "Patient intake cycle time (arrival to complete intake)",
            "baseline": "Confirm in week 1 from scheduling / EHR timestamps or a time-motion sample.",
            "target": "A modest, agreed reduction on the steps the slice actually touches (set after the baseline is measured), without a rise in registration error rates.",
            "how_measured": "EHR / scheduling timestamps plus a short observed sample on the pilot unit.",
        },
        {
            "metric": "After-hours documentation time for participating clinicians",
            "baseline": "EHR audit or self-reported after-hours charting time, agreed in week 1 (this number is often incomplete — say so if it is).",
            "target": "A directionally lower after-hours burden on the documentation steps in scope, with no drop in note quality.",
            "how_measured": "EHR audit logs where available, plus a weekly clinician pulse.",
        },
        {
            "metric": "Documentation quality / safety flags",
            "baseline": "A small scored sample of notes or intake packets against a quality checklist (completeness, obvious inconsistencies).",
            "target": "No increase in quality defects; any hallucinated or unsafe draft is caught before it could reach a record.",
            "how_measured": "Dual review of a weekly sample during the pilot; track 'assistant errors caught by the human'.",
        },
        {
            "metric": "Clinician and staff adoption / trust",
            "baseline": "Zero (new tool).",
            "target": "A majority of pilot users would continue using the slice, and no safety-related stop-the-line event is left unaddressed.",
            "how_measured": "Short pulse survey plus a live debrief with the clinical sponsor.",
        },
    ],
    "risks": _common_risks()
    + [
        {
            "risk": "Prototype outputs look like clinical advice or are trusted too much.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "Label every output as a draft for human review. Ban diagnosis/treatment language in the slice. Review wording with the clinical sponsor in week 3.",
        },
        {
            "risk": "PHI is accidentally used in a demo, log, or vendor tool.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "Default to synthetic or de-identified data. Written data-handling rules. No screenshots of real charts. Compliance invited to the week-3 review.",
        },
    ],
    "staffing": [
        {
            "role": "Forward Deployed / Solutions Engineer (lead)",
            "time": "Full-time, 4 weeks",
            "responsibilities": "Discovery, HIPAA-aware architecture, prototype, threat model, and the final readout.",
        },
        {
            "role": "Clinical sponsor (CMIO, nursing lead, or clinic medical director)",
            "time": "2–3 hours per week",
            "responsibilities": "Scope decisions, safety review, and go/no-go.",
        },
        {
            "role": "Clinical informatics / EHR analyst",
            "time": "4–6 hours per week",
            "responsibilities": "Workflow truth, extract or sandbox access, and EHR constraints.",
        },
        {
            "role": "Privacy / compliance / information security",
            "time": "3–5 hours in weeks 2–4",
            "responsibilities": "Data-handling review, BAA questions, threat model, and pilot conditions.",
        },
        {
            "role": "End-user reviewers (intake staff and clinicians)",
            "time": "2–4 hours across weeks 1 and 3",
            "responsibilities": "Show the real work, test the thin slice, flag unsafe or unusable output.",
        },
    ],
}


INSURANCE: dict[str, Any] = {
    "problem_summary": (
        "{customer} is a mid-size insurance organization ({size_hint}) asking for "
        "AI help with {use_cases} in {departments}. Those workflows run on "
        "{systems} and involve {data_types}. That is a {sensitivity} engagement: "
        "policyholder PII, financials, and any fraud-scoring output have to be "
        "explainable and carefully controlled.\n\n"
        "The business problem underneath the ask is cycle time and manual review. "
        "FNOL intake is repetitive, and SIU triage is slow because analysts hunt "
        "for signals by hand. A four-week scoping engagement will map the intake "
        "and referral path, design a thin slice that assists — not auto-decides — "
        "claims and SIU staff, and leave the carrier with a pilot plan, KPIs, and "
        "a clear stance on model-risk and fairness questions. This is not a book "
        "of business go-live, and it is not an automated decline engine."
    ),
    "assumptions": _common_assumptions()
    + [
        "Fraud or SIU scoring, if shown at all, is a triage aid for human investigators — not an automatic denial or cancellation.",
        "A claims operations lead and, if fraud is in scope, an SIU contact will join discovery and the week-3 review.",
        "A historical claims extract (or a realistic synthetic set) can be provided with direct identifiers minimized.",
    ],
    "in_scope": [
        "Discovery with {departments} and a current-state map of FNOL / claims intake and, if in scope, SIU referral through {systems}.",
        "A target architecture for {use_cases} with read-only integration, access control, and an audit trail of recommendations.",
        "A STRIDE-style threat model covering PII, financial data, prompt injection against claims data, and misuse of fraud flags.",
        "A thin-slice prototype on historical or synthetic claims that illustrates intake structuring and/or SIU triage support.",
        "A pilot recommendation for one claims pod or line of business, with cycle-time and quality KPIs and model-risk notes.",
    ],
    "out_of_scope": _common_out_of_scope()
    + [
        "Automated claim denial, settlement, or policy action without a human decision-maker.",
        "A production fraud model replacement, credit-style scoring rollout, or a formal model-risk validation opinion.",
        "Changes to policy wording, rating, or underwriting guidelines.",
    ],
    "weeks": [
        {
            "week": 1,
            "title": "Discovery and current-state mapping",
            "goals": [
                "Pin the ask to concrete FNOL steps and, if requested, the SIU referral path.",
                "Inventory {systems} and the claims data that would feed a thin slice.",
            ],
            "activities": [
                "Kickoff with claims operations, intake leadership, SIU (if in scope), and IT.",
                "Sit with adjusters / intake specialists and walk live or recent FNOL files.",
                "Document handoffs, downstream systems, and where work today sits in email or spreadsheets.",
                "Agree which lines of business are in the slice and which claim types are excluded (e.g. litigated, SIU already open, catastrophe surge).",
                "Capture current cycle-time and quality metrics, however imperfect.",
            ],
            "deliverables": [
                "Current-state map of {use_cases}.",
                "System and data inventory, including sensitive financial and PII fields.",
                "Confirmed prototype scope and exclusions.",
            ],
        },
        {
            "week": 2,
            "title": "Architecture, explainability, and threat model",
            "goals": [
                "Design an architecture that assists intake and triage without becoming a silent decision engine.",
                "Write down how fraud signals would be explained and audited.",
            ],
            "activities": [
                "Draft architecture: policy admin and claims read-only paths, minimization, access control, audit log, assistant / triage queue.",
                "Define output style: structured FNOL drafts, missing-info checklists, and (if in scope) a ranked 'review suggested' flag with reasons — not a fraud score presented as fact.",
                "STRIDE-style threat model with IT security and a claims quality or compliance contact.",
                "Choose the week-3 dataset and the identifier minimization approach.",
            ],
            "deliverables": [
                "Target architecture diagram and narrative.",
                "Data-handling and explainability note.",
                "STRIDE threat model for the four-week slice.",
            ],
        },
        {
            "week": 3,
            "title": "Thin-slice prototype",
            "goals": [
                "Show one working slice of {use_cases} that an intake specialist or SIU analyst can react to.",
                "Test whether the explanations are actually useful, not just technically present.",
            ],
            "activities": [
                "Build a narrow prototype on the agreed extract: FNOL structuring and/or a 'please review' queue with human-readable reasons.",
                "Review with intake and SIU users. Score a small set of historical claims: would this have helped, and would it have been unfair or noisy?",
                "Record false positives / false negatives qualitatively — this is not a model validation, but we should not demo a clearly noisy flag as if it were ready.",
                "No write-back to the claims system.",
            ],
            "deliverables": [
                "Working prototype (demo-quality) and a demo script for claims and SIU leaders.",
                "Qualitative error notes and user feedback.",
                "Updated architecture if needed.",
            ],
        },
        {
            "week": 4,
            "title": "Pilot plan, KPIs, and handoff",
            "goals": [
                "Propose a pilot in one claims pod or line of business, with human decision rights unchanged.",
                "Leave a clear list of model-risk, fairness, and regulatory follow-ups.",
            ],
            "activities": [
                "Draft the pilot: users, volume, duration, escalation to SIU, and what is explicitly not automated.",
                "Lock KPIs (cycle time, rework, referral quality) and how baselines come from {systems}.",
                "Write residual risks and a go/no-go checklist, including any need for a formal model-risk review before wider use.",
                "Handoff readout with claims, SIU, IT, and compliance as available.",
            ],
            "deliverables": [
                "Pilot plan with staffing, KPIs, and human-in-the-loop rules.",
                "Go/no-go checklist and residual risk register.",
                "Final architecture, threat model, and readout.",
            ],
        },
    ],
    "architecture_narrative": (
        "The proposed slice sits beside {systems}; it does not replace the claims "
        "or policy admin platforms and it does not issue claim decisions. A "
        "read-only, minimized extract feeds an assistant used by {departments} "
        "for {use_cases}. Access control and an audit log record what was "
        "suggested and why, which matters for both quality review and any later "
        "regulatory question. Data class is {sensitivity}; relevant controls "
        "include {compliance}. Fraud-related output, if present, is a 'review "
        "suggested' aid with reasons, never an automatic adverse action. No "
        "write-back in weeks 1–3."
    ),
    "threats": [
        {
            "stride": "Spoofing",
            "threat": "An unauthorized user, vendor, or shared desk login queries policyholder files or SIU flags through the assistant.",
            "mitigation": "Named accounts / SSO, role-based access (intake vs. adjuster vs. SIU), and session timeout. SIU flags are visible only to permitted roles.",
            "priority": "High",
        },
        {
            "stride": "Tampering",
            "threat": "A user or injected prompt alters FNOL facts, reserve suggestions, or fraud flags if write-back is enabled.",
            "mitigation": "Read-only in this engagement. Later write-back would be a draft requiring a licensed/authorized user confirm, with a full audit trail.",
            "priority": "High",
        },
        {
            "stride": "Repudiation",
            "threat": "A customer, regulator, or internal quality team asks why a claim was referred to SIU or delayed, and the reasoning is not reconstructable.",
            "mitigation": "Log the recommendation, the human-readable reasons, the data sources used, and the human's final action.",
            "priority": "High",
        },
        {
            "stride": "Information disclosure",
            "threat": "Policyholder PII, financials, or SIU status leak to the wrong role, a model vendor, or another claim file's context.",
            "mitigation": "Minimization and field-level exclusion; claim-level isolation; vendor terms / no training on carrier data by default; role-aware retrieval.",
            "priority": "High",
        },
        {
            "stride": "Denial of service",
            "threat": "A volume spike (weather event, outage) makes the assistant unavailable just when intake load is highest.",
            "mitigation": "The tool is an aid. Existing FNOL process remains usable without it. Document a fallback and do not put the assistant on the critical path in the pilot.",
            "priority": "Medium",
        },
        {
            "stride": "Elevation of privilege",
            "threat": "An intake role sees SIU indicators, special investigations notes, or other claims they should not see.",
            "mitigation": "Inherit claims-system permissions. Separate SIU views. Exclude open-investigation notes from the intake slice unless SIU is the user.",
            "priority": "High",
        },
    ],
    "kpis": [
        {
            "metric": "FNOL intake cycle time (first notice to a complete, usable claim file)",
            "baseline": "Confirm in week 1 from the claims system (median and 90th percentile, for the line of business in scope).",
            "target": "A 15–30% reduction in elapsed time on the intake steps the slice touches, without a rise in rework or missing-info send-backs.",
            "how_measured": "Claims-system timestamps on a pre/post cohort, same line of business, excluding catastrophe spikes if possible.",
        },
        {
            "metric": "Intake rework / missing-information rate",
            "baseline": "Share of new claims sent back or delayed for missing FNOL fields, from quality reports or a week-1 sample.",
            "target": "A lower missing-info rate, or at least no increase while cycle time improves.",
            "how_measured": "Existing quality queues plus a structured sample of files.",
        },
        {
            "metric": "SIU referral usefulness (if fraud triage is in the slice)",
            "baseline": "Current referral volume, and a qualitative sense of signal-to-noise from SIU (a formal precision/recall baseline may not exist — say so).",
            "target": "SIU analysts judge a majority of flagged 'review suggested' items as worth a look, with documented reasons. No automatic action on a flag.",
            "how_measured": "SIU review of a labeled sample during the pilot; track 'useful / not useful / unfair or unexplained'.",
        },
        {
            "metric": "User adoption and trust",
            "baseline": "Zero (new tool).",
            "target": "A majority of pilot intake staff or SIU analysts would keep the slice, and can explain what it does and does not decide.",
            "how_measured": "Short weekly pulse plus a debrief with claims leadership.",
        },
    ],
    "risks": _common_risks()
    + [
        {
            "risk": "A fraud flag is treated as a decision, creating fairness, complaint, or regulatory exposure.",
            "likelihood": "Medium",
            "impact": "High",
            "mitigation": "No automated adverse action. Language is 'review suggested' with reasons. Week-4 plan includes a model-risk follow-up before any wider use.",
        },
        {
            "risk": "Historical claims data is too messy or biased for a useful week-3 demo.",
            "likelihood": "Medium",
            "impact": "Medium",
            "mitigation": "Have a synthetic or heavily cleaned sample ready. Be honest in the readout about data quality and what that means for a later pilot.",
        },
    ],
    "staffing": [
        {
            "role": "Forward Deployed / Solutions Engineer (lead)",
            "time": "Full-time, 4 weeks",
            "responsibilities": "Discovery, architecture, prototype, threat model, and the final readout.",
        },
        {
            "role": "Claims operations sponsor",
            "time": "2–3 hours per week",
            "responsibilities": "Scope, access to a claims pod, KPI definitions, and go/no-go.",
        },
        {
            "role": "SIU lead (if fraud triage is in scope)",
            "time": "2–4 hours in weeks 1, 3, and 4",
            "responsibilities": "Referral-path truth, review of flag language, and qualitative scoring of the sample.",
        },
        {
            "role": "Claims / policy IT owner",
            "time": "4–6 hours per week",
            "responsibilities": "Extracts, permissions, integration constraints, and architecture review.",
        },
        {
            "role": "Compliance / model-risk contact (as available)",
            "time": "2–4 hours in weeks 2–4",
            "responsibilities": "Review of explainability, adverse-action boundaries, and residual follow-ups.",
        },
    ],
}


GENERAL: dict[str, Any] = {
    "problem_summary": (
        "{customer} has asked for AI support in {departments}, described as: "
        "“{ask}” The industry signal is {industry}, and the likely workflows are "
        "{use_cases}. Existing systems appear to include {systems}. Data involved "
        "may include {data_types}, treated as {sensitivity} until discovery "
        "confirms otherwise ({size_hint}; team context: {team_size}).\n\n"
        "The job of this four-week engagement is the same one an FDE does on a "
        "first customer visit: turn a vague 'we want AI' request into a scoped "
        "plan. We will map the current work, draw a thin-slice architecture, "
        "write down risks, and demo one narrow workflow on safe data — then leave "
        "a pilot recommendation. This is a scoping demo plan, not a production "
        "rollout."
    ),
    "assumptions": _common_assumptions()
    + [
        "Industry, systems, and data classes will be confirmed in week 1; this draft is based on keyword signals and any form fields provided.",
    ],
    "in_scope": [
        "Discovery with {departments} and a current-state map of {use_cases} across {systems}.",
        "A proposed target architecture with a read-only integration path, access control, and audit logging.",
        "A simple STRIDE-style threat model for the data classes detected.",
        "A thin-slice prototype or structured demo on sample or minimized data.",
        "A pilot recommendation with staffing, KPIs, and a go/no-go checklist.",
    ],
    "out_of_scope": _common_out_of_scope(),
    "weeks": [
        {
            "week": 1,
            "title": "Discovery and current-state mapping",
            "goals": [
                "Replace the vague ask with one or two measurable workflows.",
                "Inventory {systems} and the data that would have to move.",
            ],
            "activities": [
                "Kickoff with a business sponsor and a technical counterpart.",
                "Watch the real workflow with end users, not only leadership.",
                "Confirm systems, data sensitivity, and what 'good' looks like.",
                "Agree the thin-slice candidate and explicit non-goals.",
            ],
            "deliverables": [
                "Current-state workflow map.",
                "System and data inventory.",
                "Confirmed prototype scope.",
            ],
        },
        {
            "week": 2,
            "title": "Architecture, data handling, and threat model",
            "goals": [
                "Propose a target architecture that sits beside {systems}.",
                "Write down data handling and a first threat model.",
            ],
            "activities": [
                "Draft users, systems, connector, governance, and assistant.",
                "Define minimization, access, and retention for the prototype.",
                "Walk a STRIDE-style threat model with IT and a security contact if available.",
            ],
            "deliverables": [
                "Target architecture diagram and narrative.",
                "Data-handling note.",
                "STRIDE threat model for the four-week slice.",
            ],
        },
        {
            "week": 3,
            "title": "Thin-slice prototype",
            "goals": [
                "Show one working slice of {use_cases} that an end user can react to.",
            ],
            "activities": [
                "Build a narrowly scoped assistant on sample or minimized data.",
                "Review with a small group of users and capture trust and usability notes.",
                "Do not widen scope; park new ideas for week 4.",
            ],
            "deliverables": [
                "Working prototype (demo-quality) and a short demo script.",
                "User feedback and must-fix items.",
            ],
        },
        {
            "week": 4,
            "title": "Pilot plan, metrics, and handoff",
            "goals": [
                "Leave a plan the customer can accept or reject.",
            ],
            "activities": [
                "Draft a limited pilot: users, duration, support, and rollback.",
                "Lock KPIs and residual risks.",
                "Hold a readout with the sponsor and IT.",
            ],
            "deliverables": [
                "Pilot plan with staffing and KPIs.",
                "Go/no-go checklist and residual risk register.",
                "Final architecture, threat model, and readout.",
            ],
        },
    ],
    "architecture_narrative": (
        "The proposed slice sits beside {systems}. A read-only connector feeds a "
        "minimized dataset into an assistant for {departments}, scoped to "
        "{use_cases}. Access control and an audit log sit in front of the "
        "assistant. Data class is {sensitivity}; relevant controls include "
        "{compliance}. No production write-back in weeks 1–3."
    ),
    "threats": [
        {
            "stride": "Spoofing",
            "threat": "An unauthorized user accesses the assistant with a shared or borrowed account and sees customer or employee data.",
            "mitigation": "Named accounts or SSO, session timeout, and role inheritance from existing systems.",
            "priority": "High",
        },
        {
            "stride": "Tampering",
            "threat": "A prompt or a compromised connector changes records in a system of record.",
            "mitigation": "Read-only in this engagement. Future write-back would require a human confirm and an audit log.",
            "priority": "High",
        },
        {
            "stride": "Repudiation",
            "threat": "No record exists of what the assistant suggested or what a user did with it.",
            "mitigation": "Audit log of prompts, sources, and outputs with an agreed retention period.",
            "priority": "Medium",
        },
        {
            "stride": "Information disclosure",
            "threat": "Sensitive data leaks into logs, a model vendor, or the wrong role.",
            "mitigation": "Data minimization, role-aware retrieval, contractual or local model endpoints, and no training on customer data by default.",
            "priority": "High",
        },
        {
            "stride": "Denial of service",
            "threat": "The assistant is down and work has been designed to depend on it.",
            "mitigation": "Keep the existing process as the fallback; do not put the prototype on the critical path.",
            "priority": "Medium",
        },
        {
            "stride": "Elevation of privilege",
            "threat": "A user sees records or fields their existing system role does not allow.",
            "mitigation": "Inherit permissions from the system of record; never grant the assistant a wider role than the user.",
            "priority": "High",
        },
    ],
    "kpis": [
        {
            "metric": "Cycle time of the chosen workflow",
            "baseline": "Confirm in week 1 from system timestamps or a short observed sample.",
            "target": "A modest, agreed reduction on the steps in scope, without a rise in error or rework rates.",
            "how_measured": "System timestamps and a weekly sample.",
        },
        {
            "metric": "Quality / rework rate",
            "baseline": "Agree a simple quality checklist in week 1 and score a baseline sample.",
            "target": "No increase in defects; ideally a lower rework rate.",
            "how_measured": "Checklist scoring on a weekly sample.",
        },
        {
            "metric": "User adoption and trust",
            "baseline": "Zero (new tool).",
            "target": "A majority of pilot users would keep using the slice and can name one way it helped.",
            "how_measured": "Short weekly pulse plus qualitative notes.",
        },
    ],
    "risks": _common_risks(),
    "staffing": [
        {
            "role": "Forward Deployed / Solutions Engineer (lead)",
            "time": "Full-time, 4 weeks",
            "responsibilities": "Discovery, architecture, prototype, threat model, and the final readout.",
        },
        {
            "role": "Customer business sponsor",
            "time": "2–3 hours per week",
            "responsibilities": "Scope decisions, access to users, and go/no-go.",
        },
        {
            "role": "Customer IT / system owner",
            "time": "4–6 hours per week",
            "responsibilities": "Extracts, access, integration constraints, and architecture review.",
        },
        {
            "role": "End-user reviewers",
            "time": "2–4 hours across weeks 1 and 3",
            "responsibilities": "Show the real workflow and test the thin slice.",
        },
    ],
}


PACKS: dict[str, dict[str, Any]] = {
    "automotive": AUTOMOTIVE,
    "healthcare": HEALTHCARE,
    "insurance": INSURANCE,
    "general": GENERAL,
}


def for_industry(industry_id: str) -> dict[str, Any]:
    return PACKS.get(industry_id, GENERAL)
