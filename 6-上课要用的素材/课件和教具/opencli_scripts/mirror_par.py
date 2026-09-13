import base64, os, subprocess, sys, time, urllib.parse

BASE = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts"
TOKEN_FILE = os.path.join(BASE, "token.txt")
OPENCLI = r"C:\Users\郭永涛\AppData\Roaming\npm\opencli.cmd"
if not os.path.exists(OPENCLI):
    OPENCLI = "opencli"

SESSIONS = {"vip-18": "m1", "vip-13": "m2", "vip-14": "m3", "vip-11": "m4"}

COMMON = (" Flat vector illustration style, 16:9 widescreen, deep navy night-sky background (#1B2A4A), "
          "warm yellow stars (#FFC845), simple flat cartoon primary-school children, clean shapes, no gradients, "
          "NO text, NO letters, NO words, NO numbers anywhere in the image.")

IMAGES = [
    ("img01_cover", "A floating weekly class-schedule card in cream white in the center of a starry navy sky, "
     "the card has 12 empty rows and each row ends with three small outline stars. Three flat cartoon children "
     "look up at the card with wonder. Simple flat doodle icons of school subjects float nearby: a book, a paint "
     "palette, a soccer ball, a musical note, a calculator, a green leaf."),
    ("img02_tuxing", "A child sitting at a desk holding a yellow pencil, coloring stars on a paper chart. The chart "
     "has rows with three stars per row; some stars are filled golden, some are empty outlines. Navy classroom "
     "background with warm star decorations."),
    ("img03_duibi", "Two identical cream-white school timetable cards side by side, each with 12 rows carrying "
     "golden stars; the filled stars appear in different rows on each card, showing the same timetable rated "
     "differently. A question-mark shape made of small golden stars floats above between them."),
    ("img04_shuoliyou", "Three primary-school children standing together, each with an empty speech bubble; inside "
     "the bubbles are simple icons instead of words: a smiley face, a trophy, a frowning face, a puzzle piece."),
    ("img05_jiaoshi", "A cozy primary-school classroom scene: a blackboard with a colorful bulletin-board poster, "
     "desks, a pencil case with a patterned cover, a small shop counter with coins, a running child, a thermometer "
     "and a bandage. Each object has a tiny golden star attached, as if something is being found."),
    ("img06_jiaru", "A weekly timetable grid hanging on a wall with one whole column removed, leaving a clear empty "
     "gap outlined by a dashed line. A small group of children stand in front looking at the gap with surprise."),
    ("img07_kakou", "A child standing face to face with a large personified school-subject book character, a book "
     "with simple arms and a round friendly face but no facial features. They look at each other. A glowing "
     "heart-shaped star floats between them."),
    ("img08_china", "A panorama of Chinese science achievements as simple flat icons: an ancient armillary sphere, "
     "a bronze seismoscope, a rice plant, a herbal plant in a flask, a satellite, a moon rover, a large radio "
     "telescope dish, a high-speed train. All connected by one golden constellation line."),
    ("img09_global", "A blue-green Earth seen from space, surrounded by a ring of flat icons representing science "
     "for humanity: a stethoscope, a wind turbine, a water drop, a rocket, a wheat ear, a DNA helix. A golden "
     "constellation arc links them."),
    ("img10_xingdong", "Two golden cards side by side on a navy starry background. Left card shows a lightbulb icon, "
     "right card shows a footprint stepping forward. A child's hand is placing a golden star onto each card."),
    ("img11_faxian", "A child holding up a glowing golden star, looking at it with a smile, surrounded by many small "
     "stars in a deep navy night sky. Soft light radiates from the star."),
]


def run(args, timeout=90):
    try:
        p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           errors="ignore", timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return "EXC:" + str(e)


def build_inject(text):
    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    return ("(() => { const ce = document.querySelector('#prompt-textarea[contenteditable=true]') || "
            "document.querySelector('[contenteditable=true]'); if (!ce) return JSON.stringify({err:'no-composer'}); "
            "const txt = decodeURIComponent(escape(atob('%s'))); ce.focus(); ce.innerHTML=''; "
            "document.execCommand('insertText', false, txt); "
            "return JSON.stringify({ok:true, len:(ce.innerText||'').length}); })()" % b64)


def get_token():
    return open(TOKEN_FILE, encoding="utf-8").read().strip()


def open_all():
    token = get_token()
    for acc, sess in SESSIONS.items():
        url = "https://%s.67673.live/api/v2/plus-login?account=%s&jwt=%s" % (
            acc, acc, urllib.parse.quote(token, safe=""))
        out = run([OPENCLI, "browser", sess, "open", url], timeout=60)
        print(acc, sess, "ok" if "page" in out else out[:90])
        time.sleep(2)


