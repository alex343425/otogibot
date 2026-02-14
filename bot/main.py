import os
import discord
import asyncio
import requests
from botUI import utilityUI, funUI, privateUI, publicUI , publicUI_kirby
from checkupdate import checkupdate,event_check
from nick import loadnick, loadsp
from parseskills import skillsourcecate, updatemfiles
from discord.ext import commands
from datetime import datetime, timedelta
import cfg
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

privateUICommandList = {#'?getcg',
                        #'?inspect',
                        '?beid',
                        #'?loadnick',
                        #'?loadsp',
                        '?update',
                        '?labyrinth',
                        '?palace'
                        }

publicUICommandList = {'?char',
                       '？char',
                       #'?nick',
                       #'？nick',
                       '?spirit',
                       '？spirit',
                       '?be',
                       '？be'
                       #'?卡池',
                       #'？卡池',
                       #'!story',
                       #'!event'                       
                       }
publicUICommandList_kirby={'?公告','?圖片'}

# --- 新增功能區塊：自訂指令載入邏輯 (改為讀取網址) ---
custom_commands_list = []

def load_custom_commands():
    """從 GitHub 網址讀取 Commands.txt"""
    global custom_commands_list
    # 指定 GitHub Raw 網址
    url = 'https://raw.githubusercontent.com/alex343425/otogibot/refs/heads/main/bot/Commands.txt'
    
    try:
        print(f"正在從網址讀取指令: {url}")
        response = requests.get(url, timeout=10) # 設定 10 秒超時
        
        if response.status_code == 200:
            response.encoding = 'utf-8' # 強制設定編碼為 utf-8，避免亂碼
            lines = [line.strip() for line in response.text.splitlines()]
            
            # 清空舊清單 (防止重複載入)
            custom_commands_list = []
            
            # 以每兩行為一組：單數行為觸發(index i)，雙數行為回復(index i+1)
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    trigger = lines[i]
                    response_text = lines[i+1]
                    # 確保觸發詞和回復都不是空的
                    if trigger and response_text:
                        custom_commands_list.append((trigger, response_text))
            
            print(f"成功載入 {len(custom_commands_list)} 組自訂指令。")
        else:
            print(f"讀取失敗，HTTP 狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"讀取 Commands.txt 時發生錯誤: {e}")
# --------------------------------------

loadnick()
loadsp()
updatemfiles()
skillsourcecate()
load_custom_commands() # 執行載入自訂指令
cfg.check_day = datetime.now().date() - timedelta(days=1)

@bot.event
async def on_ready():
    await checkupdate(bot)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        return
    
    if message.guild.id in guild_ids:
        pass
    else:
        return

    # --- 新增功能區塊：自訂指令判斷 ---
    # 邏輯：檢查訊息開頭是否符合 Commands.txt 中的設定
    # 由於列表是有序的，會優先觸發檔案中排序較前的指令
    for trigger, response_text in custom_commands_list:
        if message.content.startswith(trigger):
            await message.channel.send(response_text)
            #return # 觸發後直接結束，不再進行後續特定的指令判斷
    # --------------------------------

    # 添加新功能: 當有人在頻道ID = 803624040529920001內輸入「謝謝」時，發送Direct Message
    if message.channel.id == 803624040529920001 and "謝謝緋神" in message.content:
        try:
            await message.author.send("https://mega.nz/folder/QcBzGSrB#c6khaXbbF9sIuhQ7lgY_Zg")
        except discord.Forbidden:
            # 無法發送DM，可能用戶設定不接受DM
            print(f"無法發送DM給 {message.author}")
    
    if message.channel.id == 803624040529920001 and "海苔" in message.content:
        utc_time = datetime.utcnow()
        # 定義 GMT+9 的時區
        gmt_plus_9 = pytz.timezone('Asia/Tokyo')  # GMT+9 對應的時區
        # 將 UTC 時間轉換為 GMT+9
        gmt_plus_9_time = utc_time.replace(tzinfo=pytz.utc).astimezone(gmt_plus_9)
        
        
        # 預設值
        default_date = (2025, 1, 1)
        # 讀取網址
        url = 'https://raw.githubusercontent.com/alex343425/otogibot/refs/heads/main/bot/date.txt'
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # 如果HTTP狀態不是200會拋例外
            date_text = response.text.strip()  # 像 "2025, 5, 5"
            year, month, day = map(int, date_text.split(','))
        except Exception as e:
            print(f"讀取日期失敗，使用預設值: {e}")
            year, month, day = default_date

        # 組合 comparison_time
        comparison_time = gmt_plus_9.localize(datetime(year, month, day, 3, 0, 0))
        if gmt_plus_9_time < comparison_time:
            try:
                await message.author.send("https://mega.nz/folder/HRRxHSaC#dDdCYEtoOt0QoDvKEvR4NQ") 
            except discord.Forbidden:
                # 無法發送DM，可能用戶設定不接受DM
                print(f"無法發送DM給 {message.author}")
            # 嘗試添加表情反應
            try:
                emoji = "<:thank2:669472881150918666>"  # 使用完整表情格式
                await message.add_reaction(emoji)
            except discord.HTTPException:
                print(f"無法為訊息 {message.id} 添加表情")
        else:
            try:
                await message.author.send(f"期限已過，本次只到 {comparison_time}，現在是 {gmt_plus_9_time}，下次開放時間請關注更新情報頻道。")
            except discord.Forbidden:
                # 無法發送DM，可能用戶設定不接受DM
                print(f"無法發送DM給 {message.author}")
            # 嘗試添加表情反應
            try:
                emoji = "<:juuchao_X_X:1376207289660473434>"  # 使用完整表情格式
                await message.add_reaction(emoji)
            except discord.HTTPException:
                print(f"無法為訊息 {message.id} 添加表情")
                
    if "@everyone" in message.content:
        # 踢除用户
        await message.guild.ban(message.author, reason="提及了 everyone", delete_message_seconds=3600)

        # 发送通知
        await message.channel.send(f"{message.author.mention} 由於提及了 everyone，已被踢除！")
        #####測試
    
    # 檢查是否為指定的頻道
    if message.channel.id == 717056995995156480:        
        # 篩選條件：
        # 1. 附件數量剛好為 4
        # 2. 訊息文字內容為空 (去除前後空白後長度為 0)
        if len(message.attachments) == 4 and not message.content.strip():
            try:
                # 執行停權 (Ban)
                reason = "發送四張圖片且無文字的違規訊息"
                await message.guild.ban(message.author, reason=reason, delete_message_seconds=3600)                
                # 選項：在頻道內發送通知 (可刪除此行)
                # print(f"已封鎖使用者 {message.author}，原因：符合四圖篩選條件。")                
                await message.channel.send(f"{message.author.mention} 疑似發送廣告訊息，已被踢除！")
            except discord.Forbidden:
                print("錯誤：Bot 權限不足，無法停權該成員。")
            except discord.HTTPException as e:
                print(f"停權失敗：{e}")
               
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