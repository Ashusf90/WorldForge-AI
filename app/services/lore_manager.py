import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path


class LoreManager:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="world_lore",
            embedding_function=embedding_function
        )

    def load_lore(self):
        file_path = Path("data/lore/world_lore.txt")
        text = file_path.read_text(encoding="utf-8")

        chunks = [
            chunk.strip()
            for chunk in text.split("\n\n")
            if chunk.strip()
        ]

        self.collection.upsert(
            documents=chunks,
            ids=[f"lore-{i}" for i in range(len(chunks))]
        )

        return len(chunks)

    def search_lore(self, question):
        results = self.collection.query(
            query_texts=[question],
            n_results=3
        )

        return results["documents"][0]