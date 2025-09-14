# cli.py
import os
import google.generativeai as genai
from embed_store import EmbedStore
import argparse, textwrap

GEMINI_ENV = "AIzaSyA_xJt7wWCa5lGx483Ka-Gqri4zfrRH9Z0"

def build_prompt(query, retrieved):
    context = "\n\n---\n".join([f"Recipe: {text}" for _, text, _ in retrieved])
    prompt = f"""You are a recipe assistant. Use only the context to answer concisely.

Context:
{context}

Query: {query}

Answer concisely with recipe suggestions:"""
    return prompt

def ask_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') and response.text else ""

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="create store from sample recipes")
    parser.add_argument("--query", type=str, help="ingredient or dish name")
    args = parser.parse_args()

    store = EmbedStore()
    if args.init:
        import json
        with open("sample_recipes.json") as f:
            items = json.load(f)
        store.bulk_add([(it["id"], it["text"]) for it in items])
        store.save()
        print("Initialized store with sample_recipes.json")
        return

    if not os.path.exists("store.json"):
        print("Run --init first to build store")
        return

    store.load()
    if args.query:
        retrieved = store.retrieve(args.query, top_k=3)
        prompt = build_prompt(args.query, retrieved)
        api_key = os.environ.get(GEMINI_ENV, "AIzaSyA_xJt7wWCa5lGx483Ka-Gqri4zfrRH9Z0")
        if not api_key:
            print("GEMINI_API_KEY missing. Showing retrieved recipes only:\n")
            print("\n\n".join([t for _, t, _ in retrieved]))
            return
        answer = ask_gemini(prompt, api_key)
        print("=== Suggested Recipe(s) ===")
        print(answer)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
