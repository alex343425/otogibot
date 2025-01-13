import discord
from datetime import datetime, timedelta
import asyncio
import requests
import cfg
from numpy import size, array
from PIL import Image, ImageOps
from io import BytesIO
from bs4 import BeautifulSoup
import pytz
import calendar

def get_last_day_of_month_23_59(gmt_plus_9_time):

    # 取得當前年份和月份
    year = gmt_plus_9_time.year
    month = gmt_plus_9_time.month
    
    # 取得當月的最後一天
    last_day = calendar.monthrange(year, month)[1]
    
    # 設定為當月最後一天的 23:59
    last_day_23_59 = gmt_plus_9_time.replace(day=last_day, hour=23, minute=59, second=0, microsecond=0)
    
    return last_day_23_59


def get_sunday_23_59(gmt_plus_9_time):

    # 計算當前是星期幾 (星期日是 6)
    days_until_sunday = 6 - gmt_plus_9_time.weekday()
    
    # 計算當週的星期日
    sunday_23_59 = gmt_plus_9_time + timedelta(days=days_until_sunday)
    sunday_23_59 = sunday_23_59.replace(hour=23, minute=59, second=0, microsecond=0)
    
    return sunday_23_59

def get_14th_23_59(gmt_plus_9_time):
    # 取得當月 14 日的 23:59
    date_14th = gmt_plus_9_time.replace(day=14, hour=23, minute=59, second=0, microsecond=0)
    
    # 如果當前時間超過了本月的 14 日 23:59，則計算下個月的 14 日 23:59
    if gmt_plus_9_time > date_14th:
        # 如果當前月份是 12 月，則進入下一年
        if gmt_plus_9_time.month == 12:
            year = gmt_plus_9_time.year + 1
            month = 1
        else:
            year = gmt_plus_9_time.year
            month = gmt_plus_9_time.month + 1
        
        # 取得下個月 14 日的 23:59
        date_14th = date_14th.replace(year=year, month=month, day=14)
    
    return date_14th

