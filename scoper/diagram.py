"""Local HTML architecture diagram — no CDN, works fully offline."""

from __future__ import annotations

from html import escape

from scoper.detect import ScopeProfile


def architecture_html(profile: ScopeProfile) -> str:
    users = profile.departments[:4] or ["Business users"]
    systems = profile.existing_systems[:5]
    use_case = profile.use_cases[0] if profile.use_cases else "AI assistant"

    def chips(items: list[str]) -> str:
        return "".join(f'<div class="chip">{escape(item)}</div>' for item in items)

    return f"""
<style>
  .arch {{
    font-family: "Source Sans 3", "Segoe UI", sans-serif;
    background: #f3f5f8;
    border: 1px solid #d5dbe3;
    border-radius: 12px;
    padding: 18px 16px 14px;
    color: #1c2430;
  }}
  .arch-row {{
    display: flex;
    gap: 12px;
    align-items: stretch;
    justify-content: space-between;
    flex-wrap: wrap;
  }}
  .arch-col {{
    flex: 1 1 160px;
    background: #fff;
    border: 1px solid #cfd6e0;
    border-radius: 10px;
    padding: 12px;
    min-width: 140px;
  }}
  .arch-col h4 {{
    margin: 0 0 10px;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4a5a70;
    font-weight: 700;
  }}
  .chip {{
    background: #e8eef6;
    border: 1px solid #c5d0e0;
    border-radius: 6px;
    padding: 6px 8px;
    margin: 0 0 6px;
    font-size: 13px;
    line-height: 1.3;
  }}
  .arch-col.slice {{
    background: #1e3a5f;
    border-color: #1e3a5f;
    color: #fff;
    flex: 1.4 1 220px;
  }}
  .arch-col.slice h4 {{ color: #c8d7ea; }}
  .arch-col.slice .chip {{
    background: #2a4d77;
    border-color: #3b628f;
    color: #fff;
  }}
  .flow {{
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4a5a70;
    font-size: 22px;
    flex: 0 0 16px;
  }}
  .caption {{
    margin: 10px 0 0;
    font-size: 12px;
    color: #4a5a70;
  }}
</style>
<div class="arch">
  <div class="arch-row">
    <div class="arch-col">
      <h4>Users</h4>
      {chips(users)}
    </div>
    <div class="arch-col">
      <h4>Existing systems</h4>
      {chips(systems)}
    </div>
    <div class="arch-col slice">
      <h4>4-week thin slice</h4>
      {chips(["Read-only data connector", "Access control and audit log", use_case])}
    </div>
  </div>
  <p class="caption">
    Flow: existing systems &rarr; read-only connector &rarr; access control / audit log
    &rarr; assistant. The assistant does not replace the systems of record, and this
    engagement does not write back into them.
  </p>
</div>
"""
