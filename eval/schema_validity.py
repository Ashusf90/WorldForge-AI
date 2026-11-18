"""Measure three-step planner-format adherence; planner is plain text, not Pydantic."""
import json
import os
import re
from pathlib import Path
from app.agents.planner import Planner

ACTIONS = [
    "Investigate the Whispering Forest.", "Prepare for a Shadow Beast encounter.",
    "Find the Crystal Sword.", "Ask Elara about King Arveth.",
    "Explore the Sunken Citadel.", "Recover after a dangerous journey.",
    "Search cursed ruins for clues.", "Travel from Silverkeep to the forest.",
    "Learn why trees remember conversations.", "Protect myself from dark creatures.",
] * 5
HERE = Path(__file__).resolve().parent

def valid(text):
    lines = [x.strip() for x in str(text).splitlines() if x.strip()]
    nums = [re.match(r"^([1-3])[.)]\s+\S", x) for x in lines]
    nums = [x.group(1) for x in nums if x]
    return nums == ["1", "2", "3"]

def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("Set GEMINI_API_KEY before running planner evaluation.")
    planner = Planner()
    rows = []
    for i, action in enumerate(ACTIONS, 1):
        try:
            first = planner.create_plan(action, {"health": 100, "location": "Silverkeep"}, [])
            if valid(first):
                status = "first_try"
            else:
                retry = planner.ai.generate("Rewrite as exactly three numbered steps 1. 2. 3., no introduction:\n" + str(first))
                status = "retry_pass" if valid(retry) else "failed"
        except Exception as exc:
            status = "failed"
        rows.append({"action": action, "status": status})
        print(f"Checked {i}/{len(ACTIONS)}")
    first = sum(x["status"] == "first_try" for x in rows)
    retry = sum(x["status"] == "retry_pass" for x in rows)
    report = {"total": len(rows), "first_try": first, "retry_pass": retry,
              "failed": len(rows)-first-retry, "first_try_rate": first/len(rows),
              "final_valid_rate": (first+retry)/len(rows), "results": rows}
    (HERE / "schema_validity.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "results"}, indent=2))

if __name__ == "__main__":
    main()
