import base64, sys, os

BASE = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts"

name = sys.argv[1] if len(sys.argv) > 1 else "prompt_chat1"
src = os.path.join(BASE, name + ".txt")
with open(src, "r", encoding="utf-8") as f:
    text = f.read().strip()

b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")

js = """(() => {
  const ce = document.querySelector('#prompt-textarea[contenteditable=true]') || document.querySelector('[contenteditable=true]');
  if (!ce) return JSON.stringify({err:'no-composer', host: location.host});
  const txt = decodeURIComponent(escape(atob('%s')));
  ce.focus();
  ce.innerHTML = '';
  document.execCommand('insertText', false, txt);
  return JSON.stringify({ok:true, len:(ce.innerText||'').length, host:location.host});
})()""" % b64

out = os.path.join(BASE, "inject_" + name + ".js")
with open(out, "w", encoding="utf-8") as f:
    f.write(js)

print("built:", out, "chars:", len(text))
