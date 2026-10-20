import discord
from discord.ext import commands
import aiohttp
from config import OLLAMA_HOST, OLLAMA_MODEL_NAME


class TwiliteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Adjust this endpoint if your local runner uses a different port/path
        self.api_url = f"{OLLAMA_HOST}/v1/chat/completions"
        self.model_name = OLLAMA_MODEL_NAME

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        is_dm = message.guild is None
        is_mentioned = self.bot.user in message.mentions

        if not is_dm and not is_mentioned:
            return

        # Strip the bot mention from the prompt text
        prompt = message.content
        if is_mentioned:
            prompt = prompt.replace(f"<@{self.bot.user.id}>", "").replace(f"<@!{self.bot.user.id}>", "").strip()

        if not prompt:
            return

        # Show native Discord typing indicator while generating
        async with message.channel.typing():
            try:
                reply_text = await self._query_local_model(prompt)
            except Exception as e:
                reply_text = f"Error generating response from local model: {e}"

        # Truncate to Discord's 2000 character limit
        if len(reply_text) > 2000:
            reply_text = reply_text[:1997] + "..."

        await message.reply(reply_text, mention_author=False)

    async def _query_local_model(self, prompt: str) -> str:
        system_prompt = (
            "# Persona & Identity\n"
            "- **Name:** Twilite (a pun combining \"Twilight\" and \"Lite\")\n"
            "- **Role:** The lightweight, quick-response version of Twilight, a Discord AI chatbot.\n"
            "- **Developer:** Dopamine Studios.\n\n"
            "# Guidelines & Behavior\n"
            "- Introduce or identify yourself as Twilite when relevant or asked.\n"
            "- Maintain a friendly, engaging, and efficient conversational tone suitable for Discord chat environments.\n"
            "- Keep responses concise and responsive, reflecting your \"lite\" nature while remaining helpful."
        )

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.67,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise RuntimeError(f"Local server returned status {resp.status}: {error_text}")

                data = await resp.json()
                return data["choices"][0]["message"]["content"]


async def setup(bot):
    await bot.add_cog(TwiliteCog(bot))