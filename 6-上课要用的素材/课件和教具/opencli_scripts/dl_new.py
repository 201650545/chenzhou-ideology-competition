import sys, os, glob, time, importlib.util

spec = importlib.util.spec_from_file_location(
    "mp", r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts\mirror_par.py")
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

DL = r"C:\Users\郭永涛\Downloads"
DST = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\生成图\课件配图"
os.makedirs(DST, exist_ok=True)


def snap():
    return set(glob.glob(os.path.join(DL, "*.tmp"))) | set(glob.glob(os.path.join(DL, "*.png")))


def grab(idx, sess):
    name = mp.IMAGES[idx][0]
    before = snap()
    js = ("(()=>{const im=[...document.querySelectorAll('img')].filter(i=>/estuary\\/content/.test(i.src||''));"
          "if(!im.length) return 'no-img'; return fetch(im[im.length-1].src,{credentials:'include'})"
          ".then(r=>r.ok?r.blob():('HTTP'+r.status)).then(b=>{if(typeof b==='string')return b;"
          "const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='%s.png';"
          "document.body.appendChild(a);a.click();a.remove();return 'ok:'+b.size;}).catch(e=>'ERR:'+e);})()") % name
    out = mp.run([mp.OPENCLI, "browser", sess, "eval", js], timeout=90)
    first = out.strip().split("\n")[0][-50:]
    newf = None
    for _ in range(25):
        time.sleep(1)
        diff = snap() - before
        if diff:
            newf = sorted(diff, key=os.path.getmtime)[-1]
            break
    if newf and os.path.getsize(newf) > 20000:
        dst = os.path.join(DST, name + ".png")
        open(dst, "wb").write(open(newf, "rb").read())
        print("OK", name, os.path.getsize(newf), first)
        return True
    print("FAIL", name, sess, first)
    return False


if __name__ == "__main__":
    for pair in sys.argv[1:]:
        i, s = pair.split(":")
        grab(int(i), s)
