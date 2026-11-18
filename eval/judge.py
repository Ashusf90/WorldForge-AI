"""Gemini judge for factual grounding and contradiction checks."""
import json
import os
import re
from pathlib import Path
from google import genai
from app.config import GEMINI_MODEL

HERE = Path(__file__).resolve().parent

def parse_json(text):
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", (text or "").strip(), flags=re.I)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("Judge did not return a JSON object")
    return json.loads(text[start:end + 1])

def score(client, action, facts, story):
    prompt = f"""Judge this generated fantasy story against canon facts.
A contradiction is an explicit conflict with any supplied fact.
A fact is used only if at least one supplied fact is accurately reflected.
Do not infer unsupported facts. Return JSON only:
{{"contradiction_free": true, "correct_fact_used": true, "evidence": "short explanation"}}
PLAYER ACTION: {action}
CANON FACTS: {json.dumps(facts)}
STORY: {json.dumps(story, ensure_ascii=False)}
"""
    last = None
    for attempt in range(2):
        try:
            response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            data = parse_json(response.text)
            if not isinstance(data.get("contradiction_free"), bool) or not isinstance(data.get("correct_fact_used"), bool):
                raise ValueError("Judge booleans missing or invalid")
            return data
        except Exception as exc:
            last = exc
            prompt += "\nYour prior answer was invalid. Return a valid JSON object only."
    return {"error": f"{type(last).__name__}: {last}"}

def main():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY before running the judge.")
    rows = json.loads((HERE / "outputs.json").read_text(encoding="utf-8"))
    client = genai.Client(api_key=key)
    scored = []
    for i, row in enumerate(rows, 1):
        out = {k: row[k] for k in ("id", "topic", "action", "ground_truth_facts")}
        for mode in ("rag", "no_rag"):
            item = row.get(mode, {})
            out[mode] = {"error": item["error"]} if "error" in item else score(client, row["action"], row["ground_truth_facts"], item)
        scored.append(out)
        print(f"Judged {i}/{len(rows)}")
    (HERE / "scored.json").write_text(json.dumps(scored, indent=2, ensure_ascii=False), encoding="utf-8")
    for mode in ("rag", "no_rag"):
        valid = [x[mode] for x in scored if "error" not in x[mode]]
        if valid:
            cf = sum(x["contradiction_free"] for x in valid)
            grounded = sum(x["correct_fact_used"] for x in valid)
            print(f"{mode}: judged={len(valid)}, contradiction-free={cf}/{len(valid)} ({cf/len(valid):.1%}), fact-grounded={grounded}/{len(valid)} ({grounded/len(valid):.1%})")
        else:
            print(f"{mode}: no valid judge results")

if __name__ == "__main__":
    main()
