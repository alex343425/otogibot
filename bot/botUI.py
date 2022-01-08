import discord
import asyncio
import requests
import cfg
from nick import matchnick, loadnick, loadsp
from idparse import check_sc, check_sa, isinforward, isinor, isinbackward, isindamage, isininterval, isinand, setskilltype, skillclass, weaponclass, skillrank, attribute
from cgunity import cg_extract
from parseskills import skillsourcecate,skillsourcecate_tw, updatemfiles
from PIL import Image
from io import BytesIO

async def utilityUI(message,bot):
    if message.content.startswith('!ping'):
        await message.channel.send('pong!')
        return

async def funUI(message,bot):
    if message.content.startswith('?rotate'):
        try:
            degree = int(message.content.lower().split(' ')[1])
            msg_id = message.content.lower().split('/')[-1]
            msg = await message.channel.fetch_message(msg_id)
            msg_attach = msg.attachments
            async def get_img(img_url):
                return Image.open(BytesIO(requests.get(img_url).content))
            img = await get_img(msg_attach[0].url)
            img.rotate(degree, expand=1).save('temp.png')
            file = discord.File('temp.png',filename='temp.png')
            await message.channel.send(file=file)
        except:
            await message.channel.send('格式錯誤')
        return
  
async def privateUI(message,bot):
    nickname = message.author.name
    if message.content.startswith('?getcg'):
        cg_id = message.content.lower().split(' ')[1]
        if cg_id[0] != '2' or len(cg_id) != 6:
            await message.channel.send('格式錯誤')
            return
        try:
            cgname = cg_extract(cg_id)
            cgname += '.zip'
        except:
            await message.channel.send('錯誤')
            return
        imagezip = discord.File(cgname,filename=cgname)
        img_message = await message.channel.send(file=imagezip)
        return
  
    if message.content.startswith('?inspect'):
        user_id = message.content.lower().split(' ')[1]
        async def get_img(img_url):
            return Image.open(BytesIO(requests.get(img_url).content))
        embed_list = []
        for i in range(0,7):
            url = 'https://api-pc.otogi-frontier.com/api/UFriend/Deck/'+user_id+'/'+str(i)
            
            try:
                party = requests.get(url, headers={'token': cfg.token_jp}).json()
            except:
                await message.channel.send('錯誤 請回報BUG')
                return
            if i == 5:
                title_text = '十人隊伍'
            elif i == 6:
                title_text = '迷宮隊伍'
            else:
                title_text = '隊伍'+str(i+1)
            myembed = discord.Embed(title='用戶ID:'+str(user_id), description=title_text, color=10181046)
            if i == 5:
                mylst = [[],[],[],[],[],[],[],[],[],[],[],[]]
                canvas = Image.new('RGB', (912,332))
            else:
                mylst = [[],[],[],[],[],[]]
                canvas = Image.new('RGB', (912,166))
            for x in party['UParty']['UParties']:
                pos = x['Position']
                text = '【角色名】:'
                y = x['UMonster']
                try:
                    char_url = 'https://otogimigwestsp.blob.core.windows.net/prodassets/SpBrowser/BustShot/'+str(y['MMonsterId'])+'.png?96'
                    char_img = await get_img(char_url)
                    if pos < 7:
                        canvas.paste(char_img,(152*(pos-1),0))
                    else:
                        canvas.paste(char_img,(152*(pos-7),166))
                except:
                    pass
                try:
                    text += next(z for z in cfg.MMonsters if z['id'] == y['MMonsterId'])['n']+'\n'
                except:
                    text += '\n'
                text += '【拆技1】:'
                try:
                    text += next(z for z in cfg.MSkills if z['id'] == y['Sub1']['MSkillId'])['n']+'\n'
                except:
                    text += '\n'
                text += '【拆技2】:'
                try:
                    text += next(z for z in cfg.MSkills if z['id'] == y['Sub2']['MSkillId'])['n']+'\n'
                except:
                    text += '\n'
                text += '【拆技3】:'
                try:
                    text += next(z for z in cfg.MSkills if z['id'] == y['Sub3']['MSkillId'])['n']+'\n'
                except:
                    text += '\n'
                text += '【武器】:'
                try:
                    text += next(z for z in cfg.MWeapons if z['id'] == y['UWeapon']['MWeaponId'])['n']+'\n'
                except:
                    text += '\n'
                text += '【飾品】:'
                try:
                    text += next(z for z in cfg.MAccessory if z['id'] == y['UAccessory']['MAccessoryId'])['n']+'\n'
                except:
                    pass
                try:
                    mylst[pos-1] = text
                except:
                    pass
            leader = 0
            for x in mylst:
                if x != [] and leader == 0:
                    myembed.add_field(name='隊长', value=x, inline=False)
                if x != [] and leader > 0:
                    myembed.add_field(name='隊員'+str(leader), value=x, inline=False)
                leader += 1
            canvas.save('team.png')
            image_channel = bot.get_channel(855880309853126696)
            picture = discord.File('team.png',filename='team.png')
            img_message = await image_channel.send(file=picture)
            myembed.set_image(url=img_message.attachments[0].url)
            embed_list.append(myembed)
      
        channel = message.channel
        disp_num = 0
        n = len(embed_list)
        if n == 0:
            await message.channel.send('沒有找到任何結果')
            return
        else:
            reactions = ['<:aleft:855895123644907531>',
                         '<:aright:855895123224035358>']
        try:
            char_msg = await message.channel.send(embed=embed_list[disp_num])
        except:
            await message.channel.send('錯誤 請回報BUG')
            return
        for react in reactions:
            await char_msg.add_reaction(react)
        while True:
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=300.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    disp_num = disp_num - 1
                    if disp_num == -1:
                        disp_num = n-1
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    disp_num = disp_num + 1
                    if disp_num == n:
                        disp_num = 0
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
        return
  
    if message.content.lower().startswith('?beid'):
        try:
            url = 'https://api-pc.otogi-frontier.com/api/Events/17001/ranking/'
            response = requests.get(url, headers={'token': cfg.token_jp})
        except:
            await message.channel.send('找不到相應信息')
            return
        if message.content.lower().startswith('?beidlast'):
            title = response.json()["PreviousWeekQuestName"]
            ranking = response.json()["PreviousWeekTopPlayers"]
        else:
            title = response.json()["ThisWeekQuestName"]
            ranking = response.json()["ThisWeekTopPlayers"]
        
        text_jp_1 = ''
        text_jp_2 = ''
        text_jp_3 = ''
        for x in ranking:
            text_temp = str(x["Rank"]) + ':' + '**' + x["Name"] + '**'
            try:
                text_temp += '  ID:' + str(x["UUserId"]) + '  Level:' + str(x["Level"])
            except:
                pass
            num = x["Score"]
            num_dis = f"{num:,}"
            text_temp += '\n' + 'Score:' + num_dis + '\n'
            if x["Rank"] < 11:
              text_jp_1 += text_temp
            elif x["Rank"] < 21:
              text_jp_2 += text_temp
            else:
              text_jp_3 += text_temp
        
        myembed = discord.Embed(title='競技場標題:' + title, color=10181046)
        myembed.set_thumbnail(url="https://media.discordapp.net/attachments/649188205509345290/804836609244790794/be.png")
        myembed.add_field(name="排名1-10", value=text_jp_1, inline=False)
        myembed.add_field(name="排名11-20", value=text_jp_2, inline=False)
        myembed.add_field(name="排名21-30", value=text_jp_3, inline=False)
        myembed.set_footer(text=nickname + "的請求")
      
        try:
            await message.channel.send(embed=myembed)
        except:
            await message.channel.send('錯誤 請回報BUG')
        return
    
    if message.content.lower().startswith('?loadnick'):
        await message.channel.send('Updating...')
        loadnick()
        await message.channel.send('Updated.')
        return
        
    if message.content.lower().startswith('?loadsp'):
        await message.channel.send('Updating...')
        loadsp()
        await message.channel.send('Updated.')
        return
        
    if message.content.lower().startswith('?update'):
        await message.channel.send('Updating...')
        updatemfiles()
        await message.channel.send('檔案讀取完成')
        skillsourcecate()
        await message.channel.send('日版技能整理完成')
        skillsourcecate_tw()
        await message.channel.send('台版技能整理完成')
        await message.channel.send('Updated.')
        return
        
    if message.content.lower().startswith('?labyrinth'):
        def get_img(img_url):
            return Image.open(BytesIO(requests.get(img_url).content))
        url = cfg.addressHead3 + 'Dungeons/1'
        try:
            labyrinth = requests.get(url, headers={'token': cfg.token_jp}).json()
        except:
            await message.channel.send('未找到迷宮信息')
            return
        
        space = 39
        red_mark = get_img('https://cdn.discordapp.com/emojis/807226965891088404.png').resize((36,36))
        canvas = get_img('https://cdn.discordapp.com/attachments/806469332116308039/807655253075034132/canvas.png')
        
        myembed = discord.Embed(title='迷宮關卡要求', color=10181046)
        myembed.set_footer(text=nickname + "的請求")
        
        j = 1
        for x in labyrinth['Quests']:
            q_id = str(x['Id'])
            url = cfg.addressHead3 + 'Quests/' + q_id
            quest_dis = requests.get(url, headers={'token': cfg.token_jp}).json()
            myembed.add_field(name=quest_dis['Name'], value=quest_dis['Missions'][0]['Name']+'\n'+quest_dis['Missions'][1]['Name']+'\n'+quest_dis['Missions'][2]['Name'], inline=False)
            common_quest = ''
            if '一人も倒' in quest_dis['Missions'][0]['Name'] or 'ターン' in quest_dis['Missions'][0]['Name']:
                common_quest += quest_dis['Missions'][0]['Name']
            if '一人も倒' in quest_dis['Missions'][1]['Name'] or 'ターン' in quest_dis['Missions'][1]['Name']:
                common_quest += '\n' + quest_dis['Missions'][1]['Name']
            if '一人も倒' in quest_dis['Missions'][2]['Name'] or 'ターン' in quest_dis['Missions'][2]['Name']:
                common_quest += '\n' + quest_dis['Missions'][2]['Name']
            sentence = quest_dis['Missions'][0]['Name']
            i = 1
            if '以外' in sentence:
                if '属性' in sentence:
                    for x in '火水樹光闇':
                        if x in sentence:
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
                else:
                    pass
                i = 6
                if '属性' in sentence:
                    pass
                else:
                    for x in '剣斧槍本杖短弓特':
                        if x == '剣':
                            n = sentence.find('剣')
                            if n == -1:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                            else:
                                pass
                        else:
                            if x in sentence:
                                pass
                            else:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
            else:
                for x in '火水樹光闇':
                    if x in sentence:
                        canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        pass
                    i += 1
                i = 6
                for x in '剣斧槍本杖短弓特':
                    if x == '剣':
                        n = sentence.find('剣')
                        if n == -1 or (n != -1 and sentence[n-1] == '短'):
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        if x in sentence:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        else:
                            pass
                    i += 1
            sentence = quest_dis['Missions'][1]['Name']
            i = 1
            if '以外' in sentence:
                if '属性' in sentence:
                    for x in '火水樹光闇':
                        if x in sentence:
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
                else:
                    pass
                i = 6
                if '属性' in sentence:
                    pass
                else:
                    for x in '剣斧槍本杖短弓特':
                        if x == '剣':
                            n = sentence.find('剣')
                            if n == -1:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                            else:
                                pass
                        else:
                            if x in sentence:
                                pass
                            else:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
            else:
                for x in '火水樹光闇':
                    if x in sentence:
                        canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        pass
                    i += 1
                i = 6
                for x in '剣斧槍本杖短弓特':
                    if x == '剣':
                        n = sentence.find('剣')
                        if n == -1 or (n != -1 and sentence[n-1] == '短'):
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        if x in sentence:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        else:
                            pass
                    i += 1
            sentence = quest_dis['Missions'][2]['Name']
            i = 1
            if '以外' in sentence:
                if '属性' in sentence:
                    for x in '火水樹光闇':
                        if x in sentence:
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
                else:
                    pass
                i = 6
                if '属性' in sentence:
                    pass
                else:
                    for x in '剣斧槍本杖短弓特':
                        if x == '剣':
                            n = sentence.find('剣')
                            if n == -1:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                            else:
                                pass
                        else:
                            if x in sentence:
                                pass
                            else:
                                canvas.paste(red_mark,(1+space*i,1+space*j))
                        i += 1
            else:
                for x in '火水樹光闇':
                    if x in sentence:
                        canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        pass
                    i += 1
                i = 6
                for x in '剣斧槍本杖短弓特':
                    if x == '剣':
                        n = sentence.find('剣')
                        if n == -1 or (n != -1 and sentence[n-1] == '短'):
                            pass
                        else:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                    else:
                        if x in sentence:
                            canvas.paste(red_mark,(1+space*i,1+space*j))
                        else:
                            pass
                    i += 1
            j += 1
        myembed.add_field(name='共通條件', value=common_quest, inline=False)
        canvas.save('canvas.png')
        file = discord.File('canvas.png',filename='canvas.png')
        myembed.set_image(url="attachment://canvas.png")
        await message.channel.send(file=file, embed=myembed)
        return
    return

