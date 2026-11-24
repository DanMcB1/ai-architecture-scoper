"""End-to-end checks for the three interview samples and the renderer."""

from __future__ import annotations

import unittest

from scoper.detect import build_profile
from scoper.engine import generate_sow
from scoper.render import render_markdown
from scoper.samples import SAMPLES, get_sample


REQUIRED_HEADINGS = [
    "# ",
    "## 1. Problem summary",
    "## 2. Assumptions",
    "## 3. Scope",
    "### In scope",
    "### Out of scope",
    "## 4. Four-week plan",
    "### Week 1:",
    "### Week 2:",
    "### Week 3:",
    "### Week 4:",
    "## 5. Proposed architecture",
    "```mermaid",
    "## 6. STRIDE-style threat model",
    "## 7. Success metrics and KPIs",
    "## 8. Risks",
    "## 9. Staffing",
    "## Appendix: Detected signals",
]


def sow_for(key: str, polish: bool = False):
    sample = get_sample(key)
    profile = build_profile(
        ask=sample["ask"],
        industry=sample.get("industry", ""),
        data_sensitivity=sample.get("data_sensitivity", ""),
        team_size=sample.get("team_size", ""),
        existing_systems=sample.get("existing_systems", ""),
        customer_name=sample.get("customer_name", ""),
    )
    return generate_sow(profile, polish_summary=polish)


class SampleGenerationTests(unittest.TestCase):
    def test_three_samples_exist(self):
        self.assertEqual(
            set(SAMPLES),
            {"auto-dealer", "regional-hospital", "mid-size-insurer"},
        )

    def test_auto_dealer_profile(self):
        sow = sow_for("auto-dealer")
        self.assertEqual(sow.profile.industry_id, "automotive")
        self.assertEqual(sow.profile.sensitivity, "Regulated")
        self.assertEqual(sow.profile.site_count, 40)
        self.assertTrue(any("F&I" in d for d in sow.profile.departments))
        self.assertTrue(any("Service" in d for d in sow.profile.departments))
        self.assertTrue(any("DMS" in s for s in sow.profile.existing_systems))
        self.assertTrue(any("Payment" in t or "credit" in t.lower() for t in sow.profile.data_types))

    def test_hospital_profile(self):
        sow = sow_for("regional-hospital")
        self.assertEqual(sow.profile.industry_id, "healthcare")
        self.assertEqual(sow.profile.sensitivity, "Regulated")
        self.assertEqual(sow.profile.site_count, 3)
        self.assertTrue(any("PHI" in t for t in sow.profile.data_types))
        self.assertTrue(any("EHR" in s for s in sow.profile.existing_systems))
        self.assertTrue(any("HIPAA" in c for c in sow.compliance))

    def test_insurer_profile(self):
        sow = sow_for("mid-size-insurer")
        self.assertEqual(sow.profile.industry_id, "insurance")
        self.assertEqual(sow.profile.sensitivity, "Regulated")
        self.assertTrue(any("FNOL" in u or "Fraud" in u for u in sow.profile.use_cases))
        self.assertTrue(any("Claims" in s for s in sow.profile.existing_systems))

    def test_samples_are_distinct(self):
        industries = {sow_for(k).profile.industry_id for k in SAMPLES}
        self.assertEqual(industries, {"automotive", "healthcare", "insurance"})

    def test_markdown_has_all_sections(self):
        for key in SAMPLES:
            md = render_markdown(sow_for(key))
            for heading in REQUIRED_HEADINGS:
                self.assertIn(heading, md, f"{key} missing {heading!r}")
            self.assertIn("Spoofing", md)
            self.assertIn("Information disclosure", md)
            self.assertGreater(len(md), 4000)

    def test_sow_structure_complete(self):
        for key in SAMPLES:
            sow = sow_for(key)
            self.assertEqual(len(sow.weeks), 4)
            self.assertEqual(len(sow.threats), 6)
            self.assertGreaterEqual(len(sow.kpis), 3)
            self.assertGreaterEqual(len(sow.risks), 4)
            self.assertGreaterEqual(len(sow.staffing), 4)
            self.assertIn("flowchart", sow.architecture_mermaid)
            self.assertFalse(sow.llm_used)

    def test_deterministic(self):
        a = render_markdown(sow_for("auto-dealer"))
        b = render_markdown(sow_for("auto-dealer"))
        self.assertEqual(a, b)

    def test_plain_ask_without_optionals(self):
        profile = build_profile(
            "We're a 40-rooftop auto dealer group and want AI for our F&I and service departments"
        )
        self.assertEqual(profile.industry_id, "automotive")
        self.assertEqual(profile.site_count, 40)
        sow = generate_sow(profile, polish_summary=False)
        md = render_markdown(sow)
        self.assertIn("Week 1", md)
        self.assertIn("```mermaid", md)


    def test_no_duplicate_systems(self):
        for key in SAMPLES:
            systems = [s.lower() for s in sow_for(key).profile.existing_systems]
            self.assertEqual(systems, list(dict.fromkeys(systems)), key)

    def test_auto_dealer_does_not_treat_privacy_as_department(self):
        depts = sow_for("auto-dealer").profile.departments
        self.assertNotIn("Compliance / privacy", depts)

    def test_unknown_industry_falls_back_to_general(self):
        profile = build_profile("We want a chatbot for our office lunch orders.")
        self.assertEqual(profile.industry_id, "general")
        md = render_markdown(generate_sow(profile, polish_summary=False))
        self.assertIn("## 4. Four-week plan", md)


if __name__ == "__main__":
    unittest.main()
