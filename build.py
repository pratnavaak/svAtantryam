import os
import sys
import shutil
import markdown

from pathlib import Path

pages_repo = sys.argv[1]
site = os.path.join(pages_repo, '_site')

Path(site).mkdir(exist_ok=True)

def convert(fn, md):
    divisions = md.split('\n---\n')
    yaml, matter = '', divisions[-1]
    if len(divisions) > 2:
        yaml = divisions[1]
    title = fn[:-3]
    for line in yaml.split('\n'):
        ss = line.split(':')
        if ss[0] == 'title' and len(ss) > 1:
            title = ss[1].replace('"', '').replace("'", "")
    return open('template.html').read().replace('<title></title>', f'<title>{title}</title>').replace('<body></body>', f'<body>{markdown.markdown(matter)}</body>')

for root, subdirs, files in os.walk(os.path.join(pages_repo, 'content')):
    for dir in subdirs:
        Path(os.path.join(site, root, dir)).mkdir(exist_ok=True)
    for file in files:
        fp = os.path.join(root, file)
        nfp = os.path.join(site, fp).replace('./content/','')
        if file.endswith('.md'):
            with open(nfp.replace('.md', '.html'), 'w+') as f:
                f.write(convert(file, open(fp).read()))
        else:
            shutil.copy(fp, nfp)