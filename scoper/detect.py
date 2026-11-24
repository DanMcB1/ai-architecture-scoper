"""Explainable keyword detection for industry, data types, and systems.

The scoper is a rules engine, not a model. We scan the customer ask and
optional form fields, record the phrases that fired, and turn those
signals into a structured ScopeProfile. The UI shows this evidence so
the thinking is easy to walk through in an interview.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Iterable


@dataclass
class Signal:
    category: str
    label: str
    evidence: str
    weight: int = 1


@dataclass
class ScopeProfile:
    raw_ask: str
    customer_name: str
    industry_id: str
    industry_label: str
    departments: list[str]
    use_cases: list[str]
    data_types: list[str]
    sensitivity: str
    sensitivity_reason: str
    compliance: list[str]
    existing_systems: list[str]
    size_hint: str
    site_count: int | None
    team_size: str
    signals: list[Signal] = field(default_factory=list)
    overrides_used: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


# ---------------------------------------------------------------------------
# Pattern libraries
# ---------------------------------------------------------------------------

# Each industry rule is a list of (compiled-at-runtime) regex strings.
INDUSTRY_RULES: list[dict[str, Any]] = [
    {
        "id": "automotive",
        "label": "Automotive retail / dealer group",
        "patterns": [
            r"\bdealer(?:ship)?s?\b",
            r"\bdealer group\b",
            r"\brooftops?\b",
            r"\bautomotive\b",
            r"\bauto (?:dealer|group|retail)\b",
            r"\bf&i\b",
            r"\bfinance and insurance\b",
            r"\bdms\b",
            r"\bcdk\b",
            r"\breynolds\b",
            r"\btekion\b",
            r"\bdealr\b",
            r"\bvin\b",
            r"\bservice (?:department|lane|advisor|advisors|drive|ro)\b",
            r"\bdeal jackets?\b",
            r"\bproduct penetration\b",
            r"\bper vehicle retail\b",
            r"\bpvr\b",
        ],
    },
    {
        "id": "healthcare",
        "label": "Healthcare / hospital",
        "patterns": [
            r"\bhospital(?:s| system)?\b",
            r"\bhealth system\b",
            r"\bclinic(?:s|al)?\b",
            r"\bpatient(?:s)?\b",
            r"\bphi\b",
            r"\bhipaa\b",
            r"\behr\b",
            r"\bemr\b",
            r"\bepic\b",
            r"\bcerner\b",
            r"\bmeditech\b",
            r"\bathena(?:health)?\b",
            r"\bfhir\b",
            r"\bclinician(?:s)?\b",
            r"\bphysician(?:s)?\b",
            r"\bnurs(?:e|es|ing)\b",
            r"\bcharting\b",
            r"\bclinical documentation\b",
            r"\bpatient intake\b",
            r"\bcampus(?:es)?\b",
        ],
    },
    {
        "id": "insurance",
        "label": "Insurance (P&C)",
        "patterns": [
            r"\binsurer(?:s)?\b",
            r"\binsurance\b",
            r"\bclaims?\b",
            r"\bfnol\b",
            r"\bfirst notice of loss\b",
            r"\bunderwrit(?:e|ing|ers?)\b",
            r"\bpolicy(?:holder)?s?\b",
            r"\bsiu\b",
            r"\bfraud\b",
            r"\badjusters?\b",
            r"\bpolicy admin\b",
            r"\bguidewire\b",
            r"\bduck creek\b",
            r"\bp&c\b",
            r"\bproperty and casualty\b",
            r"\bcarrier\b",
            r"\bpremiums?\b",
        ],
    },
]

DATA_TYPE_RULES: list[tuple[str, list[str]]] = [
    (
        "PHI (protected health information)",
        [
            r"\bphi\b",
            r"\bhipaa\b",
            r"\bpatient(?:s)?\b",
            r"\behr\b",
            r"\bemr\b",
            r"\bclinical\b",
            r"\bdiagnosis\b",
            r"\bmedical (?:record|records|data)\b",
            r"\bcharting\b",
        ],
    ),
    (
        "Payment / consumer credit data",
        [
            r"\bf&i\b",
            r"\bfinance and insurance\b",
            r"\bcredit(?: data| application| report)?\b",
            r"\bdeal jackets?\b",
            r"\bpayment(?:s)?\b",
            r"\bpci\b",
            r"\bcredit card(?:s)?\b",
            r"\bfinancing\b",
            r"\bach\b",
            r"\bbanking\b",
        ],
    ),
    (
        "Financial / claims amounts",
        [
            r"\bclaims?\b",
            r"\bfraud\b",
            r"\bpremiums?\b",
            r"\bloss(?:es)?\b",
            r"\bfinancial data\b",
            r"\bpolicy admin\b",
        ],
    ),
    (
        "PII (personally identifiable information)",
        [
            r"\bpii\b",
            r"\bpolicyholder(?:s)?\b",
            r"\bcustomer (?:data|records|information|pii)\b",
            r"\bemployee(?:s)?\b",
            r"\bssn\b",
            r"\bdriver'?s license\b",
            r"\bemail\b",
            r"\bphone\b",
            r"\bprivacy\b",
            r"\bcredit data\b",
        ],
    ),
]

SYSTEM_RULES: list[tuple[str, list[str]]] = [
    ("DMS", [r"\bdms\b", r"\bcdk\b", r"\breynolds\b", r"\btekion\b", r"\bdealr\b", r"\bdealertrack\b"]),
    ("CRM", [r"\bcrm\b", r"\bsalesforce\b", r"\bhubspot\b", r"\bvinsolutions\b", r"\belead\b"]),
    ("Service scheduling", [r"\bservice schedul", r"\bxtime\b", r"\bno-shows?\b", r"\bservice appointment"]),
    ("EHR", [r"\behr\b", r"\bemr\b", r"\bepic\b", r"\bcerner\b", r"\bmeditech\b", r"\bathena"]),
    ("Patient scheduling", [r"\bpatient-scheduling\b", r"\bpatient scheduling\b"]),
    ("Identity / SSO", [r"\bsso\b", r"\bidentity\b", r"\bactive directory\b", r"\bokta\b"]),
    ("Claims system", [r"\bclaims system\b", r"\bclaimcenter\b", r"\bguidewire\b"]),
    ("Policy admin", [r"\bpolicy admin\b", r"\bpolicycenter\b", r"\bduck creek\b"]),
    ("ERP", [r"\berp\b", r"\bsap\b", r"\bnetsuite\b"]),
]

# Third item is the set of industries the rule may fire in, or None for all.
DEPARTMENT_RULES: list[tuple[str, list[str], set[str] | None]] = [
    ("F&I", [r"\bf&i\b", r"\bfinance and insurance\b"], {"automotive"}),
    (
        "Service",
        [r"\bservice (?:department|departments|lane|advisors?|drive)\b"],
        {"automotive"},
    ),
    ("Sales", [r"\bsales (?:department|desk|team)\b"], {"automotive"}),
    ("Parts", [r"\bparts (?:department|counter)\b"], {"automotive"}),
    ("Clinical / physicians", [r"\bclinician", r"\bphysician", r"\bdoctor", r"\bprovider"], {"healthcare"}),
    ("Nursing", [r"\bnurs(?:e|es|ing)\b"], {"healthcare"}),
    (
        "Patient intake / front desk",
        [r"\bpatient intake\b", r"\bfront-?desk\b", r"\badmissions?\b"],
        {"healthcare"},
    ),
    ("Health information management", [r"\bhim\b", r"\bmedical records\b"], {"healthcare"}),
    (
        "Compliance / privacy",
        [r"\bcompliance\b", r"\bprivacy (?:team|office|officer|review)\b", r"\bhipaa\b"],
        None,
    ),
    ("Claims operations", [r"\bclaims?\b", r"\badjusters?\b", r"\bfnol\b"], {"insurance"}),
    ("Special Investigations (SIU)", [r"\bsiu\b", r"\bfraud\b"], {"insurance"}),
    ("Underwriting", [r"\bunderwrit"], {"insurance"}),
]

USE_CASE_RULES: list[tuple[str, list[str], set[str] | None]] = [
    ("F&I menu / product presentation", [r"\bmenus?\b", r"\bproduct penetration\b", r"\bf&i\b"], {"automotive"}),
    ("Service write-up quality", [r"\bwrite-?up\b", r"\bservice advisors?\b"], {"automotive"}),
    ("Appointment no-show reduction", [r"\bno-shows?\b"], {"automotive"}),
    ("Patient intake acceleration", [r"\bpatient intake\b", r"\bfront-?desk intake\b"], {"healthcare"}),
    ("Clinical documentation assistance", [r"\bdocumentation\b", r"\bcharting\b", r"\bafter hours\b"], {"healthcare"}),
    (
        "FNOL / claims intake",
        [r"\bfnol\b", r"\bfirst notice of loss\b", r"\bclaims intake\b", r"\bintake\b"],
        {"insurance"},
    ),
    ("Fraud triage for SIU", [r"\bfraud\b", r"\bsiu\b"], {"insurance"}),
]

SIZE_PATTERNS = [
    (r"(\d+)\s*-?\s*rooftops?", "rooftops"),
    (r"(\d+)\s*-?\s*(?:stores?|locations?|sites?|campuses|dealerships)", "sites"),
    (r"\bthree campuses\b", "three campuses"),
    (r"\bmid-?size\b", "mid-size"),
    (r"\bregional\b", "regional"),
    (r"\benterprise\b", "enterprise"),
    (r"\bnational\b", "national"),
    (r"\bsmall\b", "small"),
]

SENSITIVITY_RANK = {"Low": 1, "Medium": 2, "High": 3, "Regulated": 4}

INDUSTRY_ALIASES = {
    "automotive retail / dealer group": "automotive",
    "automotive": "automotive",
    "auto": "automotive",
    "dealer": "automotive",
    "healthcare / hospital": "healthcare",
    "healthcare": "healthcare",
    "hospital": "healthcare",
    "insurance (p&c)": "insurance",
    "insurance": "insurance",
    "p&c": "insurance",
    "general / other": "general",
    "general": "general",
    "auto-detect from the ask": "",
    "": "",
}


def _scan(text: str, patterns: Iterable[str]) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            hits.append(match.group(0))
    return hits


def _unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        cleaned = re.sub(r"\s+", " ", item).strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return out


def _normalize_industry(value: str | None) -> str:
    if not value:
        return ""
    return INDUSTRY_ALIASES.get(value.strip().lower(), "")


def detect_industry(text: str) -> tuple[str, str, list[Signal]]:
    scores: dict[str, int] = {}
    signals: list[Signal] = []
    labels = {rule["id"]: rule["label"] for rule in INDUSTRY_RULES}
    for rule in INDUSTRY_RULES:
        hits = _scan(text, rule["patterns"])
        if hits:
            scores[rule["id"]] = scores.get(rule["id"], 0) + len(hits)
            signals.append(
                Signal(
                    category="industry",
                    label=rule["label"],
                    evidence=", ".join(f'"{h}"' for h in hits[:6]),
                    weight=len(hits),
                )
            )
    if not scores:
        return "general", "General / other", signals
    winner = max(scores, key=lambda k: (scores[k], k))
    return winner, labels[winner], signals


def detect_list(
    text: str,
    rules: list[tuple],
    category: str,
    industry_id: str | None = None,
) -> tuple[list[str], list[Signal]]:
    """Apply label/pattern rules, optionally limited to one industry."""
    labels: list[str] = []
    signals: list[Signal] = []
    for rule in rules:
        if len(rule) == 3:
            label, patterns, industries = rule
            if industries is not None and industry_id not in industries:
                continue
        else:
            label, patterns = rule
        hits = _scan(text, patterns)
        if hits:
            labels.append(label)
            signals.append(
                Signal(
                    category=category,
                    label=label,
                    evidence=", ".join(f'"{h}"' for h in hits[:5]),
                    weight=len(hits),
                )
            )
    return labels, signals


def detect_size(text: str) -> tuple[str, int | None, list[Signal]]:
    site_count: int | None = None
    hints: list[str] = []
    signals: list[Signal] = []
    rooftop = re.search(r"(\d+)\s*-?\s*rooftops?", text, flags=re.IGNORECASE)
    sites = re.search(
        r"(\d+)\s*-?\s*(?:stores?|locations?|sites?|campuses|dealerships)",
        text,
        flags=re.IGNORECASE,
    )
    words = re.search(r"\b(three|four|five|six|seven|eight|nine|ten)\s+campuses\b", text, flags=re.IGNORECASE)
    word_map = {
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    if rooftop:
        site_count = int(rooftop.group(1))
        hints.append(f"{site_count}-rooftop group")
        signals.append(Signal("size", f"{site_count} rooftops", f'"{rooftop.group(0)}"'))
    elif sites:
        site_count = int(sites.group(1))
        hints.append(f"{site_count} sites")
        signals.append(Signal("size", f"{site_count} sites", f'"{sites.group(0)}"'))
    elif words:
        site_count = word_map[words.group(1).lower()]
        hints.append(f"{site_count} campuses")
        signals.append(Signal("size", f"{site_count} campuses", f'"{words.group(0)}"'))

    for pattern, label in [
        (r"\bmid-?size\b", "mid-size organization"),
        (r"\bregional\b", "regional footprint"),
        (r"\benterprise\b", "enterprise scale"),
        (r"\bnational\b", "national footprint"),
        (r"\bsmall\b", "small organization"),
    ]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            hints.append(label)
            signals.append(Signal("size", label, f'"{match.group(0)}"'))

    if site_count and site_count >= 20:
        hints.append("multi-site / complex rollout")
    elif site_count and site_count >= 3:
        hints.append("multi-site organization")

    if not hints:
        return "Size not specified — assume a single pilot site until confirmed", site_count, signals
    return "; ".join(_unique(hints)), site_count, signals


def infer_sensitivity(
    data_types: list[str],
    industry_id: str,
    override: str | None,
) -> tuple[str, str, list[str], list[str]]:
    """Return sensitivity, reason, compliance frameworks, and overrides used."""
    compliance: list[str] = ["Internal access control", "Audit logging"]
    score = 2  # default Medium
    reasons: list[str] = []

    if any("PHI" in item for item in data_types) or industry_id == "healthcare":
        score = 4
        reasons.append("health data / PHI")
        compliance.extend(["HIPAA", "Business Associate Agreement (if a vendor handles PHI)"])
    if any("Payment" in item or "credit" in item.lower() for item in data_types) or industry_id == "automotive":
        score = max(score, 4 if any("Payment" in item or "credit" in item.lower() for item in data_types) else 3)
        if any("Payment" in item or "credit" in item.lower() for item in data_types):
            reasons.append("consumer credit / payment data")
            compliance.extend(["GLBA (consumer financial information)", "PCI-DSS if card data is in scope"])
    if any(item.startswith("Financial") for item in data_types) or industry_id == "insurance":
        score = max(score, 4 if industry_id == "insurance" else 3)
        reasons.append("financial / claims data")
        compliance.extend(["GLBA", "Model risk / explainability documentation for fraud flags", "State insurance regulatory expectations"])
    if any(item.startswith("PII") for item in data_types):
        score = max(score, 3)
        reasons.append("personally identifiable information")
        compliance.append("State privacy laws (e.g. applicable US state privacy acts)")

    if industry_id == "healthcare":
        score = 4
    if industry_id == "insurance":
        score = max(score, 4)
    if industry_id == "automotive" and any("Payment" in item or "PII" in item for item in data_types):
        score = max(score, 4)

    rank_to_label = {1: "Low", 2: "Medium", 3: "High", 4: "Regulated"}
    sensitivity = rank_to_label[score]
    reason = (
        "Detected " + ", ".join(_unique(reasons)) + "."
        if reasons
        else "No high-risk data types detected; defaulting to Medium until confirmed."
    )

    overrides: list[str] = []
    if override and override.strip() and override.strip() != "Auto-detect":
        chosen = override.strip()
        if chosen in SENSITIVITY_RANK:
            if SENSITIVITY_RANK[chosen] != SENSITIVITY_RANK[sensitivity]:
                overrides.append(f"data sensitivity set to {chosen} by the user (detected: {sensitivity})")
            sensitivity = chosen
            reason = f"User-selected sensitivity: {chosen}. Detected signals: " + (
                ", ".join(_unique(reasons)) or "none"
            ) + "."

    compliance = _unique(compliance)
    return sensitivity, reason, compliance, overrides


def _split_systems(raw: str) -> list[str]:
    # Split only on commas, semicolons, or " and " — never on "/"
    # so names like "Identity / SSO" stay together.
    parts = re.split(r"[,;]|\s+and\s+", raw, flags=re.IGNORECASE)
    return _unique(parts)


def build_profile(
    ask: str,
    industry: str = "",
    data_sensitivity: str = "",
    team_size: str = "",
    existing_systems: str = "",
    customer_name: str = "",
) -> ScopeProfile:
    """Build a ScopeProfile from the free-text ask plus optional form fields."""
    ask = (ask or "").strip()
    # Size clues should come from the ask itself, not from the team-size
    # field (which may contain words like "enterprise IT").
    detect_text = " ".join(
        part for part in (ask, industry, data_sensitivity, existing_systems, customer_name) if part
    ).strip()
    haystack = detect_text

    industry_id, industry_label, industry_signals = detect_industry(haystack)
    overrides: list[str] = []
    forced = _normalize_industry(industry)
    if forced:
        labels = {rule["id"]: rule["label"] for rule in INDUSTRY_RULES}
        labels["general"] = "General / other"
        if forced != industry_id:
            overrides.append(f"industry set to {labels[forced]} by the user (detected: {industry_label})")
        industry_id = forced
        industry_label = labels[forced]

    data_types, data_signals = detect_list(haystack, DATA_TYPE_RULES, "data")
    if industry_id == "healthcare" and not any("PHI" in item for item in data_types):
        data_types.insert(0, "PHI (protected health information)")
        data_signals.append(Signal("data", "PHI (protected health information)", "inferred from healthcare industry"))
    if industry_id == "automotive" and not any("PII" in item for item in data_types):
        data_types.append("PII (personally identifiable information)")
        data_signals.append(Signal("data", "PII (personally identifiable information)", "inferred from dealer/customer records"))
    if industry_id == "insurance" and not any("PII" in item for item in data_types):
        data_types.append("PII (personally identifiable information)")
        data_signals.append(Signal("data", "PII (personally identifiable information)", "inferred from policyholder records"))

    systems, system_signals = detect_list(haystack, SYSTEM_RULES, "system")
    if existing_systems.strip():
        already = {s.lower() for s in systems}
        for item in _split_systems(existing_systems):
            if item.lower() not in already:
                systems.append(item)
                already.add(item.lower())
                system_signals.append(Signal("system", item, "provided in the Existing systems field"))

    departments, dept_signals = detect_list(
        haystack, DEPARTMENT_RULES, "department", industry_id
    )
    use_cases, use_case_signals = detect_list(
        haystack, USE_CASE_RULES, "use_case", industry_id
    )
    size_hint, site_count, size_signals = detect_size(haystack)

    sensitivity, sensitivity_reason, compliance, sens_overrides = infer_sensitivity(
        data_types, industry_id, data_sensitivity
    )
    overrides.extend(sens_overrides)

    team = team_size.strip() if team_size.strip() else "Not specified — confirm during week 1 discovery"
    if team_size.strip():
        overrides.append("team size provided by the user")

    name = customer_name.strip() or "Your organization"

    # Industry-specific default systems if none found
    if not systems:
        defaults = {
            "automotive": ["DMS", "CRM"],
            "healthcare": ["EHR"],
            "insurance": ["Claims system", "Policy admin"],
            "general": ["Existing line-of-business systems (to be inventoried)"],
        }
        systems = defaults.get(industry_id, defaults["general"])
        for item in systems:
            system_signals.append(Signal("system", item, "defaulted from industry pack (not named in the ask)"))

    if not departments:
        defaults = {
            "automotive": ["F&I", "Service"],
            "healthcare": ["Clinical / physicians", "Patient intake / front desk"],
            "insurance": ["Claims operations"],
            "general": ["Business operations (to be confirmed)"],
        }
        departments = defaults.get(industry_id, defaults["general"])

    if not use_cases:
        defaults = {
            "automotive": ["F&I menu / product presentation", "Service write-up quality"],
            "healthcare": ["Patient intake acceleration", "Clinical documentation assistance"],
            "insurance": ["FNOL / claims intake", "Fraud triage for SIU"],
            "general": ["AI assistant for a high-friction operational workflow (to be confirmed)"],
        }
        use_cases = defaults.get(industry_id, defaults["general"])

    signals = (
        industry_signals
        + data_signals
        + system_signals
        + dept_signals
        + use_case_signals
        + size_signals
    )

    return ScopeProfile(
        raw_ask=ask,
        customer_name=name,
        industry_id=industry_id,
        industry_label=industry_label,
        departments=departments,
        use_cases=use_cases,
        data_types=data_types or ["Unspecified business data (confirm in discovery)"],
        sensitivity=sensitivity,
        sensitivity_reason=sensitivity_reason,
        compliance=compliance,
        existing_systems=systems,
        size_hint=size_hint,
        site_count=site_count,
        team_size=team,
        signals=signals,
        overrides_used=overrides,
    )
