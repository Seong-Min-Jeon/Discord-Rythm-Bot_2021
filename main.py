import discord
import os
import asyncio
import random
token='Token'

client = discord.Client()

stack = []

def make_msg(music, repeat):
    msg = ''    
    if(len(stack) == 0):        
        if(repeat == True):
            msg = "'" + music + "' 재생하는 중 (반복재생)"
        else:
            msg = "'" + music + "' 재생하는 중"
    else:
        for i in range(len(stack)):
            msg += str(i+1) + ". " + stack[i] + "\n"
        if(repeat == True):
            msg += "'" + music + "' 재생하는 중 (반복재생)"
        else:
            msg += "'" + music + "' 재생하는 중"
    return msg

class ThisBot(discord.Client):
    def __init__(self):
        super().__init__()        
        self.vc = None
        self.music = None
        self.repeat = False
    
    async def on_ready(self):
        print('로딩 완료')

    async def on_message(self,message):
        if(message.channel.id == 866943376980180993):            
            if(message.author.name == "아이유봇"):
                pass          
            else:
                await message.delete()

        if message.content.startswith('랜덤재생'):
            for file in os.listdir(os.getcwd()):
                if(".mp3" in file):
                    stack.append(file.replace('.mp3', ''))        

        if(self.vc == None):                        
            voice_channel = message.author.voice.channel
            msg_channel = message.channel
            vc = await voice_channel.connect()            
            self.vc = vc
            music = message.content
            self.music = music

            if(len(stack) != 0):
                self.music = stack[0]
                del stack[0]
            
            while(True):                          
                self.player = self.vc.play(discord.FFmpegPCMAudio(executable="C:/Users/home/Documents/app/ffmpeg/bin/ffmpeg.exe", source= self.music + ".mp3"))  
                     
                number = 100
                counter = 0
                async for x in msg_channel.history(limit = number):
                    if counter < number:
                        if(x.author.name == "아이유봇"):
                            await x.delete()
                            counter += 1
                            await asyncio.sleep(1.2)                

                await message.channel.send(make_msg(self.music))
                
                while(self.vc.is_playing() or len(stack) == 0):
                    await asyncio.sleep(1)
                
                if(self.repeat == True):
                    self.music = music
                else:
                    if(len(stack) >= 1):                
                        self.music = stack[0]
                        del stack[0]                           
                    else:
                        self.music = None 
        else:
            if message.content.startswith('랜덤화'):
                random.shuffle(stack)

                msg_channel = message.channel
                number = 100
                counter = 0
                async for x in msg_channel.history(limit = number):
                    if counter < number:
                        if(x.author.name == "아이유봇"):
                            await x.delete()
                            counter += 1
                            await asyncio.sleep(1.2)                

                await message.channel.send(make_msg(self.music))
            elif message.content.startswith('반복'):
                if(self.repeat == False):
                    self.repeat = True
                else:
                    self.repeat = False

            if(message.content + ".mp3" in os.listdir(os.getcwd())):                
                stack.append(message.content)   

                msg_channel = message.channel
                number = 100
                counter = 0
                async for x in msg_channel.history(limit = number):
                    if counter < number:
                        if(x.author.name == "아이유봇"):
                            await x.delete()
                            counter += 1
                            await asyncio.sleep(1.2)                

                await message.channel.send(make_msg(self.music))
           
bot=ThisBot()
bot.run(token)