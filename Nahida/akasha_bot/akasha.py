from dotenv import load_dotenv
import discord
import os
from Nahida.chatgpt.openai import chatgpt_response
from Nahida.yts.ytsummary import getTranscription

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 314197725212049408

class Client(discord.Client):
    async def on_ready(self):
        print("Welcome to Teyvat:", self.user)

    async def on_message(self, message):
        print(message.content)
        userMessage = None
        if message.author == self.user:
            return
        
        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('!gpt'):
            userMessage = message.content.replace('!gpt', '')
            #print(userMessage)
            akasha_response = chatgpt_response(userMessage)
            await message.reply(akasha_response)
        
        if message.content.startswith('!yts'):

            userMessage = message.content.replace('!yts', '')
            transcript = getTranscription(userMessage)

            #print(userMessage)
            prompt = "Summarize this video: "
            sentMessage = str(prompt + transcript)
            akasha_response = chatgpt_response(sentMessage)
            await message.reply(akasha_response)

intents = discord.Intents.all()
intents.message_content = True
client = Client(intents = intents)