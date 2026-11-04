from app.services.lore_manager import LoreManager

lore = LoreManager()

count = lore.load_lore()
print(f"\nLore documents loaded: {count}")

question = "Who knows the history of Aethelgard?"

results = lore.search_lore(question)

print("\nRelevant knowledge:")
for result in results:
    print("-", result)