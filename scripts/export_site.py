"""Stage only the generated public site for a static-host deployment."""
from pathlib import Path
import os
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'.site'
if not os.environ.get('SITE_URL') or 'example.com' in os.environ['SITE_URL']:
    raise SystemExit('Set a real SITE_URL before creating a deployment artifact.')
OUTPUT.mkdir(exist_ok=True)
for name in ('index.html','robots.txt','sitemap.xml'):
    shutil.copy2(ROOT/name,OUTPUT/name)
for name in ('assets','about','contact','privacy-policy','terms','disclaimer','stripchat-token-generator','stripchat-live','strip-chat-sites'):
    shutil.copytree(ROOT/name,OUTPUT/name,dirs_exist_ok=True)
(OUTPUT/'.nojekyll').write_text('')
print(f'Public deployment artifact staged in {OUTPUT.name}/')
