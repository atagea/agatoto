"""Tworzy lekkie wersje zdjęć dla galerii.
images/thumbs/<nazwa>.webp  – miniatura do siatki (szer. 640 px)
images/medium/<nazwa>.webp  – podgląd kadru (dłuższy bok 1600 px)
Uruchamiane automatycznie przez GitHub Actions po wgraniu zdjęć; można też ręcznie: python tools/miniatury.py
"""
import os, json, hashlib
from PIL import Image, ImageOps
SRC='images'; EXT=('.jpg','.jpeg','.png','.webp')
def out(name,folder): return os.path.join(SRC,folder,os.path.splitext(name)[0]+'.webp')
HASHES=os.path.join(SRC,'thumbs','sumy.json')
def build(name,sums):
    src=os.path.join(SRC,name); t=out(name,'thumbs'); m=out(name,'medium')
    h=hashlib.sha1(open(src,'rb').read()).hexdigest()
    if sums.get(name)==h and os.path.exists(t) and os.path.exists(m): return False
    sums[name]=h
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    a=im.copy(); a.thumbnail((640,10000),Image.LANCZOS); a.save(t,'WEBP',quality=80,method=6)
    b=im.copy(); b.thumbnail((1600,1600),Image.LANCZOS); b.save(m,'WEBP',quality=84,method=6)
    return True
if __name__=='__main__':
    for f in ('thumbs','medium'): os.makedirs(os.path.join(SRC,f),exist_ok=True)
    sums=json.load(open(HASHES)) if os.path.exists(HASHES) else {}
    n=0
    for name in sorted(os.listdir(SRC)):
        if name.lower().endswith(EXT) and os.path.isfile(os.path.join(SRC,name)): n+=build(name,sums)
    json.dump(sums,open(HASHES,'w'),indent=1,ensure_ascii=False)
    print('nowe/odświeżone:',n)
