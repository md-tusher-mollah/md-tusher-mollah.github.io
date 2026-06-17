#!/usr/bin/env python3
"""
Extract Figures 1-4 from paper PDFs and place them where the website can display them.

Usage:
  python tools/extract_pdf_figures.py papers/rebar-paper.pdf publication/computational-fluid-dynamics-modelling-and-experimental-analysis-of-reinforcement/figures

It extracts embedded raster images from the PDF and saves the first four sufficiently large images as:
  fig1.png, fig2.png, fig3.png, fig4.png

Requirements:
  pip install pymupdf pillow

Note: please only publish extracted figures when copyright/licensing allows it.
"""
import sys, io
from pathlib import Path
try:
    import fitz  # PyMuPDF
    from PIL import Image
except Exception as e:
    print("Missing dependency. Install with: pip install pymupdf pillow", file=sys.stderr)
    raise

def extract(pdf_path, out_dir, max_figures=4, min_width=250, min_height=180):
    pdf_path=Path(pdf_path); out_dir=Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    doc=fitz.open(str(pdf_path))
    saved=0; seen=set()
    for page_index in range(len(doc)):
        page=doc[page_index]
        for img_index, info in enumerate(page.get_images(full=True)):
            xref=info[0]
            if xref in seen: continue
            seen.add(xref)
            data=doc.extract_image(xref)
            image_bytes=data.get('image')
            if not image_bytes: continue
            try:
                im=Image.open(io.BytesIO(image_bytes)).convert('RGB')
            except Exception:
                continue
            w,h=im.size
            if w < min_width or h < min_height: continue
            saved += 1
            im.save(out_dir / f'fig{saved}.png')
            print(f'Saved fig{saved}.png from page {page_index+1}, image {img_index+1}, size {w}x{h}')
            if saved >= max_figures:
                return saved
    return saved

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    n=extract(sys.argv[1], sys.argv[2])
    print(f'Done. Saved {n} figure(s).')
