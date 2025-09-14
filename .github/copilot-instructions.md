# Copilot Instructions for AI Agents

## Project Overview
This project is a simple Retrieval-Augmented Generation (RAG) recipe assistant. It consists of a CLI tool that retrieves relevant recipes based on a user query and optionally uses OpenAI's API to generate concise recipe suggestions.

## Key Components
- `cli.py`: Main entry point. Handles CLI arguments, store initialization, querying, and OpenAI integration.
- `embed_store.py`: Manages recipe embeddings, storage, retrieval, and persistence to `store.json`.
- `sample_recipes.json`: Example recipes for initializing the store.
- `store.json`: Persistent storage for recipe embeddings (created at runtime).

## Data Flow
1. On `--init`, recipes from `sample_recipes.json` are embedded and saved to `store.json`.
2. On `--query`, the store is loaded, top-k relevant recipes are retrieved, and a prompt is built.
3. If an OpenAI API key is available, the prompt is sent to OpenAI for a concise answer; otherwise, retrieved recipes are shown directly.

## Developer Workflows
- **Initialize the store:**
  ```sh
  python cli.py --init
  ```
- **Query recipes:**
  ```sh
  python cli.py --query "chicken curry"
  ```
- **OpenAI API Key:**
  - The API key is expected in an environment variable named as the value of `OPENAI_ENV` in `cli.py`.
  - If missing, only retrieval is performed (no LLM call).

## Conventions & Patterns
- Embedding and retrieval logic is encapsulated in `EmbedStore`.
- All persistent data is stored in the project root (`store.json`).
- The CLI is the only supported interface; no web or GUI components.
- Uses `gpt-4o-mini` as the default model (can be changed in `cli.py`).
- Prompts are constructed with a clear context boundary (`---`).

## External Dependencies
- `openai` Python package
- Any additional dependencies are listed in `requirements.txt`.

## Example Usage
- To re-initialize the store with new recipes, update `sample_recipes.json` and run with `--init`.
- To debug embedding or retrieval, modify or inspect `embed_store.py`.

## Key Files
- `recipes-rag/cli.py`
- `recipes-rag/embed_store.py`
- `recipes-rag/sample_recipes.json`
- `recipes-rag/requirements.txt`

## Notes
- No tests or CI/CD are present by default.
- All code is Python 3.11+.
- For new features, follow the CLI-driven, minimal-dependency approach.
