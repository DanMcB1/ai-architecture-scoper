# Automated Architecture Scoper

**Portfolio project #11 of 12** from [@suraj_sharma14's FDE project list](https://x.com/suraj_sharma14/status/2125197762752806998).

A small, offline demo that turns a vague customer ask — *“We're a 40-rooftop auto dealer group and want AI for our F&I and service departments”* — into a **4-week Statement of Work**.

This is a **portfolio demo**, not production software. It does not connect to real customer systems, and the document it writes is a starting point for a human to review, not a binding proposal.

Built for **Daniel McBrearty** as part of a Forward Deployed Engineer / solutions engineer portfolio.

## Why this matters for FDE work

The first thing a Forward Deployed Engineer does with a customer is not “stand up a model.” It is **scoping**.

A customer rarely arrives with a clean requirements document. They arrive with a feeling: *we want AI in F&I and service.* The FDE’s job on that first engagement is the same job a good salesperson already knows from discovery calls:

- listen to the messy ask
- name the real workflow and the data involved
- say what is in scope and what is not
- put a plan, risks, and success measures on one page
- leave the customer with something they can say yes or no to

This tool is a practice version of that first artifact. It is useful in interviews because you can walk through the *thinking* — industry, sensitive data, existing systems, a thin slice, a threat model — without hiding behind a black-box model.

## Quick start

You need Python 3.10+ (3.13 is fine). No account, no cloud key, no internet after the packages are installed.

```bash
git clone https://github.com/DanMcB1/ai-architecture-scoper.git
cd ai-architecture-scoper
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Or: `./run.sh`

The app opens in your browser (usually [http://localhost:8501](http://localhost:8501)).

- Click one of the three samples (**Auto dealer group**, **Regional hospital**, **Mid-size insurer**), or paste your own ask.
- Optionally fill in industry, data sensitivity, team size, and existing systems.
- Click **Generate 4-week Statement of Work**.
- Review the tabs, then **Download Markdown**.

You can also generate a document from the command line, which is how the files in `examples/` were produced:

```bash
source .venv/bin/activate
python -m scoper --all-samples --outdir examples --no-llm
python -m scoper --sample auto-dealer --out examples/auto-dealer-group.md
python -m scoper --ask "We want AI for claims intake" --industry insurance
```

That last command should describe claims / FNOL work, not a hospital “Patient intake” department. Department and use-case rules are scoped to the detected or chosen industry.


To run the checks:

```bash
python -m unittest discover -s tests
```

## What’s in a generated SOW

Every document includes:

1. **Problem summary** — what the customer asked for, in plain language
2. **Assumptions**
3. **In scope / out of scope**
4. **A week-by-week plan** with goals, activities, and deliverables
5. **A proposed architecture** (narrative + a Mermaid diagram)
6. **A STRIDE-style threat model table** (a discussion starter, not an audit)
7. **Success metrics / KPIs** with proposed baselines and targets
8. **Risks** and mitigations
9. **Staffing** for the four weeks
10. An **appendix of detected signals** so you can see *why* the engine made its choices

The three built-in samples are saved in:

- [`examples/auto-dealer-group.md`](examples/auto-dealer-group.md)
- [`examples/regional-hospital.md`](examples/regional-hospital.md)
- [`examples/mid-size-insurer.md`](examples/mid-size-insurer.md)

## How it works

There is **no paid API** in the default path. The app is a deterministic **rules and template engine**.

1. **Detect.** `scoper/detect.py` scans the ask (and any optional form fields) for keywords: industry (dealer / hospital / insurer), industry-scoped departments and use cases (F&I and Service for dealers, patient intake for hospitals, claims/SIU for insurers — not shared across industries), data types (PII, PHI, payments, claims), systems (DMS, CRM, EHR, policy admin), and size clues (“40-rooftop”, “three campuses”, “mid-size”). Each match is stored as evidence. A bare word like “customer” or “service” is not enough to flag PII or the auto Service department.
2. **Fill a pack.** `scoper/packs.py` holds industry-specific language, week plans, KPIs, threats, and staffing. The engine fills in the detected systems, departments, and sensitivity.
3. **Render.** `scoper/render.py` writes Markdown. The Streamlit app in `app.py` shows the same content in tabs and offers a file download.

The same inputs always produce the same output. That makes the tool easy to test and easy to talk through: you can open the **Detected signals** section and point at the phrases that fired.

Optional form fields **override** a detection when you need to (for example, forcing the industry if the ask is ambiguous).

### Optional LLM polish (off by default)

If you later want a local model (for example [Ollama](https://ollama.com)) or any OpenAI-compatible endpoint to tighten the **problem summary only**, set environment variables and restart the app. If the call fails, the rules-engine text is kept.

```bash
export OPENAI_API_KEY=ollama
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_MODEL=llama3
streamlit run app.py
```

The week plan, threat model, KPIs, and staffing are never generated by a model in this demo. See `.env.example`.

## Honest limitations

- This is a **demo**. It cannot see the customer’s real DMS, EHR, or claims system.
- Keyword rules **miss nuance**. A “hospital cafeteria” business is no longer treated as clinical / PHI, but unusual wording can still land in the wrong pack.
- Templates are **starting points**. A real SOW is written after sitting with users, not after a text box.
- The threat model is a **STRIDE discussion table**, not a penetration test, architecture review, or compliance certification.
- KPI baselines are **proposed**. Week 1 of a real engagement is where you find out whether the baseline even exists.
- Mermaid diagrams render in GitHub and many Markdown previewers; some editors show only the source. The app also draws a simple offline diagram that does not need the internet.
- Optional LLM support is a convenience, not the product. The default path has no key and no network call.

## What a production version would add

- A real discovery questionnaire and workshop notes, not just a pasted paragraph
- Connectors or safe data-room intake from the actual systems of record
- Human-in-the-loop review and redlines before anything is sent to a customer
- A proper threat-modeling workshop (and, where needed, a formal security review)
- Customer-specific constraints: contracts, BAAs, fair-lending, model-risk, union or clinical safety rules
- Estimation that uses actual access timelines, not a generic four-week skeleton
- Versioning, audit history, and collaboration for a delivery team
- Evaluation of any prototype against held-out examples, not just a demo script

## Project layout

```
ai-architecture-scoper/
  app.py                 Streamlit UI
  run.sh                 One-command launcher
  requirements.txt       The only dependency: streamlit
  README.md
  LICENSE                MIT, Copyright (c) 2026 Daniel McBrearty
  DEMO_SCRIPT.md         ~1-minute talk track for interviews
  scoper/                Rules engine, packs, Markdown renderer, optional LLM
  examples/              Generated SOWs for the three samples
  screenshots/           App screenshot (if present)
  tests/                 Happy-path samples plus cross-industry keyword-bleed checks
```

## For interviewers

If you only have a minute, start the app, click **Sample: Auto dealer group**, generate the SOW, and walk through signals → scope → week plan → threat model. The talk track is in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).

Daniel’s background is car sales, F&I, and auto software sales (Dealr.cloud), not professional software engineering. This project is meant to show **scoping judgment** and an honest demo, not production-grade platform engineering.

## License

This project is released under the [MIT License](LICENSE). Copyright (c) 2026 Daniel McBrearty.
