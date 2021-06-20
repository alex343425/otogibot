import cfg
import requests
from idparse import weaponclass, attribute
from operator import itemgetter

addressS = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MSkills.json'
addressM = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MMonsters.json'
addressR = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MSpirits.json'
addressW = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MWeapons.json'
addressA = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MAccessory.json'
addressI = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MItems.json'
addressF = 'https://otogimigwestsp.blob.core.windows.net/prodassets/MasterData/MFoods.json'

def check_cate(rsid,xid,l,ml):
    if l < ml:
        return([0,'q','','m'])
    
    for y in cfg.MSpirits:
        if y['psid'] == rsid or y['sid1'] == rsid or y['sid2'] == rsid or y['sid3'] == rsid:
            return([y['rsid'],'r',y['n']+'【'+attribute(y['a'])+'】','m'])
    if ml == 1:
        for y in cfg.MMonsters:
            if y['lsid'] == rsid:
                spname = 'SP未知'
                for spindex in cfg.spjson:
                    if str(y['id']) == spindex['id']:
                        spname = spindex['classify']
                        break
                if y['r'] == 3:
                    spname = '3星'
                if y['r'] == 4:
                    spname = '4星'
                return([y['rmid'],'l',y['n']+'【'+attribute(y['a'])+weaponclass(y['wc'])+'】'+'【'+spname+'】','m'])
        for y in cfg.MWeapons:
            if y['msid'] == rsid:
                if y['rmid'] is None:
                    return([1,'n',y['n']+'【'+weaponclass(y['wc'])+'】','m'])
                else:
                    for z in cfg.MMonsters:
                        if z['rmid'] == y['rmid']:
                            spname = 'SP未知'
                            for spindex in cfg.spjson:
                                if str(z['id']) == spindex['id']:
                                    spname = spindex['classify']
                                    break
                            if z['r'] == 3:
                                spname = '3星'
                            if z['r'] == 4:
                                spname = '4星'
                            return([z['rmid'],'w',z['n']+'【'+attribute(z['a'])+weaponclass(z['wc'])+'】'+'【'+spname+'】','m'])
    else:
        return([0,'o','','m'])
    return([0,'q','','m'])

def skillsourcecate():
    for x in cfg.MMonsters:
        if x['ce'] != x['me']:
            continue
        spname = 'SP未知'
        for spindex in cfg.spjson:
            if str(x['id']) == spindex['id']:
                spname = spindex['classify']
                break
        if x['r'] == 3:
            spname = '3星'
            if x['me'] == 3:
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
            if x['me'] == 4:
                i = 1
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        if i == 1:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        else:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'u',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
        if x['r'] == 4:
            spname = '4星'
            if x['me'] == 4:
                i = 1
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        if i == 1:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        else:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
            if x['me'] == 5:
                i = 1
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        if i == 1:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        elif i == 2:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        else:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'u',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
        if x['r'] == 5:
            if x['me'] == 5:
                i = 1
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        if i == 1:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        elif i == 2:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        elif i == 3:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'t',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            i += 1
                        else:
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'s',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
            if x['me'] == 6:
                k = 0
                for y in cfg.MSkills:
                    if y['rsid'] == x['vsid'] and y['l'] == y['ml'] and y['d'] != '':
                        k += 1
            
                i = 1
                if k == 3:
                    for y in cfg.MSkills:
                        if y['rsid'] == x['vsid']:
                            if y['l'] != y['ml'] or y['d'] == '':
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                continue
                            if i == 1:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 2:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            else:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'u',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            
                if k == 5 or k == 4:
                    for y in cfg.MSkills:
                        if y['rsid'] == x['vsid']:
                            if y['l'] != y['ml'] or y['d'] == '':
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                continue
                            if i == 1:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 2:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 3:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'t',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 4:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'u',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            else:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'v',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            
                if k == 7 or k == 6:
                    for y in cfg.MSkills:
                        if y['rsid'] == x['vsid']:
                            if y['l'] != y['ml'] or y['d'] == '':
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                continue
                            if i == 1:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 2:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'a',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 3:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'t',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 4:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'s',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 5:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'u',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            elif i == 6:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'v',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                                i += 1
                            else:
                                [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'x',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']

    for x in cfg.MSkills:
        if x['er'] == 'm':
            continue
        [x['tm'],x['tc'],x['sp'],x['er']] = check_cate(x['rsid'],x['id'],x['l'],x['ml'])
        if x['tm'] == 0:
            x['tm']=9999999 
    
    cfg.MSkills = sorted(cfg.MSkills, key=itemgetter('tm'))
    for x in cfg.MSkills:
        if x['tm'] == 9999999:
            x['tm']=0
    

def updatemfiles():
    cfg.MSkills = requests.get(addressS).json()
    cfg.MMonsters = requests.get(addressM).json()
    cfg.MSpirits = requests.get(addressR).json()
    cfg.MWeapons = requests.get(addressW).json()
    cfg.MAccessory = requests.get(addressA).json()
