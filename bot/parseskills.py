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

addressS_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MSkills.json'
addressM_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MMonsters.json'
addressR_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MSpirits.json'
addressW_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MWeapons.json'
addressA_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MAccessory.json'
addressI_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MItems.json'
addressF_tw = 'https://otogi-cdn-dmm-tw.azureedge.net/prod/MasterData/MFoods.json'


def check_cate_tw(rsid,xid,l,ml):
    if l < ml:
        return([0,'q','','m'])
    
    for y in cfg.MSpirits_tw:
        if y['psid'] == rsid or y['sid1'] == rsid or y['sid2'] == rsid or y['sid3'] == rsid:
            return([y['rsid'],'r',y['n']+'【'+attribute(y['a'])+'】','m'])
    if ml == 1:
        for y in cfg.MMonsters_tw:
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
        for y in cfg.MWeapons_tw:
            if y['msid'] == rsid:
                if y['rmid'] is None:
                    return([1,'n',y['n']+'【'+weaponclass(y['wc'])+'】','m'])
                else:
                    for z in cfg.MMonsters_tw:
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

def skillsourcecate_tw():
    for x in cfg.MMonsters_tw:
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
                for y in cfg.MSkills_tw:
                    if y['rsid'] == x['vsid']:
                        if y['l'] != y['ml'] or y['d'] == '':
                            [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'q',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
                            continue
                        [y['tm'],y['tc'],y['sp'],y['er']] = [x['rmid'],'i',x['n']+'【'+attribute(x['a'])+weaponclass(x['wc'])+'】'+'【'+spname+'】','m']
            if x['me'] == 4:
                i = 1
                for y in cfg.MSkills_tw:
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
                for y in cfg.MSkills_tw:
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
                for y in cfg.MSkills_tw:
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
                for y in cfg.MSkills_tw:
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
                for y in cfg.MSkills_tw:
                    if y['rsid'] == x['vsid'] and y['l'] == y['ml'] and y['d'] != '':
                        k += 1
            
                i = 1
                if k == 3:
                    for y in cfg.MSkills_tw:
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
                    for y in cfg.MSkills_tw:
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
                    for y in cfg.MSkills_tw:
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

    for x in cfg.MSkills_tw:
        if x['er'] == 'm':
            continue
        [x['tm'],x['tc'],x['sp'],x['er']] = check_cate_tw(x['rsid'],x['id'],x['l'],x['ml'])
        if x['tm'] == 0:
            x['tm']=9999999 
    
    cfg.MSkills_tw = sorted(cfg.MSkills_tw, key=itemgetter('tm'))
    for x in cfg.MSkills_tw:
        if x['tm'] == 9999999:
            x['tm']=0

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
    cfg.MSkills_tw = requests.get(addressS_tw).json()
    cfg.MMonsters_tw = requests.get(addressM_tw).json()
    cfg.MSpirits_tw = requests.get(addressR_tw).json()
    cfg.MWeapons_tw = requests.get(addressW_tw).json()
    cfg.MAccessory_tw = requests.get(addressA_tw).json()
