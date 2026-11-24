"""Automated Architecture Scoper — Streamlit UI.

Run with:  streamlit run app.py
Works fully offline. No API key required.
"""

from __future__ import annotations

from datetime import date

import streamlit as st
import streamlit.components.v1 as components

from scoper.detect import build_profile
from scoper.diagram import architecture_html
from scoper.engine import generate_sow
from scoper.llm import llm_config
from scoper.render import render_markdown
from scoper.samples import SAMPLES

st.set_page_config(
    page_title="Automated Architecture Scoper",
    page_icon="blueprint",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
  .block-container { padding-top: 1.4rem; max-width: 1200px; }
  .demo-banner {
    background: #fff6e5;
    border: 1px solid #e6d2a8;
    color: #5a4500;
    padding: 0.7rem 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    margin-bottom: 0.8rem;
  }
  .signal-pill {
    display: inline-block;
    background: #e8eef6;
    border: 1px solid #c5d0e0;
    border-radius: 999px;
    padding: 2px 10px;
    margin: 0 6px 6px 0;
    font-size: 0.85rem;
  }
  h1 { letter-spacing: -0.02em; }
  div[data-testid="stMetric"] {
    background: #f3f5f8;
    border: 1px solid #d5dbe3;
    border-radius: 10px;
    padding: 8px 12px;
  }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

INDUSTRY_OPTIONS = [
    "Auto-detect from the ask",
    "Automotive retail / dealer group",
    "Healthcare / hospital",
    "Insurance (P&C)",
    "General / other",
]
SENSITIVITY_OPTIONS = ["Auto-detect", "Low", "Medium", "High", "Regulated"]

SAMPLE_FILENAMES = {
    "auto-dealer": "sow-auto-dealer-group.md",
    "regional-hospital": "sow-regional-hospital.md",
    "mid-size-insurer": "sow-mid-size-insurer.md",
}


def _init_state() -> None:
    defaults = {
        "customer_name": "",
        "ask": "",
        "industry": INDUSTRY_OPTIONS[0],
        "data_sensitivity": SENSITIVITY_OPTIONS[0],
        "team_size": "",
        "existing_systems": "",
        "sow_md": None,
        "sow": None,
        "loaded_sample": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_sample(key: str) -> None:
    sample = SAMPLES[key]
    st.session_state.customer_name = sample["customer_name"]
    st.session_state.ask = sample["ask"]
    st.session_state.industry = sample["industry"]
    st.session_state.data_sensitivity = sample["data_sensitivity"]
    st.session_state.team_size = sample["team_size"]
    st.session_state.existing_systems = sample["existing_systems"]
    st.session_state.loaded_sample = key
    st.session_state.sow_md = None
    st.session_state.sow = None


def generate() -> None:
    ask = st.session_state.ask.strip()
    if not ask:
        st.session_state.sow = None
        st.session_state.sow_md = None
        st.warning("Paste a customer ask, or click one of the three sample buttons.")
        return
    industry = st.session_state.industry
    if industry == "Auto-detect from the ask":
        industry = ""
    sensitivity = st.session_state.data_sensitivity
    if sensitivity == "Auto-detect":
        sensitivity = ""
    profile = build_profile(
        ask=ask,
        industry=industry,
        data_sensitivity=sensitivity,
        team_size=st.session_state.team_size,
        existing_systems=st.session_state.existing_systems,
        customer_name=st.session_state.customer_name,
    )
    sow = generate_sow(profile)
    st.session_state.sow = sow
    st.session_state.sow_md = render_markdown(sow)


_init_state()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("How this works")
    st.markdown(
        """
This is a **rules engine**, not a hidden model.

1. You paste a vague customer ask.
2. The app looks for keywords (industry, F&I, PHI, claims, DMS, EHR, and so on) and records the evidence.
3. It fills a 4-week Statement of Work template: scope, plan, architecture, STRIDE threats, KPIs, risks, and staffing.
4. You can export the result as Markdown.

The same inputs always produce the same output. That is on purpose — it is easy to explain in an interview, and it runs with **no API key and no internet**.
        """
    )
    st.markdown("---")
    cfg = llm_config()
    if cfg:
        st.success(
            f"Optional LLM polish is on ({cfg['model']} at {cfg['base']}). "
            "Only the problem summary may be rewritten. Everything else stays rules-based."
        )
    else:
        st.info("Optional LLM is off. No `OPENAI_API_KEY` is set, which is the default.")
    st.markdown(
        """
To try a local model later, see the README
(`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`).
        """
    )
    st.markdown("---")
    st.caption("Portfolio demo for Daniel McBrearty · Forward Deployed / Solutions Engineer")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Automated Architecture Scoper")
st.caption(
    "Turn a vague “we want AI” ask into a 4-week Statement of Work. "
    "A portfolio demo — not production software."
)
st.markdown(
    '<div class="demo-banner">'
    "<strong>Honest label:</strong> this tool is a demo for interviews and practice. "
    "It does not inspect real systems, it does not replace a discovery call, "
    "and the SOW it writes is a starting point for a human to review — "
    "not a binding proposal or a security assessment."
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
st.subheader("1. Customer ask")
st.markdown("Start from a sample, or paste your own. Optional fields just sharpen the result.")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Sample: Auto dealer group", use_container_width=True):
        load_sample("auto-dealer")
        st.rerun()
with c2:
    if st.button("Sample: Regional hospital", use_container_width=True):
        load_sample("regional-hospital")
        st.rerun()
with c3:
    if st.button("Sample: Mid-size insurer", use_container_width=True):
        load_sample("mid-size-insurer")
        st.rerun()

st.text_input("Customer / project name (optional)", key="customer_name")
st.text_area(
    "What did the customer say they want?",
    key="ask",
    height=150,
    placeholder="Example: We're a 40-rooftop auto dealer group and want AI for our F&I and service departments…",
)

with st.expander("Optional inputs (industry, data sensitivity, team, systems)", expanded=False):
    o1, o2 = st.columns(2)
    with o1:
        st.selectbox("Industry", INDUSTRY_OPTIONS, key="industry")
        st.text_input("Team size or IT context (optional)", key="team_size")
    with o2:
        st.selectbox("Data sensitivity", SENSITIVITY_OPTIONS, key="data_sensitivity")
        st.text_input(
            "Existing systems (optional, comma-separated)",
            key="existing_systems",
            placeholder="DMS, CRM, EHR, claims system…",
        )

generate_clicked = st.button("Generate 4-week Statement of Work", type="primary")
if generate_clicked:
    generate()

sow = st.session_state.sow
if sow is None:
    st.markdown(
        "Generate an SOW to see the problem summary, scope, week-by-week plan, "
        "architecture, threat model, KPIs, risks, and staffing — plus a Markdown download."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
p = sow.profile
st.subheader("2. Detected signals")
st.markdown(
    "These are the phrases the rules engine used. If something looks wrong, "
    "change the ask or the optional fields and generate again."
)
m1, m2, m3, m4 = st.columns(4)
short_industry = {
        "automotive": "Automotive",
        "healthcare": "Healthcare",
        "insurance": "Insurance",
    }.get(p.industry_id, "General")
m1.metric("Industry", short_industry)
m2.metric("Sensitivity", p.sensitivity)
m3.metric("Sites (if found)", str(p.site_count) if p.site_count else "Not stated")
m4.metric("Systems tagged", str(len(p.existing_systems)))

pill_bits = []
for signal in p.signals[:16]:
    pill_bits.append(f'<span class="signal-pill">{signal.category}: {signal.label}</span>')
st.markdown("".join(pill_bits) or "_No keyword signals._", unsafe_allow_html=True)
if p.overrides_used:
    st.caption("Overrides: " + "; ".join(p.overrides_used))
if sow.llm_used:
    st.caption(sow.llm_note)
elif sow.llm_note and "No OPENAI_API_KEY" not in sow.llm_note:
    st.caption(sow.llm_note)

st.subheader("3. Statement of Work")
st.markdown(f"**{sow.title}**  \nGenerated {sow.generated_on}")

md = st.session_state.sow_md
sample_key = st.session_state.loaded_sample
download_name = SAMPLE_FILENAMES.get(
    sample_key,
    f"sow-{date.today().isoformat()}.md",
)
st.download_button(
    "Download Markdown",
    data=md.encode("utf-8"),
    file_name=download_name,
    mime="text/markdown",
    type="primary",
)

tab_names = [
    "Summary & scope",
    "4-week plan",
    "Architecture",
    "Threat model",
    "KPIs, risks & staffing",
    "Full Markdown",
]
t_summary, t_plan, t_arch, t_threat, t_kpis, t_md = st.tabs(tab_names)

with t_summary:
    st.markdown("#### Problem summary")
    st.write(sow.problem_summary)
    st.markdown("#### Assumptions")
    for item in sow.assumptions:
        st.markdown(f"- {item}")
    left, right = st.columns(2)
    with left:
        st.markdown("#### In scope")
        for item in sow.in_scope:
            st.markdown(f"- {item}")
    with right:
        st.markdown("#### Out of scope")
        for item in sow.out_of_scope:
            st.markdown(f"- {item}")

with t_plan:
    for week in sow.weeks:
        st.markdown(f"#### Week {week.week}: {week.title}")
        st.markdown("**Goals**")
        for item in week.goals:
            st.markdown(f"- {item}")
        st.markdown("**Activities**")
        for item in week.activities:
            st.markdown(f"- {item}")
        st.markdown("**Deliverables**")
        for item in week.deliverables:
            st.markdown(f"- {item}")

with t_arch:
    st.write(sow.architecture_narrative)
    components.html(architecture_html(p), height=320, scrolling=False)
    st.markdown("##### Mermaid source (also included in the Markdown export)")
    st.code(sow.architecture_mermaid, language="text")

with t_threat:
    st.caption(
        "A STRIDE-style discussion starter — not a penetration test or a formal assessment."
    )
    st.dataframe(
        [
            {
                "STRIDE": t.stride,
                "Threat": t.threat,
                "Mitigation in this slice": t.mitigation,
                "Priority": t.priority,
            }
            for t in sow.threats
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("**Compliance and control notes**")
    for item in sow.compliance:
        st.markdown(f"- {item}")
    st.caption(p.sensitivity_reason)

with t_kpis:
    st.markdown("#### Success metrics")
    st.dataframe(
        [
            {
                "Metric": k.metric,
                "Baseline": k.baseline,
                "Target": k.target,
                "How measured": k.how_measured,
            }
            for k in sow.kpis
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### Risks")
    st.dataframe(
        [
            {
                "Risk": r.risk,
                "Likelihood": r.likelihood,
                "Impact": r.impact,
                "Mitigation": r.mitigation,
            }
            for r in sow.risks
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("#### Staffing")
    st.dataframe(
        [
            {
                "Role": s.role,
                "Time over 4 weeks": s.time,
                "Responsibilities": s.responsibilities,
            }
            for s in sow.staffing
        ],
        use_container_width=True,
        hide_index=True,
    )

with t_md:
    st.download_button(
        "Download Markdown file",
        data=md.encode("utf-8"),
        file_name=download_name,
        mime="text/markdown",
        key="download_md_tab",
    )
    st.code(md, language="markdown")
