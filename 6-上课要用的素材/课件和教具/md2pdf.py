# -*- coding: utf-8 -*-
"""Markdown -> HTML -> PDF (Chrome headless)"""
import os, subprocess, sys, tempfile
import markdown

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Microsoft YaHei", "微软雅黑", sans-serif; font-size: 11pt; line-height: 1.75;
       color: #1a1a1a; }
h1 { font-size: 20pt; text-align: center; color: #1B2A4A; margin: 0 0 6pt; page-break-after: avoid; }
h2 { font-size: 14pt; color: #1B2A4A; border-left: 4px solid #FFC845; padding-left: 8px;
     margin: 16pt 0 8pt; page-break-after: avoid; }
h3 { font-size: 12pt; color: #24436b; margin: 12pt 0 6pt; page-break-after: avoid; }
p { margin: 5pt 0; }
blockquote { margin: 6pt 0; padding: 6pt 10pt; background: #FDF6E3; border-left: 3px solid #FFC845;
             color: #4a4a4a; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 10pt; }
th, td { border: 1px solid #c8cdd6; padding: 4pt 6pt; vertical-align: top; }
th { background: #1B2A4A; color: #fff; }
code { background: #f2f2f2; padding: 1pt 3pt; font-size: 10pt; }
pre { background: #f2f2f2; padding: 8pt; font-size: 9pt; white-space: pre-wrap; }
hr { border: none; border-top: 1px solid #ddd; margin: 12pt 0; }
ul, ol { margin: 5pt 0; padding-left: 20pt; }
strong { color: #1B2A4A; }
"""


def convert(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s</style></head>'
            '<body>%s</body></html>') % (CSS, body)
    tmp = os.path.join(tempfile.gettempdir(), "md2pdf_tmp.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    out_dir = os.path.dirname(pdf_path)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--print-to-pdf=" + pdf_path,
           "file:///" + tmp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="ignore", timeout=180)
    ok = os.path.exists(pdf_path)
    print(("OK  " if ok else "FAIL"), os.path.basename(pdf_path),
          os.path.getsize(pdf_path) if ok else "")
    return ok


if __name__ == "__main__":
    jobs = [
        (r"D:\Work\课程思政教学竞赛\3-讲哪一课\教案（第1课）.md",
         r"D:\Work\课程思政教学竞赛\3-讲哪一课\教案（第1课）.pdf"),
        (r"D:\Work\课程思政教学竞赛\3-讲哪一课\教学设计（第1课）.md",
         r"D:\Work\课程思政教学竞赛\3-讲哪一课\教学设计（第1课）.pdf"),
        (r"D:\Work\课程思政教学竞赛\3-讲哪一课\三个版本设计（第1课）.md",
         r"D:\Work\课程思政教学竞赛\3-讲哪一课\三个版本设计（第1课）.pdf"),
    ]
    for a, b in jobs:
        if os.path.exists(a):
            convert(a, b)
        else:
            print("missing:", a)
