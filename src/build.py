"""Rebuild the published files from src/.
   python3 src/build.py
   - src/guide/template.html + imgs.js  -> 360/index.html   (360 Photo Booth Guide, EN/ES/FR)
   - src/page/page.tpl.html + covers.json -> index.html      (Tutorials section)
   - src/page/embed.js, viewer.html       -> assets/embed.js, viewer.html
"""
import json, base64, os
SRC = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(SRC)
HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
BASE = '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n'

# 360 guide
g = open(f'{SRC}/guide/template.html').read().replace('__IMGS__', open(f'{SRC}/guide/imgs.js').read())
g = g.replace('<title>Selfie Booth AI Tutorials</title>', '<title>360 Photo Booth Guide · Selfie Booth AI</title>', 1)
os.makedirs(f'{R}/360', exist_ok=True)
open(f'{R}/360/index.html', 'w').write(HEAD + BASE + g + '\n</html>\n')

# Tutorials section (drop the design-proposal ribbon, stand-in site header and footer)
L = open(f'{SRC}/page/page.tpl.html').read().split('\n')
find = lambda s, a=0: next(i for i in range(a, len(L)) if s in L[i])
a = find('<div id="landing">'); h = find('</header>', a); f = find('<footer><div class="wrap">')
t = '\n'.join(L[:a] + ['<div id="landing"><div id="root">'] + L[h+1:f] + ['</div>'] + L[f+1:])
for k, n in (('QA1', 'cover-start'), ('LC1', 'cover-events'), ('SR1', 'cover-speed')):
    t = t.replace(f'src="__{k}__"', f'src="assets/{n}.jpg"')
t = t.replace('const GUIDE="360/index.html";', 'const EMBED=window.parent!==window;\nconst GUIDE="360/";', 1)
t = t.replace('function openGuide(sec){', 'function openGuide(sec){\n  if(EMBED){try{parent.postMessage({sbt:"open",sec:sec||"",lang},"*")}catch(e){}return}', 1)
t = t.replace('</style>', '#root{padding-bottom:1px}\nhtml.embed,html.embed body{height:auto}\n</style>', 1)
emb = '''
/* Embedded in selfieboothapp.com/tutorials: report height so the host iframe fits the content */
if(EMBED){document.documentElement.classList.add("embed");const root=document.getElementById("root");
 const send=()=>{try{parent.postMessage({sbt:"h",h:Math.ceil(root.getBoundingClientRect().height)+40},"*")}catch(e){}};
 try{new ResizeObserver(send).observe(root)}catch(e){}addEventListener("load",send);send();}
'''
i = t.rindex('</script>'); t = t[:i] + emb + t[i:]
t = t.replace('<title>Selfie Booth AI Tutorials</title>', '<title>Tutorials · Selfie Booth AI</title>', 1)
meta = '<meta name="description" content="Interactive tutorials for the Selfie Booth AI app: learn the 360 Photo Booth screen by screen, in English, Spanish, French, Italian and Portuguese.">\n'
assert '__QA1__' not in t
open(f'{R}/index.html', 'w').write(HEAD + meta + BASE + t + '\n</html>\n')

os.makedirs(f'{R}/assets', exist_ok=True)
c = json.load(open(f'{SRC}/page/covers.json'))
for k, n in (('qa1', 'cover-start'), ('lc1', 'cover-events'), ('sr1', 'cover-speed')):
    open(f'{R}/assets/{n}.jpg', 'wb').write(base64.b64decode(c[k].split(',')[1]))
open(f'{R}/assets/embed.js', 'w').write(open(f'{SRC}/page/embed.js').read())
open(f'{R}/viewer.html', 'w').write(open(f'{SRC}/page/viewer.html').read())
print('built')
