# Demo script (~1 minute)

A talk track you can say out loud in an interview. Plain language. Practice it once or twice with the app open; you do not need to memorize it word for word.

**Setup:** `streamlit run app.py` is already running. You will click **Sample: Auto dealer group**, then **Generate 4-week Statement of Work**.

---

## The talk track

“In sales, the first thing I learned is you don’t jump to a product. You ask questions, you figure out what the customer actually needs, and only then do you put a plan in front of them. That’s the same job a Forward Deployed Engineer does on day one — except the plan has to cover systems, data, risks, and how you’ll measure success.

Customers almost never show up with a clean requirements doc. They show up with something like this: *we’re a 40-rooftop dealer group and we want AI for F&I and service.* That’s a feeling, not a project.

This demo takes that messy ask and turns it into a four-week Statement of Work: what’s in scope and what’s not, a week-by-week plan, a simple architecture, a STRIDE-style threat model because we’re dealing with credit data and deal jackets, KPIs, risks, and staffing. I can export the whole thing as Markdown.

I want to be honest: this is a demo, not production. Under the hood it is not calling a paid model. It’s a rules engine. It looks for keywords — ‘rooftop,’ ‘F&I,’ ‘DMS,’ ‘credit data’ — shows you the signals it used, and fills in a template. I built it that way on purpose. It runs offline with no API key, and I can explain every choice instead of hiding behind a black box.

The point isn’t that software can replace discovery. The point is that I know what good scoping looks like, because I’ve been on those calls.”

---

## Timing notes

Spoken at a normal pace, that is about 50–60 seconds. If you have a few extra seconds after you click Generate, point at two things on the screen:

1. **Detected signals** — “Here’s why it knew this was auto retail with regulated data.”
2. **Out of scope** — “And it says up front we’re not rolling this out to all 40 rooftops in four weeks. That’s the kind of expectation-setting I’d do on a real call.”

Then stop and let them ask questions.

## If they ask a follow-up

- **“Why not just use ChatGPT?”**  
  “I can optionally point this at a local model to polish the summary, but I didn’t want the demo to depend on a key or a network. For an interview, I’d rather show the structure of a good SOW than a fluent paragraph I can’t defend.”

- **“What would you do on a real engagement?”**  
  “Sit with F&I managers and service advisors, not just the director. Confirm what’s in the DMS, what data I’m allowed to touch, and whether a baseline for PVR or no-shows even exists. This tool would be a first draft I’d mark up after those conversations.”

- **“Why STRIDE?”**  
  “It’s a simple way to walk a customer through spoofing, leaking data, and privilege issues without pretending I’ve done a formal security assessment. On a dealer group, the question I care about most is: does this assistant ever show credit data to someone who couldn’t see it in the DMS?”

- **“Can I see another industry?”**  
  Click **Regional hospital** or **Mid-size insurer**, generate again, and point out that the pack changes — HIPAA and no write-back to the legal record for the hospital; no automated claim denial and explainable ‘review suggested’ flags for the insurer.
