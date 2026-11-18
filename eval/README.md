# WorldForge AI evaluation

Run from the repository root after installing requirements and setting `GEMINI_API_KEY`.

```bash
export GEMINI_API_KEY="..."
export GEMINI_MODEL="gemini-flash-lite-latest"  # optional; defaults to app model
python -m eval.run_generation
python -m eval.judge
python -m eval.sample_for_review
python -m eval.schema_validity
pytest -q tests/test_memory_roundtrip_eval.py
```

The fixed 30-case dataset is grounded in `data/lore/world_lore.txt`. The generation runner compares the same story prompt with and without retrieved ChromaDB lore. The Gemini judge measures contradiction-free outputs and whether at least one supplied fact is used. The sample script prints ten reproducible examples for manual review.

The planner currently returns plain text. Its evaluation checks compliance with an exact three-numbered-step format and retries once; this is not native Pydantic/JSON-schema enforcement.

The persistence test round-trips 25 deterministic randomized player/game states, including a sample story-history payload. The current Streamlit save flow does not populate a persistent turn-history field, so the test verifies the generic JSON game_state round-trip contract, not existing UI history tracking.

Do not publish benchmark percentages until these scripts have been run with a valid API key. Preserve raw JSON outputs, model name, date, and sample size with any reported metric.
