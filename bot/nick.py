import cfg
import requests

def loadnick():
    try:
        url = 'https://api.jsonbin.io/v3/b/60ccca018a4cd025b7a05805/latest'
        request = requests.get(url)
        cfg.nickname = request.json()
    except:
        pass
    return

def loadsp():
    try:
        url = 'https://api.jsonbin.io/v3/b/60ccca018a4cd025b7a05805/latest'
        request = requests.get(url)
        cfg.spjson = request.json()
    except:
        pass
    return
    
def nickisin(kw,sentence):
    for x in kw:
        if x in sentence.lower():
            return True
    return False

def matchnick(kw):
    kw_list = []
    for x in cfg.nickname:
        if nickisin(kw,x['name_cn']):
            kw_list.append(str(x['id']))
    if kw_list == []:
        kw_list = 0
    return(kw_list)
