"""Static preview with a public-file allowlist; never expose .git or source files."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os
ROOT=Path(__file__).resolve().parents[1]
PUBLIC={'index.html','robots.txt','sitemap.xml','favicon.ico'}
ROUTES={'about','contact','privacy-policy','terms','disclaimer','strip-chat-sites','stripchat-live','stripchat-token-generator'}
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def send_head(self):
        path=unquote(urlsplit(self.path).path)
        parts=Path(path).parts[1:]
        valid=(not parts or len(parts)==1 and parts[0] in PUBLIC or len(parts) in (1,2) and parts[0] in ROUTES and (len(parts)==1 or parts[1]=='index.html') or len(parts)>1 and parts[0]=='assets' and all(not p.startswith('.') and p!='..' for p in parts))
        if not valid:
            self.send_error(404,'Not found');return None
        return super().send_head()
    def list_directory(self,path):
        self.send_error(404,'Not found');return None
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy','camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; frame-src https://www.youtube-nocookie.com; object-src 'none'; base-uri 'none'; form-action 'none'")
        super().end_headers()
if __name__=='__main__':
    port=int(os.environ.get('PORT','3000'))
    print(f'OpenRoom preview listening on 0.0.0.0:{port}',flush=True)
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
