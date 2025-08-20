import datetime
import aiohttp
import discord
import asyncio
import json
from utils.log import logger

class ChatLogger(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
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
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            
            if message.attachments:
                if len(message.attachments) == 1:
                    embed.set_image(url=message.attachments[0].url)
                else:
                    attachments = "\n".join([f"[{att.filename}]({att.url})" for att in message.attachments])
                    embed.add_field(name="Attachments", value=attachments, inline=False)
            
            embed.set_footer(text=f"ID: {message.author.id}")
            
            avatar_url = message.author.display_avatar.url
            
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(self.data["webhook"], session=session)
                await webhook.send(
                    username=f"{message.author.display_name} | Deleted",
                    avatar_url=avatar_url,
                    embed=embed
                )
            logger.info(f"Sent webhook for deleted message from {message.author}")
                
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")
            
    async def on_message_edit(self, before, after):
        try:
            if not before.guild or before.guild.id != self.data["server_id"] or before.author.bot or before.content == after.content:
                return
            
            embed = discord.Embed(
                color=0xffff00,
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="Before", value=before.content or "*No content*", inline=False)
            embed.add_field(name="After", value=after.content or "*No content*", inline=False)
            embed.add_field(name="Channel", value=before.channel.mention, inline=True)
            
            embed.set_footer(text=f"ID: {before.author.id}")
            
            avatar_url = before.author.display_avatar.url
            
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(self.data["webhook"], session=session)
                await webhook.send(
                    username=f"{before.author.display_name} | Edited",
                    avatar_url=avatar_url,
                    embed=embed
                )
            logger.info(f"Sent webhook for edited message from {before.author}")
                
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")

async def main():
    client = ChatLogger()
    await client.start(client.data["token"])

if __name__ == "__main__":
    asyncio.run(main())