"""Run paired RAG/no-retrieval generations for the fixed lore evaluation set."""
import json
import time
from pathlib import Path
from app.services.story_engine import StoryEngine

HERE = Path(__file__).resolve().parent

def main():
    cases = json.loads((HERE / "eval_set.json").read_text(encoding="utf-8"))
    engine = StoryEngine()
    results = []
    for case in cases:
        row = {k: case[k] for k in ("id", "topic", "action", "ground_truth_facts")}
        for enabled, label in ((True, "rag"), (False, "no_rag")):
            started = time.perf_counter()
            try:
                result = engine.process_action(
                    "Evaluation Player", "Aethelgard",
                    "The player is exploring Aethelgard.",
                    "The adventure has just begun.", case["action"],
                    use_rag=enabled,
                )
                row[label] = result.model_dump()
            except Exception as exc:
                row[label] = {"error": f"{type(exc).__name__}: {exc}"}
            row[label + "_latency_seconds"] = round(time.perf_counter() - started, 3)
        results.append(row)
        print(f"Generated {case['id']}/{len(cases)}")
    (HERE / "outputs.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(results)} paired cases to eval/outputs.json")

if __name__ == "__main__":
    main()
