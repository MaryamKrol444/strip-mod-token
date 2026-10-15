"""Package only public deployment files, with launch notes; never package the repository."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
output=ROOT/'openroom-html.zip'
files=[ROOT/'index.html',ROOT/'sitemap.xml',ROOT/'robots.txt']
for route in ('stripchat-token-generator','stripchat-live','strip-chat-sites','about','contact','privacy-policy','terms','disclaimer'):
    files.append(ROOT/route/'index.html')
files+=list((ROOT/'assets').rglob('*'))
with ZipFile(output,'w',ZIP_DEFLATED) as archive:
    for file in sorted(files):
        if file.is_file():archive.write(file,file.relative_to(ROOT))
    archive.write(ROOT/'README.md','BUILD-AND-LAUNCH-NOTES.md')
    archive.write(ROOT/'LINK_AUDIT.md','LINK_AUDIT.md')
print(f'{output.name}: {output.stat().st_size:,} bytes; public HTML, assets, sitemap, robots and launch notes only')
