#!/usr/bin/env python3
"""Lillian's Guide — mirror-4 handbook build. EVEglyphDesign canon PDF."""
import hashlib, datetime, re, sys, os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer)

W, H = LETTER
CREAM = HexColor("#fdfaf4"); CREAM2 = HexColor("#f7f2e7")
INK = HexColor("#1a1a1a"); LINE = HexColor("#e7e1d3")
ORNG = HexColor("#e87722"); MUTE = HexColor("#6b665c")

F = "/home/user/workspace/fonts"
pdfmetrics.registerFont(TTFont("Fraunces", f"{F}/Fraunces-400.ttf"))
pdfmetrics.registerFont(TTFont("Fraunces-Bold", f"{F}/Fraunces-700.ttf"))
pdfmetrics.registerFont(TTFont("Inter", f"{F}/Inter-400.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SB", f"{F}/Inter-600.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", f"{F}/Inter-700.ttf"))

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = f"{HERE}/handbook_source.md"
OUT = f"{HERE}/Lillians_Guide.pdf"
TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
DOC_ID = "EgD-HANDBOOK-M3"; KEY_ID = "EgD-KEY-2026-07"; VERSION = "rev 7"
TITLE = "Lillian's Guide"
SUB = "Transformational program management for information & technology · The Sovereign practitioner canon"
RAW = open(SRC, encoding="utf-8").read()
SHA = hashlib.sha256(RAW.encode("utf-8")).hexdigest()
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 0

MARGIN_L, MARGIN_R = 22*mm, 22*mm
TOP, BOT = 26*mm, 24*mm
FW = W - MARGIN_L - MARGIN_R


def S(name, **kw):
    b = dict(name=name, fontName="Inter", fontSize=10.2, leading=15.4,
             textColor=INK, alignment=TA_LEFT, spaceAfter=0)
    b.update(kw); return ParagraphStyle(**b)


st_h1 = S("h1", fontName="Fraunces-Bold", fontSize=17, leading=21, spaceAfter=6, spaceBefore=6)
st_h2 = S("h2", fontName="Fraunces-Bold", fontSize=12.4, leading=16, spaceAfter=3, spaceBefore=4)
st_body = S("b", spaceAfter=9)
st_bul = S("bu", spaceAfter=6, leftIndent=15, bulletIndent=2, firstLineIndent=0)
st_quote = S("q", fontName="Fraunces", fontSize=11.5, leading=18, spaceAfter=6,
             leftIndent=18, rightIndent=10, textColor=HexColor("#2a2a2a"))
st_cap = S("cap", fontSize=8.4, leading=12.4, textColor=MUTE, spaceAfter=6)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def inline(s):
    s = esc(s)
    # bold **x** ; italic *x* -> keep as span with slight style
    s = re.sub(r"\*\*([^*]+)\*\*", r'<font name="Inter-Bold">\1</font>', s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r'<font name="Fraunces">\1</font>', s)
    return s


def parse(raw):
    lines = raw.split("\n")
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("### "):
            out.append(Paragraph(inline(ln[4:]), S("h3", fontName="Fraunces", fontSize=13, leading=17, textColor=MUTE, spaceAfter=8)))
        elif ln.startswith("## "):
            out.append(Spacer(1, 4))
            out.append(Paragraph(inline(ln[3:]), st_h1))
            from reportlab.platypus import Flowable
            class Rule(Flowable):
                def __init__(self): Flowable.__init__(self); self.width=44; self.height=2
                def draw(self):
                    self.canv.setFillColor(ORNG); self.canv.rect(0, 0, 44, 2, stroke=0, fill=1)
            out.append(Rule()); out.append(Spacer(1, 8))
        elif ln.startswith("# "):
            # Title is on cover; skip
            pass
        elif ln.startswith("---"):
            out.append(Spacer(1, 6))
        elif ln.startswith("> "):
            # blockquote — accumulate consecutive '> ' lines
            buf = [ln[2:]]
            while i+1 < len(lines) and lines[i+1].startswith("> "):
                i += 1; buf.append(lines[i][2:])
            text = " ".join(buf).strip()
            out.append(Paragraph(inline(text), st_quote))
        elif ln.startswith("- "):
            # bullet list
            while ln.startswith("- "):
                out.append(Paragraph(inline(ln[2:]), st_bul, bulletText="—"))
                i += 1
                if i >= len(lines): break
                ln = lines[i].rstrip()
            continue
        elif re.match(r"^\d+\.\s", ln):
            # numbered
            n = 0
            while True:
                # skip blank lines within a numbered block
                while i < len(lines) and not lines[i].strip():
                    i += 1
                if i >= len(lines): break
                ln2 = lines[i].rstrip()
                if not re.match(r"^\d+\.\s", ln2):
                    break
                n += 1
                content = re.sub(r"^\d+\.\s+", "", ln2)
                out.append(Paragraph(inline(content), st_bul, bulletText=f"{n}."))
                i += 1
            continue
        else:
            out.append(Paragraph(inline(ln), st_body))
        i += 1
    return out


