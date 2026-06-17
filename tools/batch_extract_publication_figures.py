
import re
from pathlib import Path
import fitz
from PIL import Image, ImageChops

def caption_blocks(page, fig_no):
    pat=re.compile(r'^\s*(fig\.?|figure)\s*%d\b[\.\s:-]'%fig_no, re.I)
    blocks=[]
    data=page.get_text('dict')
    for b in data.get('blocks',[]):
        if 'lines' not in b: continue
        txt=' '.join(s.get('text','') for l in b.get('lines',[]) for s in l.get('spans',[]))
        txt=re.sub(r'\s+',' ',txt).strip()
        if pat.search(txt): blocks.append((fitz.Rect(b['bbox']), txt))
    if not blocks:
        pat2=re.compile(r'\b(fig\.?|figure)\s*%d\b'%fig_no, re.I)
        for b in data.get('blocks',[]):
            if 'lines' not in b: continue
            txt=' '.join(s.get('text','') for l in b.get('lines',[]) for s in l.get('spans',[]))
            txt=re.sub(r'\s+',' ',txt).strip()
            if pat2.search(txt) and len(txt)<600: blocks.append((fitz.Rect(b['bbox']), txt))
    return blocks

def trim_whitespace(img):
    bg=Image.new('RGB', img.size, (255,255,255))
    diff=ImageChops.difference(img.convert('RGB'), bg)
    bbox=diff.getbbox()
    if not bbox: return img
    x0,y0,x1,y1=bbox; pad=12
    return img.crop((max(0,x0-pad), max(0,y0-pad), min(img.width,x1+pad), min(img.height,y1+pad)))

def extract_caption_figures(pdf_path, outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    for f in outdir.glob('fig*.*'): f.unlink()
    doc=fitz.open(pdf_path)
    saved=[]
    for n in range(1,5):
        found=None
        for pi,page in enumerate(doc):
            cbs=caption_blocks(page,n)
            if cbs:
                cbs=sorted(cbs, key=lambda x:x[0].y0)
                found=(page,cbs[0][0]); break
        if not found: continue
        page,cap_rect=found; W,H=page.rect.width,page.rect.height
        y1=max(5,cap_rect.y0-8); y0=max(0,y1-min(420,H*0.55))
        if y1 < H*0.28: y0=0
        x0=30; x1=W-30
        if cap_rect.x1 < W*0.55: x1=W*0.55
        elif cap_rect.x0 > W*0.45: x0=W*0.45
        if cap_rect.width > W*0.45: x0=30; x1=W-30
        clip=(fitz.Rect(x0,y0,x1,y1) & page.rect)
        if clip.is_empty or clip.height<40: continue
        pix=page.get_pixmap(matrix=fitz.Matrix(2.2,2.2),clip=clip,alpha=False)
        img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        img=trim_whitespace(img)
        if img.width<120 or img.height<80: continue
        out=outdir/f'fig{n}.jpg'; img.save(out,quality=88,optimize=True); saved.append(out)
    return saved

if __name__ == '__main__':
    import json
    root=Path(__file__).resolve().parents[1]
    mapping=json.loads((root/'publication_pdf_map.json').read_text(encoding='utf-8'))
    total=0
    for slug,pdf in mapping.items():
        pdf_path=root/pdf
        outdir=root/'publication'/slug/'figures'
        if pdf_path.exists():
            saved=extract_caption_figures(pdf_path,outdir)
            print(slug, len(saved))
            total += len(saved)
        else:
            print(slug, 'missing PDF:', pdf)
    print('Total figures saved:', total)
