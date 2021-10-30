def setskilltype(w):
    if w == 'i':
        return('拆技')
    elif w == 'a':
        return('昇華')
    elif w == 't':
        return('昇華變化')
    elif w == 's':
        return('昇華超變化')
    elif w == 'u':
        return('限突')
    elif w == 'v':
        return('限突變化')
    elif w == 'x':
        return('限突超變化')
    elif w == 'w':
        return('專武技能')
    elif w == 'l':
        return('隊長技')
    elif w == 'n':
        return('非專武武器技能')
    elif w == 'r':
        return('精靈技能')
    elif w == 'o':
        return('未能確定來源技能')
    else:
        return('不明技能')


def attribute(a):
    if a == 1:
        return('火')
    elif a == 2:
        return('水')
    elif a == 3:
        return('樹')
    elif a == 4:
        return('光')
    elif a == 5:
        return('闇')
    else:
        return('')

def weaponclass(wc):
    if wc == 1:
        return('劍')
    elif wc == 2:
        return('斧')
    elif wc == 3:
        return('槍')
    elif wc == 4:
        return('本')
    elif wc == 5:
        return('杖')
    elif wc == 6:
        return('短劍')
    elif wc == 7:
        return('弓')
    elif wc == 8:
        return('特殊')
    else:
        return('')

def skillclass(sc):
    if sc == 1:
        return('橘')
    elif sc == 2:
        return('藍')
    elif sc == 3:
        return('紫')
    elif sc == 4:
        return('粉')
    elif sc == 5:
        return('綠')
    else:
        return('')

def skillrank(sr):
    if sr == 2:
        return('D')
    elif sr == 3:
        return('C')
    elif sr == 4:
        return('B')
    elif sr == 5:
        return('A')
    elif sr == 6:
        return('S')
    elif sr == 7:
        return('SS')
    elif sr == 8:
        return('S3')
    else:
        return('')

def isinor(kw,sentence):
    for k in kw:
        if k.startswith('-'):
            if k[1:] in sentence.lower():
                return False
    for k in kw:
        if k in sentence.lower():
            return True
    return False

def isinand(kw,sentence):
    for k in kw:
        if k.startswith('-'):
            if k[1:] in sentence.lower():
                return False
        else:
            if k not in sentence.lower():
                return False
    return True

def isinforward(kw,sentence):
    n = 0
    first = 0    
    for k in kw:
        if k.startswith('-'):
            if sentence.lower().find(k[1:],n) != -1:
                return False        
        elif k.startswith('*'):
            sub = sentence.lower()[first:n]
            print(sub)
            if '。' in sub or '・' in sub:
                return False        
        else:
            n = sentence.lower().find(k,n)+1
            if n == 0:
                return False
            if first ==0:
                first = n
    return True

def isinbackward(kw,sentence):
    n = len(sentence.lower())-1
    for k in kw:
        if k.startswith('-'):
            if sentence.lower().find(k[1:],0,n) != -1:
                return False
        else:
            n = sentence.lower().find(k,0,n)
            if n == -1:
                return False
    return True

def isininterval(kw,sentence):
    lb = kw[0]
    ub = kw[1]
    kw = kw[2:]
    
    if lb == '-':
        lbn = 0
    else:
        lbn = sentence.lower().find(lb)
        
    if lbn == -1:
        return False
    
    n = len(sentence.lower())-1
    
    if ub == '-':
        ubn = n
    else:
        ubn = sentence.lower().find(ub,lbn)
        
    if ubn == -1:
        return False
        
    if lbn >= ubn:
        return False
    
    for k in kw:
        if k.startswith('-'):
            if sentence.lower().find(k[1:],lbn,ubn) != -1:
                return False
        else:
            if sentence.lower().find(k,lbn,ubn) == -1:
                return False
    return True

def isindamage(kw,sentence):
    try:
        threshold = int(kw[0])
    except:
        return False
    if not isinand(kw[1:],sentence.lower()):
        return False
    
    location = sentence.lower().find('威力')
    while location != -1:
        damage = ''
        for x in sentence.lower()[location+2:]:
            if x.isdigit():
                damage += x
            else:
                break
        if damage != '' and int(damage) >= threshold:
            return True
        else:
            location  = sentence.lower().find('威力',location+2)
    return False
    
def check_sc(sc,cate):
    if str(sc-1) in cate:
        return True
    else:
        pass
    return False

def check_sa(a,cate):
    if a == 6:
        return False
    elif str(a+4) in cate:
        return True
    else:
        pass
    return False