async def publicUI(message,bot):
    nickname = message.author.name
    if message.content.lower().startswith('?skill') or message.content.lower().startswith('？skill') or message.content.startswith('?skitw') or message.content.startswith('？skitw'):
        keyword = message.content.split(' ')
        n = len(keyword)
        keyword[0] = keyword[0].replace('？','?')
        cate = keyword[0][6:]
        keyword = message.content.lower().split(' ')[1:n]
        
        if len(keyword) == 0:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
  
        kw_dis = ''
        for k in keyword:
            kw_dis += k + ' '
        
        embed_list = []
        skill_id_list = []
        list_num = 1
        page_num = 1
        myembed = discord.Embed(title='技能搜索結果', description='關鍵字:' + kw_dis, color=10181046)
        myembed.set_footer(text='↓用箭頭翻頁。 '+nickname + "的請求")
        #不重複結果
        
        skill_for_search=[]
        if message.content.startswith('?skitw'):
            skill_for_search = cfg.MSkills_tw
        else:
            skill_for_search = cfg.MSkills
        
        
        norepeated=[]
        for x in skill_for_search:
            if x['l'] != x['ml'] and x['ml']<=6:
                continue
  
            count = 1
            for k in '01234':
                if k in cate:
                    count = 0
            if count == 0:
                if check_sc(x['sc'],cate):
                    pass
                else:
                    continue
  
            count = 1 
            for k in '56789':
                if k in cate:
                    count = 0
            if count == 0:
                if check_sa(x['a'],cate):
                    pass
                else:
                    continue
  
            skillsource = x['tm']
            skillcate = x['tc']
            sourcename = x['sp']
            

            
            count = 1
            for k in 'QWERTYUIASDFG':
                if k in cate:
                    count = 0
            if count == 0:
                letter_position = sourcename.find('【')
                if letter_position == -1:
                    continue
                source_category = sourcename[letter_position:]
                if 'Q' in cate:
                    if '劍' in source_category and '短劍' not in source_category:
                        pass
                    else:
                        continue
                if 'W' in cate:
                    if '斧' in source_category:
                        pass
                    else:
                        continue
                if 'E' in cate:
                    if '槍' in source_category:
                        pass
                    else:
                        continue
                if 'R' in cate:
                    if '本' in source_category:
                        pass
                    else:
                        continue
                if 'T' in cate:
                    if '杖' in source_category:
                        pass
                    else:
                        continue
                if 'Y' in cate:
                    if '短劍' in source_category:
                        pass
                    else:
                        continue
                if 'U' in cate:
                    if '弓' in source_category:
                        pass
                    else:
                        continue
                if 'I' in cate:
                    if '特殊' in source_category:
                        pass
                    else:
                        continue
                if 'A' in cate:
                    if '火' in source_category:
                        pass
                    else:
                        continue
                if 'S' in cate:
                    if '水' in source_category:
                        pass
                    else:
                        continue
                if 'D' in cate:
                    if '樹' in source_category:
                        pass
                    else:
                        continue
                if 'F' in cate:
                    if '光' in source_category:
                        pass
                    else:
                        continue
                if 'G' in cate:
                    if '闇' in source_category:
                        pass
                    else:
                        continue
            
            count = 1
            for k in 'iatsuvxwlnro':
                if k in cate:
                    count = 0
            if count == 0:
                if skillcate in cate:
                    pass
                else:
                    continue
            
            
            if 'f' in cate:
                search_result = isinforward(keyword,x['d'])
            elif 'g' in cate:
                search_result = isinor(keyword,x['n']+x['d'])
            elif 'h' in cate:
                search_result = isinbackward(keyword,x['d'])
            elif 'd' in cate:
                search_result = isindamage(keyword,x['d'])
            elif 'e' in cate:
                search_result = isininterval(keyword,x['d'])
            elif 'z' in cate:####不重複
                if x['tm'] in norepeated:
                    search_result = False
                else:
                    search_result = isinand(keyword,x['d'])
                    if search_result == True:
                        norepeated.append(x['tm'])
            else:
                search_result = isinand(keyword,x['n']+x['d'])
  
            if search_result:
                name_jp = str(list_num) + '.技能名:' + x['n'] + '【' + setskilltype(skillcate)
                name_jp += '】' + skillclass(x['sc']) + skillrank(x['sr']) 
                text_jp = '效果:' + x['d'] + '\n'
                if skillsource > 0:
                    text_jp += '技能來源:' + sourcename + '\n'
                skill_id_list.append(skillsource)
                myembed.add_field(name=name_jp, value=text_jp, inline=False)
                list_num += 1
                if list_num == 6:
                    list_num = 1
                    myembed.set_author(name='頁:' + str(page_num))
                    page_num += 1
                    embed_list.append(myembed)
                    myembed = discord.Embed(title='技能搜索結果', description='關鍵字:' + kw_dis, color=10181046)
                    myembed.set_footer(text=nickname + "的請求")
                      
        if list_num > 1:
            myembed.set_author(name='頁:' + str(page_num))
            embed_list.append(myembed)
            
            
        reactions = ['<:aleft:855895123644907531>',
                     '<:aright:855895123224035358>',
                     '<:1_:855895123052331039>',
                     '<:2_:855895123148668928>',
                     '<:3_:855895123628130354>',
                     '<:4_:855895123069239367>',
                     '<:5_:855895122926108693>']
        
        channel = message.channel
        disp_num = 0
        skill_id = 0
        n = len(embed_list)
        if n == 0:
            await message.channel.send('沒有找到任何結果')
            return
        if n == 1:
            reactions = ['<:1_:855895123052331039>',
                         '<:2_:855895123148668928>',
                         '<:3_:855895123628130354>',
                         '<:4_:855895123069239367>',
                         '<:5_:855895122926108693>']
        try:
            char_msg = await message.channel.send(embed=embed_list[disp_num])
        except:
            await message.channel.send('錯誤 請回報BUG')
            return
        for react in reactions:
            await char_msg.add_reaction(react)
        while True:
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    disp_num -= 1
                    skill_id -= 5
                    if disp_num == -1:
                        skill_id += 5*n
                        disp_num = n-1
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    disp_num += 1
                    skill_id += 5
                    if disp_num == n:
                        disp_num = 0
                        skill_id = 0
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:1_:855895123052331039>':
                    try:
                        if skill_id_list[skill_id] == 0:
                            continue
                    except:
                        continue
                    try:
                        img_url = cfg.addresschar1 + str(skill_id_list[skill_id]) + '.png?96'
                        embed_list[disp_num].set_thumbnail(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        pass
                if str(reaction.emoji) == '<:2_:855895123148668928>':
                    try:
                        if skill_id_list[skill_id+1] == 0:
                            continue
                    except:
                        continue
                    try:
                        img_url = cfg.addresschar1 + str(skill_id_list[skill_id+1]) + '.png?96'
                        embed_list[disp_num].set_thumbnail(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        pass
                if str(reaction.emoji) == '<:3_:855895123628130354>':
                    try:
                        if skill_id_list[skill_id+2] == 0:
                            continue
                    except:
                        continue
                    try:
                        img_url = cfg.addresschar1 + str(skill_id_list[skill_id+2]) + '.png?96'
                        embed_list[disp_num].set_thumbnail(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        pass
                if str(reaction.emoji) == '<:4_:855895123069239367>':
                    try:
                        if skill_id_list[skill_id+3] == 0:
                            continue
                    except:
                        continue
                    try:
                        img_url = cfg.addresschar1 + str(skill_id_list[skill_id+3]) + '.png?96'
                        embed_list[disp_num].set_thumbnail(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        pass
                if str(reaction.emoji) == '<:5_:855895122926108693>':
                    try:
                        if skill_id_list[skill_id+4] == 0:
                            continue
                    except:
                        continue
                    try:
                        img_url = cfg.addresschar1 + str(skill_id_list[skill_id+4]) + '.png?96'
                        embed_list[disp_num].set_thumbnail(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        pass
        return
    
    if message.content.lower().startswith('?char') or message.content.lower().startswith('？char') or message.content.lower().startswith('?nick') or message.content.lower().startswith('？nick'):
        keyword = message.content.lower().split(' ')
        n = len(keyword)
        keyword = keyword[1:n]
        
        if len(keyword) == 0:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
      
        nick_list=[]
        
        if message.content.lower().startswith('?nick') or message.content.lower().startswith('？nick') or message.content.lower().startswith('?nicktw') or message.content.lower().startswith('？nicktw'):
            nick_list = matchnick(keyword)
            if nick_list == 0:
                await message.channel.send('沒有找到任何結果')
                return
        
        kw_dis = ''
        for k in keyword:
            kw_dis += k + ' '
            
        embed_list = []
        rmid_list = []
        
        monsters_for_search=[]
        skill_for_search=[]
        weapons_for_search=[]
        accessory_for_search=[]
        if 'tw' in message.content.lower().split(' ')[0]:
            monsters_for_search = cfg.MMonsters_tw
            skill_for_search = cfg.MSkills_tw
            weapons_for_search = cfg.MWeapons_tw
            accessory_for_search = cfg.MAccessory_tw
        else:
            monsters_for_search = cfg.MMonsters
            skill_for_search = cfg.MSkills
            weapons_for_search = cfg.MWeapons
            accessory_for_search = cfg.MAccessory
        
        for x in monsters_for_search:
            if ( isinand(keyword,str(x['id'])[1:4]+x['n'])  or str(x['id']) in nick_list ) and x['ce'] == x['me']:
                myembed = discord.Embed(title='角色搜索結果', description='關鍵字:' + kw_dis, color=10181046)
                myembed.set_footer(text=nickname + "的請求")
                for y in skill_for_search:
                    if y['rsid'] == x['lsid']:
                        myembed.add_field(name="【隊長技】" + y['n'], value=y['d'], inline=False)
                        break
                
                for y in skill_for_search:
                    if y['rsid'] == x['vsid']:
                        if y['l'] == y['ml'] and y['d'] != '':
                            myembed.add_field(name='【' + setskilltype(y['tc']) + '】' + y['n'] + ':' + skillclass(y['sc']) + skillrank(y['sr']), value=y['d'], inline=False)
                for y in weapons_for_search:
                    if y['rmid'] == x['rmid']:
                        for z in skill_for_search:
                            if z['rsid'] == y['msid']:
                                myembed.add_field(name="【專武】" + z['n'], value=z['d'], inline=False)
                for y in accessory_for_search:
                    if 'の絆' in y['n']:
                        continue
                    if y['rmid'] == x['rmid']:
                        myembed.add_field(name="【專飾品】" + y['n'], value=y['d'], inline=False)
                
                
                sp_classify=''
                for y in cfg.spjson:
                    if str(x['rmid']) == str(y['id']):
                        sp_classify='('+y['classify']+')'
                        break
                        
                name_dis = '(' + str(x['rmid']) + sp_classify+ x['n'] + ':' + str(x['r']) + '星'
                name_dis += attribute(x['a']) + weaponclass(x['wc']) + '  技能格子:'
                name_dis += skillclass(x['sc1']) + skillrank(x['sr1'])
                name_dis += skillclass(x['sc2']) + skillrank(x['sr2'])
                name_dis += skillclass(x['sc3']) + skillrank(x['sr3'])
                
                myembed.set_author(name=name_dis)
                try:
                    img_url_1 = cfg.addresschar1 + str(x['rmid']) + '.png?96'
                    img_url_2 = cfg.addresschar2 + str(x['rmid']) + '.png?97'
                    myembed.set_thumbnail(url=img_url_1)
                    myembed.set_image(url=img_url_2)
                except:
                    await message.channel.send('角色' + str(x['rmid']) + '未找到頭像')
                embed_list.append(myembed)
                rmid_list.append(x['rmid'])
                
        reactions = ['<:aleft:855895123644907531>',
                     '<:aright:855895123224035358>',
                     '<:1_:855895123052331039>',
                     '<:2_:855895123148668928>',
                     '<:3_:855895123628130354>',
                     '<:4_:855895123069239367>',
                     '<:5_:855895122926108693>']
        channel = message.channel
        disp_num = 0
        n = len(embed_list)
        if n == 0:
            await message.channel.send('沒有找到任何結果')
            return
        if n == 1:
            reactions = ['<:1_:855895123052331039>',
                         '<:2_:855895123148668928>',
                         '<:3_:855895123628130354>',
                         '<:4_:855895123069239367>',
                         '<:5_:855895122926108693>']
        try:
            char_msg = await message.channel.send(embed=embed_list[disp_num])
        except:
            await message.channel.send('錯誤 請回報BUG')
            return
            
        for react in reactions:
            await char_msg.add_reaction(react)
        while True:
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    disp_num = disp_num - 1
                    if disp_num == -1:
                        disp_num = n-1
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    disp_num = disp_num + 1
                    if disp_num == n:
                        disp_num = 0
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:1_:855895123052331039>':
                    try:
                        img_url = cfg.addresschar2 + str(rmid_list[disp_num]) + '.png?97'
                        embed_list[disp_num].set_image(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:2_:855895123148668928>':
                    try:
                        img_url = cfg.addresschar2 + str(rmid_list[disp_num]+1) + '.png?97'
                        embed_list[disp_num].set_image(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:3_:855895123628130354>':
                    try:
                        img_url = cfg.addresschar2 + str(rmid_list[disp_num]+2) + '.png?97'
                        embed_list[disp_num].set_image(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:4_:855895123069239367>':
                    try:
                        img_url = cfg.addresschar2 + str(rmid_list[disp_num]+3) + '.png?97'
                        embed_list[disp_num].set_image(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:5_:855895122926108693>':
                    try:
                        img_url = cfg.addresschar2 + str(rmid_list[disp_num]+4) + '.png?97'
                        embed_list[disp_num].set_image(url=img_url)
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
        return
      
    if message.content.lower().startswith('?spirit') or message.content.lower().startswith('？spirit'):
        keyword = message.content.lower().split(' ')
        n = len(keyword)
        keyword = keyword[1:n]
        
        if len(keyword) == 0:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
        
        kw_dis = ''
        for k in keyword:
            kw_dis += k + ' '
            
        embed_list = []
        
        for x in cfg.MSpirits:
            if isinor(keyword,str(x['id'])[1:4]+x['n']) and x['ce'] == x['me']:
                myembed = discord.Embed(title='精靈搜索結果', description='關鍵字:' + kw_dis, color=10181046)
                myembed.set_footer(text=nickname + "的請求")
                for y in cfg.MSkills:
                    if y['l'] != y['ml']:
                       continue
                    if y['rsid'] == x['psid']:
                        myembed.add_field(name="【被動技】" + y['n'], value=y['d'], inline=False)
                        break
                for y in cfg.MSkills:
                    if y['l'] != y['ml']:
                       continue
                    if y['rsid'] == x['sid1']:
                        myembed.add_field(name="【主動技1】" + y['n'], value=y['d'], inline=False)
                    if y['rsid'] == x['sid2']:
                        myembed.add_field(name="【主動技2】" + y['n'], value=y['d'], inline=False)
                    if y['rsid'] == x['sid3']:
                        myembed.add_field(name="【主動技3】" + y['n'], value=y['d'], inline=False)
                
                name_dis = '(' + str(x['rsid']) + ')' + x['n'] + ':' + str(x['r']) + '星' + attribute(x['a'])
                
                myembed.set_author(name=name_dis)
                try:
                    img_url_1 = cfg.addresschar1 + str(x['rsid']) + '.png?96'
                    img_url_2 = cfg.addresschar2 + str(x['rsid']) + '.png?97'
                    myembed.set_thumbnail(url=img_url_1)
                    myembed.set_image(url=img_url_2)
                except:
                    await message.channel.send('精靈' + str(x['rsid']) + '未找到頭像')
                embed_list.append(myembed)
                
        reactions = ['<:aleft:855895123644907531>',
                     '<:aright:855895123224035358>']
        channel = message.channel
        disp_num = 0
        n = len(embed_list)
        if n == 0:
            await message.channel.send('沒有找到任何結果')
            return
        try:
            char_msg = await message.channel.send(embed=embed_list[disp_num])
        except:
            await message.channel.send('錯誤 請回報BUG')
            return
        if n == 1:
            return
        for react in reactions:
            await char_msg.add_reaction(react)
        while True:
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    disp_num = disp_num - 1
                    if disp_num == -1:
                        disp_num = n-1
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    disp_num = disp_num + 1
                    if disp_num == n:
                        disp_num = 0
                    try:
                        await char_msg.edit(embed=embed_list[disp_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
        return
    
    if message.content.lower().startswith('?be') or message.content.lower().startswith('？be'):
        if 'tw' in message.content.lower():
            try:
                url = 'https://otogi-traffic-dmm-tw.trafficmanager.net/api/Events/17001/ranking/'
                response = requests.get(url, headers={'token': cfg.token_cn})
            except:
                await message.channel.send('找不到相應信息')
                return
            
        else:
            try:
                url = 'https://api-pc.otogi-frontier.com/api/Events/17001/ranking/'
                response = requests.get(url, headers={'token': cfg.token_jp})
            except:
                await message.channel.send('找不到相應信息')
                return
            
        title = response.json()["ThisWeekQuestName"]
        ranking = response.json()["ThisWeekTopPlayers"]
        text_jp_1 = ''
        text_jp_2 = ''
        text_jp_3 = ''
        for x in ranking:
            text_temp = str(x["Rank"]) + ':' + '**' + x["Name"] + '**'
            try:
                text_temp += '  【' + x["Introduction"] + '】'
            except:
                pass
            num = x["Score"]
            num_dis = f"{num:,}"
            text_temp += '\n' + 'Score:' + num_dis + '\n'
            if x["Rank"] < 11:
              text_jp_1 += text_temp
            elif x["Rank"] < 21:
              text_jp_2 += text_temp
            else:
              text_jp_3 += text_temp
        
        myembed = discord.Embed(title='競技場標題:' + title, color=10181046)
        myembed.set_thumbnail(url="https://media.discordapp.net/attachments/649188205509345290/804836609244790794/be.png")
        myembed.add_field(name="排名1-10", value=text_jp_1, inline=False)
        myembed.add_field(name="排名11-20", value=text_jp_2, inline=False)
        myembed.add_field(name="排名21-30", value=text_jp_3, inline=False)
        myembed.set_footer(text=nickname + "的請求")
      
        try:
            await message.channel.send(embed=myembed)
        except:
            await message.channel.send('錯誤 請回報BUG')
        return
    if message.content.lower().startswith('?卡池') or message.content.lower().startswith('？卡池') :
        await message.channel.send('正在獲取資訊...')
        url = 'https://api-pc.otogi-frontier.com/api/UGachas/'
        r = requests.get(url,headers={'token': cfg.token_jp}).json()['AvailableGachas']
        l=[]
        for x in r:
            if x['Tabs'] == 2:
                l.append(x)
        result = ''
        for x in l:    
            r2 = requests.get(url+str(x['Id']),headers={'token': cfg.token_jp}).json()
            result += '卡池名：' + r2['Name']+'\nPU角:'
            for y in r2['DisplayItems']:
                y=y['ItemId']
                for z in cfg.spjson:
                    if int(z['id']) == y:
                        result += z['name_jp']+'('+z['classify']+') '
                        break
            result +='\n'
        try:
            await message.channel.send(result)
        except:
            await message.channel.send('錯誤 請回報BUG')
        return
        
        
    
    if message.content.lower().startswith('?story'):
        try:
            scene_num = int(message.content.split('?story')[1])
        except:
            myembed = discord.Embed(title='主線劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url=cfg.url_story)
            await message.channel.send(embed=myembed)
            return
        
        myembed = discord.Embed(title='主線劇情列表', color=10181046)
        myembed.set_footer(text=nickname + "的請求")
      
        try:
            if scene_num < 10:
                address = cfg.addressHead1 + '100' + str(scene_num)
                response = requests.get(address, headers={'token': cfg.token_jp})
            else:
                address = cfg.addressHead1 + '10' + str(scene_num)
                response = requests.get(address, headers={'token': cfg.token_jp})
          
            mydic = response.json()["Adventures"]
            text_jp = ''
            for x in mydic:
                text_jp += x["Name"]+':'+str(x["MSceneId"])+'\n'
            
            myembed.add_field(name=str(scene_num), value=text_jp, inline=False)
  
            try:
                await message.channel.send(embed=myembed)
            except:
                await message.channel.send('錯誤 請回報BUG')
                return
        except:
            await message.channel.send('找不到相應信息')
            return
        return
        
    if message.content.lower().startswith('?event'):
        if message.content.lower() == '?event17':
            myembed = discord.Embed(title='17年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806503947094589460/17.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event18a':
            myembed = discord.Embed(title='18年上半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806508037396234260/18a.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event18b':
            myembed = discord.Embed(title='18年下半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806510395220033556/18b.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event19a':
            myembed = discord.Embed(title='19年上半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806516245284651049/19a.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event19b':
            myembed = discord.Embed(title='19年下半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806518115738845194/19b.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event20a':
            myembed = discord.Embed(title='20年上半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806519052352618496/20a.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event20b':
            myembed = discord.Embed(title='20年下半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806520076814778378/20b.png')
            await message.channel.send(embed=myembed)
        elif message.content.lower() == '?event21a':
            myembed = discord.Embed(title='21年上半年活動劇情編號', color=10181046)
            myembed.set_footer(text=nickname + "的請求")
            myembed.set_image(url='https://cdn.discordapp.com/attachments/806494796079300628/806520257078362134/21a.png')
            await message.channel.send(embed=myembed)
        else:
            pass
        
        if message.content.lower() == '?eventtitle17':
            scene_num = 3
        elif message.content.lower() == '?eventtitle18a':
            scene_num = 4
        elif message.content.lower() == '?eventtitle18b':
            scene_num = 5
        elif message.content.lower() == '?eventtitle19a':
            scene_num = 6
        elif message.content.lower() == '?eventtitle19b':
            scene_num = 7
        elif message.content.lower() == '?eventtitle20a':
            scene_num = 8
        elif message.content.lower() == '?eventtitle20b':
            scene_num = 9
        elif message.content.lower() == '?eventtitle21a':
            scene_num = 10
        elif message.content.lower() == '?eventtitle21b':
            scene_num = 11
        else:
            return
  
        char_msg = await message.channel.send('稍等...')
        
        myembed = discord.Embed(title='活動劇情列表', color=10181046)
        myembed.set_footer(text=nickname + "的請求")
      
        try:
            address = cfg.addressHead2 + str(scene_num)
            response = requests.get(address, headers={'token': cfg.token_jp})
          
            scene_list = response.json()
            chapter_title = '活動劇情列表'
            text_jp = ''
            for x in scene_list:
                j = str(x["Id"])
                address = cfg.addressHead1 + j
                response = requests.get(address, headers={'token': cfg.token_jp})
          
                mydic = response.json()["Adventures"]
                for x in mydic:
                    text_jp += x["Name"]+':'+str(x["MSceneId"])+'\n'
                    break
            
            myembed.add_field(name='列表', value=text_jp, inline=False)
      
            try:
                await char_msg.edit(embed=myembed)
            except:
                await message.channel.send('錯誤 請回報BUG')
                return
        except:
            await message.channel.send('找不到相應信息')
            return
        return
      
    if message.content.lower().startswith('!story'):
        try:
            scene_num = int(message.content.split(' ')[1])
            scene_num_old = -1
        except:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
        
        myembed_jp = discord.Embed(title='劇情', color=10181046)
        myembed_jp.set_footer(text=nickname + ":日文劇情")
        myembed_cn = discord.Embed(title='劇情', color=10181046)
        myembed_cn.set_footer(text=nickname + ":中文劇情")
        
        char_msg = await message.channel.send(embed=myembed_jp)
        
        reactions = ['<:aleft:855895123644907531>',
                     '<:aright:855895123224035358>',
                     '<:J_:855895123618693150>',
                     '<:C_:855895123270828054>',
                     '<:crossbutton:855895123031359518>']
        for react in reactions:
            await char_msg.add_reaction(react)
      
        channel = message.channel
        state = 0
        
        while True:
            if state == 0:
                myembed_jp = 0
                text_jp = ''
                list_num_jp = 1
                try:
                    address = cfg.url_jp + str(scene_num)
                    response = requests.get(address, headers={'token': cfg.token_jp})
              
                    mydic = response.json()["MSceneDetails"]
                    chapter_title = '#'+str(scene_num)+':'+response.json()["Title"]
                    myembed_jp = discord.Embed(title=chapter_title, color=10181046)
                    myembed_jp.set_footer(text=nickname + ":日文劇情")
                  
                    for x in mydic:
                        mystr = x["Name"]+':'+x["Phrase"]
                        mystr = mystr.replace("%user_name", "Human")+'\n'
                        text_jp += mystr
                      
                        list_num_jp += 1
                        if list_num_jp == 21:
                            list_num_jp = 1
                            myembed_jp.add_field(name='劇情', value=text_jp, inline=False)
                            text_jp = ''
                    if list_num_jp > 1:
                        myembed_jp.add_field(name='劇情', value=text_jp, inline=False)
                    await char_msg.edit(embed=myembed_jp)
                except:
                    await message.channel.send('#'+str(scene_num)+':'+'無日文劇情!')
                    scene_num = scene_num_old
                    if scene_num == -1:
                        return   
            else:
                myembed_cn = 0
                list_num_cn = 1
                text_cn = ''
                try:
                    address = cfg.url_cn + str(scene_num)
                    response = requests.get(address, headers={'token': cfg.token_cn})
              
                    mydic = response.json()["MSceneDetails"]
                    chapter_title = '#'+str(scene_num)+':'+response.json()["Title"]
                    myembed_cn = discord.Embed(title=chapter_title, color=10181046)
                    myembed_cn.set_footer(text=nickname + ":中文劇情")
                  
                    for x in mydic:
                        mystr = x["Name"]+':'+x["Phrase"]
                        mystr = mystr.replace("%user_name", "Human")+'\n'
                        text_cn += mystr
                      
                        list_num_cn += 1
                        if list_num_cn == 21:
                            list_num_cn = 1
                            myembed_cn.add_field(name='劇情', value=text_cn, inline=False)
                            text_cn = ''
                    if list_num_cn > 1:
                        myembed_cn.add_field(name='劇情', value=text_cn, inline=False)
                    await char_msg.edit(embed=myembed_cn)
                except:
                    await message.channel.send('#'+str(scene_num)+':'+'無中文劇情!')
                    if scene_num != scene_num_old:
                        scene_num = scene_num_old
                    else:
                        state = 0
                    scene_num = scene_num_old
  
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                scene_num_old = scene_num
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    scene_num -= 1
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    scene_num += 1
                if str(reaction.emoji) == '<:crossbutton:855895123031359518>':
                    await char_msg.delete()
                    return
                if str(reaction.emoji) == '<:J_:855895123618693150>':
                    state = 0
                if str(reaction.emoji) == '<:C_:855895123270828054>':
                    state = 1
        return
      
    if message.content.lower().startswith('!event'):
        try:
            scene_num_jp = int(message.content.split(' ')[1])
        except:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
        if scene_num_jp < 100000:
            await message.channel.send('格式錯誤 請仔細閱讀' + cfg.addresshelpdoc)
            return
        scene_num_cn = int(message.content.split(' ')[1])
        await message.channel.send('稍等...')
        myembed_list_jp = []
        myembed_list_cn = []
        
        upper_bound = 1
        while True:
            try:
                address = cfg.url_jp + str(scene_num_jp)
                response = requests.get(address, headers={'token': cfg.token_jp})
              
                mydic = response.json()["MSceneDetails"]
                chapter_title = '#'+str(scene_num_jp)+':'+response.json()["Title"]
                myembed_jp = discord.Embed(title=chapter_title, color=10181046)
                myembed_jp.set_footer(text=nickname + ":日文劇情")
                text_jp = ''
                list_num_jp = 1
                for x in mydic:
                    mystr = x["Name"]+':'+x["Phrase"]
                    mystr = mystr.replace("%user_name", "Human")+'\n'
                    text_jp += mystr
                      
                    list_num_jp += 1
                    if list_num_jp == 21:
                        list_num_jp = 1
                        myembed_jp.add_field(name='劇情', value=text_jp, inline=False)
                        text_jp = ''
                if list_num_jp > 1:
                    myembed_jp.add_field(name='劇情', value=text_jp, inline=False)
                myembed_list_jp.append(myembed_jp)
                scene_num_jp += 1
                upper_bound += 1
                if upper_bound == 30:
                    break
            except:
                break
        upper_bound = 1
        while True:
            try:
                address = cfg.url_cn + str(scene_num_cn)
                response = requests.get(address, headers={'token': cfg.token_cn})
              
                mydic = response.json()["MSceneDetails"]
                chapter_title = '#'+str(scene_num_cn)+':'+response.json()["Title"]
                myembed_cn = discord.Embed(title=chapter_title, color=10181046)
                myembed_cn.set_footer(text=nickname + ":中文劇情")
                text_cn = ''
                list_num_cn = 1
                for x in mydic:
                    mystr = x["Name"]+':'+x["Phrase"]
                    mystr = mystr.replace("%user_name", "Human")+'\n'
                    text_cn += mystr
                      
                    list_num_cn += 1
                    if list_num_cn == 21:
                        list_num_cn = 1
                        myembed_cn.add_field(name='劇情', value=text_cn, inline=False)
                        text_cn = ''
                if list_num_cn > 1:
                    myembed_cn.add_field(name='劇情', value=text_cn, inline=False)
                myembed_list_cn.append(myembed_cn)
                scene_num_cn += 1
                upper_bound += 1
                if upper_bound == 30:
                    break
            except:
                break
        
        n = len(myembed_list_jp)
        if n == 0:
            await message.channel.send('找不到相應信息')
        
        embed_list_num = 0
        char_msg = await message.channel.send(embed=myembed_list_jp[embed_list_num])
        
        m = len(myembed_list_cn)
        if  m == 0:
            reactions = ['<:aleft:855895123644907531>',
                         '<:aright:855895123224035358>',
                         '<:crossbutton:855895123031359518>']
        else:
            reactions = ['<:aleft:855895123644907531>',
                         '<:aright:855895123224035358>',
                         '<:J_:855895123618693150>',
                         '<:C_:855895123270828054>',
                         '<:crossbutton:855895123031359518>']
        for react in reactions:
            await char_msg.add_reaction(react)
      
        channel = message.channel
        state = 0
        
        while True:
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactions
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
            except asyncio.TimeoutError:
                cache_dung_msg = await channel.fetch_message(char_msg.id)
                for r in cache_dung_msg.reactions:
                    await r.remove(bot.user)
                return
            else:
                await reaction.remove(message.author)
                if str(reaction.emoji) == '<:aleft:855895123644907531>':
                    embed_list_num -= 1
                    if embed_list_num == -1:
                        if state == 0:
                            embed_list_num = n-1
                        else:
                            embed_list_num = m-1
                    try:
                        if state == 0:
                            await char_msg.edit(embed=myembed_list_jp[embed_list_num])
                        else:
                            await char_msg.edit(embed=myembed_list_cn[embed_list_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:aright:855895123224035358>':
                    embed_list_num += 1
                    if state == 0:
                        if embed_list_num == n:
                            embed_list_num = 0
                    else:
                        if embed_list_num == m:
                            embed_list_num = 0
                    try:
                        if state == 0:
                            await char_msg.edit(embed=myembed_list_jp[embed_list_num])
                        else:
                            await char_msg.edit(embed=myembed_list_cn[embed_list_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:crossbutton:855895123031359518>':
                    await char_msg.delete()
                    return
                if m == 0:
                    continue
                if str(reaction.emoji) == '<:J_:855895123618693150>':
                    state = 0
                    try:
                        await char_msg.edit(embed=myembed_list_jp[embed_list_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
                if str(reaction.emoji) == '<:C_:855895123270828054>':
                    state = 1
                    if embed_list_num > m-1:
                        await message.channel.send('#'+str(embed_list_num)+':'+'無中文劇情!')
                        state = 0
                        continue
                    try:
                        await char_msg.edit(embed=myembed_list_cn[embed_list_num])
                    except:
                        await message.channel.send('錯誤 請回報BUG')
                        return
        return 
    return
