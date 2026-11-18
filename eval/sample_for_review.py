"""Print ten deterministic examples for human review."""
import json
import random
from pathlib import Path
HERE = Path(__file__).resolve().parent

def main():
    scored = json.loads((HERE / "scored.json").read_text(encoding="utf-8"))
    outputs = {x["id"]: x for x in json.loads((HERE / "outputs.json").read_text(encoding="utf-8"))}
    for row in random.Random(42).sample(scored, min(10, len(scored))):
        print("\nCASE", row["id"], row["action"])
        print("FACTS:", row["ground_truth_facts"])
        for mode in ("rag", "no_rag"):
            print("\n", mode.upper(), json.dumps(outputs[row["id"]].get(mode), ensure_ascii=False, indent=2))
            print("JUDGE:", row.get(mode))

if __name__ == "__main__":
    main()
