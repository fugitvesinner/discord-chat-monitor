import datetime
import aiohttp
import discord
import asyncio
import json
from utils.log import logger

class ChatLogger(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        
        with open("config.json") as f:
            self.data = json.load(f)
    
    async def on_ready(self):
        logger.info(f'{self.user} online')
        await self.change_presence(status=discord.Status.offline)

    async def on_message_delete(self, message):
        try:
            if not message.guild or message.guild.id != self.data["server_id"] or message.author.bot:
                return
            
            embed = discord.Embed(
                description=message.content or "*No content*",
                color=0xff0000,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            
            if message.attachments:
                if len(message.attachments) == 1:
                    embed.set_image(url=message.attachments[0].url)
                else:
                    attachments = "\n".join([f"[{att.filename}]({att.url})" for att in message.attachments])
                    embed.add_field(name="Attachments", value=attachments, inline=False)
            
            embed.set_footer(text=f"ID: {message.author.id}")
            av_url = message.author.avatar_url if message.author.avatar else message.author.default_avatar_url
            
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(self.data["webhook"], adapter=discord.AsyncWebhookAdapter(session))
                await webhook.send(
                    username=f"{message.author.name} | Deleted",
                    avatar_url=av_url,
                    embed=embed
                )
                logger.info(f"Sent webhook")
                
        except Exception as e:
            logger.error(f"Sending webhook: {e}")
            
    async def on_message_edit(self, before, after):
        try:
            if not before.guild or before.guild.id != self.data["server_id"] or before.author.bot or before.content == after.content:
                return
            
            embed = discord.Embed(
                color=0xffff00,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            embed.add_field(name="Before", value=before.content or "*No content*", inline=False)
            embed.add_field(name="After", value=after.content or "*No content*", inline=False)
            embed.add_field(name="Channel", value=before.channel.mention, inline=True)
            
            embed.set_footer(text=f"ID: {before.author.id}")
            avatar_url = before.author.avatar_url if before.author.avatar else before.author.default_avatar_url
            
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(self.data["webhook"], adapter=discord.AsyncWebhookAdapter(session))
                await webhook.send(
                    username=f"{before.author.name} | Edited",
                    avatar_url=avatar_url,
                    embed=embed
                )
                logger.info(f"Sent webhook")
                
        except Exception as e:
            logger.error(f"Sending webhook: {e}")

async def main():
    client = ChatLogger()
    await client.start(client.data["token"])

if __name__ == "__main__":
    asyncio.run(main())