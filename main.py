from beacon import BeaconAutoShardedBot
import discord
import logging
from logging.handlers import RotatingFileHandler
from config import TOKEN, LOGGING_DEBUG_MODE
import os
import traceback
import asyncio
import urllib.parse

if not TOKEN:
    raise SystemExit("ERROR: Set DISCORD_TOKEN in a .env in root folder.")

logger = logging.getLogger("discord")
if LOGGING_DEBUG_MODE:
    logger.setLevel(logging.DEBUG)
    print("Running logger in DEBUG mode")
else:
    logger.setLevel(logging.INFO)
    print("Running logger in PRODUCTION mode")
log_path = os.path.join(os.path.dirname(__file__), "discord.log")
handler = RotatingFileHandler(
    filename=log_path,
    encoding="utf-8",
    mode="a",
    maxBytes=1 * 1024 * 1024,
    backupCount=5
)
logger.addHandler(handler)

log_format = '%(asctime)s||%(levelname)s: %(message)s'
date_format = '%H:%M:%S %d-%m'

formatter = logging.Formatter(log_format, datefmt=date_format)

handler.setFormatter(formatter)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

allowed_mentions = discord.AllowedMentions(replied_user=False)
async def on_shard_ready(shard_id: int):
    activity_name = f"DM or Mention @Twilite#4614"

    await bot.change_presence(
        activity=discord.Streaming(name=activity_name, url="https://www.twitch.tv/dopaminediscordbot"),
        shard_id=shard_id
    )
bot = BeaconAutoShardedBot(command_prefix="!", intents=intents, minimal_caching=True, allowed_mentions=allowed_mentions, accent_colour=discord.Colour(0xFFFFFF), on_shard_ready_callback=on_shard_ready)

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Twilite Bot is running!")
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

if __name__ == "__main__":
    async def main_async():
        try:
            async with bot:
                await bot.start(TOKEN)
        except Exception as e:
            print(f"ERROR: Failed to start the bot: {e}")
            traceback.print_exc()


    asyncio.run(main_async())