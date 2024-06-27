

import discord
import asyncio
import os

# Ensure the discord.py version is compatible with this script
assert discord.__version__ >= '1.7.3', "This script requires discord.py version 1.7.3 or higher"

# Your bot's token
TOKEN = os.getenv('bbanner')

intents = discord.Intents.default()
intents.bans = True
intents.guilds = True

client = discord.Client(intents=intents)

source_server_id = None
target_server_id = None

async def transfer_bans():
    global source_server_id, target_server_id
    await client.wait_until_ready()

    source_guild = client.get_guild(source_server_id)
    target_guild = client.get_guild(target_server_id)

    if not source_guild or not target_guild:
        print(f"One of the guilds was not found. Source: {source_guild}, Target: {target_guild}")
        return

    print(f"Fetching bans from {source_guild.name}...")
    bans_count = 0
    async for ban_entry in source_guild.bans():
        bans_count += 1
        user = ban_entry.user
        print(f"Attempting to ban {user} ({user.id}) in {target_guild.name}...")
        try:
            await target_guild.ban(user, reason="Transferred ban")
            print(f"Successfully banned {user} ({user.id}) in {target_guild.name}.")
        except Exception as e:
            print(f"Failed to ban {user} ({user.id}) - {e}")
    
    print(f"Total bans fetched from {source_guild.name}: {bans_count}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await transfer_bans()
    await client.close()

if __name__ == "__main__":
    source_server_id = int(input("Enter the source server ID to export the ban list from: "))
    target_server_id = int(input("Enter the target server ID to import the ban list to: "))
    client.run(TOKEN)