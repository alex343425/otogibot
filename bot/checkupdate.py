import discord
import datetime
import asyncio
import requests
import cfg
from numpy import size, array
from PIL import Image, ImageOps
from io import BytesIO
from bs4 import BeautifulSoup

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
    async def get_img(img_url):
        return Image.open(BytesIO(requests.get(img_url).content))
    try:
        news_latest = requests.get(cfg.addresslatest, headers={'token': cfg.token_jp}).json()
        news_now = requests.get(cfg.addressnow, headers={'token': cfg.token_jp}).json()
        maint_img = await get_img('https://otogimigwestsp.blob.core.windows.net/static/pc/maintenance/maintenance.png')
        ranking = requests.get('https://api-pc.otogi-frontier.com/api/Events/17001/ranking/', headers={'token': cfg.token_jp}).json()
        foobaa_level = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/10898', headers={'token': cfg.token_jp}).json()["Level"]
        failure = 0
    except:
        await starting_channel.send('獲取公告失敗')
        failure = 1
    
    [width, height] = size(maint_img)
    img_save = maint_img.crop((round(width/2),round(height/2),round(width/2)+20,round(height/2)+20))
    a_sum_old = 0
    for x in array(ImageOps.grayscale(img_save)):
        a_sum_old += sum(x)
    
    print("Logged in as {}({})".format(bot.user.name, bot.user.id))
    await starting_channel.send('Bot initiated.')
    reminder_channel = bot.get_channel(626708913257185280)
    reminder_channel_alt = bot.get_channel(624974729689694230)
    private_chat_channel = bot.get_channel(820282343247183882)
    be_update_channel = bot.get_channel(902930492683325440)
    debug_channel = bot.get_channel(855880392045363230)
    while True:
        if failure == 1:
            break
        await asyncio.sleep(30)
        current_time = str(datetime.datetime.now()).split(' ')
        if current_time[1][3:5] in ['03','08','13','18','23','28','33','38','43','48','53','58']:
            await asyncio.sleep(30)
            try:
                ranking_check = requests.get('https://api-pc.otogi-frontier.com/api/Events/17001/ranking/', headers={'token': cfg.token_jp}).json()
                foobaa_level_check = requests.get('https://api-pc.otogi-frontier.com/api/UFriend/Detail/10898', headers={'token': cfg.token_jp}).json()["Level"]
            except:
                continue
            try:
                if foobaa_level_check > foobaa_level:
                    text = 'foobaa等級變動.由' + str(foobaa_level) + '升為' + str(foobaa_level_check) + '.'
                    await private_chat_channel.send(text)
                    foobaa_level = foobaa_level_check
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
            await asyncio.sleep(30)
            try:
                news_latest_check = requests.get(cfg.addresslatest, headers={'token': cfg.token_jp}).json()
                news_now_check = requests.get(cfg.addressnow, headers={'token': cfg.token_jp}).json()
            except:
                await starting_channel.send('獲取公告失敗')
                continue
            count = 0
            overall_check_mark = 0
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
                news_latest = news_latest_check
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
                    img_url = 'https://otogimigwest.blob.core.windows.net/static/pc/Banner/Info/' + x['ImagePath'] + '?458'
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
                        await starting_channel.send('獲取活动圖片失敗')
                        await starting_channel.send(img_url)
            if overall_check_mark == 1:
                news_now = news_now_check
            try:
                maint_img = await get_img('https://otogimigwestsp.blob.core.windows.net/static/pc/maintenance/maintenance.png')
            except:
                await starting_channel.send('獲取維修圖片失敗')
                continue
            [width, height] = size(maint_img)
            img_save = maint_img.crop((round(width/2),round(height/2),round(width/2)+20,round(height/2)+20))
            a_sum_new = 0
            for x in array(ImageOps.grayscale(img_save)):
                a_sum_new += sum(x)
            if a_sum_new == a_sum_old:
                pass
            else:
                a_sum_old = a_sum_new
                maint_img.save('news.png')
                file = discord.File('news.png',filename='news.png')
                myembed = discord.Embed(title='網頁版', color=10181046)
                myembed.set_author(name="維修公告", icon_url=cfg.icon_url)
                myembed.set_image(url="attachment://news.png")
                await reminder_channel_alt.send(file=file, embed=myembed)