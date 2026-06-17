# Publication figure workflow

The website displays publication figures from each publication folder when image files exist in its `figures/` subfolder.

## Folder structure

- Journal PDFs: `papers/journal/`
- Conference PDFs: `papers/conference/`
- Extracted publication figures: `publication/<publication-slug>/figures/`

## Batch extraction

Install the requirements once:

```bash
pip install pymupdf pillow
```

Then run:

```bash
python tools/batch_extract_publication_figures.py
```

The script reads `publication_pdf_map.json`, extracts up to four large images from each mapped PDF, and saves them as:

```text
publication/<publication-slug>/figures/fig1.jpg
publication/<publication-slug>/figures/fig2.jpg
publication/<publication-slug>/figures/fig3.jpg
publication/<publication-slug>/figures/fig4.jpg
```

After reviewing the extracted images, commit and push the generated figure files.
