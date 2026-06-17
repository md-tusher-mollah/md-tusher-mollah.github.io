#!/usr/bin/env python3
"""Extract the first four large images from a publication PDF.
Usage: python tools/extract_pdf_figures.py "papers/journal/example.pdf" "publication/example/figures"
"""
import sys, pathlib, fitz
from PIL import Image
MIN_AREA=45000
MAX_DIM=1400

def save_resized(pix, out_path):
    mode='RGB' if pix.alpha==0 else 'RGBA'
    img=Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    if mode=='RGBA':
        bg=Image.new('RGB', img.size, (255,255,255)); bg.paste(img, mask=img.split()[3]); img=bg
    else:
        img=img.convert('RGB')
    img.thumbnail((MAX_DIM,MAX_DIM), Image.LANCZOS)
    img.save(out_path, 'JPEG', quality=86, optimize=True)

def main(pdf_path, out_dir):
    pdf_path=pathlib.Path(pdf_path); out_dir=pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    doc=fitz.open(pdf_path); seen=set(); candidates=[]
    for page_idx in range(min(len(doc), 20)):
        for imginfo in doc[page_idx].get_images(full=True):
            xref=imginfo[0]
            if xref in seen: continue
            seen.add(xref)
            try:
                pix=fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:
                    pix=fitz.Pixmap(fitz.csRGB, pix)
                w,h=pix.width,pix.height
                if w*h < MIN_AREA or w < 180 or h < 120: continue
                if max(w/h, h/w) > 10: continue
                candidates.append((page_idx, -(w*h), pix))
            except Exception:
                pass
    candidates.sort(key=lambda x:(x[0], x[1]))
    for old in out_dir.glob('fig*.*'):
        old.unlink()
    for i,(_,__,pix) in enumerate(candidates[:4], start=1):
        save_resized(pix, out_dir/f'fig{i}.jpg')
    print(f'Extracted {min(4,len(candidates))} figure(s) to {out_dir}')

if __name__=='__main__':
    if len(sys.argv)!=3:
        print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
