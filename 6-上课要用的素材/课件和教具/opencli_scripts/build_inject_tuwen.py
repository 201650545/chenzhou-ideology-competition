import base64, re

src = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\学具1_海报提示词_图文版.md"
out_dir = r"D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts"

with open(src, encoding="utf-8") as f:
    text = f.read()

blocks = re.findall(r"```\r?\n([\s\S]*?)\r?\n```", text)
labels = ["color", "bw"]
for label, blk in zip(labels, blocks):
    b64 = base64.b64encode(blk.encode("utf-8")).decode("ascii")
    js = (
        "(() => {\n"
        "  const b = atob('" + b64 + "');\n"
        "  const u = new Uint8Array(b.length);\n"
        "  for (let i=0;i<b.length;i++) u[i]=b.charCodeAt(i);\n"
        "  const s = new TextDecoder().decode(u);\n"
        "  const ce = document.querySelector('#prompt-textarea[contenteditable=true]') || document.querySelector('[contenteditable=true]');\n"
        "  if(!ce) return JSON.stringify({err:'no-ce'});\n"
        "  ce.focus(); ce.innerHTML=''; document.execCommand('insertText', false, s);\n"
        "  return JSON.stringify({len: (ce.innerText||'').length, tail: (ce.innerText||'').slice(-25)});\n"
        "})()\n"
    )
    p = f"{out_dir}/inject_tuwen_{label}.js"
    with open(p, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"wrote {p} (prompt chars={len(blk)})")
