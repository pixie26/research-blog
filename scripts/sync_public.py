#!/usr/bin/env python3
"""Export an already-public static blog build for this GitHub Pages project."""
import argparse, json, re, shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('source', type=Path, help='Directory containing the approved public static build')
p.add_argument('--source-origin', required=True, help='Original public website origin')
a = p.parse_args()
source = a.source.resolve()
root = Path(__file__).resolve().parents[1]
out = root / 'docs'
origin = 'https://pixie26.github.io/research-blog'
base = '/research-blog/'
allowed = {'.html', '.css', '.js', '.json', '.xml', '.txt', '.svg'}
files = sorted(source.rglob('*'))
for f in files:
    if f.is_symlink(): raise SystemExit(f'Symlinks are not accepted: {f}')
    if f.is_file() and f.suffix == '.svg':
        svg = ET.fromstring(f.read_text())
        tags = {'svg','g','rect','line','path','circle','polyline','polygon','text','tspan','title','desc','defs','clipPath'}
        for el in svg.iter():
            if el.tag.split('}')[-1] not in tags: raise SystemExit(f'Unsafe SVG tag: {f}')
            for key, value in el.attrib.items():
                if key.lower().startswith('on') or key.split('}')[-1].lower() == 'href' or 'url(' in value.lower():
                    raise SystemExit(f'Unsafe SVG attribute: {f}')
    if f.is_file() and (f.suffix not in allowed or any(x.startswith('.') for x in f.relative_to(source).parts)):
        raise SystemExit(f'Unexpected public-build file: {f}')
if not (source/'index.html').is_file(): raise SystemExit('Missing public index.html')
articles = json.loads((source/'articles.json').read_text())
if out.exists(): shutil.rmtree(out)
for f in files:
    if not f.is_file(): continue
    text = f.read_text(encoding='utf-8').replace(a.source_origin.rstrip('/'), origin)
    if f.suffix == '.html':
        text = re.sub(r'(\b(?:href|src|action)=[\"\'])/(?!/|research-blog/)', r'\1'+base, text)
    if f.relative_to(source).as_posix() == 'assets/app.js':
        text = text.replace("location.pathname === '/'", "location.pathname === '/research-blog/'")
        text = text.replace("location.replace('/archive/", "location.replace('/research-blog/archive/")
    dest = out/f.relative_to(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')
(out/'.nojekyll').touch()
print(f'Exported {len(articles)} public articles to docs/')
