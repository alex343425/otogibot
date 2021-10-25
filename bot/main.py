import os
import discord
import asyncio
from botUI import utilityUI, funUI, privateUI, publicUI
from checkupdate import checkupdate
from nick import loadnick, loadsp
from parseskills import skillsourcecate,skillsourcecate_tw, updatemfiles
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

guild_ids = {855879876815618078, # Test Server
             624974729689694228  # Main Server
            }

private_message_ids = {649153350431932437, # Scarlet
                       361903872270270465, # 卡比
                       554311206119145472, # Be
                       268293880108023808, # 海苔
                       470123343568175106, # T佬
                       870289853911289907 # Bu
                       }

utilityUICommandList = {'!ping'
                        }

funUICommandList = {'?rotate'
                    }

privateUICommandList = {'?getcg',
                        '?inspect',
                        '?beid',
                        '?loadnick',
                        '?loadsp',
                        '?update',
                        '?labyrinth'
                        }

publicUICommandList = {'?char',
                       '？char',
                       '?nick',
                       '？nick',
                       '?spirit',
                       '？spirit',
                       '?be',
                       '？be',
                       '!story',
                       '!event'
                       }

loadnick()
loadsp()
updatemfiles()
skillsourcecate()
skillsourcecate_tw()

@bot.event
async def on_ready():
    await checkupdate(bot)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.guild.id in guild_ids:
        pass
    else:
        return
      
    if message.content.split(' ')[0] in funUICommandList:
        await funUI(message,bot)
        return
    
    if message.content.split(' ')[0] in utilityUICommandList:
        await utilityUI(message,bot)
        return
  
    if message.content.split(' ')[0] in privateUICommandList:
        if message.author.id in private_message_ids:
            pass
        else:
            return
        await privateUI(message,bot)
        return
    
    if message.content.split(' ')[0] in publicUICommandList or message.content.startswith('?skill') or message.content.startswith('？skill') or message.content.startswith('?story') or message.content.startswith('?event') or message.content.startswith('?skitw') or message.content.startswith('？skitw'):
        await publicUI(message,bot)
        return

if __name__ == "__main__":
    bot.run(TOKEN)
