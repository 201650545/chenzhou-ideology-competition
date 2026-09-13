import sys, os, base64, importlib.util

spec = importlib.util.spec_from_file_location(
    "mp", r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts\mirror_par.py")
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

DST = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\生成图\课件配图"
os.makedirs(DST, exist_ok=True)

JS = r"""
(() => {
  const im = [...document.querySelectorAll('img')].filter(i => /estuary\/content/.test(i.src||''));
  if (!im.length) return 'NOIMG';
  const img = im[im.length-1];
  const draw = () => {
    const W = Math.min(1600, img.naturalWidth || 1600);
    const H = Math.round(W * (img.naturalHeight / img.naturalWidth));
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d'); g.drawImage(img, 0, 0, W, H);
    return c.toDataURL('image/jpeg', 0.9);
  };
  try {
    const d = draw();
    return d;
  } catch (e) {
    return 'CERR:' + e.message;
  }
})()
"""


def grab(idx, sess):
    name = mp.IMAGES[idx][0]
    out = mp.run([mp.OPENCLI, "browser", sess, "eval", JS], timeout=180)
    out = out.strip()
    marker = "data:image/jpeg;base64,"
    pos = out.find(marker)
    if pos < 0:
        print("FAIL", name, sess, out[-80:].replace("\n", " "))
        return False
    b64 = out[pos + len(marker):].split()[0].strip().strip('"').strip("'")
    try:
        data = base64.b64decode(b64)
    except Exception as e:
        print("DECODE FAIL", name, e)
        return False
    dst = os.path.join(DST, name + ".png")
    open(dst, "wb").write(data)
    print("OK", name, len(data))
    return True


if __name__ == "__main__":
    for pair in sys.argv[1:]:
        i, s = pair.split(":")
        grab(int(i), s)