def watermark(canv, doc):
    canv.saveState()
    canv.setFont("Fraunces", 68)
    canv.setFillColor(HexColor("#eee6d4"))
    canv.translate(W/2, H/2)
    canv.rotate(30)
    canv.drawCentredString(0, 30, "EVEglyphDesign")
    canv.setFont("Inter", 10)
    canv.drawCentredString(0, -12, "CANON  ·  CONTROLLED COPY")
    canv.restoreState()
    # header
    canv.saveState()
    canv.setFont("Fraunces", 9); canv.setFillColor(MUTE)
    canv.drawString(MARGIN_L, H - 16*mm, f"EVEglyphDesign  ·  {TITLE}  ·  {DOC_ID} {VERSION}")
    canv.drawRightString(W - MARGIN_R, H - 16*mm, KEY_ID)
    canv.setStrokeColor(LINE); canv.setLineWidth(0.6)
    canv.line(MARGIN_L, H - 18.5*mm, W - MARGIN_R, H - 18.5*mm)
    # footer
    canv.setFont("Inter", 7.6); canv.setFillColor(MUTE)
    canv.line(MARGIN_L, BOT - 4*mm, W - MARGIN_R, BOT - 4*mm)
    tot = f" of {PAGES}" if PAGES else ""
    canv.drawString(MARGIN_L, BOT - 9*mm,
                    f"© 2026 EVEglyphDesign. All rights reserved. Controlled copy.  ·  {TS}  ·  SHA-256 {SHA[:16]}…")
    canv.drawRightString(W - MARGIN_R, BOT - 9*mm, f"Page {canv.getPageNumber()}{tot}")
    canv.setFont("Fraunces", 7.6)
    canv.drawString(MARGIN_L, BOT - 13*mm, "Pour le bien-être du peuple.")
    canv.restoreState()


def cover_page(canv, doc):
    watermark(canv, doc)


from reportlab.platypus import Flowable as _Flowable
class AccentRule(_Flowable):
    def __init__(self, w=52, h=3): _Flowable.__init__(self); self.width=w; self.height=h+16
    def draw(self):
        self.canv.setFillColor(ORNG)
        self.canv.rect(0, 10, 52, 3, stroke=0, fill=1)


def cover_flow():
    return [
        Spacer(1, 30),
        Paragraph(f'<font name="Fraunces" size="9" color="#e87722">EVEGLYPHDESIGN · MIRROR 3 · {DOC_ID}</font>',
                  S("k", fontSize=9, spaceAfter=6, textColor=ORNG)),
        Paragraph(TITLE, S("t", fontName="Fraunces-Bold", fontSize=42, leading=48, spaceAfter=6)),
        Paragraph("Transformational program management for information and technology",
                  S("st", fontName="Fraunces", fontSize=18, leading=24, textColor=HexColor("#2a2a2a"), spaceAfter=4)),
        Paragraph("The Sovereign practitioner canon",
                  S("st2", fontName="Inter-SB", fontSize=13, leading=18, textColor=MUTE, spaceAfter=20)),
        AccentRule(),
        Paragraph('<font name="Inter-Bold">The peer-review canon.</font> This mirror of the handbook is the room-agnostic version, '
                  'offered so consultants working in Lilian Corvington&rsquo;s lineage have something durable to practise from. It carries '
                  'no client, no engagement, and no room-specific vocabulary. Where a specific room is being met, a tuned revision '
                  'is published on a separate mirror; the peer-review canon stays here so the method can be judged on its own merits.',
                  st_body),
        Paragraph('<font name="Inter-Bold">Written in the lineage of Lillian.</font> The handbook is offered without ceremony; the reader is free '
                  'to copy it, mirror it, and pass it along. Watermark and hash make tampering legible without preventing use.',
                  st_body),
        Spacer(1, 24),
        Paragraph(f'<font name="Inter-SB">Version</font>  {VERSION}  ·  <font name="Inter-SB">Issued</font>  {TS}',
                  st_cap),
        Paragraph(f'<font name="Inter-SB">Source SHA-256</font>  <font name="Courier" size="7.4">{SHA}</font>', st_cap),
        Paragraph(f'<font name="Inter-SB">Key ID</font>  {KEY_ID}  ·  <font name="Inter-SB">Companion mirrors</font>  '
                  f'Mirror-4 Lillian&rsquo;s Guide (Group Platforms revision)', st_cap),
    ]


def build():
    from reportlab.platypus import PageBreak, NextPageTemplate
    doc = BaseDocTemplate(OUT, pagesize=LETTER, leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                          topMargin=TOP, bottomMargin=BOT)
    frame = Frame(MARGIN_L, BOT, FW, H - TOP - BOT, id="f", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=cover_page),
                          PageTemplate(id="body", frames=[frame], onPage=watermark)])
    story = cover_flow() + [NextPageTemplate("body"), PageBreak()] + parse(RAW)
    doc.build(story)
    from pypdf import PdfReader
    return len(PdfReader(OUT).pages)


if __name__ == "__main__":
    n = build()
    print("pages", n, "stamped", PAGES, "sha", SHA[:16])
