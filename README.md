#  WorldForge AI – Your AI-Powered Fantasy Adventure

**WorldForge AI** is an interactive fantasy adventure game powered by Generative AI, RAG (Retrieval-Augmented Generation), and Agentic AI. Players can explore an evolving fantasy world, make decisions, fight enemies, collect rewards, and experience AI-generated storytelling.

##  Features

- **AI Story Generation:** Dynamic fantasy stories powered by Google Gemini.
- **Interactive Gameplay:** Make choices that influence your adventure.
- **Agentic AI:** AI agent analyzes player actions and determines the appropriate response.
- **AI Planning:** Generates action plans for story-related decisions.
- **RAG Integration:** Retrieves relevant fantasy world knowledge to maintain story consistency.
- **Player Management:** Track health, XP, levels, gold, and inventory.
- **Combat System:** Fight enemies, take damage, and earn rewards.
- **Game Memory:** Save and load game progress.
- **Custom UI:** Interactive fantasy-themed interface built with Streamlit.

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| Google Gemini API | AI story generation and agent reasoning |
| ChromaDB | Vector database for RAG |
| Sentence Transformers | Text embeddings |
| Pydantic | Data validation and structured outputs |
| Python-dotenv | Environment variable management |

##  AI Architecture

WorldForge AI combines multiple AI components:

1. **LLM:** Generates dynamic stories and responses.
2. **RAG:** Retrieves relevant information from the fantasy world's knowledge base.
3. **AI Agent:** Classifies player actions.
4. **AI Planner:** Creates multi-step action plans.
5. **Memory System:** Maintains player progress and important game events.

## 📂 Project Structure

```text
WorldForge-AI/
│
├── app/
│   ├── agents/
│   ├── llm/
│   ├── schemas/
│   └── services/
│
├── data/
│   ├── lore/
│   ├── saves/
│   └── chroma_db/
│
├── tests/
├── frontend.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WorldForge-AI.git
cd WorldForge-AI
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-flash-lite-latest
```

Never upload your API key to GitHub.

### 5. Launch the application

```bash
streamlit run frontend.py
```

##  Live Demo

**Try WorldForge AI:**  
https://worldforge-aigit-jizr5xg2yj7twljrzb3nat.streamlit.app

##  Future Improvements

- Persistent cloud-based player accounts and game saves.
- More fantasy worlds, quests, and enemies.
- Advanced NPC interactions.
- Multiplayer adventure mode.
- Expanded AI-driven gameplay.

##  Author

**Harshit Gupta**

B.Tech – Computer Science and Engineering (AI)



---

 If you find this project interesting, consider giving it a star on GitHub!

*Built with Python, Generative AI, RAG, and Agentic AI.*

## Evaluation and reproducibility

A repeatable evaluation suite is available in `eval/`. It includes 30 lore-grounded player actions, paired generation with retrieval enabled/disabled, a Gemini-based factual-grounding judge, a deterministic ten-case review sample, and planner three-step format checks.

Run the evaluation from the repository root:

```bash
export GEMINI_API_KEY="your_api_key"
python -m eval.run_generation
python -m eval.judge
python -m eval.sample_for_review
python -m eval.schema_validity
pytest -q tests/test_memory_roundtrip_eval.py
```

See [eval/README.md](eval/README.md) for metric definitions and limitations. Benchmark metrics are intentionally not pre-filled: report only results produced by running the scripts with a configured Gemini API key. The planner currently returns plain text, so its format metric is not native JSON-schema validation.
