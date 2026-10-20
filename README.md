# Twilite Artificial Disintelligence

Twilite is the lite version of the Discord AI chatbot Twilight. 

Unlike Twilight, which runs on actual cloud infrastructure and capable models through Google AI Studio, Twilite runs on models so small (135M to 0.5B parameters) that calling them "AI" is legally generous. It is not meant to be self-hosted, it is not meant to have features, and it is definitely not meant to solve any of your problems. It just *is*.

A **Dopamine Studios** Project.

---

## What to Expect

* **Tiny Brains:** Powered by the models SmolLM2 (135M) or Qwen2.5 (0.5B). Expect profound wisdom such as repeating your prompt back to you or hallucinating recipes for toaster bath water.
* **Zero Features:** It chats. Sometimes. If the container doesn't OOM or segment fault first.
* **Overengineered Infrastructure:** Uses Docker, Docker Compose, and custom Ollama Modelfiles just to run a model smaller than the Instagram app on your phone. Peak software engineering.

---

## Quick Start (If You Must)

If you hate peace and quiet:

1. Create a `.env` file with your token and model choice (`smollm2` or `qwen2.5`, defaults to `smollm2`):
   ```env
   DISCORD_TOKEN=your_token_here
   OLLAMA_MODEL=smollm2
   ```
2. Spin up the docker nightmare:
   ```env
   docker-compose up --build -d
   ```
3. Ping `@Twilite` and regret your life choices immediately.

---

## License

GNU Affero General Public License v3.0 (AGPL-3.0). Feel free to share your misery. I miss that kinda misery the kind where you are nice to me but only in the evening so I ask am I just dreaming? I love you so much that it's dripping dripping from my arms and such I'm sorry I know I'm too much to love to trust I'm nothing but.
