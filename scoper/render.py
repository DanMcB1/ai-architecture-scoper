"""Render a StatementOfWork as a clean Markdown document."""

from __future__ import annotations

from scoper.engine import StatementOfWork


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _table(headers: list[str], rows: list[list[str]]) -> str:
    def cell(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ").strip()

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")
    return "\n".join(lines)


def render_markdown(sow: StatementOfWork) -> str:
    p = sow.profile
    parts: list[str] = [
        f"# {sow.title}",
        "",
        f"**Generated:** {sow.generated_on}  ",
        f"**Industry:** {p.industry_label}  ",
        f"**Data sensitivity:** {p.sensitivity}  ",
        f"**Size / footprint:** {p.size_hint}  ",
        f"**Existing systems:** {', '.join(p.existing_systems)}  ",
        f"**Team context:** {p.team_size}",
        "",
        f"> {sow.disclaimer}",
        "",
        "## 1. Problem summary",
        "",
        sow.problem_summary,
        "",
        "### Original customer ask",
        "",
        f"> {p.raw_ask}",
        "",
        "## 2. Assumptions",
        "",
        _bullets(sow.assumptions),
        "",
        "## 3. Scope",
        "",
        "### In scope",
        "",
        _bullets(sow.in_scope),
        "",
        "### Out of scope",
        "",
        _bullets(sow.out_of_scope),
        "",
        "## 4. Four-week plan",
        "",
    ]

    for week in sow.weeks:
        parts.extend(
            [
                f"### Week {week.week}: {week.title}",
                "",
                "**Goals**",
                "",
                _bullets(week.goals),
                "",
                "**Activities**",
                "",
                _bullets(week.activities),
                "",
                "**Deliverables**",
                "",
                _bullets(week.deliverables),
                "",
            ]
        )

    parts.extend(
        [
            "## 5. Proposed architecture",
            "",
            sow.architecture_narrative,
            "",
            "The diagram below is a Mermaid flowchart. GitHub, many Markdown "
            "previewers, and this app will render it. If your viewer does not, "
            "the text is still readable as a source list of systems and flows.",
            "",
            "```mermaid",
            sow.architecture_mermaid,
            "```",
            "",
            "## 6. STRIDE-style threat model",
            "",
            "This is a discussion starter for week 2, not a penetration test or "
            "a formal security assessment. STRIDE groups threats into Spoofing, "
            "Tampering, Repudiation, Information disclosure, Denial of service, "
            "and Elevation of privilege.",
            "",
            _table(
                ["STRIDE", "Threat", "Mitigation in this slice", "Priority"],
                [[t.stride, t.threat, t.mitigation, t.priority] for t in sow.threats],
            ),
            "",
            "### Compliance and control notes",
            "",
            _bullets(sow.compliance),
            "",
            f"_{p.sensitivity_reason}_",
            "",
            "## 7. Success metrics and KPIs",
            "",
            "Baselines and targets are proposals. Week 1 confirms the real "
            "numbers, or honestly records that a baseline does not yet exist.",
            "",
            _table(
                ["Metric", "Baseline", "Target", "How it will be measured"],
                [[k.metric, k.baseline, k.target, k.how_measured] for k in sow.kpis],
            ),
            "",
            "## 8. Risks",
            "",
            _table(
                ["Risk", "Likelihood", "Impact", "Mitigation"],
                [[r.risk, r.likelihood, r.impact, r.mitigation] for r in sow.risks],
            ),
            "",
            "## 9. Staffing",
            "",
            _table(
                ["Role", "Time over 4 weeks", "Responsibilities"],
                [[s.role, s.time, s.responsibilities] for s in sow.staffing],
            ),
            "",
            "## Appendix: Detected signals",
            "",
            "This SOW was produced by a deterministic rules engine. The table "
            "below shows the phrases and fields that drove industry, data, "
            "system, and size choices. Optional form fields can override a "
            "detection; those overrides are listed after the table.",
            "",
        ]
    )

    if p.signals:
        parts.append(
            _table(
                ["Category", "Label", "Evidence", "Weight"],
                [[s.category, s.label, s.evidence, str(s.weight)] for s in p.signals],
            )
        )
    else:
        parts.append("_No keyword signals fired. The general template was used._")

    parts.extend(["", ""])
    if p.overrides_used:
        parts.extend(["**Overrides and user-provided fields**", "", _bullets(p.overrides_used), ""])
    if sow.llm_used:
        parts.extend(
            [
                f"**LLM polish:** {sow.llm_note}",
                "",
            ]
        )
    elif sow.llm_note:
        parts.extend([f"**LLM polish:** not applied ({sow.llm_note})", ""])

    parts.extend(
        [
            "---",
            "",
            "_Automated Architecture Scoper — portfolio demo. Review with a human before use._",
            "",
        ]
    )
    return "\n".join(parts)