def time_trans(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")

def event_check():
    # 取得伺服器當前的時間 (假設是 UTC)
    utc_time = datetime.utcnow()
    # 定義 GMT+9 的時區
    gmt_plus_9 = pytz.timezone('Asia/Tokyo')  # GMT+9 對應的時區
    # 將 UTC 時間轉換為 GMT+9
    gmt_plus_9_time = utc_time.replace(tzinfo=pytz.utc).astimezone(gmt_plus_9)
    
    if gmt_plus_9_time.hour != 23:
        return ''
    if gmt_plus_9_time.minute >= 30:
        return ''
    url = 'https://otogi-rest.otogi-frontier.com/api/WorldMap'
    try:
        r = requests.get(url, headers={'token': cfg.token_jp}).json()
    except:
        return ''
    l=[]
    l2=[]
    for x in r['Worlds']:
        try:
            date_item = time_trans(x['Event']['EndDate'])
            if date_item.year == 2100:
                continue
            if x['Name'] == '記憶のピラミッド':
                continue
            if x['Name'] in l:
                continue
            l.append(x['Name'])
            l2.append((x['Name'],date_item,x['Id']))
        except:
            pass
    #檢查靈殿
    url = 'https://otogi-rest.otogi-frontier.com/api/Events/21010'
    try:
        r = requests.get(url, headers={'token': cfg.token_jp}).json()        
        CollapsedTemple = datetime.strptime(r['CollapsedTemple']['PhaseEndDate'], "%Y-%m-%dT%H:%M:%S")
        if CollapsedTemple.year >= 2024:
            l2.append(('天墜霊殿',CollapsedTemple,0))
    except:
        pass
    
    flag_3day = False
    flag_1day = False
    s_mention=''
    s=''
    l_result=[]
    for x,y in l2:
        y = y.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
        t = y - gmt_plus_9_time
        if t.days < 0:
            s +=f"僅領取報酬: {x}\n"
            continue        
        s +=f"{t.days}天 {int((t.seconds)/3600)+1}小時: {x}\n"
        if t.days<=3:
            flag_3day=True
        if t.days<=1:
            flag_1day=True
        #嘗試獲得高難挑戰
        try:
            url = 'https://otogi-rest.otogi-frontier.com/api/Events/'+str(z)
            r_worlds = requests.get(url, headers={'token': cfg.token_jp}).json()['Worlds'][-1]['Id']
            url='https://otogi-rest.otogi-frontier.com/api/Worlds/'+str(r_worlds)
            r_quests = requests.get(url, headers={'token': cfg.token_jp}).json()['Locations'][0]['Id']
            url = 'https://otogi-rest.otogi-frontier.com/api/Locations/'+str(r_quests)
            r_Locations = requests.get(url, headers={'token': cfg.token_jp}).json()['Quests']
            event_count=0
            event_count_lock=0
            for item in r_Locations:
                if '高難易度' not in item['Name']:
                    continue
                event_count+=1
                if item['LockDescription'] == None:
                    event_count_lock+=1
            if event_count > 0:
                s+=f"　　　　　高難挑戰開放{event_count_lock}/{event_count}"
                if event_count_lock == event_count:
                    s+=f"　已全部開放"
                s+='\n'
        except:            
            pass
    l_result.append(s)
    if flag_3day:
        s_mention+="<@&1287472215947870359> "
    if flag_1day:
        s_mention+="<@&1154075408392781874> "
    s=''
    t = get_sunday_23_59(gmt_plus_9_time) - gmt_plus_9_time
    s +=f"{t.days}天 {int((t.seconds)/3600)+1}小時: 星之魔宮殿刷新\n"
    if t.days<=0:
        s_mention+="<@&1288132433069342752> "
    t = get_14th_23_59(gmt_plus_9_time) - gmt_plus_9_time
    s+=f"{t.days}天 {int((t.seconds)/3600)+1}小時: 深層迷宮刷新\n"
    if t.days<=1:
        s_mention+="<@&1288132511330861056> "
    t = get_last_day_of_month_23_59(gmt_plus_9_time) - gmt_plus_9_time
    s+=f"{t.days}天 {int((t.seconds)/3600)+1}小時: 金字塔/競技場刷新\n"
    if t.days<=1:
        s_mention+="<@&1288132586274553938> "
    l_result.append(s)    
    s_mention+="<@&999704934264078576>"
    l_result.append(s_mention)       
    return l_result

def free_gacha_check():    
    url = 'https://otogi-rest.otogi-frontier.com/api/UGachas?include='
    r=requests.get(url, headers={'token': cfg.token_jp}).json()['AvailableGachas']    
    for x in r:
        if '無料10連ガチャ' in x['Name']:
            return True
    return False    

def ch_number(i):
    lch = ['','萬','億','兆','京','垓','秭','穰']
    i = str(i)
    l=[]
    while True:
        if int(i) > 10000:
            l.append(i[-4:])
            i = i[0:len(i)-4]
        else:
            l.append(i)
            break
    list.reverse(l)
    result = ''
    i=len(l)-1
    for x in l:
        result += x + lch[i]
        i-=1
    return result


async def checkupdate(bot):
    starting_channel = bot.get_channel(855880177224253440)
    log_channel = bot.get_channel(630699387542306839)
    bot_channel = bot.get_channel(803624040529920001)
    async def get_img(img_url):
        return Image.open(BytesIO(requests.get(img_url).content))
    try:
        news_latest = requests.get(cfg.addresslatest, headers={'token': cfg.token_jp}).json()
        news_now = requests.get(cfg.addressnow, headers={'token': cfg.token_jp}).json()
        #maint_img = await get_img('https://cos-web-assets.otogi-frontier.com/static/sp/maintenance/maintenance.png')
        ranking = requests.get('https://api-pc.otogi-frontier.com/api/Events/17001/ranking/', headers={'token': cfg.token_jp}).json()
        foobaa_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/10898', headers={'token': cfg.token_jp}).json()["Level"]
        ollumi_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/843672', headers={'token': cfg.token_jp}).json()["Level"]
        sack_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/99142', headers={'token': cfg.token_jp}).json()["Level"]
        Be_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/61640', headers={'token': cfg.token_jp}).json()["Level"]
        Scarlet_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/835519', headers={'token': cfg.token_jp}).json()["Level"]
        Kirby_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/553222', headers={'token': cfg.token_jp}).json()["Level"]
        bu_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/521954', headers={'token': cfg.token_jp}).json()["Level"]
        failure = 0
    except:
        await starting_channel.send('獲取公告失敗')
        failure = 1
    try:
        #[width, height] = size(maint_img)
        #img_save = maint_img.crop((round(width/2),round(height/2),round(width/2)+20,round(height/2)+20))
        #a_sum_old = 0
        #for x in array(ImageOps.grayscale(img_save)):
        #    a_sum_old += sum(x)
        
        print("Logged in as {}({})".format(bot.user.name, bot.user.id))
        await starting_channel.send('Bot initiated.')
        reminder_channel = bot.get_channel(626708913257185280)
        reminder_channel_alt = bot.get_channel(624974729689694230)
        private_chat_channel = bot.get_channel(913303883273625620)
        be_update_channel = bot.get_channel(902930492683325440)
        debug_channel = bot.get_channel(855880392045363230)
    except:
        await starting_channel.send('公告處理失敗')
        failure = 1
    
    while True:
        if failure == 1:
            break
        await asyncio.sleep(30)
        current_time = str(datetime.now()).split(' ')
        
        if current_time[1][3:5] in ['03','08','13','18','23','28','33','38','43','48','53','58']:
            await asyncio.sleep(30)
            try:
                ranking_check = requests.get('https://api-pc.otogi-frontier.com/api/Events/17001/ranking/', headers={'token': cfg.token_jp}).json()
                foobaa_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/10898', headers={'token': cfg.token_jp}).json()["Level"]
                ollumi_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/843672', headers={'token': cfg.token_jp}).json()["Level"]
                sack_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/99142', headers={'token': cfg.token_jp}).json()["Level"]
                Be_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/61640', headers={'token': cfg.token_jp}).json()["Level"]
                Scarlet_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/835519', headers={'token': cfg.token_jp}).json()["Level"]
                Kirby_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/553222', headers={'token': cfg.token_jp}).json()["Level"]
                bu_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/521954', headers={'token': cfg.token_jp}).json()["Level"]
            except:
                pass
            try:
                if foobaa_level_check > foobaa_level:
                    text = 'foobaa等級變動.由' + str(foobaa_level) + '升為' + str(foobaa_level_check) + '.'
                    await private_chat_channel.send(text)
                    foobaa_level = foobaa_level_check
                if ollumi_level_check > ollumi_level:
                    text = 'ollumi等級變動.由' + str(ollumi_level) + '升為' + str(ollumi_level_check) + '.'
                    await private_chat_channel.send(text)
                    ollumi_level = ollumi_level_check
                if sack_level_check > sack_level:
                    text = 'sack(海苔)等級變動.由' + str(sack_level) + '升為' + str(sack_level_check) + '.'
                    await private_chat_channel.send(text)
                    sack_level = sack_level_check
                if Be_level_check > Be_level:
                    text = 'Be等級變動.由' + str(Be_level) + '升為' + str(Be_level_check) + '.'
                    await private_chat_channel.send(text)
                    Be_level = Be_level_check
                if Scarlet_level_check > Scarlet_level:
                    text = 'Scarlet等級變動.由' + str(Scarlet_level) + '升為' + str(Scarlet_level_check) + '.'
                    await private_chat_channel.send(text)
                    Scarlet_level = Scarlet_level_check
                if Kirby_level_check > Kirby_level:
                    text = 'Kirby等級變動.由' + str(Kirby_level) + '升為' + str(Kirby_level_check) + '.'
                    await private_chat_channel.send(text)
                    Kirby_level = Kirby_level_check
                if bu_level_check > bu_level:
                    text = '村人521954等級變動.由' + str(bu_level) + '升為' + str(bu_level_check) + '.'
                    await private_chat_channel.send(text)
                    bu_level = bu_level_check
            except:
                await debug_channel.send('等級探針出現bug.')
            try:
                if ranking["ThisWeekQuestName"] == ranking_check["ThisWeekQuestName"]:
                    for x in ranking_check["ThisWeekTopPlayers"]:
                        if x["Rank"] == 1:
                            while True:
                                if x["UUserId"] != ranking["ThisWeekTopPlayers"][0]["UUserId"]:
                                    text = '競技場第一名變更,ID為: **'+str(x["UUserId"])+'**'
                                elif x["Score"] > ranking["ThisWeekTopPlayers"][0]["Score"]:
                                    text = '競技場第一名成績上升,ID為: **'+str(x["UUserId"])+'**'
                                else:
                                    break
                                await be_update_channel.send(text)
                                for i in range(0,5):
                                    flag = 0
                                    url_inspect = 'https://api-pc.otogi-frontier.com/api/UFriend/Deck/'+str(x["UUserId"])+'/'+str(i)
                                    try:
                                        party = requests.get(url_inspect, headers={'token': cfg.token_jp}).json()
                                        for y in x["Party"]:
                                            w = []
                                            try:
                                                w = next(z for z in party["UParty"]["UParties"] if y['MMonsterId'] == z['UMonster']['MMonsterId'])
                                            except:
                                                pass
                                            if w == []:
                                                flag = 1
                                                break
                                            else:
                                                continue
                                        if flag == 1:
                                            continue
                                        mylst = [[],[],[],[],[],[]]
                                        canvas = Image.new('RGB', (912,166))
                                        myembed = discord.Embed(title='疑似使用的隊伍', description='可能有變動', color=10181046)
                                        for u in party['UParty']['UParties']:
                                            pos = u['Position']
                                            text = '【角色名】:'
                                            v = u['UMonster']
                                            try:
                                                char_url = 'https://otogimigwestsp.blob.core.windows.net/prodassets/SpBrowser/BustShot/'+str(v['MMonsterId'])+'.png?96'
                                                char_img = await get_img(char_url)
                                                canvas.paste(char_img,(152*(pos-1),0))
                                            except:
                                                pass
                                            try:
                                                text += next(s for s in cfg.MMonsters if s['id'] == v['MMonsterId'])['n']+'\n'
                                            except:
                                                text += '\n'
                                            text += '【拆技1】:'
                                            try:
                                                text += next(s for s in cfg.MSkills if s['id'] == v['Sub1']['MSkillId'])['n']+'\n'
                                            except:
                                                text += '\n'
                                            text += '【拆技2】:'
                                            try:
                                                text += next(s for s in cfg.MSkills if s['id'] == v['Sub2']['MSkillId'])['n']+'\n'
                                            except:
                                                text += '\n'
                                            text += '【拆技3】:'
                                            try:
                                                text += next(s for s in cfg.MSkills if s['id'] == v['Sub3']['MSkillId'])['n']+'\n'
                                            except:
                                                text += '\n'
                                            text += '【武器】:'
                                            try:
                                                text += next(s for s in cfg.MWeapons if s['id'] == v['UWeapon']['MWeaponId'])['n']+'\n'
                                            except:
                                                text += '\n'
                                            text += '【飾品】:'
                                            try:
                                                text += next(s for s in cfg.MAccessory if s['id'] == v['UAccessory']['MAccessoryId'])['n']+'\n'
                                            except:
                                                pass
                                            try:
                                                mylst[pos-1] = text
                                            except:
                                                pass
                                        leader = 0
                                        for u in mylst:
                                            if u != [] and leader == 0:
                                                myembed.add_field(name='隊长', value=u, inline=False)
                                            if u != [] and leader > 0:
                                                myembed.add_field(name='隊員'+str(leader), value=u, inline=False)
                                            leader += 1
                                        canvas.save('team.png')
                                        image_channel = bot.get_channel(855880309853126696)
                                        picture = discord.File('team.png',filename='team.png')
                                        img_message = await image_channel.send(file=picture)
                                        myembed.set_image(url=img_message.attachments[0].url)
                                        try:
                                            await be_update_channel.send(embed=myembed)
                                            break
                                        except:
                                            await be_update_channel.send('錯誤 請回報BUG')
                                    except:
                                        pass
                                break
                        try:        
                            if '海苔' in x["Name"] or '海苔' in x["Introduction"]:
                                y = []
                                try:
                                    y = next(z for z in ranking["ThisWeekTopPlayers"] if z['UUserId'] == x['UUserId'])
                                except:
                                    pass
                                if y == []:
                                    text = '**'+x['Name']+'**登上了競技場榜單,排名為: **'+str(x["Rank"])+'**,分數為: **'+ ch_number(str(x['Score'])) +'**.謝謝海苔!'
                                    await reminder_channel_alt.send(text)
                                else:
                                    if x['Rank'] < y['Rank']:
                                        text = '**'+x['Name']+'**的競技場排名從**'+str(y["Rank"])+'**上升為**'+str(x["Rank"])+'**,分數為: **'+ ch_number(str(x['Score']))+'**.謝謝海苔!'
                                        await reminder_channel_alt.send(text)
                                    elif x['Score'] > y['Score']:
                                        text = '**'+x['Name']+'**的競技場分數從**'+ch_number(str(y["Score"]) )+'**上升為**'+ch_number(str(x["Score"]))+'**,排名為: **'+str(x['Rank'])+'**.謝謝海苔!'
                                        await reminder_channel_alt.send(text)
                                    else:
                                        pass
                        except:
                            pass
                    ranking = ranking_check
                else:
                    ranking = ranking_check
                    for x in ranking["ThisWeekTopPlayers"]:
                        try:
                            if '海苔' in x["Name"]+x["Introduction"]:
                                text = x["Name"]+'登上了競技場第**'+str(x["Rank"])+'**名,分數是: **'+ch_number(str(x["Score"]))+'**.謝謝海苔!'
                                await reminder_channel_alt.send(text)
                        except:
                            pass
            except:
                ranking = ranking_check
        
        if current_time[1][3:5] in ['00','30']:
            l_result = event_check()
            if len(l_result)>1:
                myembed_event = discord.Embed(title="活動提醒",colour=0x00b0f4)
                myembed_event.add_field(name="限時活動",value=l_result[0],inline=False)
                myembed_event.add_field(name="常態活動",value=l_result[1],inline=False)
                if free_gacha_check():
                    myembed_event.add_field(name="免費十連",value='現在有免費十連抽，記得抽',inline=False)
                await reminder_channel_alt.send(content=l_result[2],embed=myembed_event)
            await asyncio.sleep(30)
            try:
                news_latest_check = requests.get(cfg.addresslatest, headers={'token': cfg.token_jp}).json()
                news_now_check = requests.get(cfg.addressnow, headers={'token': cfg.token_jp}).json()
            except:
                await starting_channel.send('獲取公告失敗')
                continue
            count = 0
            overall_check_mark = 0
            
            ##################
            #temp_str=''
            #for x in news_latest_check:
            #    temp_str+=str(x['Id'])+' '
            #    count+=1
            #    if count == 10:
            #        break
            #await log_channel.send(temp_str+'\n'+str(datetime.datetime.now()))                        
            ##################
            count = 0
            for x in news_latest_check:
                check_mark = 0
                for y in news_latest:
                    if y['Id'] == x['Id']:
                        check_mark = 1
                        break
                if check_mark == 0:
                    overall_check_mark = 1
                    soup = BeautifulSoup(x['Body'],'html.parser')
                    text_reminder = soup.text
                    try:
                        myembed = discord.Embed(title=x['Title'], color=10181046)
                        myembed.set_author(name="新公告", icon_url=cfg.icon_url)
                        
                        passage = 1
                        max_length = 500
                        while len(text_reminder) > max_length:
                            location = text_reminder[max_length:].find('\n')
                            text_reminder_cut = text_reminder[0:max_length+location+1]
                            myembed.add_field(name='公告第' + str(passage) + '段', value=text_reminder_cut, inline=False)
                            text_reminder = text_reminder[max_length+location+1:]
                            passage += 1
                        if passage > 1:
                            myembed.add_field(name='公告第' + str(passage) + '段', value=text_reminder, inline=False)
                        else:
                            myembed.add_field(name='公告內容', value=text_reminder, inline=False)
                        await reminder_channel.send(embed=myembed)
                    except:
                        text_reminder = soup.text
                        await reminder_channel.send('```' + '新公告:' + x['Title'] + '```')
                        
                        passage = 1
                        while len(text_reminder) > 1500:
                            location = text_reminder[1500:].find('\n')
                            text_reminder_cut = text_reminder[0:1500+location+1]
                            await reminder_channel.send('```\n公告第' + str(passage) + '段:\n' + text_reminder_cut + '\n```')
                            text_reminder = text_reminder[1500+location+1:]
                            passage += 1
                        if passage > 1:
                            await reminder_channel.send('```\n公告第' + str(passage) + '段:\n' + text_reminder + '\n```')
                        else:
                            await reminder_channel.send('```\n' + text_reminder + '\n```')
                count += 1
                if count == 10:
                    break
            if overall_check_mark == 1:
                news_latest = news_latest_check.copy()
            overall_check_mark = 0
            news_i = 1
            
            for x in news_now_check:
                check_mark = 0
                for y in news_now:
                    if y['ImagePath'] == x['ImagePath']:
                        check_mark = 1
                        break
                if check_mark == 0:
                    overall_check_mark = 1                    
                    img_url = 'https://web-assets.otogi-frontier.com/static/sp/Banner/Info/' + x['ImagePath']
                    img_url2 = 'https://az-otogi-web-assets.azureedge.net/static/sp/Banner/Info/' + x['ImagePath']
                    try:
                        img = await get_img(img_url)
                        img.save('news.png')
                        file1 = discord.File('news.png',filename='news.png')
                        file2 = discord.File('news.png',filename='news.png')
                        myembed = discord.Embed(title='【#' + str(news_i) + '】', color=10181046)
                        myembed.set_author(name="新活動和轉蛋", icon_url=cfg.icon_url)                
                        myembed.set_image(url="attachment://news.png")
                        await reminder_channel_alt.send(file=file1, embed=myembed)
                        await reminder_channel.send(file=file2, embed=myembed)
                        news_i += 1
                    except:
                        try:
                            img = await get_img(img_url2)
                            img.save('news.png')
                            file1 = discord.File('news.png',filename='news.png')
                            file2 = discord.File('news.png',filename='news.png')
                            myembed = discord.Embed(title='【#' + str(news_i) + '】', color=10181046)
                            myembed.set_author(name="新活動和轉蛋", icon_url=cfg.icon_url)                
                            myembed.set_image(url="attachment://news.png")
                            await reminder_channel_alt.send(file=file1, embed=myembed)
                            await reminder_channel.send(file=file2, embed=myembed)
                            news_i += 1
                        except:
                            await starting_channel.send('獲取活动圖片失敗')
                            await starting_channel.send(img_url)
                            await starting_channel.send(img_url2)
            if overall_check_mark == 1:
                news_now = news_now_check.copy()
            overall_check_mark = 0
