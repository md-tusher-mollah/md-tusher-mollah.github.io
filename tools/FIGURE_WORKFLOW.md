# Publication figure workflow

For each publication page, upload Figures 1–4 to the paper folder like this:

```
publication/paper-slug/figures/fig1.png
publication/paper-slug/figures/fig2.png
publication/paper-slug/figures/fig3.png
publication/paper-slug/figures/fig4.png
```

The page automatically tries `.jpg`, `.jpeg`, `.png`, `.svg`, and `.webp`. Missing figures are hidden.

To extract the first four large images from a PDF on your computer:

```
pip install pymupdf pillow
python tools/extract_pdf_figures.py papers/my-paper.pdf publication/paper-slug/figures
```

Only publish extracted figures when copyright/licensing allows it.
