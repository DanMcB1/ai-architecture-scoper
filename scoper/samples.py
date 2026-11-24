"""One-click sample customer asks used in the app and in example exports."""

from __future__ import annotations

from typing import Any

SAMPLES: dict[str, dict[str, Any]] = {
    "auto-dealer": {
        "title": "Auto dealer group",
        "customer_name": "Lakeside Auto Group (sample)",
        "ask": (
            "We're a 40-rooftop auto dealer group and want AI for our F&I and "
            "service departments. F&I managers spend too long building menus, "
            "product penetration is inconsistent across stores, and service "
            "advisors struggle with no-shows and write-up quality. We run a "
            "common DMS and a CRM today, and we care a lot about customer "
            "credit data and deal-jacket privacy."
        ),
        "industry": "Automotive retail / dealer group",
        "data_sensitivity": "Regulated",
        "team_size": "Large enterprise IT (central) plus store-level managers",
        "existing_systems": "DMS, CRM, service scheduling",
    },
    "regional-hospital": {
        "title": "Regional hospital",
        "customer_name": "Cedar Ridge Health System (sample)",
        "ask": (
            "We're a regional hospital system with three campuses. We want AI "
            "to speed up patient intake and reduce the time clinicians spend "
            "on documentation after hours. Nurses and physicians are burned "
            "out on charting in the EHR, front-desk intake is slow, and our "
            "compliance team is strict about PHI and HIPAA. We use a major "
            "EHR and a separate patient-scheduling system."
        ),
        "industry": "Healthcare / hospital",
        "data_sensitivity": "Regulated",
        "team_size": "Mid-size health system IT and clinical informatics",
        "existing_systems": "EHR, patient scheduling, identity / SSO",
    },
    "mid-size-insurer": {
        "title": "Mid-size insurer",
        "customer_name": "Northbridge P&C (sample)",
        "ask": (
            "We're a mid-size property and casualty insurer. We want AI to "
            "help with claims intake (FNOL) and to flag potentially fraudulent "
            "claims for our SIU team. Cycle time on first notice of loss is "
            "too long, adjusters spend hours on repetitive intake, and fraud "
            "review is mostly manual. We have a claims system and a policy "
            "admin platform, and we hold a lot of policyholder PII and "
            "financial data."
        ),
        "industry": "Insurance (P&C)",
        "data_sensitivity": "Regulated",
        "team_size": "Mid-size carrier IT and claims operations",
        "existing_systems": "Claims system, policy admin, CRM",
    },
}


def get_sample(key: str) -> dict[str, Any]:
    if key not in SAMPLES:
        known = ", ".join(SAMPLES)
        raise KeyError(f"Unknown sample '{key}'. Choose one of: {known}")
    return SAMPLES[key]
