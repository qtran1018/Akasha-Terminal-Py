from dotenv import load_dotenv
import discord
import os
import asyncio
import math
from Nahida.chatgpt.openai import chatgpt_response4K, chatgpt_response16K, dalle_response
from Nahida.chatgpt.tokenizer import getTokenCount
from Nahida.yts.ytsummary import getTranscription
import textwrap

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 314197725212049408
MAX_TOKEN_COUNT = 4097
MAX_DISCORD_MESSAGE_LENGTH = 2000

class Client(discord.Client):
    async def on_ready(self):
        print("Welcome to Teyvat:", self.user)

    async def on_message(self, message):
        try:
            userMessage = None
            if message.author == self.user:
                return
    #--------------------------------------------------------------------------        
            if message.content == 'ping':
                await message.channel.send('pong')
    #--------------------------------------------------------------------------
            if message.content.startswith('!gpt'):
                async with message.channel.typing():
                    userMessage = message.content.replace('!gpt', '')
                    akasha_response = chatgpt_response4K(userMessage)
                    await message.reply(akasha_response)
    #--------------------------------------------------------------------------        
            if message.content.startswith('!yts'):
                async with message.channel.typing():
                    
                    userMessage = message.content
                    
                    replaceChars = {'!yts':'','-short':'','-long':'','-bullet':''}
                    for key, value in replaceChars.items():
                        userMessage = userMessage.replace(key, value)
                    #Add in long.
                    if '-short' in message.content:
                        prompt = "Give a short summary of this video in 2000 characters or less: "
                    elif '-short' in message.content and '-bullet' in message.content:
                        prompt = "Give a short summary of this video in bullet points: "  
                    elif '-long' in message.content:
                        prompt = "Give a long summary of this video: "
                    elif '-long' in message.content and '-bullet' in message.content:
                        prompt = "Give a long summary of this video in bullet points: "             
                    elif '-bullet' in message.content:
                        prompt = "Summarize this video in bullet points: "
                    else:         
                        prompt = "Summarize this video: "
                
                    transcript = getTranscription(userMessage)
                    tokenCount = getTokenCount(transcript)

                    if tokenCount > MAX_TOKEN_COUNT:
                        sentMessage = str(prompt + transcript)
                        akasha_response = chatgpt_response16K(sentMessage)
                        '''
                        gptDivisor = (tokenCount//MAX_TOKEN_COUNT) + 1
                        dividerCharCount = math.ceil(tokenCount/gptDivisor)
                        transcriptList = textwrap.wrap(transcript, dividerCharCount)

                        prompt = "Combine the next " + str(gptDivisor) + " messages and tell me the subject."

                        chatgpt_response4K(prompt)

                        for splitMessage in transcriptList:
                            if splitMessage != transcriptList[-1]:
                                chatgpt_response4K(splitMessage)
                            else:
                                akasha_response = chatgpt_response4K(splitMessage)
                                print(akasha_response)
                                akasha_response = "Feature WIP, token count is over the max token limit."
                                await message.replay(akasha_response)
                        '''
                    else:
                        sentMessage = str(prompt + transcript)
                        akasha_response = chatgpt_response4K(sentMessage)

                    print('Transcript Length = ' + str(len(transcript)))
                    print('GPT Response Length = ' + str(len(akasha_response)))

                    if len(akasha_response) > MAX_DISCORD_MESSAGE_LENGTH:
                        discordDivisor = math.ceil(len(akasha_response)/MAX_DISCORD_MESSAGE_LENGTH)
                        akasha_response_split = textwrap.wrap(akasha_response,discordDivisor)
                        for discord_message_split in akasha_response_split:
                           await message.reply(discord_message_split)
                    else:
                        await message.reply(akasha_response)
    #--------------------------------------------------------------------------
            if message.content.startswith('!dalle2'):
                async with message.channel.typing():
                    userMessage = message.content.replace('!dalle2','')
                    akasha_response = dalle_response(userMessage)
                    await message.reply(akasha_response)
                    
        except Exception as e:
            print(e)
            async with message.channel.typing():
                await message.reply(e)

intents = discord.Intents.all()
intents.message_content = True
client = Client(intents = intents)