import cfg
import requests

def loadnick():
    try:
        token = '$2b$10$5PAG13iqTYBBw/F6VJJye.1HL61OTBOyjoNnKqKeNb4TyKBdFxB/q'
        url = 'https://api.jsonbin.io/b/601bf6d606934b65f52e5aa7/latest'
        request = requests.get(url,headers={'secret-key': token})
        cfg.nickname = request.json()
    except:
        pass
    return

def loadsp():
    try:
        url = 'https://api.jsonbin.io/b/60ccca018a4cd025b7a05805/latest'
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
            kw_list.append(x['name_jp'])
    if kw_list == []:
        kw_list = 0
    return(kw_list)
