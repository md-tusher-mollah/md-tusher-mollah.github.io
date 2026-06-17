#!/usr/bin/env python3
"""Batch extract Figures 1-4 for mapped publication PDFs."""
import json, subprocess, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
mp=json.load(open(ROOT/'publication_pdf_map.json',encoding='utf-8'))
for slug, pdf in mp.items():
    pdf_path=ROOT/pdf
    out_dir=ROOT/'publication'/slug/'figures'
    if not pdf_path.exists():
        print('Missing PDF:', pdf); continue
    subprocess.run([sys.executable, str(ROOT/'tools'/'extract_pdf_figures.py'), str(pdf_path), str(out_dir)], check=False)
