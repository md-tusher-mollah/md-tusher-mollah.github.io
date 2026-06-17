# Publication figure workflow

The website pages display existing images from each publication folder under `figures/fig1.jpg` to `figures/fig4.jpg`. The batch tool extracts caption-based crops for Figure 1 to Figure 4 from the uploaded PDFs listed in `publication_pdf_map.json`.

Run from the repository root:

```bash
pip install pymupdf pillow
python tools/batch_extract_publication_figures.py
```

After checking the extracted images, commit and push the new `publication/<slug>/figures/` files.
