import base64, json, os, subprocess, sys, time, urllib.parse

BASE = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts"
STATE = os.path.join(BASE, "batch_state.json")
SESSION = "n8hh7hyn"
OPENCLI = r"C:\Users\郭永涛\AppData\Roaming\npm\opencli.cmd"
if not os.path.exists(OPENCLI):
    OPENCLI = "opencli"
TOKEN_FILE = os.path.join(BASE, "token.txt")
ACCOUNTS = ["vip-18", "vip-13", "vip-14", "vip-11"]

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
                           errors="ignore", timeout=timeout, shell=False)
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
    if os.path.exists(TOKEN_FILE):
        return open(TOKEN_FILE, encoding="utf-8").read().strip()
    return None


def open_tabs():
    token = get_token()
    if not token:
        print("NO TOKEN")
        return
    tabs = {}
    for acc in ACCOUNTS:
        url = "https://%s.67673.live/api/v2/plus-login?account=%s&jwt=%s" % (
            acc, acc, urllib.parse.quote(token, safe=""))
        out = run([OPENCLI, "browser", SESSION, "tab", "new", url])
        tid = None
        for frag in out.replace("\n", " ").split("{"):
            try:
                obj = json.loads("{" + frag.split("}")[0] + "}")
            except Exception:
                continue
            for k in ("page", "targetId", "tabId", "id", "target"):
                if k in obj and isinstance(obj[k], str) and len(obj[k]) > 8:
                    tid = obj[k]
                    break
            if tid:
                break
        tabs[acc] = tid
        print(acc, "->", tid, "" if tid else out[:120])
        time.sleep(3)
    json.dump(tabs, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved tabs:", json.dumps(tabs, ensure_ascii=False))


def send_batch(start, count):
    st = json.load(open(STATE, encoding="utf-8"))
    accs = list(st.keys())
    todo = IMAGES[start:start + count]
    for i, (name, desc) in enumerate(todo):
        acc = accs[i % len(accs)]
        tid = st.get(acc)
        if not tid:
            print(name, "no tab for", acc)
            continue
        prompt = desc + COMMON + "\n\n请直接生成这张图片（16:9 横版）。画面中绝对不要出现任何文字、字母或数字。"
        js = build_inject(prompt)
        r1 = run([OPENCLI, "browser", SESSION, "eval", js, "--tab", tid])
        print(name, "inject", r1.strip()[-60:].replace("\n", " "))
        time.sleep(1)
        r2 = run([OPENCLI, "browser", SESSION, "eval",
                  "(()=>{const s=document.querySelector('[data-testid=send-button]');if(s&&!s.disabled){s.click();return 'sent'}return JSON.stringify({send:!!s})})()",
                  "--tab", tid])
        print(name, "send", r2.strip()[-40:].replace("\n", " "))
        time.sleep(2)


def check():
    st = json.load(open(STATE, encoding="utf-8"))
    for acc, tid in st.items():
        if not tid:
            continue
        js = ("(()=>{const imgs=[...document.querySelectorAll('img')].filter(i=>/estuary\\/content/.test(i.src||''));"
              "const a=[...document.querySelectorAll('[data-message-author-role=assistant]')];"
              "return JSON.stringify({host:location.host,n:imgs.length,asst:a.length,alt:imgs.map(i=>(i.alt||'').slice(0,40))});})()")
        out = run([OPENCLI, "browser", SESSION, "eval", js, "--tab", tid])
        print(acc, out.strip()[-200:].replace("\n", " "))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "open"
    if cmd == "open":
        open_tabs()
    elif cmd == "send":
        send_batch(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "check":
        check()
