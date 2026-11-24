"""Keyword-bleed and default-name checks beyond the three happy-path samples."""

from __future__ import annotations

import unittest

from scoper.detect import build_profile
from scoper.engine import generate_sow
from scoper.render import render_markdown


def departments(profile) -> list[str]:
    return profile.departments


def use_cases(profile) -> list[str]:
    return profile.use_cases


def data_types(profile) -> list[str]:
    return profile.data_types


class CrossIndustryBleedTests(unittest.TestCase):
    def test_claims_intake_is_insurance_not_patient_intake(self):
        profile = build_profile(
            "We want AI for claims intake",
            industry="insurance",
        )
        self.assertEqual(profile.industry_id, "insurance")
        self.assertTrue(any("Claims" in d for d in departments(profile)))
        self.assertTrue(any("FNOL" in u or "claims intake" in u.lower() for u in use_cases(profile)))
        self.assertFalse(any("Patient intake" in d for d in departments(profile)))
        self.assertFalse(any("Patient intake" in u for u in use_cases(profile)))
        md = render_markdown(generate_sow(profile, polish_summary=False))
        self.assertNotIn("Patient intake", md)
        self.assertNotIn("Customer engagement", md)

    def test_claims_intake_without_override_detects_insurance(self):
        # "intake" alone used to score as healthcare and win a tie.
        profile = build_profile("We want AI for claims intake")
        self.assertEqual(profile.industry_id, "insurance")
        self.assertFalse(any("Patient intake" in d for d in departments(profile)))
        self.assertTrue(any("FNOL" in u or "claims intake" in u.lower() for u in use_cases(profile)))

    def test_patient_intake_still_works_for_healthcare(self):
        profile = build_profile(
            "We want AI to speed up patient intake and front-desk admissions.",
            industry="healthcare",
        )
        self.assertEqual(profile.industry_id, "healthcare")
        self.assertTrue(any("Patient intake" in d for d in departments(profile)))
        self.assertTrue(any("Patient intake" in u for u in use_cases(profile)))


class CustomerServiceTests(unittest.TestCase):
    def test_customer_service_is_not_auto_service_department(self):
        profile = build_profile(
            "We're a mid-size insurer and want AI to help customer service answer policy questions."
        )
        self.assertEqual(profile.industry_id, "insurance")
        self.assertNotIn("Service", departments(profile))
        self.assertFalse(any(d == "Service" or d.startswith("Service ") for d in departments(profile)))

    def test_service_department_still_detected_for_dealers(self):
        profile = build_profile(
            "We're a dealer group and want AI for our F&I and service departments."
        )
        self.assertEqual(profile.industry_id, "automotive")
        self.assertTrue(any(d == "Service" for d in departments(profile)))
        self.assertTrue(any("F&I" in d for d in departments(profile)))


class GenericCustomerMentionTests(unittest.TestCase):
    def test_generic_customers_mention_does_not_flag_pii(self):
        profile = build_profile("We want a chatbot that answers questions for our customers.")
        self.assertEqual(profile.industry_id, "general")
        self.assertFalse(any(t.startswith("PII") for t in data_types(profile)))

    def test_customer_data_phrase_still_flags_pii(self):
        profile = build_profile(
            "We want a chatbot, but it must not leak customer data."
        )
        self.assertTrue(any(t.startswith("PII") for t in data_types(profile)))


class DefaultNameTests(unittest.TestCase):
    def test_default_name_is_your_organization(self):
        profile = build_profile("We want AI for claims intake", industry="insurance")
        self.assertEqual(profile.customer_name, "Your organization")
        md = render_markdown(generate_sow(profile, polish_summary=False))
        self.assertIn("Your organization is a mid-size insurance organization", md)
        self.assertNotIn("Customer engagement", md)

    def test_explicit_name_is_kept(self):
        profile = build_profile(
            "We want AI for claims intake",
            industry="insurance",
            customer_name="Northbridge P&C",
        )
        self.assertEqual(profile.customer_name, "Northbridge P&C")


class EdgeAskTests(unittest.TestCase):
    def test_empty_ask_is_still_a_document(self):
        profile = build_profile("")
        self.assertEqual(profile.industry_id, "general")
        self.assertEqual(profile.customer_name, "Your organization")
        md = render_markdown(generate_sow(profile, polish_summary=False))
        self.assertIn("## 4. Four-week plan", md)

    def test_industry_override_beats_dealer_keywords(self):
        profile = build_profile(
            "We run a DMS and have an F&I desk, but we are actually a carrier.",
            industry="insurance",
        )
        self.assertEqual(profile.industry_id, "insurance")
        self.assertFalse(any(d == "Service" for d in departments(profile)))
        self.assertFalse(any("F&I" in d for d in departments(profile)))

    def test_hospital_compliance_still_detected(self):
        profile = build_profile(
            "A hospital wants AI for charting. The compliance team is strict about HIPAA and PHI."
        )
        self.assertEqual(profile.industry_id, "healthcare")
        self.assertTrue(any("Compliance" in d for d in departments(profile)))
        self.assertTrue(any("PHI" in t for t in data_types(profile)))

    def test_hospital_cafeteria_is_not_clinical_phi(self):
        profile = build_profile("We want AI in a hospital cafeteria business.")
        self.assertNotEqual(profile.industry_id, "healthcare")
        self.assertFalse(any("PHI" in t for t in data_types(profile)))
        self.assertFalse(any("Clinical" in d for d in departments(profile)))


if __name__ == "__main__":
    unittest.main()