def send_batch(start, count):
    accs = list(SESSIONS.keys())
    for i, (name, desc) in enumerate(IMAGES[start:start + count]):
        acc = accs[i % len(accs)]
        sess = SESSIONS[acc]
        prompt = desc + COMMON + "\n\n请直接生成这张图片（16:9 横版）。画面中绝对不要出现任何文字、字母或数字。"
        r1 = run([OPENCLI, "browser", sess, "eval", build_inject(prompt)], timeout=60)
        print(name, "inject", r1.strip()[-45:].replace("\n", " "))
        time.sleep(1)
        r2 = run([OPENCLI, "browser", sess, "eval",
                  "(()=>{const s=document.querySelector('[data-testid=send-button]');if(s&&!s.disabled){s.click();return 'sent'}return JSON.stringify({send:!!s})})()"],
                 timeout=60)
        print(name, "send", r2.strip()[-28:].replace("\n", " "))
        time.sleep(2)


def check():
    for acc, sess in SESSIONS.items():
        js = ("(()=>{const imgs=[...document.querySelectorAll('img')].filter(i=>/estuary\\/content/.test(i.src||''));"
              "const a=[...document.querySelectorAll('[data-message-author-role=assistant]')];"
              "return JSON.stringify({h:location.host,n:imgs.length,asst:a.length,alt:imgs.map(i=>(i.alt||'').slice(0,35))});})()")
        out = run([OPENCLI, "browser", sess, "eval", js], timeout=60)
        print(acc, out.strip()[-200:].replace("\n", " "))


def download(idx=None):
    names = [n for n, _ in IMAGES]
    outdir = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\生成图\课件配图"
    os.makedirs(outdir, exist_ok=True)
    for i, name in enumerate(names):
        if idx is not None and i != idx:
            continue
        sess = SESSIONS[list(SESSIONS.keys())[i % len(SESSIONS)]]
        js = ("(()=>{const im=[...document.querySelectorAll('img')].filter(i=>/estuary\\/content/.test(i.src||''));"
              "if(!im.length) return 'no-img'; return fetch(im[im.length-1].src,{credentials:'include'})"
              ".then(r=>r.ok?r.blob():('HTTP'+r.status)).then(b=>{if(typeof b==='string')return b;"
              "const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='%s.png';"
              "document.body.appendChild(a);a.click();a.remove();return 'ok:'+b.size;}).catch(e=>'ERR:'+e);})()") % name
        out = run([OPENCLI, "browser", sess, "eval", js], timeout=90)
        print(name, sess, out.strip()[-60:].replace("\n", " "))
        time.sleep(2)
    print("outdir:", outdir)


def send_one(idx, sess):
    name, desc = IMAGES[idx]
    prompt = desc + COMMON + "\n\n请直接生成这张图片（16:9 横版）。画面中绝对不要出现任何文字、字母或数字。"
    r1 = run([OPENCLI, "browser", sess, "eval", build_inject(prompt)], timeout=60)
    print(name, "inject", r1.strip().split("\n")[0][-60:])
    time.sleep(1)
    r2 = run([OPENCLI, "browser", sess, "eval",
              "(()=>{const s=document.querySelector('[data-testid=send-button]');if(s&&!s.disabled){s.click();return 'SENT'}return 'NOSEND'})()"],
             timeout=60)
    print(name, "send", r2.strip().split("\n")[0][-40:])
    return name


def dl_one(idx, sess):
    name, _ = IMAGES[idx]
    js = ("(()=>{const im=[...document.querySelectorAll('img')].filter(i=>/estuary\\/content/.test(i.src||''));"
          "if(!im.length) return 'no-img'; return fetch(im[im.length-1].src,{credentials:'include'})"
          ".then(r=>r.ok?r.blob():('HTTP'+r.status)).then(b=>{if(typeof b==='string')return b;"
          "const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='%s.png';"
          "document.body.appendChild(a);a.click();a.remove();return 'ok:'+b.size;}).catch(e=>'ERR:'+e);})()") % name
    out = run([OPENCLI, "browser", sess, "eval", js], timeout=90)
    print(name, sess, out.strip().split("\n")[0][-70:])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "s1":
        send_one(int(sys.argv[2]), sys.argv[3])
    elif cmd == "d1":
        dl_one(int(sys.argv[2]), sys.argv[3])
    if cmd == "open":
        open_all()
    elif cmd == "send":
        send_batch(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "check":
        check()
    elif cmd == "dl":
        download(int(sys.argv[2]) if len(sys.argv) > 2 else None)
