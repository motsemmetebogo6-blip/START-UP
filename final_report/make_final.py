#!/usr/bin/env python3
"""Two-pass build: assemble, render, read the page of every heading and caption, assemble again with the page numbers."""
import os, re, subprocess, sys, tempfile
import docx
from docx.oxml.ns import qn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_report as B

K = "/root/.claude/skills/synced/5781b4f6-95d3-4d19-a418-bf62a852dd55_c98d0078-f0d0-4d57-bc29-a3640d48cbd1/docx/scripts/office/soffice.py"


def to_pdf(docx_path, outdir):
    subprocess.run(["python3", K, "--headless", "--convert-to", "pdf", "--outdir", outdir, docx_path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return os.path.join(outdir, os.path.basename(docx_path).replace(".docx", ".pdf"))


def page_texts(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = txt.split("\f")
    out = []
    for pg in pages:
        lines = [l for l in pg.split("\n") if "....." not in l]
        out.append(re.sub(r"\s+", " ", " ".join(lines)).upper())
    return out


def discover(docx_path, pdf):
    d = docx.Document(docx_path)
    body = d.element.body
    pages = page_texts(pdf)
    res = {}
    cur = 0
    heads = [h for h in B.heading_numbers(body) if h[0] <= 2]
    for i, (lvl, label, title, el) in enumerate(heads):
        key = (label + " " + title.upper()).strip()
        key = re.sub(r"\s+", " ", key)
        for pg in range(cur, len(pages)):
            if key in pages[pg]:
                res[("H", i)] = pg + 1
                cur = pg
                break
        else:
            print("  not found:", key[:60])
    for kind, sid in (("Table", "TableCaption"), ("Figure", "FigureCaption")):
        cur = 0
        caps = [re.sub(r"\s+", " ", B.para_text(p)).strip() for p in body.iter(qn("w:p"))
                if B.style_of(p) == sid and not B.in_table(p)]
        for i, c in enumerate(caps):
            key = re.sub(r"\s+", " ", c[:38]).upper()
            for pg in range(cur, len(pages)):
                if key in pages[pg]:
                    res[(kind, i)] = pg + 1
                    cur = pg
                    break
            else:
                print("  not found:", key)
    return res


def main(src, out):
    with tempfile.TemporaryDirectory() as tmp:
        p0 = os.path.join(tmp, "pass0.docx")
        B.assemble(src, p0, tmp=tmp)
        pdf0 = to_pdf(p0, tmp)
        pages = discover(p0, pdf0)
        p1 = os.path.join(tmp, "pass1.docx")
        B.assemble(src, p1, pages=pages, tmp=tmp)
        pdf1 = to_pdf(p1, tmp)
        pages2 = discover(p1, pdf1)
        diff = {k: (pages[k], pages2[k]) for k in pages if pages2.get(k) != pages[k]}
        print("page-number differences between passes:", len(diff))
        if diff:
            B.assemble(src, out, pages=pages2, tmp=tmp)
        else:
            import shutil
            shutil.copy(p1, out)
    print("final:", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
