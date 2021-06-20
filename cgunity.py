import UnityPy
import requests
import json
from Crypto.Cipher import AES
from io import BytesIO
from zipfile import ZipFile

def cg_extract(filename):
    key = b'kms1kms2kms3kms4'
    IV = b'nekonekonyannyan'
    aes = AES.new(key, AES.MODE_CBC, IV)
    
    url = "https://otogimigwest.blob.core.windows.net/prodassets/WebGL/Assets/Chara/Still/"+filename+".enc"
    fin = BytesIO(requests.get(url).content)
    with open(filename, 'wb') as fout:
        while True:
            data = fin.read(16)
            n = len(data)
            if n == 0:
                break
            dec_data = aes.decrypt(data)
            fout.write(dec_data)
    fin.close()
    
    env = UnityPy.load(filename)
    
    count = 0
    for obj in env.objects:
        if obj.type == "TextAsset":
            data = obj.read()
            if 'atlas' in data.name:
                count += 1
    mylist = []
    name_start = int(filename[-1])
    name_end = name_start+count
    for i in range(name_start,name_end):
        mylist.append(str(i))
    
    image_index = 1
    atlas_index = 1
    json_index = 1
    for myindex in mylist:
        for obj in env.objects:
            if obj.type == "Texture2D":
                data = obj.read()
                name = data.name
                if int(myindex) < 10:
                    if name[-1] != myindex or name[-2].isdigit():
                        continue
                else:
                    if name[-2:] != myindex:
                        continue
                if image_index == 1:
                    x_name = name
                    zipObj = ZipFile(name+'.zip', 'w')
                    image_index = 2
                data.image.save(name+".png")
                zipObj.write(name+'.png')
            if obj.type == "TextAsset":
                data = obj.read()
                name = data.name
                if "atlas" in name:
                    if int(myindex) < 10:
                        if name[-7] != myindex or name[-8].isdigit():
                            continue
                    else:
                        if name[-8:-6] != myindex:
                            continue
                    if atlas_index == 1:
                        s = open(name, 'wb')
                        s.write(bytes(data.script))
                        atlas_index = 2
                    else:
                        s.write(bytes(data.script))
                else:
                    if int(myindex) < 10:
                        if name[-1] != myindex or name[-2].isdigit():
                            continue
                    else:
                        if name[-2:] != myindex:
                            continue
                    if json_index == 1:
                        myjson = json.loads(bytes(data.script).decode("utf-8"))
                        f = open(name+".json", 'w', encoding='utf-8')
                        json_index = 2
                    else:
                        myjson2 = json.loads(bytes(data.script).decode("utf-8"))
                        for y in myjson2["slots"]:
                            myjson["slots"].append(y)
                        myjson["skins"]["default"].update(myjson2["skins"]["default"])
    json.dump(myjson,f)
    f.close()
    s.close()
    zipObj.write(x_name+'.atlas')
    zipObj.write(x_name+'.json')
    zipObj.close()
    return(x_name)
