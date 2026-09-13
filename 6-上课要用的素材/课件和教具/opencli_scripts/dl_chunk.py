import sys, os, base64, importlib.util

spec = importlib.util.spec_from_file_location(
    "mp", r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts\mirror_par.py")
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

DST = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\生成图\课件配图"
os.makedirs(DST, exist_ok=True)
STEP = 30000

def prep_js(pos):
    pick = "im[%s]" % ("im.length-1" if pos < 0 else str(pos))
    return ("(() => { const im = [...document.querySelectorAll('img')].filter(i => /estuary\\/content/.test(i.src||'')); "
            "if (!im.length) { window.__dl = ''; return 'NOIMG:' + im.length; } "
            "const pick = %s; if (!pick) return 'NOPOS:' + im.length; "
            "const W = Math.min(1500, pick.naturalWidth || 1500); "
            "const H = Math.round(W * (pick.naturalHeight / pick.naturalWidth)); "
            "const c = document.createElement('canvas'); c.width = W; c.height = H; "
            "const g = c.getContext('2d'); g.drawImage(pick, 0, 0, W, H); "
            "window.__dl = c.toDataURL('image/jpeg', 0.88); "
            "return 'LEN=' + window.__dl.length + ' DIM=' + W + 'x' + H; })()") % pick


PREP = ("(() => { const im = [...document.querySelectorAll('img')].filter(i => /estuary\\/content/.test(i.src||'')); "
        "if (!im.length) { window.__dl = ''; return 'NOIMG'; } "
        "const pick = im[im.length-1]; const W = Math.min(1500, pick.naturalWidth || 1500); "
        "const H = Math.round(W * (pick.naturalHeight / pick.naturalWidth)); "
        "const c = document.createElement('canvas'); c.width = W; c.height = H; "
        "const g = c.getContext('2d'); g.drawImage(pick, 0, 0, W, H); "
        "window.__dl = c.toDataURL('image/jpeg', 0.88); "
        "return 'LEN=' + window.__dl.length + ' DIM=' + W + 'x' + H; })()")


def grab(idx, sess, pos=-1):
    name = mp.IMAGES[idx][0]
    out = mp.run([mp.OPENCLI, "browser", sess, "eval", prep_js(pos)], timeout=120)
    line = out.strip().split("\n")[0]
    if not line.startswith("LEN="):
        print("FAIL", name, sess, line[-70:])
        return False
    total = int(line.split("LEN=")[1].split()[0])
    alt = line.split("ALT=")[-1] if "ALT=" in line else ""
    parts = []
    pos = 0
    while pos < total:
        js = "window.__dl.substr(%d,%d)" % (pos, STEP)
        chunk = mp.run([mp.OPENCLI, "browser", sess, "eval", js], timeout=60)
        marker = "data:image/jpeg;base64,"
        p = chunk.find(marker)
        if p >= 0:
            chunk = chunk[p:]
        chunk = chunk.strip()
        chunk = chunk.split("\n")[0].strip().strip('"').strip("'")
        parts.append(chunk)
        pos += STEP
        print("  chunk", pos, "/", total, end="\r")
    data_url = "".join(parts)
    b64 = data_url.split(",", 1)[1] if "," in data_url else data_url
    try:
        raw = base64.b64decode(b64 + "=" * (-len(b64) % 4))
    except Exception as e:
        print("DECODE FAIL", name, e)
        return False
    dst = os.path.join(DST, name + ".png")
    open(dst, "wb").write(raw)
    print("OK", name, len(raw), "alt=", alt[:30], " " * 20)
    return True


if __name__ == "__main__":
    for spec_arg in sys.argv[1:]:
        parts = spec_arg.split(":")
        i, s = int(parts[0]), parts[1]
        pos = int(parts[2]) if len(parts) > 2 else -1
        grab(i, s, pos)
