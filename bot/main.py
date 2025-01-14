import os
import discord
import asyncio
from botUI import utilityUI, funUI, privateUI, publicUI , publicUI_kirby
from checkupdate import checkupdate,event_check
from nick import loadnick, loadsp
from parseskills import skillsourcecate, updatemfiles
from discord.ext import commands
from datetime import datetime, timedelta
import pytz

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)
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
                        '?labyrinth',
                        '?palace'
                        }

publicUICommandList = {'?char',
                       '？char',
                       '?nick',
                       '？nick',
                       '?spirit',
                       '？spirit',
                       '?be',
                       '？be',
                       '?卡池',
                       '？卡池',
                       '!story',
                       '!event'                       
                       }
publicUICommandList_kirby={'?公告','?圖片'}

loadnick()
loadsp()
updatemfiles()
skillsourcecate()


@bot.event
async def on_ready():
    await checkupdate(bot)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    
    #if message.channel.id == 803624040529920001 and "謝謝海苔" in message.content:
    if isinstance(message.channel, discord.DMChannel) and "謝謝海苔" in message.content:
        utc_time = datetime.utcnow()
        # 定義 GMT+9 的時區
        gmt_plus_9 = pytz.timezone('Asia/Tokyo')  # GMT+9 對應的時區
        # 將 UTC 時間轉換為 GMT+9
        gmt_plus_9_time = utc_time.replace(tzinfo=pytz.utc).astimezone(gmt_plus_9)
        comparison_time = gmt_plus_9.localize(datetime(2025, 1, 11, 3, 0, 0))
        if gmt_plus_9_time < comparison_time:
            try:
                await message.author.send("https://mega.nz/folder/HRRxHSaC#dDdCYEtoOt0QoDvKEvR4NQ")
            except discord.Forbidden:
                # 無法發送DM，可能用戶設定不接受DM
                print(f"無法發送DM給 {message.author}")      
        else:
            await message.author.send(f"期限已過，本次只到 {comparison_time}，現在是 {gmt_plus_9_time}")
    if message.guild is None:
        return
    
    if message.guild.id in guild_ids:
        pass
    else:
        return
    # 添加新功能: 當有人在頻道ID = 803624040529920001內輸入「謝謝」時，發送Direct Message
    if message.channel.id == 803624040529920001 and "謝謝緋神" in message.content:
        try:
            await message.author.send("https://mega.nz/folder/QcBzGSrB#c6khaXbbF9sIuhQ7lgY_Zg")
        except discord.Forbidden:
            # 無法發送DM，可能用戶設定不接受DM
            print(f"無法發送DM給 {message.author}")
    if '!呼叫活動通知' in message.content:
        l_result = event_check()
        if len(l_result)>1:
            myembed_event = discord.Embed(title="活動提醒",colour=0x00b0f4)
            myembed_event.add_field(name="限時活動",value=l_result[0],inline=False)
            myembed_event.add_field(name="常態活動",value=l_result[1],inline=False)
            await reminder_channel_alt.send(content=l_result[2],embed=myembed_event)
  

    if "@everyone" in message.content:
        # 踢除用户
        await message.guild.ban(message.author, reason="提及了 everyone", delete_message_seconds=3600)

        # 发送通知
        await message.channel.send(f"{message.author.mention} 由於提及了 everyone，已被踢除！")
        #####測試
       
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

    if message.content.split(' ')[0] in publicUICommandList_kirby:
        if message.author.id in private_message_ids:
            pass
        else:
            return
        await publicUI_kirby(message,bot)
        return
        


if __name__ == "__main__":
    bot.run(TOKEN)
