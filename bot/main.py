import os
import discord
import asyncio
import requests
import hashlib
import io
import math
from PIL import Image
from botUI import utilityUI, funUI, privateUI, publicUI , publicUI_kirby
from checkupdate import checkupdate,event_check
from nick import loadnick, loadsp
from parseskills import skillsourcecate, updatemfiles
from discord.ext import commands
from datetime import datetime, timedelta
import cfg
import pytz

# --- 廣告圖片比對設定：SHA-256 + pHash ---
AD_IMAGE_FILENAMES = ["1.jpg", "2.jpg", "3.jpg", "4.jpg"]
PHASH_THRESHOLD = 5  # Hamming distance <= 8 視為相似；越小越嚴格


def calculate_phash(image_bytes, hash_size=8, highfreq_factor=4):
    """使用 Pillow 計算 64-bit pHash，不依賴 imagehash / scipy / numpy。"""
    size = hash_size * highfreq_factor  # 8 * 4 = 32

    with Image.open(io.BytesIO(image_bytes)) as img:
        img = img.convert("L").resize((size, size), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())

    # 只計算 DCT 左上角 hash_size x hash_size 的低頻係數。
    cos_table = [
        [math.cos((2 * x + 1) * u * math.pi / (2 * size)) for x in range(size)]
        for u in range(hash_size)
    ]

    coeffs = []
    for v in range(hash_size):
        cos_v = cos_table[v]
        for u in range(hash_size):
            cos_u = cos_table[u]
            value = 0.0
            for y in range(size):
                row_offset = y * size
                cy = cos_v[y]
                for x in range(size):
                    value += pixels[row_offset + x] * cos_u[x] * cy
            coeffs.append(value)

    # 忽略 DC 係數，用其餘 63 個低頻係數的中位數作門檻。
    sorted_coeffs = sorted(coeffs[1:])
    median = sorted_coeffs[len(sorted_coeffs) // 2]

    phash = 0
    for value in coeffs:
        phash = (phash << 1) | (1 if value > median else 0)
    return phash


def phash_distance(hash_a, hash_b):
    """計算兩個 64-bit pHash 的 Hamming distance。"""
    return (hash_a ^ hash_b).bit_count()


def load_ad_image_hashes():
    """程式啟動時載入同目錄 1.jpg ~ 4.jpg 的 SHA-256 與 pHash。"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    references = []

    for filename in AD_IMAGE_FILENAMES:
        path = os.path.join(base_dir, filename)
        if not os.path.isfile(path):
            print(f"廣告參考圖片不存在，略過：{path}")
            continue

        try:
            with open(path, "rb") as f:
                data = f.read()

            references.append({
                "filename": filename,
                "sha256": hashlib.sha256(data).hexdigest(),
                "phash": calculate_phash(data)
            })
            print(f"已載入廣告參考圖片：{filename}")
        except Exception as e:
            print(f"載入廣告參考圖片 {filename} 失敗：{e}")

    return references


def match_ad_image(image_bytes):
    """
    回傳 (是否命中, 比對方式, 參考檔名, pHash距離)。
    先做 SHA-256 完全比對，再做 pHash 相似度比對。
    """
    sha256 = hashlib.sha256(image_bytes).hexdigest()

    for ref in ad_image_hashes:
        if sha256 == ref["sha256"]:
            return True, "SHA-256", ref["filename"], 0

    try:
        current_phash = calculate_phash(image_bytes)
    except Exception:
        return False, None, None, None

    best_ref = None
    best_distance = None
    for ref in ad_image_hashes:
        distance = phash_distance(current_phash, ref["phash"])
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_ref = ref

    if best_ref is not None and best_distance <= PHASH_THRESHOLD:
        return True, "pHash", best_ref["filename"], best_distance

    return False, None, None, best_distance


ad_image_hashes = load_ad_image_hashes()
# ------------------------------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")

# 最近的疑似廣告違規紀錄，最多保留 10 筆
# 每筆資料格式：{"user_id": 使用者ID, "channel_id": 頻道ID}
violation_records = []
MAX_VIOLATION_RECORDS = 10
AD_ALERT_CHANNEL_ID = 624975992947081229

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

privateUICommandList = {'?beid',
                        '?update',
                        '?labyrinth',
                        '?palace'
                        }

publicUICommandList = {'?char',
                       '？char',
                       '?spirit',
                       '？spirit',
                       '?be',
                       '？be'
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
    
    # 疑似廣告訊息判定：剛好 4 個附件，而且沒有任何文字內容
    if len(message.attachments) == 4 and not message.content.strip():
        # 原本的特殊頻道邏輯保留：此頻道符合條件時直接 Ban
        if message.channel.id == 717056995995156480:
            try:
                reason = "發送四張圖片且無文字的違規訊息"
                await message.guild.ban(
                    message.author,
                    reason=reason,
                    delete_message_seconds=3600
                )
                await message.channel.send(
                    f"{message.author.mention} 疑似發送廣告訊息，已被踢除！"
                )
            except discord.Forbidden:
                print("錯誤：Bot 權限不足，無法停權該成員。")
            except discord.HTTPException as e:
                print(f"停權失敗：{e}")

        # 其他頻道：加入最近 10 筆違規紀錄，跨 3 個不同頻道累積 3 次才 Ban
        else:
            violation_records.append({
                "user_id": message.author.id,
                "channel_id": message.channel.id
            })

            # 只保留最近 10 筆違規紀錄；第 11 筆加入時刪除最舊的一筆
            if len(violation_records) > MAX_VIOLATION_RECORDS:
                violation_records.pop(0)

            # 取出目前這名使用者在最近 10 筆紀錄中的所有違規
            user_records = [
                record for record in violation_records
                if record["user_id"] == message.author.id
            ]
            user_channel_ids = {record["channel_id"] for record in user_records}

            # 同一使用者違規至少 3 筆，而且來自至少 3 個不同頻道時停權
            if len(user_records) >= 3 and len(user_channel_ids) >= 3:
                reason = "疑似在至少三個不同頻道發送四張圖片且無文字的廣告訊息"
                try:
                    await message.guild.ban(
                        message.author,
                        reason=reason,
                        delete_message_seconds=3600
                    )

                    # Ban 成功後清除該使用者的違規紀錄，避免重複觸發
                    violation_records[:] = [
                        record for record in violation_records
                        if record["user_id"] != message.author.id
                    ]

                    # 在指定頻道發送停權通知
                    alert_channel = bot.get_channel(AD_ALERT_CHANNEL_ID)
                    if alert_channel is None:
                        try:
                            alert_channel = await bot.fetch_channel(AD_ALERT_CHANNEL_ID)
                        except (discord.Forbidden, discord.NotFound, discord.HTTPException) as e:
                            print(f"取得廣告停權通知頻道失敗：{e}")
                            alert_channel = None

                    if alert_channel is not None:
                        try:
                            await alert_channel.send(
                                f"{message.author.mention} 疑似發送廣告訊息，已被停權"
                            )
                        except discord.HTTPException as e:
                            print(f"發送廣告停權通知失敗：{e}")

                except discord.Forbidden:
                    print("錯誤：Bot 權限不足，無法停權該成員。")
                except discord.HTTPException as e:
                    print(f"停權失敗：{e}")
               
    # 廣告圖片比對：放在跨頻道違規紀錄判定之後執行。
    # 只要任何一個附件與 1.jpg ~ 4.jpg 的 SHA-256 完全相同，
    # 或 pHash 足夠相似，就刪除整則訊息；目前不會因圖片比對直接停權。
    if message.attachments and ad_image_hashes:
        for attachment in message.attachments:
            try:
                attachment_bytes = await attachment.read()
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"讀取附件失敗 {attachment.filename}：{e}")
                continue

            matched, method, ref_filename, distance = await asyncio.to_thread(
                match_ad_image,
                attachment_bytes
            )

            if matched:
                try:
                    await message.delete()
                    if method == "SHA-256":
                        print(
                            f"已刪除廣告圖片訊息：user={message.author.id}, "
                            f"channel={message.channel.id}, attachment={attachment.filename}, "
                            f"match={ref_filename}, method=SHA-256"
                        )
                    else:
                        print(
                            f"已刪除廣告圖片訊息：user={message.author.id}, "
                            f"channel={message.channel.id}, attachment={attachment.filename}, "
                            f"match={ref_filename}, method=pHash, distance={distance}"
                        )
                except discord.NotFound:
                    # 訊息可能已被前面的 Ban 邏輯一併刪除。
                    pass
                except discord.Forbidden:
                    print("錯誤：Bot 權限不足，無法刪除匹配廣告圖片的訊息。")
                except discord.HTTPException as e:
                    print(f"刪除廣告圖片訊息失敗：{e}")

                # 一則訊息只需要命中一個附件就刪除，不再繼續下載/比對其他附件。
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

    if message.content.split(' ')[0] in publicUICommandList_kirby:
        if message.author.id in private_message_ids:
            pass
        else:
            return
        await publicUI_kirby(message,bot)
        return
        


if __name__ == "__main__":
    bot.run(TOKEN)